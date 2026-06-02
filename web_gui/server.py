import queue
import threading
import logging
import uuid
from typing import Tuple, Dict, Union, Optional
from flask import Flask, request, jsonify, render_template, Response
from shared.logger import get_logger

import os
class WebServer:
    def __init__(self) -> None:
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.app = Flask(__name__, template_folder=template_dir)
        
        self._query_queue: queue.Queue[Tuple[str, str]] = queue.Queue()
        self._active_query_id: Optional[str] = None
        
        self._search_results: Dict[str, dict] = {}
        self._search_events: Dict[str, threading.Event] = {}
        
        self._rag_results: Dict[str, dict] = {}
        self._rag_events: Dict[str, threading.Event] = {}

        self._setup_routes()

    def _setup_routes(self) -> None:
        self.app.add_url_rule('/', 'index', self._index)
        self.app.add_url_rule('/api/search', 'search', self._search, methods=['POST'])
        self.app.add_url_rule('/api/rag/<query_id>', 'rag', self._rag, methods=['GET'])

    def _index(self) -> str:
        return render_template('index.html')

    def _search(self) -> Union[Response, Tuple[Response, int]]:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({"error": "No query provided"}), 400
            
        query_id = str(uuid.uuid4())
        self._search_events[query_id] = threading.Event()
        self._rag_events[query_id] = threading.Event()
        
        self._query_queue.put((query_id, data['query']))
        
        self._search_events[query_id].wait()
        results = self._search_results.pop(query_id)
        
        return jsonify({
            "id": query_id,
            "results": results
        })

    def _rag(self, query_id: str) -> Union[Response, Tuple[Response, int]]:
        if query_id not in self._rag_events:
            return jsonify({"error": "Invalid request ID"}), 404
            
        self._rag_events[query_id].wait()
        rag = self._rag_results.pop(query_id)
        
        if query_id in self._search_events:
            del self._search_events[query_id]
        if query_id in self._rag_events:
            del self._rag_events[query_id]
            
        return jsonify({
            "rag": rag
        })

    def run(self, port: int = 5000) -> None:
        self._thread = threading.Thread(
            target=self.app.run,
            kwargs={"host": "127.0.0.1", "port": port, "use_reloader": False, "debug": False},
            daemon=True
        )
        self._thread.start()

    def wait_query(self) -> str:
        query_id, query = self._query_queue.get()
        self._active_query_id = query_id
        return query

    def show_search_results(self, results: dict) -> None:
        if self._active_query_id:
            self._search_results[self._active_query_id] = results
            self._search_events[self._active_query_id].set()

    def show_rag_results(self, rag: dict) -> None:
        if self._active_query_id:
            self._rag_results[self._active_query_id] = rag
            self._rag_events[self._active_query_id].set()
            self._active_query_id = None

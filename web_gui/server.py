import queue
import threading
import uuid
from typing import Tuple, Dict, Union, Optional, Any
from flask import Flask, request, jsonify, render_template, Response
import os

from contracts.use_cases import (
    SearchRequest, ImproveQueryRequest, SystemRequest,
    SearchResultsResponse, RAGResponse, ImprovedQueryResponse, SystemResponse
)
from contracts.either import Ok, Error

class WebServer:
    def __init__(self) -> None:
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.app = Flask(__name__, template_folder=template_dir)
        
        self._query_queue: queue.Queue[Tuple[str, SystemRequest]] = queue.Queue()
        self._active_query_id: Optional[str] = None
        
        self._search_results: Dict[str, dict] = {}
        self._search_events: Dict[str, threading.Event] = {}
        
        self._rag_results: Dict[str, dict] = {}
        self._rag_events: Dict[str, threading.Event] = {}

        self._improved_query_results: Dict[str, dict] = {}
        self._improved_query_events: Dict[str, threading.Event] = {}

        self._setup_routes()

    def _setup_routes(self) -> None:
        self.app.add_url_rule('/', 'index', self._index)
        self.app.add_url_rule('/api/search', 'search', self._search, methods=['POST'])
        self.app.add_url_rule('/api/rag/<query_id>', 'rag', self._rag, methods=['GET'])
        self.app.add_url_rule('/api/improve_query', 'improve_query', self._improve_query, methods=['POST'])

    def _index(self) -> str:
        return render_template('index.html')

    def _search(self) -> Union[Response, Tuple[Response, int]]:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({"error": "No query provided"}), 400
            
        query_id = str(uuid.uuid4())
        self._search_events[query_id] = threading.Event()
        self._rag_events[query_id] = threading.Event()
        
        self._query_queue.put((query_id, SearchRequest(query=data['query'])))
        
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

    def _improve_query(self) -> Union[Response, Tuple[Response, int]]:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({"error": "No query provided"}), 400
            
        query_id = str(uuid.uuid4())
        self._improved_query_events[query_id] = threading.Event()
        
        self._query_queue.put((query_id, ImproveQueryRequest(query=data['query'])))
        
        self._improved_query_events[query_id].wait()
        results = self._improved_query_results.pop(query_id)
        
        del self._improved_query_events[query_id]
            
        return jsonify({
            "id": query_id,
            "improved_query": results
        })

    def run(self, port: int = 5000) -> None:
        self._thread = threading.Thread(
            target=self.app.run,
            kwargs={"host": "127.0.0.1", "port": port, "use_reloader": False, "debug": False},
            daemon=True
        )
        self._thread.start()

    def wait_request(self) -> SystemRequest:
        query_id, req = self._query_queue.get()
        self._active_query_id = query_id
        return req

    def show(self, response: SystemResponse) -> None:
        if not self._active_query_id:
            return

        match response:
            case SearchResultsResponse(results=results_either):
                self._search_results[self._active_query_id] = self._serialize_either(results_either, "data")
                self._search_events[self._active_query_id].set()
            case RAGResponse(rag=rag_either):
                self._rag_results[self._active_query_id] = self._serialize_either(rag_either, "message")
                self._rag_events[self._active_query_id].set()
                self._active_query_id = None
            case ImprovedQueryResponse(improved_query=query_either):
                self._improved_query_results[self._active_query_id] = self._serialize_either(query_either, "improved_query")
                self._improved_query_events[self._active_query_id].set()
                self._active_query_id = None

    def _serialize_either(self, either_val: Any, success_key: str) -> dict:
        results_data = {}
        match either_val:
            case Ok(value=val):
                results_data[success_key] = val
            case Error(error=app_error):
                results_data["error"] = getattr(app_error, 'error_message', str(app_error))
        return results_data

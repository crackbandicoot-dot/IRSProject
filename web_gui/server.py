import os
import queue
import threading
import logging
from typing import Tuple, Dict, Union
from flask import Flask, request, jsonify, render_template, Response

class WebServer:
    def __init__(self) -> None:
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.app = Flask(__name__, template_folder=template_dir)
        
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        self._query_queue: queue.Queue[str] = queue.Queue()
        self._result_queue: queue.Queue[tuple] = queue.Queue()

        self._setup_routes()

    def _setup_routes(self) -> None:
        @self.app.route('/')
        def _index() -> str:
            return render_template('index.html')

        @self.app.route('/api/search', methods=['POST'])
        def _search() -> Union[Response, Tuple[Response, int]]:
            data = request.json
            if not data or 'query' not in data:
                return jsonify({"error": "No query provided"}), 400
                
            self._query_queue.put(data['query'])
            
            results, rag = self._result_queue.get()
            
            return jsonify({
                "results": results,
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
        return self._query_queue.get()

    def show_result(self, results: dict, rag: dict) -> None:
        self._result_queue.put((results, rag))

import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
import logging

from Graph import Graph, Node

# the main Flask application object
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# create logger instance
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

graph = Graph()

graph.nodes.append(Node(30, 30, 1))


@app.route('/', methods=['GET'])
def index():
    return render_template('page.html', text="# Write your graph here")


@app.route('/load_graph', methods=['GET'])
def load_graph():
    try:
        return jsonify({"success": True, "n": len(graph.nodes), "m": len(
            graph.links),
                        **{"l{}i1".format(i): lk.n1.num for i, lk in enumerate(
                            graph.links)},
                        **{"l{}i2".format(i): lk.n2.num for i, lk in enumerate(
                            graph.links)},
                        **{"l{}w".format(i): lk.w for i, lk in enumerate(
                            graph.links)},
                        **{"n{}x".format(i): nd.x for i, nd in enumerate(
                            graph.nodes)},
                        **{"n{}y".format(i): nd.y for i, nd in enumerate(
                            graph.nodes)},
                        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@socketio.on('rebuild_graph')
def rebuild_graph(data):
    global graph
    new_graph = Graph()
    try:
        new_graph.from_text(data['text'])
        graph = new_graph
        emit('rebuild_graph', )
    except Exception as e:
        pass


if __name__ == "__main__":
    app.run(debug=True)

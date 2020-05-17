import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
import logging

from Graph import Graph, Node, Link

# the main Flask application object
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# create logger instance
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

graph = Graph()

text = "5\n1 2\n1 3\n1 4\n1 5\n2 3\n2 4\n2 5\n3 4\n3 5\n4 5"

graph.from_text(text)


@app.route('/', methods=['GET'])
def index():
    return render_template('page.html', text=text)


@app.route('/load_graph', methods=['GET'])
def load_graph():
    try:
        return jsonify({"success": True, "n": len(graph.nodes), "m": len(
            graph.links),
                        **{"l{}i1".format(i): lk.n1 for i, lk in enumerate(
                            graph.links)},
                        **{"l{}i2".format(i): lk.n2 for i, lk in enumerate(
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
def rebuild_sgraph(data):
    global graph
    new_graph = Graph()
    try:
        new_graph.from_text(data['text'])
        graph = new_graph
        emit('rebuild_graph', graph.to_dict(), broadcast=True)
    except Exception as e:
        emit("error", {"error": str(e)})

@socketio.on('move_node')
def move_node(data):
    try:
        graph.nodes[data['i']].x = data['x']
        graph.nodes[data['i']].y = data['y']
        emit('rebuild_graph', graph.to_dict(), broadcast=True, include_self=False)
    except Exception as e:
        emit("error", {"error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

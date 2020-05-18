from random import randint
from math import sin, cos, pi


class Link:
    def __init__(self, n1, n2, w=0):
        """строится по номерам нод"""
        self.n1 = n1
        self.n2 = n2
        self.w = w


class Node:
    def __init__(self, x, y, num):
        """coordinates in range [-1;1] or it will be out of screen"""
        self.links = []
        self.num = num
        self.x = x
        self.y = y


class Graph:
    def __init__(self):
        self.nodes = []
        self.links = []

    def from_text(self, text, positions=[]):
        self.nodes = []
        self.links = []
        lines = text.split('\n')
        lines = [ln for ln in lines if not ln.startswith('#') and ln != ""]
        try:
            n = tuple(map(int, [s for s in lines[0].split(' ') if s != '']))[0]
        except:
            raise Exception("line 1: invalid format")
        assert n > 0, "line 1: node quantity must be > 0"
        for i in range(n):
            if i < len(positions):
                self.nodes.append(Node(*positions[i], i))
            else:
                self.nodes.append(Node(0.8 * sin(pi*2*i/n),
                                        0.8 * cos(pi*2*i/n), i))
        for i in range(1, len(lines)):
            try:
                ints = tuple(map(int, [s for s in lines[i].split(' ') if s
                                       != '']))
                assert len(ints) == 2 or len(ints) == 3
            except:
                raise Exception("line {}: invalid format".format(i+1))
            if len(ints) == 2:
                i1, i2 = ints
                w = 0
            else:
                i1, i2, w = ints
            assert 0 < i1 <= n and 0 < i2 <= n, "Line {}:indexes must be in " \
                                                "(0;n] range".format(i + 1)
            link = Link(i1 - 1, i2 - 1, w)
            self.links.append(link)
            self.nodes[i1 - 1].links.append(link)
            self.nodes[i2 - 1].links.append(link)

    def to_dict(self):
        return {"n": len(self.nodes), "m": len(self.links),
                        **{"l{}i1".format(i): lk.n1 for i, lk in enumerate(
                            self.links)},
                        **{"l{}i2".format(i): lk.n2 for i, lk in enumerate(
                            self.links)},
                        **{"l{}w".format(i): lk.w for i, lk in enumerate(
                            self.links)},
                        **{"n{}x".format(i): nd.x for i, nd in enumerate(
                            self.nodes)},
                        **{"n{}y".format(i): nd.y for i, nd in enumerate(
                            self.nodes)},
                        }

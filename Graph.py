from random import randint


class Link:
    def __init__(self, n1, n2, w=0):
        self.n1 = n1
        self.n2 = n2
        self.w = w


class Node:
    def __init__(self, x, y, num):
        self.links = []
        self.num = num
        self.x = x
        self.y = y


class Graph:
    def __init__(self):
        self.nodes = []
        self.links = []

    def from_text(self, text):
        self.nodes = []
        self.links = []
        lines = text.split('\r\n')
        lines = [ln for ln in lines if not ln.startswith('#') and ln != ""]
        n, m = tuple(map(int, lines[0].split(' ')))
        assert m == len(lines) - 1, \
            "not enough lines: {}/{}".format(len(lines) - 1, m) if \
            (m > len(lines) - 1)\
            else "too many lines: {}/{}".format(len(lines) - 1, m)
        for i in range(n):
            self.nodes.append(Node(randint(0, 100), randint(0, 100), i + 1))
        for i in range(1, len(lines)):
            ints = tuple(map(int, lines[i].split(' ')))
            assert len(ints) == 2 or len(ints) == 3
            if len(ints) == 2:
                i1, i2 = ints
                w = 0
            else:
                i1, i2, w = ints
            link = Link(self.nodes[i1 - 1], self.nodes[i2 - 1], w)
            self.links.append(link)
            self.nodes[i1 - 1].links.append(link)
            self.nodes[i2 - 1].links.append(link)

    def to_dict(self):
        return {"n": len(self.nodes),
                "m": len(self.links),
                **{"l{}i1".format(i): lk.n1.num for i, lk in enumerate(
                    self.links)},
                **{"l{}i2".format(i): lk.n2.num for i, lk in enumerate(
                            self.links)},
                **{"l{}w".format(i): lk.w for i, lk in enumerate(
                            self.links)},
                **{"n{}x".format(i): nd.x for i, nd in enumerate(
                            self.nodes)},
                **{"n{}y".format(i): nd.y for i, nd in enumerate(
                            self.nodes)},
                }

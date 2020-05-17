import unittest
from Graph import Graph, Node, Link


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_generating_failing(self):
        text = "blabla  \n no-numbers-here"#no n provided
        self.assertRaises((Exception, ), self.graph.from_text, text)
        text = "3  \n3 4"  # too big indexes
        self.assertRaises((Exception,), self.graph.from_text, text)

    def test_generating_right_graphs(self):
        text = "3  \n1 2\n2 3"
        self.graph.from_text(text)
        self.assertEqual(len(self.graph.nodes), 3)
        self.assertEqual(len(self.graph.links), 2)
        for i in range(len(self.graph.nodes)):
            with self.subTest(i=i):
                self.assertIsInstance(self.graph.nodes[i], Node)
        for i in range(len(self.graph.links)):
            with self.subTest(i=i):
                self.assertIsInstance(self.graph.links[i], Link)
        self.assertCountEqual([(0, 1), (1, 2)],
                         [(min(l.n1,l.n2), max(l.n1,l.n2)) for l in self.graph.links])

    def test_generating_right_graphs2(self):
        text = "5  \n1 3\n1 3\n2 4"
        self.graph.from_text(text)
        self.assertEqual(len(self.graph.nodes), 5)
        self.assertEqual(len(self.graph.links), 3)
        for i in range(len(self.graph.nodes)):
            with self.subTest(i=i):
                self.assertIsInstance(self.graph.nodes[i], Node)
        for i in range(len(self.graph.links)):
            with self.subTest(i=i):
                self.assertIsInstance(self.graph.links[i], Link)
        self.assertCountEqual([(0, 2), (0, 2), (1, 3)],
                         [(min(l.n1,l.n2), max(l.n1,l.n2)) for l in self.graph.links])


if __name__ == '__main__':
    unittest.main()
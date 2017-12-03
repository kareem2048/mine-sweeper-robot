from random import randint

from mine_sweeper.model.graph import Graph
from mine_sweeper.model.node import Node
from mine_sweeper.model.node_data import NodeData
from mine_sweeper.model.singleton import Singleton


@Singleton
class GameBoard:
    def __init__(self):
        self.row = 8
        self.col = 8
        self.game_graph = Graph()
        self.__game_data = {}

    # TODO
    # this function is  responsible for discovering the game board
    # all data for board is preserved game_data
    # see how to access it in the example below
    # modify the function as u like but by using default values
    def discover(self, node: Node) -> bool:
        node_data = self.__game_data[node]
        node_data.__class__ = NodeData
        if node_data.mine:
            # mine is hit
            return False
        elif node_data.weight == 0:
            # TODO
            # keep discovering with connected nodes till a node with data found
            # i suggest bread first search (recursive)
            pass

        # in all cases update the discovered node
        node.node_data = node_data
        return True

    def generate_initial_state(self, row: int, col: int):
        self.row = row
        self.col = col
        self.game_graph.add_connections(
            self.__get_nodes_connection(
                self.__find_minesweeper_connections(), self.__init_game_list()))

    def __find_minesweeper_connections(self):
        row = self.row
        col = self.col
        node_pairs = []
        for r in range(0, row):
            for c in range(0, col):
                current = (r, c)
                if c + 1 < col:
                    node_pairs.append((current, (r, c + 1)))
                if c - 1 >= 0:
                    node_pairs.append((current, (r, c - 1)))
                if r + 1 < row:
                    node_pairs.append((current, (r + 1, c)))
                if r - 1 >= 0:
                    node_pairs.append((current, (r - 1, c)))
                if r - 1 >= 0 and c + 1 < col:
                    node_pairs.append((current, (r - 1, c + 1)))
                if r - 1 >= 0 and c - 1 >= 0:
                    node_pairs.append((current, (r - 1, c - 1)))
                if r + 1 < row and c + 1 < col:
                    node_pairs.append((current, (r + 1, c + 1)))
                if r + 1 < row and c - 1 >= 0:
                    node_pairs.append((current, (r + 1, c - 1)))

        return node_pairs

    @staticmethod
    def __get_nodes_connection(pairs, data):
        graph_data = []
        for (r1, c1), (r2, c2) in pairs:
            pair = (data[r1][c1], data[r2][c2])
            graph_data.append(pair)
        return graph_data

    def __init_game_list(self):
        bord = [[] for i in range(0, self.row)]
        for r in range(0, self.row):
            for c in range(0, self.col):
                node = Node()
                self.__game_data[node] = NodeData()
                bord[r].append(node)
        return bord

    # receive first clicked node
    def set_mines(self, node: Node):
        present = 10 / 64
        mines_num = round(self.row * self.col * present)
        keys = []
        for key in self.game_graph.m_graph:
            keys.append(key)
        while mines_num > 0:
            rand = randint(0, len(keys) - 1)
            if (not self.game_graph.is_connected(node, keys[rand])) and (not self.__game_data[keys[rand]].mine):
                self.__game_data[keys[rand]].mine = True
                for node in self.game_graph.m_graph[keys[rand]]:
                    self.__game_data[node].weight += 1
                    mines_num -= 1

    def get_graph_nodes_as_list(self):
        m_list = [[] for dump in range(0, self.row)]
        row = 0
        col = 0
        for key in self.game_graph.m_graph:
            if col == self.col:
                col = 0
                row += 1
            m_list[row].append(key)
            col += 1
        return m_list
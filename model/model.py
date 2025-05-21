import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._bestObjFunction = 0
        self._bestPath = []
        self._graph = nx.Graph()
        self._retailers = DAO.getRetailers()
        self._idMap = {}
        for r in self._retailers:
            self._idMap[r.Retailer_code] = r

    def getPaesi(self):
        return DAO.getPaesi()

    def buildGraph(self, paese, anno):
        self.addNodes(paese)
        self.addEdges(paese, anno)
        return len(self._graph.nodes), len(self._graph.edges)

    def addNodes(self, paese):
        retPaese = DAO.getRetailersPaese(paese)

        for ret in retPaese:
            self._graph.add_node(self._idMap[ret.Retailer_code])

    def addEdges(self, paese, anno):
        archi = DAO.getEdges(paese, paese, anno)

        for edg in archi:
            ret1 = self._idMap[edg.rc1]
            ret2 = self._idMap[edg.rc2]
            self._graph.add_edge(ret1, ret2, weight=edg.peso)

    def getVolumi(self):
        lista = []
        for n in self._graph.nodes():
            vicini = list(self._graph.neighbors(n))
            lista.append((n, self.countVolume(vicini, n)))

        sortedList = sorted(lista, key=lambda x: x[1], reverse=True)
        listaMax = sortedList[:6]

        return listaMax

    def countVolume(self, vicini, nodo):
        if len(vicini) == 0:
            return 0
        volume = 0
        for v in vicini:
            volume += self._graph[nodo][v]["weight"]

        return volume

    # def getPath(self, n):
    #     self._bestPath = []
    #     self._bestObjFunction = 0
    #
    #     parziale = []
    #     visitato = []
    #
    #     # self._ricorsione(parziale, n)
    #     for node in self._graph.nodes:
    #         parziale.append(node)
    #         self._ricorsione(n, node, node, parziale, [], 0)
    #         parziale.pop()
    #     print(len(self._bestPath))
    #     return self._bestPath, self._bestObjFunction
    #
    # def _ricorsione(self, n, current, start, parziale, visitato, peso):
    #
    #     if len(parziale) == n:
    #         if self._graph.has_edge(current, start):  # ciclo chiuso
    #             if peso + self._graph[start][current]["weight"] > self._bestObjFunction:
    #                 self._bestPath = copy.deepcopy(parziale)
    #                 self._bestObjFunction = peso + self._graph[start][current]["weight"]
    #                 return
    #
    #     for neighbor in list(self._graph.neighbors(current)):
    #         if neighbor not in parziale:
    #             pesoEdge = self._graph[current][neighbor]["weight"]
    #             parziale.append(neighbor)
    #             self._ricorsione(n, neighbor, start, parziale, visitato, peso + pesoEdge)
    #             parziale.pop()

    def getPath(self, n):
        self._bestPath = []
        self._bestObjFunction = 0
        parziale = []

        for node in self._graph.nodes:
            parziale.append(node)
            self._ricorsione(n, node, node, parziale, 0)
            parziale.pop()

        # Chiudi il ciclo anche in output aggiungendo il nodo iniziale
        if self._bestPath:
            print(True)
            self._bestPath.append(self._bestPath[0])
            return self.printBestPath(), self._bestObjFunction
        else:
            return [], 0

    def _ricorsione(self, n, current, start, parziale, peso):
        if len(parziale) == n:
            if self._graph.has_edge(current, start):
                pesoTot = peso + self._graph[current][start]["weight"]
                if pesoTot > self._bestObjFunction:
                    self._bestPath = copy.deepcopy(parziale)
                    self._bestObjFunction = pesoTot
            return

        for neighbor in self._graph.neighbors(current):
            if neighbor not in parziale:
                pesoEdge = self._graph[current][neighbor]["weight"]
                parziale.append(neighbor)
                self._ricorsione(n, neighbor, start, parziale, peso + pesoEdge)
                parziale.pop()

    def printBestPath(self):
        lista = []
        j = 0
        for i in self._bestPath:
            j += 1
            if j < len(self._bestPath):
                peso = self._graph[self._bestPath[j-1]][self._bestPath[j ]]["weight"]
                lista.append((self._bestPath[j-1], self._bestPath[j], peso))
        return lista

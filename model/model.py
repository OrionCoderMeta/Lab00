import copy
from collections import Counter

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.map = {}
        self.nodes = []
        self.archi = []
        self.bestPath = []
        self.bestObjFun = 0

    def getCamminoOttimo(self):
        # t invece la lunghezza percorso
        self.bestPath = []
        self.bestObjFun = 0

        for nodo in self._graph.nodes():
            parziale = [nodo]
            self._ricorsione(parziale)

        return self.bestPath, self.bestObjFun

    def _ricorsione(self, parziale):
        # verificare se quello che ho messo dentro parziale è una possibile soluzione
        if self.check(parziale):
            # verificare se parziale è meglio del best
            if self.getObjFun(parziale) > self.bestObjFun:
                self.bestObjFun = self.getObjFun(parziale)
                self.bestPath = copy.deepcopy(parziale)

        # Posso aggiungere ancora nodi
        # prendo i vicini e aggiungo un nodo alla volta solo se il peso è maggiore
        # ricorsione
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                if len(parziale) > 1:
                    if n.duration > parziale[-1].duration:
                        parziale.append(n)
                        self._ricorsione(parziale)
                        parziale.pop()
                else:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()

    def check(self, lista):
        conteggio_mesi = Counter()
        for nodo in lista:
            mese = nodo.datetime.month
            conteggio_mesi[mese] += 1

            # Se il mese è già stato usato più di 3 volte, blocco subito
            if conteggio_mesi[mese] > 3:
                return False

        return True

    def getObjFun(self, lista):
        score = 0
        i = 1
        while i < len(lista):
            nodo1 = lista[i - 1]
            nodo2 = lista[i]

            if nodo1.datetime.month == nodo2.datetime.month:
                score += 200

            score += 100
            i += 1

        return score

    def getPesoArco(self, u, v):
        peso = self._graph[u][v]['weight']
        return peso

    def buildGraph(self, anno):
        self.nodes.clear()
        self.archi.clear()
        self._graph.clear()
        self.nodi = DAO.getNodes(anno)
        self._graph.add_nodes_from(self.nodi)

        for n in self.nodi:
            self.map[n.id] = n

        """for arco in DAO.getEdges(anno, self.map):
            self.archi.append(arco)
            self._graph.add_edge(arco.n1, arco.n2, weight=arco.peso)"""

    def getInformazioni(self):
        return f"Il Grafo è stato creato correttamente con {self._graph.number_of_nodes()} nodi e {self._graph.number_of_edges()} archi"

    def getComponenti(self):
        # Trova tutte le componenti connesse
        componenti = list(nx.connected_components(self._graph))

        # Numero componenti
        num_componenti = len(componenti)

        # Trova la componente più grande
        componente_massima = max(componenti, key=len)

        # Formatta l’output
        output = f"Numero componenti connesse: {num_componenti}\n"
        output += f"Componente connessa più grande ({len(componente_massima)} nodi):\n"

        for nodo in componente_massima:
            output += f"• {nodo.city} [{nodo.state}] - {nodo.datetime.strftime('%Y-%m-%d %H:%M:%S')}\n"

        return output




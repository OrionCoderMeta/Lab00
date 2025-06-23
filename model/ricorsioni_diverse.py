def getCamminoOttimo(self, t):
    # t invece la lunghezza percorso
    self.bestPath = []
    self.bestObjFun = 0

    for nodo in self._graph.nodes():
        parziale = [nodo]
        self._ricorsione(parziale, t)

    return self.bestPath, self.bestObjFun


def _ricorsione(self, parziale, t):
    # verificare se quello che ho messo dentro parziale è una possibile soluzione
    if len(parziale) == t + 1 and parziale[-1] == parziale[0]:
        # verificare se parziale è meglio del best
        if self.getObjFun(parziale) > self.bestObjFun:
            self.bestObjFun = self.getObjFun(parziale)
            self.bestPath = copy.deepcopy(parziale)

    # Posso aggiungere ancora nodi
    # prendo i vicini e aggiungo un nodo alla volta
    # ricorsione, IMPORTANTE, escludo doppioni MA NON il nodo iniziale
    for n in self._graph.neighbors(parziale[-1]):
        if n == parziale[0] and len(parziale) == t:
            parziale.append(n)
            self._ricorsione(parziale, t)
            parziale.pop()
        elif n not in parziale:
            parziale.append(n)
            self._ricorsione(parziale, t)
            parziale.pop()


def getObjFun(self, lista):
    # ho una lista di nodi, ogni iterazione prendo l'arco che collega i due nodi e ci sommo il peso
    score = 0
    i = 1
    while i < len(lista):
        peso = self._graph[lista[i - 1]][lista[i]]['weight']
        score += peso
        i += 1

    return score


def getPesoArco(self, u, v):
    peso = self._graph[u][v]['weight']
    return peso

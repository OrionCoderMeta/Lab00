# FUNZIONI EXTRA UTILI
from model.Arco import Arco


"""Dato un nodo restituisce tutti gli archi adiacenti
   Da nodo ordinati in modo DECRESCENTE
    Se il grafo fosse odinato questo sarebbe il contrario
    di quella sotto, quindi uscenti"""
def getAdiacentiNodo(self, nodo):
    adiacenti = []
    for vicino in self._graph.neighbors(nodo):
        peso = self._graph[nodo][vicino]['weight']
        arco = Arco(nodo, vicino, peso)
        adiacenti.append(arco)

    # Ordina per peso decrescente
    adiacenti.sort(key=lambda x: x.peso, reverse=True)
    return adiacenti


"""Da un nodo restituisce gli archi entranti
    ordinati DECRESCENTI"""
def getEntrantiNodo(self, nodo):
    entranti = []
    for vicino in self._graph.predecessors(nodo):
        peso = self._graph[vicino][nodo]['weight']
        arco = Arco(vicino, nodo, peso)
        entranti.append(arco)

    # Ordina per peso decrescente
    entranti.sort(key=lambda x: x.peso, reverse=True)
    return entranti

"""Fornisce il cammino più lungo in senso di nodi
    attraversti, escludendo il primo (ORIENTATO)"""
def getCammino(self, sourceStr):
    source = self.map[int(sourceStr)]
    lp = []

    # for source in self._graph.nodes:
    tree = nx.dfs_tree(self._graph, source)
    nodi = list(tree.nodes())

    for node in nodi:
        tmp = [node]

        while tmp[0] != source:
            pred = nx.predecessor(tree, source, tmp[0])
            tmp.insert(0, pred[0])

        if len(tmp) > len(lp):
            lp = copy.deepcopy(tmp)

    return lp[1:]

"""Fornisce il cammino più lungo in senso di nodi
    attraversti, escludendo il primo (NON ORIENTATO)"""
def getCamminoNonOrientato(self, sourceStr):
    source = self.map[int(sourceStr)]
    lp = []

    # Visita in ampiezza per raggiungere tutti i nodi nella componente
    tree = nx.bfs_tree(self._graph, source)
    nodi = list(tree.nodes())

    for node in nodi:
        try:
            path = nx.shortest_path(tree, source=source, target=node)
            if len(path) > len(lp):
                lp = copy.deepcopy(path)
        except nx.NetworkXNoPath:
            continue

    return lp[1:]  # Se vuoi escludere il nodo iniziale

"""Una lista di nodi direttamente raggiungibili da nodo (NON ORIENTATI)"""
def getRaggiungibiliDaNodo(self, nodo):
    raggiungibili = nx.node_connected_component(self._graph, nodo)
    raggiungibili.remove(nodo)  # Escludi il nodo stesso

    result = []
    for altro in raggiungibili:
        # Aggiungi solo se esiste un arco diretto tra nodo e altro
        if self._graph.has_edge(nodo, altro):
            peso = self._graph[nodo][altro]['weight']
            result.append((altro, peso))

    # Ordina per peso decrescente
    result.sort(key=lambda x: x[1], reverse=True)

    # Ritorna solo la lista dei nodi, ordinati
    return [nodo for nodo, _ in result]

"""Restituisce una lista di nodi raggiungibili da 'nodo' tramite archi orientati uscenti"""
def getRaggiungibiliDaNodoOrientato(self, nodo):
    # Ottieni i nodi raggiungibili seguendo gli archi orientati
    raggiungibili = nx.descendants(self._graph, nodo)

    result = []
    for altro in raggiungibili:
        if self._graph.has_edge(nodo, altro):  # Solo se l’arco esiste ed è diretto
            peso = self._graph[nodo][altro]['weight']
            result.append((altro, peso))

    # Ordina per peso decrescente
    result.sort(key=lambda x: x[1], reverse=True)

    # Ritorna solo la lista dei nodi, ordinati
    return [nodo for nodo, _ in result]


"""chiede il la componente connessa più alta e una descrizione di esse: (NON ORIENTATO)"""
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

"""chiede il la componente connessa più alta e una descrizione di esse: (ORIENTATO)"""
def getComponenti2(self):
    # Trova tutte le componenti debolmente connesse
    componenti = list(nx.weakly_connected_components(self._graph))

    # Numero componenti
    num_componenti = len(componenti)

    # Trova la componente più grande
    componente_massima = max(componenti, key=len)

    # Formatta l’output
    output = f"Numero componenti debolmente connesse: {num_componenti}\n"
    output += f"Componente più grande ({len(componente_massima)} nodi):\n"

    for nodo in componente_massima:
        output += f"• {nodo.city} [{nodo.state}] - {nodo.datetime.strftime('%Y-%m-%d %H:%M:%S')}\n"

    return output





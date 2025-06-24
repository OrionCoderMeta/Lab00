# FUNZIONI EXTRA UTILI
from model.Arco import Arco

"""Restituisce i 5 archi con peso maggiore"""
def getTop5Archi(self):
    # Assicurati che in self.archi ci siano oggetti di tipo Arco
    archi_ordinati = sorted(self.archi, key=lambda a: a.peso, reverse=True)
    top5 = archi_ordinati[:5]
    return "\n".join(str(arco) for arco in top5)

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


"""Ordiniamo i nodi per qualcosa"""
def getNodiVolume(self):
    for nodo in self._graph.nodes():
        volume = 0
        for u, v in self._graph.edges(nodo):
            peso = self._graph[u][v]['weight']
            volume += peso
        nodo.setVolume(volume)

    # Ordinamento decrescente per volume
    sorted_nodes = sorted(self._graph.nodes(), key=lambda v: v.getVolume(), reverse=True)

    result = ""
    for v in sorted_nodes:
        result += f"{v.Retailer_name}: volume = {v.getVolume()}\n"

    return result



"""Restituisce il grado (numero archi totali) di un nodo (NON ORIENTATO)"""
def getGradoNodo(self, nodo):
    grado = self._graph.degree[nodo]
    return f"Grado del nodo {nodo}: {grado}"


"""Restituisce tutti gli archi con peso maggiore di una soglia data"""
def getArchiSopraSoglia(self, soglia):
    archi_filtrati = []
    for u, v, data in self._graph.edges(data=True):
        if data['weight'] > soglia:
            arco = Arco(u, v, data['weight'])
            archi_filtrati.append(arco)

    # Ordina per peso decrescente
    archi_filtrati.sort(key=lambda x: x.peso, reverse=True)
    return "\n".join(str(arco) for arco in archi_filtrati)


"""Verifica se esiste un arco diretto tra due nodi specifici (utile per ORIENTATO)"""
def esisteArco(self, nodo1, nodo2):
    if self._graph.has_edge(nodo1, nodo2):
        peso = self._graph[nodo1][nodo2]['weight']
        return f"Esiste un arco da {nodo1} a {nodo2} con peso {peso}"
    else:
        return f"Nessun arco diretto da {nodo1} a {nodo2}"


"""Restituisce la media del peso di tutti gli archi del grafo"""
def getPesoMedioArchi(self):
    pesi = [d['weight'] for _, _, d in self._graph.edges(data=True)]
    if not pesi:
        return "Nessun arco presente nel grafo."
    media = sum(pesi) / len(pesi)
    return f"Peso medio archi: {media:.2f}"

"""Trova il cammino più breve (per peso) tra due nodi usando Dijkstra"""
def getCamminoDijkstra(self, sorgente, destinazione):
    try:
        path = nx.dijkstra_path(self._graph, sorgente, destinazione, weight='weight')
        distanza = nx.dijkstra_path_length(self._graph, sorgente, destinazione, weight='weight')
        return f"Cammino più breve: {' -> '.join(str(n) for n in path)}\nLunghezza totale: {distanza:.2f}"
    except nx.NetworkXNoPath:
        return f"Nessun cammino disponibile tra {sorgente} e {destinazione}"

"""Trova il percorso minimo (peso) tra due nodi usando Dijkstra"""
def getPercorsoMinimo(self, nodo1, nodo2):
    try:
        path = nx.dijkstra_path(self._graph, source=nodo1, target=nodo2, weight='weight')
        peso = nx.dijkstra_path_length(self._graph, source=nodo1, target=nodo2, weight='weight')
        return f"Percorso minimo da {nodo1} a {nodo2} (peso {peso}):\n" + " -> ".join(str(n) for n in path)
    except nx.NetworkXNoPath:
        return f"Nessun percorso da {nodo1} a {nodo2}"


"""Trova tutti i percorsi tra due nodi (limitato per evitare cicli infiniti)"""
def getTuttiPercorsi(self, nodo1, nodo2, max_depth=5):
    percorsi = list(nx.all_simple_paths(self._graph, source=nodo1, target=nodo2, cutoff=max_depth))
    output = f"Trovati {len(percorsi)} percorsi tra {nodo1} e {nodo2} (max profondit\u00e0 = {max_depth})\n"
    for p in percorsi:
        output += " -> ".join(str(n) for n in p) + "\n"
    return output


"""Restituisce l'albero DFS a partire da un nodo (solo nodi coinvolti)"""
def getDFSTree(self, nodo):
    tree = nx.dfs_tree(self._graph, source=nodo)
    nodi = list(tree.nodes())
    return f"DFS da {nodo}: {len(nodi)} nodi raggiunti\n" + ", ".join(str(n) for n in nodi)


"""Restituisce l'albero BFS a partire da un nodo (solo nodi coinvolti)"""
def getBFSTree(self, nodo):
    tree = nx.bfs_tree(self._graph, source=nodo)
    nodi = list(tree.nodes())
    return f"BFS da {nodo}: {len(nodi)} nodi raggiunti\n" + ", ".join(str(n) for n in nodi)


"""Restituisce il nodo con grado massimo (orientato o non) QUA E' SOMMA USCENTI + ENTRAMBI, per la 
    differenza vedere sotto"""
def getNodoConGradoMassimo(self):
    nodo, grado = max(self._graph.degree, key=lambda x: x[1])
    return f"Nodo con grado massimo: {nodo} ({grado} archi)"


"""Restituisce i 5 nodi con differenza (peso uscente - entrante) più alta (solo ORIENTATO)"""
def getTopDifferenzaPesoUscente(self):
    differenze = []

    for nodo in self._graph.nodes:
        peso_uscenti = 0
        for u, v in self._graph.out_edges(nodo):
            peso_uscenti += self._graph[u][v]['weight']

        peso_entranti = 0
        for u, v in self._graph.in_edges(nodo):
            peso_entranti += self._graph[u][v]['weight']

        diff = peso_uscenti - peso_entranti
        differenze.append((nodo, diff))

    # Ordina per differenza decrescente
    differenze.sort(key=lambda x: x[1], reverse=True)

    # Prendi i primi 5
    top5 = differenze[:5]

    # Costruisci il risultato in formato stringa
    result = ""
    for nodo, diff in top5:
        result += f"{nodo} → diff (uscente - entrante): {diff}\n"

    return result


"""Restituisce i nodi con il maggior valore di (entranti - uscenti)
   Ordinati in modo DECRESCENTE in base alla differenza"""
def getTopNodiDifferenzaEntrantiUscenti(self, top_n=5):
    differenze = []

    for nodo in self._graph.nodes:
        entranti = self._graph.in_degree(nodo)
        uscenti = self._graph.out_degree(nodo)
        diff = entranti - uscenti  # valore positivo = più archi entranti

        differenze.append((nodo, diff))

    # Ordina per differenza decrescente
    differenze.sort(key=lambda x: x[1], reverse=True)

    # Crea output leggibile
    result = ""
    for nodo, diff in differenze[:top_n]:
        result += f"{nodo}: entranti - uscenti = {diff}\n"

    return result






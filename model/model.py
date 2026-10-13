import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMapP = {}

    def getAllCountry(self):
        return DAO.getAllCountry()

    def creaGrafo(self, paese):
        self._grafo.clear()
        self._idMapP.clear()

        clienti = DAO.getAllNodes(paese)
        for a in clienti:
            self._idMapP[a.CustomerId] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
            a.fatturato_tot = DAO.getTotPerCliente(a.CustomerId)
            # print("3 - Cast caricato:", len(clienti))

            # Insieme degli artisti dei brani acquistati
            a.artisti = DAO.getArtistiPerCliente(a.CustomerId)
        print("2 - Nodi aggiunti")


        clienti = list(self._grafo.nodes)
       # PASSO 4: Doppio ciclo per confrontare le coppie (una sola volta: i + 1)
        for i in range(len(clienti)):
            for j in range(i + 1, len(clienti)):
               id1 = clienti[i]
               id2 = clienti[j]
              # c1 = self._idMapP[id1]
               #c2 = self._idMapP[id2]
               #s1 = spesa_map[id1]
               #s2 = spesa_map[id2]
               # Verifico se hanno almeno un artista in comune
               artisti_comuni = id1.artisti & id2.artisti

               if len(artisti_comuni) > 0:

                   tot1=id1.fatturato_tot
                   tot2=id2.fatturato_tot

                   # Calcolo del peso secondo la traccia
                   peso = tot1 + tot2

                   # Regole di orientamento archi
                   if  tot1 > tot2:
                       # Da chi ha speso meno a chi ha speso di più
                       self._grafo.add_edge(id1, id2, weight=peso)
                   elif  tot1< tot2:
                       self._grafo.add_edge(id2, id1, weight=peso)
                   else:
                       # Parità: arco bidirezionale
                       self._grafo.add_edge(id1, id2, weight=peso)
                       self._grafo.add_edge(id2, id1, weight=peso)

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getTop5Archi(self):
       # return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:10]
       archi = self._grafo.edges(data=True)
       return sorted(
           archi,
           key=lambda x: x[2]["weight"],
           reverse=True
       )[:5]

    def getClientePiuInfluente(self):
        cliente_migliore = None
        influenza_max = float("-inf")

        for cliente in self._grafo.nodes:
            uscenti = sum(d["weight"] for _, _, d in self._grafo.out_edges(cliente, data=True))
            #SCRIVO COSì SE NON MI INTERSSANO I NOMI DEI VALORI
            entranti = sum(d["weight"] for _, _, d in self._grafo.in_edges(cliente, data=True))

            influenza = uscenti - entranti

            if influenza > influenza_max:
                influenza_max = influenza
                cliente_migliore = cliente

        return cliente_migliore, influenza_max

    def controllaPesi(self):
        for arco in self._grafo.edges(data=True):
            c1, c2, dati = arco
            print(c1, "->", c2, "peso:", dati["weight"],
                  "tipo:", type(dati["weight"]))
import networkx as nx

from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.id_map= {}
        self.nodi = []
        self.dao = DAO()

    def get_date_range(self):
        return DAO.get_date_range()

    def get_categories(self):
        return self.dao.get_category()

    def build_grafo(self, cat, data_inizio, data_fine):
        nodi = self.dao.get_prodotti_per_categoria(cat)
        for nodo in nodi:
            self. nodi.append(nodo)
            self.G.add_node(nodo)
            self.id_map[nodo.id] = nodo

        connessioni = self.dao.get_connessioni(cat, data_inizio, data_fine)
        for connessione in connessioni:
            v1 = connessione['vendite1']
            v2 = connessione['vendite2']

            nodo1 = self.id_map[connessione['product1']]
            nodo2 = self.id_map[connessione['product2']]

            peso = connessione.get('peso', 0)

            if v1 > v2:
                self.G.add_edge(nodo1, nodo2, weight = peso)
            elif v1 < v2:
                self.G.add_edge(nodo2, nodo1, weight = peso)
            else:
                self.G.add_edge(nodo1, nodo2, weight = peso)
                self.G.add_edge(nodo2, nodo1, weight = peso)

    def dettagli_grafo(self):
        return self.G.number_of_nodes(), self.G.number_of_edges()

    def trova_prodotti_piu_venduti(self):

        prodotti_piu_venduti = []
        for n in self.G.nodes():
            score = 0
            for e_out in self.G.out_edges(n, data=True):
                score += e_out[2]["weight"]
            for e_in in self.G.in_edges(n, data=True):
                score -= e_in[2]["weight"]
            prodotti_piu_venduti.append((n,score))
        prodotti_piu_venduti.sort(key = lambda x: x[1], reverse = True)
        return prodotti_piu_venduti[:5]










import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.prodotti = []
        self.id_map = {}
        self.best_path = []
        self.best_score = 0

    def get_date_range(self):
        return DAO.get_date_range()

    def get_categories(self):
        return DAO.get_categories()

    def crea_grafo(self, category, inizio, fine):
        self.G.clear()

        self.prodotti = DAO.get_products_by_categories(category)
        self.G.add_nodes_from(self.prodotti)

        for prodotto in self.prodotti:
            self.id_map[prodotto.id] = prodotto

        #creo archi
        dizionario_prodotto_vendite = DAO.get_sales_by_product(category, inizio, fine)
        for prodotto1 in self.prodotti:
            for prodotto2 in self.prodotti:
                if prodotto1.id == prodotto2.id:
                    continue

                vendita1 = dizionario_prodotto_vendite.get(prodotto1.id, 0)
                vendita2 = dizionario_prodotto_vendite.get(prodotto2.id, 0)


                if vendita1 > 0 and vendita2 > 0:
                    peso_arco = vendita1 + vendita2
                    if vendita1 > vendita2:
                        self.G.add_edge(prodotto1, prodotto2, weight = peso_arco)
                    elif vendita1 < vendita2:
                        self.G.add_edge(prodotto2, prodotto1, weight = peso_arco)
                    elif vendita2 == vendita1:
                        self.G.add_edge(prodotto1, prodotto2, weight = peso_arco)
                        self.G.add_edge(prodotto2, prodotto1, weight = peso_arco)

    def get_number_of_edges_and_nodes(self):
        return self.G.number_of_edges(), self.G.number_of_nodes()

    def get_5_most_sold(self):
        prodotti_piu_venduti = []
        for nodo in self.G.nodes:
            somma = 0
            for archi_uscenti in self.G.out_edges(nodo, data=True):
                somma += archi_uscenti[2]['weight']
            for archi_entranti in self.G.in_edges(nodo, data=True):
                somma -= archi_entranti[2]['weight'] #[2] perche è l'attributo
            prodotti_piu_venduti.append((nodo,somma))

        prodotti_piu_venduti.sort(key=lambda x: x[1], reverse=True)
        return prodotti_piu_venduti[0:5]


















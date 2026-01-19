from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def populate_dd_categories(self):
        categorie = self._model.get_categories()

        options = []
        for categoria in categorie:
            option = ft.dropdown.Option(text = categoria.category_name, key = str(categoria.id))
            options.append(option)
        self._view.dd_category.options = options
        self._view.update()

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        self._view.txt_risultato.controls.clear()
        if self._view.dd_category.value is None:
            self._view.show_alert("Selezionare una categoria")

        categoria_selezionata = self._view.dd_category.value
        opzione = None
        for opt in self._view.dd_category.options:
            if opt.key == categoria_selezionata:
                opzione = opt
                break
        categoria_id = int(opzione.key)

        self._model.crea_grafo(categoria_id, self._view.dp1.value, self._view.dp2.value)
        numero_archi, numero_nodi = self._model.get_number_of_edges_and_nodes()
        prodotti_piu_venduti = self._model.get_5_most_sold()

        self._view.txt_risultato.controls.append(ft.Text("Date Selezionate"))
        self._view.txt_risultato.controls.append(ft.Text(f"Start Date: {self._view.dp1.value}"))
        self._view.txt_risultato.controls.append(ft.Text(f"End Date: {self._view.dp2.value}"))
        self._view.txt_risultato.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di nodi: {numero_nodi}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di archi: {numero_archi}"))
        self._view.txt_risultato.controls.append(ft.Text("I cinque prodotti piu venduti sono:"))
        i = 0
        while i < 5:
            self._view.txt_risultato.controls.append(ft.Text(f"  {i+1}. {prodotti_piu_venduti[i]}"))
            i += 1
        self._view.update()



    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO

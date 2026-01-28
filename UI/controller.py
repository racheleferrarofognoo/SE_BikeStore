
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

    def load_categories(self):
        categorie = self._model.get_categories()
        for cat in categorie:
            self._view.dd_category.options.append(ft.dropdown.Option(key=cat.id, text=cat.category_name))


    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        self._model.G.clear()
        self._view.txt_risultato.controls.clear()

        cat_scelta = self._view.dd_category.value
        data_inizio = self._view.dp1.value.date()
        data_fine = self._view.dp2.value.date()
        print(data_fine)
        grafo = self._model.build_grafo(cat_scelta, data_inizio, data_fine)
        num_nodi, num_archi = self._model.dettagli_grafo()
        self._view.txt_risultato.controls.append(ft.Text('Date selezionate:'))
        self._view.txt_risultato.controls.append(ft.Text(f'Start date: {data_inizio}'))
        self._view.txt_risultato.controls.append(ft.Text(f'End date: {data_fine}'))
        self._view.txt_risultato.controls.append(ft.Text('Grafo correttamente creato:'))
        self._view.txt_risultato.controls.append(ft.Text(f'Numero di nodi: {num_nodi}'))
        self._view.txt_risultato.controls.append(ft.Text(f'Numero di archi: {num_archi}'))

        self._view.update()


    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        migliori_prodotti = self._model.trova_prodotti_piu_venduti()
        self._view.txt_risultato.controls.append(ft.Text('I cinque prodotti più venduti sono:'))
        for prodotto in migliori_prodotti:
            nome_prodotto = prodotto[0].product_name
            valore = prodotto[1]
            self._view.txt_risultato.controls.append(ft.Text(f'{nome_prodotto} with score {valore}'))

        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO

import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        self._view.update_page()
        if self._mese == 0:
            self._view.create_alert("Nessun mese selezionato!")
        else:
            stringa=self._model.get_umiditamedia(self._mese)
            self._view.lst_result.controls.append(ft.Text(stringa))
            self._view.update_page()


    def handle_sequenza(self, e):
        self._view.lst_result.controls.clear()
        self._view.update_page()
        if self._mese == 0:
            self._view.create_alert("Nessun mese selezionato!")
        else:
            stringa = self._model.calcola_sequenza(self._mese)
            self._view.lst_result.controls.append(ft.Text(stringa))
            self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)


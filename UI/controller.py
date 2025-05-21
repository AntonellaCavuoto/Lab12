import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        paesi = self._model.getPaesi()
        for p in paesi:
            self._view.ddcountry.options.append(ft.dropdown.Option(p))
        i = 2015
        for j in range(4):
            if i <= 2018:
                self._view.ddyear.options.append(ft.dropdown.Option(str(i)))
                i += 1
        self._view.update_page()

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        paese = self._view.ddcountry.value

        numNodi, numArchi = self._model.buildGraph(paese, anno)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {numNodi} Numero di archi: {numArchi}"))
        self._view.update_page()

    def handle_volume(self, e):
        volumi = self._model.getVolumi()

        for v in volumi:
            self._view.txtOut2.controls.append(ft.Text(f"{v[0]} --> {v[1]}"))
        self._view.update_page()

    def handle_path(self, e):
        numMax = self._view.txtN.value

        bestPath, bestObjFunc = self._model.getPath(int(numMax))
        self._view.txtOut3.controls.clear()
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {bestObjFunc}"))
        self._view.update_page()

        for i in bestPath:
            self._view.txtOut3.controls.append(ft.Text(f"{i[0]} --> {i[1]}: {i[2]}"))

            self._view.update_page()

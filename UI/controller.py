import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDCountry(self):
        try:
            paesi = self._model.getAllCountry()
            for y in paesi:
                self._view._ddCountry.options.append(ft.dropdown.Option(key=y))
                                                                       # text=y.Name))
            self._view.update_page()

        except Exception as ex:
            self._view._txt_result.controls.append(ft.Text(f"Errore nel recupero dei paesi: {ex}", color="red"))
            self._view.update_page()


    def handleCreaGrafo(self, e):
        paese = self._view._ddCountry.value
        #start_node = self._model._idMapA[album_id]

        if self._view._ddCountry.value is None:
            self._view.create_alert("Selezionare prima un PAESE di partenza.", color="red")
            return
        try:
            self._model.creaGrafo(paese)
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()

            # Stampa immediata numero di vertici e archi (Punto 1.c)
            self._view._txt_result.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red")
            )
       # self.fillDDArtisti()
        self._view.update_page()

    def handleStampaInfo(self,e):
        self._view._txt_result.controls.clear()

        if self._model.get_num_nodes() == 0 or self._model.get_num_edges() is None:
            self._view.create_alert("Creare prima il grafo!", color="red")
            return
        self._model.controllaPesi()
        cliente, influenza = self._model.getClientePiuInfluente()
        self._view._txt_result.controls.append(ft.Text(f"  Il cliente più influente è: {cliente}  - (Influenza: {influenza})\n", color="orange"))

        # C) 5 ARCHI CON PESO MAGGIORE
        top5 = self._model.getTop5Archi()
        # self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f" 5 Archi di peso maggiore ", color="green"))

        # self._view._txt_result.controls.append(ft.Text(f"{arco[0]}-->{arco[1]} (peso: {arco[2]["weight"]})"))
        for i, arco in enumerate(top5, start=1):
            a1, a2, dati = arco
            self._view._txt_result.controls.append(
                ft.Text(f"{i})  {a1.FirstName} { a1.LastName} ({ a1.Country}) -- {a2.FirstName} { a2.LastName} ({ a2.Country} )"
                    f"(peso: {dati['weight']})"  )
                )
        self._view.update_page()




    def handleSequenza(self,e):
        pass
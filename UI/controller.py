# funzioni che uso sempre nel controller
import flet as ft

def classicoText(self=None):
    self._view.txt_result.controls.clear()
    self._view.txt_result.controls.append(ft.Text("Non lasciare il campo vuoto", color="red"))
    self._view.update_page()
    return

def handle_path(self, e):
    self._view.btn_path.disabled = True

    percorso, score = self._model.getCamminoOttimo()



    self._view.txt_result2.controls.clear()
    self._view.txt_result2.controls.append(ft.Text(f"Cammino ottimo con score {score} trovato !!!\n di seguito i nodi percorsi\n"))

    for elemento in percorso:
        self._view.txt_result2.controls.append(
            ft.Text(elemento))
    self._view.update_page()
    return

def fillDD(self):
    anni = DAO.getYears()
    for anno in anni:
        self._view._ddAnno.options.append(ft.dropdown.Option(key="IL VALORE", text="QUELLO CHE ESCE"))




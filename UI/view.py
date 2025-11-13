import flet as ft
from UI.alert import AlertManager

'''
    VIEW:
    - Rappresenta l'interfaccia utente
    - Riceve i dati dal MODELLO e li presenta senza modificarli
'''

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab08"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.LIGHT

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # SEZIONE 1: Intestazione
        self.txt_titolo = ft.Text(value="Analisi Consumo", size=38, weight=ft.FontWeight.BOLD)

        # SEZIONE 2: Dropdown + Pulsanti ######################################################
        self.dropdown_mese = ft.Dropdown(
            options=[ft.dropdown.Option(key="1", text="gennaio"),
                     ft.dropdown.Option(key="2", text="febbraio"),
                     ft.dropdown.Option(key="3", text="marzo"),
                     ft.dropdown.Option(key="4", text="aprile"),
                     ft.dropdown.Option(key="5", text="maggio"),
                     ft.dropdown.Option(key="6", text="giugno"),
                     ft.dropdown.Option(key="7", text="luglio"),
                     ft.dropdown.Option(key="8", text="agosto"),
                     ft.dropdown.Option(key="9", text="settembre"),
                     ft.dropdown.Option(key="10", text="ottobre"),
                     ft.dropdown.Option(key="11", text="novembre"),
                     ft.dropdown.Option(key="12", text="dicembre"), ],
            label="Mese",
            width=200,
            hint_text="Selezionare un mese",
            on_change=self.controller.leggi_mese
        )

        pulsante_consumo = ft.ElevatedButton(
            text="Consumo medio",
            tooltip="Verifica il consumo medio per impianto, nel mese selezionato",
            on_click=self.controller.get_consumo_medio
        )

        pulsante_calcolo_sequenza = ft.ElevatedButton(
            text="Calcola Sequenza",
            tooltip="Calcola la sequenza ottimale per le analisi",
            on_click=self.controller.calcola_sequenza
        )

        # SEZIONE 3: Visualizzazione mediante ListView ########################################
        self.lista_visualizzazione = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)


        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        self.page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            ft.Divider(),

            # Sezione 2: Dropdown + Pulsanti
            ft.Row(
                spacing=40,
                controls=[self.dropdown_mese, pulsante_consumo, pulsante_calcolo_sequenza],
                alignment=ft.MainAxisAlignment.CENTER
            ),

            # Sezione 3: Visualizzazione mediante ListView
            ft.Container(
                content=self.lista_visualizzazione,
                height=400,
                border=ft.border.all(1, ft.Colors.BLACK),
                padding=5,
            ),
        )

        self.page.scroll = "adaptive"
        self.page.update()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()

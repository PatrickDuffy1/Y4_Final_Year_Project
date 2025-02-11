import gradio as gr
from ui_main_menu import UiMainPage
from ui_model_page import UiModelPage
from ui_character_identifier_page import UiCharacterIdentifierPage

class Ui:
    def __init__(self, session):
        self._session = session
        
        ui_main_page = UiMainPage(self._session)
        ui_model_page = UiModelPage(self._session)
        ui_character_identifier_page = UiCharacterIdentifierPage(self._session)
        
        main_ui = gr.TabbedInterface(
            [
                ui_main_page.main_menu,
                ui_model_page.model_page,
                ui_character_identifier_page.test_chapter_interface
            ],
            [
                "Main Menu",
                "Model",
                "Character Identifier"
            ]
        )
        
        main_ui.launch()

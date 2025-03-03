import gradio as gr
from ui_main_menu import UiMainPage
from ui_model_page import UiModelPage
from ui_character_identifier_page import UiCharacterIdentifierPage
from ui_line_identifier_page import UiLineIdentifierPage
from ui_multi_speaker_page import UiMultiSpeakerPage

class Ui:
    def __init__(self, session):
        self._session = session
        
        ui_main_page = UiMainPage(self._session)
        ui_model_page = UiModelPage(self._session)
        ui_character_identifier_page = UiCharacterIdentifierPage(self._session)
        ui_line_identifier_page = UiLineIdentifierPage(self._session)
        ui_multi_speaker_page = UiMultiSpeakerPage(self._session)
        
        main_ui = gr.TabbedInterface(
            [
                ui_main_page.main_menu,
                ui_model_page.model_page,
                ui_character_identifier_page.character_identifier_page,
                ui_line_identifier_page.line_identifier_page,
                ui_multi_speaker_page.multi_speaker_page
            ],
            [
                "Main Menu",
                "Model",
                "Character Identifier",
                "Line Identifier",
                "Multi Speaker"
            ]
        )
        
        main_ui.launch()

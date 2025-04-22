import gradio as gr
from ui_single_speaker_page import UiSingleSpeakerPage
from ui_model_page import UiModelPage
from ui_line_identifier_page import UiLineIdentifierPage
from ui_multi_speaker_page import UiMultiSpeakerPage

class Ui:
    def __init__(self, session):
        self._session = session
        
        ui_single_speaker_page = UiSingleSpeakerPage(self._session)
        ui_model_page = UiModelPage(self._session)
        ui_line_identifier_page = UiLineIdentifierPage(self._session)
        ui_multi_speaker_page = UiMultiSpeakerPage(self._session)
        
        main_ui = gr.TabbedInterface(
            [
                ui_single_speaker_page.single_speaker_page,
                ui_model_page.model_page,
                ui_line_identifier_page.line_identifier_page,
                ui_multi_speaker_page.multi_speaker_page
            ],
            [
                "Single Speaker",
                "Load Model",
                "Line Identifier",
                "Multi Speaker"
            ]
        )
        
        main_ui.launch()

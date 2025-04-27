import gradio as gr
import webbrowser
from ui_single_speaker_page import UiSingleSpeakerPage
from ui_model_page import UiModelPage
from ui_line_identifier_page import UiLineIdentifierPage
from ui_multi_speaker_page import UiMultiSpeakerPage

LOCAL_HOST = "127.0.0.1"
DEFAULT_PORT = "7860"

class Ui:
    def __init__(self, session, launch_ui_on_start_up):
        self._session = session
        
        # Initialize all UI page objects
        ui_single_speaker_page = UiSingleSpeakerPage(self._session)
        ui_model_page = UiModelPage(self._session)
        ui_line_identifier_page = UiLineIdentifierPage(self._session)
        ui_multi_speaker_page = UiMultiSpeakerPage(self._session)
        
        # Wrap them into a tabbed interface
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
        
        # Launch the UI (assuming it is on the default port) if the boolean is set
        if launch_ui_on_start_up:
            webbrowser.open(f"http://{LOCAL_HOST}:{DEFAULT_PORT}")
            
        main_ui.launch()

import gradio as gr

class UiMultiSpeakerPage:
    def __init__(self, session):
        self._session = session
        self.multi_speaker_page = self.get_gradio_page()

    def generate_multi_speaker_audio(self, book_folder):
            
        return "Test" #self._session.generate_multi_speaker_audio(self, book_folder)

    
    def get_gradio_page(self):
    
        return gr.Interface(
            fn=self.generate_multi_speaker_audio,
            inputs=[
                "file"
            ],
            outputs=["text"], # Output box for audio file
            allow_flagging="never",  # Disables the flagging functionality
        )
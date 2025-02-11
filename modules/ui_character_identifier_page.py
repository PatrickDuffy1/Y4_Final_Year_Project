import gradio as gr

class UiCharacterIdentifierPage:
    def __init__(self, session):
        self._session = session
        self.test_chapter_interface = self.get_gradio_page()

    def indentify_chapter_characters(self, chapter):
        return self._session.indentify_chapter_characters(chapter)

    
    def get_gradio_page(self):
    
        return gr.Interface(
            fn=self.indentify_chapter_characters,
            inputs=[
                "text",
            ],
            outputs=["text"], # Output box for audio file
            allow_flagging="never",  # Disables the flagging functionality
        )
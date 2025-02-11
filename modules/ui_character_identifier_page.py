import gradio as gr

class UiCharacterIdentifierPage:
    def __init__(self, session):
        self._session = session
        self.test_chapter_interface = self.get_gradio_page()

    def indentify_book_characters(self, input_text, input_file):
    
        if input_text:
            user_input = input_text
            is_file = False
        elif input_file:
            user_input = input_file.name
            is_file = True
        else:
            return "Please provide either text or a file."
            
        return self._session.indentify_book_characters(user_input, is_file)

    
    def get_gradio_page(self):
    
        return gr.Interface(
            fn=self.indentify_book_characters,
            inputs=[
                "text",
                "file"
            ],
            outputs=["text"], # Output box for audio file
            allow_flagging="never",  # Disables the flagging functionality
        )
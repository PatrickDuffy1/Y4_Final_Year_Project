import gradio as gr

class UiCharacterIdentifierPage:
    def __init__(self, session):
        self._session = session
        self.character_identifier_page = self.get_gradio_page()

    def indentify_book_characters(self, input_text, input_file):
        
        
        if input_text:
            user_input = input_text
        elif input_file:
            user_input = input_file.name
        else:
            return "Please provide either text or a file."
            
        return self._session.indentify_book_characters(user_input)

    
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
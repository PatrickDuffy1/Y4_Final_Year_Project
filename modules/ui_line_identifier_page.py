import gradio as gr

class UiLineIdentifierPage:
    def __init__(self, session):
        self._session = session
        self.line_identifier_page = self.get_gradio_page()

    def indentify_character_lines(self, input_text, input_file, start_section, end_section):
    
        if input_text:
            user_input = input_text
            is_file = False
        elif input_file:
            user_input = input_file.name
            is_file = True
        else:
            return "Please provide either text or a file."
            
        print(user_input)
            
        return self._session.indentify_character_lines(user_input, is_file, int(start_section), int(end_section))

    
    def get_gradio_page(self):
    
        return gr.Interface(
            fn=self.indentify_character_lines,
            inputs=[
                "text",
                "file",
                gr.Textbox("0"),
                gr.Textbox("-1")
            ],
            outputs=["text"], # Output box for audio file
            allow_flagging="never",  # Disables the flagging functionality
        )
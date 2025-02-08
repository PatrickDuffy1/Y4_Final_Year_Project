import gradio as gr
from ui_main_menu import main_menu
from ui_model_page import model_page, test_chapter_interface

class Ui:
  def __init__(self):
    main_ui = gr.TabbedInterface([main_menu, model_page, test_chapter_interface], ["Main Menu", "Model", "Test Chapter"])

    main_ui.launch()


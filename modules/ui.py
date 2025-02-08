import gradio as gr
from ui_main_menu import UiMainPage
from ui_model_page import UiModelPage, UiTestChapterPage

class Ui:
  def __init__(self, session):
    self._session = session
    
    ui_main_page = UiMainPage(self._session)
    ui_model_page = UiModelPage(self._session)
    ui_test_chapter_page = UiTestChapterPage(self._session)
    
    main_ui = gr.TabbedInterface([ui_main_page.main_menu,
                                  ui_model_page.model_page,
                                  ui_test_chapter_page.test_chapter_interface
                                  ],
                                  ["Main Menu",
                                  "Model",
                                  "Test Chapter"
                                  ])

    main_ui.launch()


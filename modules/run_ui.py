import os
from ui import Ui
from session import Session

launch_ui_on_start_up = True

print("Starting...")
current_session = Session() # Create a session
ui = Ui(current_session, launch_ui_on_start_up) # Load the UI

import os
from ui import Ui
from session import Session

current_session = Session() # Create a session
ui = Ui(current_session) # Load the UI

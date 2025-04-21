import os
from ui import Ui
from session import Session

# Get the parent directory of the script's location
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
outputs_path = os.path.join(parent_dir, "outputs")

# Check if the outputs folder exists, and create it if not
if not os.path.exists(outputs_path):
    os.makedirs(outputs_path)

current_session = Session()
ui = Ui(current_session)

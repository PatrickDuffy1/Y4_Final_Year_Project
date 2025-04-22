# Import the function to load an LLM model
from llm_model_loader import load_llm_model

class Llm:
    def __init__(self, model_config, model=None):
        # Store the configuration for the model
        self._model_config = model_config
        # Initialize the model attribute to None
        self._model = None
        
        # If a model instance is passed, use it
        if model is not None:
            self._model = model
        else:
            # Otherwise, load the model using the provided config
            self._model = load_llm_model(self)

    def load_model(self):
        # Method to (re)load the model using the current config
        self._model = load_llm_model(self)
        return "Model Loaded"

    # Getter for model_config
    @property
    def model_config(self):
        return self._model_config

    # Setter for model_config
    @model_config.setter
    def model_config(self, value):
        self._model_config = value

    # Getter for model
    @property
    def model(self):
        return self._model

    # Setter for model
    @model.setter
    def model(self, value):
        self._model = value

    def __str__(self):
        # String representation showing the config and model status
        config_str = ", ".join(f"{key}={value}" for key, value in self._model_config.items())
        return f"Llm({config_str}, model={'Loaded' if self._model else 'None'})"

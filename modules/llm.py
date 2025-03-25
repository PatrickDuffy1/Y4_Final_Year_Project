from llm_model_loader import load_llm_model

class Llm:
    def __init__(self, model_config, model=None):
        
        self._model_config = model_config
        self._model = None
        
        if model is not None:
            self._model = load_llm_model(self)
            
            
    def load_model(self):
        self._model = load_llm_model(self)
        
        return "Model Loaded"
        

    # Getters and Setters
    @property
    def model_config(self):
        return self._model_config
        
    @model_config.setter
    def model_config(self, value):
        self._model_config = value
    
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, value):
        self._model = value
    
    def __str__(self):
        config_str = ", ".join(f"{key}={value}" for key, value in self._model_config.items())
        return f"Llm({config_str}, model={'Loaded' if self._model else 'None'})"


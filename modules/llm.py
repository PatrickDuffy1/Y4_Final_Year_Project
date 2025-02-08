from llm_model_loader import load_llm_model

class Llm:
    def __init__(self, model_path, repo_id, context_length, gpu_layers, temperature, seed, model=None):
        self._model_path = model_path
        self._repo_id = repo_id
        self._context_length = context_length
        self._gpu_layers = gpu_layers
        self._temperature = temperature
        self._seed = seed
        
        if model is not None:
            self._model = load_llm_model(self)
        else:
            self._model = None
            
    def load_model(self):
        self._model = load_llm_model(self)
        
        return "Model Loaded"

    # Getters and Setters
    @property
    def model_path(self):
        return self._model_path
    
    @model_path.setter
    def model_path(self, value):
        self._model_path = value
    
    @property
    def repo_id(self):
        return self._repo_id
    
    @repo_id.setter
    def repo_id(self, value):
        self._repo_id = value
    
    @property
    def context_length(self):
        return self._context_length
    
    @context_length.setter
    def context_length(self, value):
        self._context_length = value
    
    @property
    def gpu_layers(self):
        return self._gpu_layers
    
    @gpu_layers.setter
    def gpu_layers(self, value):
        self._gpu_layers = value
    
    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        self._temperature = value
    
    @property
    def seed(self):
        return self._seed
    
    @seed.setter
    def seed(self, value):
        self._seed = value
    
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, value):
        self._model = value
    
    def __str__(self):
        return (f"Llm(model_path={self._model_path}, "
                f"repo_id={self._repo_id}, context_length={self._context_length}, "
                f"gpu_layers={self._gpu_layers}, temperature={self._temperature}, "
                f"seed={self._seed}, model={'Loaded' if self._model else 'None'})")

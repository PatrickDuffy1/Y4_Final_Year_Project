from llm import Llm
from llm_chapter_manager import identify_characters_in_chapter

class Session:
    def __init__(self, llm=None):
        self._llm = llm
        
    
    def set_and_load_llm(self, model_path, repo_id, context_length, gpu_layers, temperature, seed):
        self._llm = Llm(model_path, repo_id, context_length, gpu_layers, temperature, seed)
        self.load_llm()
        
        return self._llm
        
        
    def load_llm(self):
        self._llm.load_model()
        
        return self._llm
        
    def indentify_chapter_characters(self, chapter):
        
        if self._llm is not None:
            return identify_characters_in_chapter(chapter, self._llm)
        
        return "Error"
from llm import Llm
from llm_chapter_manager import indentify_book_character_lines
from audio_generator_manager import tts_generate_audio, tts_generate_multi_speaker_audio

class Session:
    def __init__(self, llm=None):
        self._llm = llm
        
    
    def set_and_load_llm(self, model_path, model_type, repo_id=None, context_length=2048, gpu_layers=0, temperature=0.7, seed=0):
    
        llm_config = {
            'model_path': model_path,
            'repo_id': repo_id,
            'context_length': context_length,
            'gpu_layers': gpu_layers,
            'temperature': temperature,
            'seed': seed,
            'model_type': model_type
        }
        
        self._llm = Llm(llm_config)
        self.load_llm()
        
        return self._llm
        
        
    def set_cloud_llm(self, model_name, api_key, model_type, max_tokens=2048, temperature=0.7):
    
        llm_config = {
            'model_name': model_name,
            'api_key': api_key,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'model_type': model_type
        }
        
        self._llm = Llm(llm_config)
        
        return self._llm
              
        
    def load_llm(self):
        self._llm.load_model()
        
        return self._llm
        
        
    def indentify_character_lines(self, user_input, is_file, output_folder="", start_section=0, end_section=-1, missing_narrator_max_retries=5):
            
        if self._llm is not None:           
            return indentify_book_character_lines(self._llm, user_input, is_file, start_section, end_section, output_folder, missing_narrator_max_retries)
        
        return "No model loaded"
        
    
    def generate_audio(self, user_input, voice, output_folder, output_file_type=".wav"):
        
        return tts_generate_audio(user_input, voice, output_folder, output_file_type)
        
        
    def generate_multi_speaker_audio(self, folder_path):
        
        return tts_generate_multi_speaker_audio(folder_path)
    
        
from llm import Llm
from llm_chapter_manager import identify_characters_in_book, identify_lines_in_book, identify_characters
from audio_generator_manager import tts_generate_audio
from utils import save_file_to_directory
from datetime import datetime

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
        
        
    def indentify_book_characters(self, user_input, is_file):
        
        if self._llm is not None:
            return identify_characters_in_book(user_input, self._llm, is_file)
        
        return "Error"
        
        
    def indentify_character_lines(self, user_input, is_file):
        
        if self._llm is not None:
            book_directory_path = "../processed_books/" + str(datetime.now()).replace(":", "_").replace(".", "_").replace(" ", "_")
            
            character_lines = identify_lines_in_book(user_input, self._llm, is_file)
            save_file_to_directory(book_directory_path, "chapter_lines.json", character_lines)
            
            save_file_to_directory(book_directory_path, "book_characters.json", identify_characters(character_lines))
            identify_characters(character_lines)
            return character_lines
        
        return "Error"
        
    
    def generate_audio(self, user_input, voice, output_folder, output_file_type):
        
        return tts_generate_audio(user_input, voice, output_folder, output_file_type)
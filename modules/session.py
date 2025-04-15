from llm import Llm
from llm_chapter_manager import identify_characters_in_book, identify_lines_in_book, identify_characters, extract_lines_and_voices, stitch_wav_files, merge_character_json_files
from audio_generator_manager import tts_generate_audio
from utils import save_file_to_directory, count_files_in_directory
from datetime import datetime
from file_reader import read_file
import os

class Session:
    def __init__(self, llm=None):
        self._llm = llm
        self.create_directories()
        
    
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
        
        
    def indentify_book_characters(self, user_input):
        
        if self._llm is not None:
            return identify_characters_in_book(user_input, self._llm)
        
        return "Error"
        
        
    def indentify_character_lines(self, user_input, is_file):
    
        if is_file:
            # Read the given file
            text = read_file(user_input)
        else:
            text = list()
            text.append(user_input)
            
        if self._llm is not None:
            book_directory_path = "../processed_books/" + str(datetime.now()).replace(":", "_").replace(".", "_").replace(" ", "_")
            
            for i in range(0, len(text)):
                character_lines = identify_lines_in_book(text[i], self._llm, is_file)
                save_file_to_directory(book_directory_path + "/chapter_lines", "chapter_" + str(i) + "_lines.json", character_lines)
                
                save_file_to_directory(book_directory_path + "/book_characters", "book_characters_chapter_" + str(i) + ".json", identify_characters(character_lines))
                merge_character_json_files(book_directory_path + "/book_characters")
                
            return character_lines
        
        return "No model loaded"
        
    
    def generate_audio(self, user_input, voice, output_folder, is_file=True, output_file_type=".wav"):
        
        return tts_generate_audio(user_input, voice, output_folder, is_file, output_file_type)
        
        
    def generate_multi_speaker_audio(self, folder_path):
        
        folder_path = folder_path.replace("\\", "/")
        number_of_chapters = count_files_in_directory(folder_path + "/chapter_lines")
        
        for i in range(0, number_of_chapters):
            lines, voices = extract_lines_and_voices(folder_path + "/chapter_lines/chapter_" + str(i) + "_lines.json", folder_path + "/book_characters/book_characters_chapter_" + str(i) + ".json")
            
            temp_files_path = folder_path + "/temp_audio_" + str(i)
            os.makedirs(temp_files_path, exist_ok=True)
            self.generate_audio(lines, voices, temp_files_path + "/")
            stitch_wav_files(folder_path + "/temp_audio_" + str(i), i)
            
        return "Audio generation complete"
        
        
    def create_directories(self):
   
        # Get the parent directory of the script's location
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        outputs_path = os.path.join(parent_dir, "outputs")

        # Check if the outputs folder exists, and create it if not
        if not os.path.exists(outputs_path):
            os.makedirs(outputs_path)
    
        

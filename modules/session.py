import os
from llm import Llm
from llm_chapter_manager import identify_book_character_lines  # Function to process and identify character lines in text
from audio_generator_manager import tts_generate_audio, tts_generate_multi_speaker_audio  # Functions to generate audio from text

# Define the Session class to manage the LLM and associated operations
class Session:
    def __init__(self, llm=None):
        # Initialize with an optional LLM instance
        self._llm = llm
        self.create_output_folders()

    def set_and_load_llm(self, model_path, model_type, repo_id=None, context_length=2048, gpu_layers=0, temperature=0.7, seed=0):
        """
        Set up a local LLM using the given configuration parameters and load it.
        """
        llm_config = {
            'model_path': model_path,
            'repo_id': repo_id,
            'context_length': context_length,
            'gpu_layers': gpu_layers,
            'temperature': temperature,
            'seed': seed,
            'model_type': model_type
        }

        # Create an LLM instance with the config
        self._llm = Llm(llm_config)
        self.load_llm()  # Load the model

        return self._llm  # Return the initialized and loaded LLM instance

    def set_cloud_llm(self, model_name, api_key, model_type, max_tokens=2048, temperature=0.7):
        """
        Set up a cloud-based LLM using the given API credentials and parameters.
        """
        llm_config = {
            'model_name': model_name,
            'api_key': api_key,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'model_type': model_type
        }

        # Create an LLM instance with cloud configuration
        self._llm = Llm(llm_config)

        return self._llm  # Return the cloud-based LLM instance

    def load_llm(self):
        """
        Load the model for inference.
        """
        self._llm.load_model()  # Trigger the model loading
        return self._llm  # Return the loaded model instance

    def indentify_character_lines(self, user_input, is_file, output_folder="", start_section=0, end_section=-1, missing_narrator_max_retries=10):
        """
        Identify character lines in the given input (file or text) using the loaded LLM.
        """
        self.create_output_folders()
        
        if self._llm is not None:
            output_path = identify_book_character_lines(
                self._llm,
                user_input,
                is_file,
                start_section,
                end_section,
                output_folder,
                missing_narrator_max_retries
            )
            
            output_path = os.path.realpath(output_path)
            os.startfile(output_path)
            
            return output_path
            
        return "No model loaded"  # Return error message if model is not set

    def generate_audio(self, user_input, voice, is_file, output_folder, output_file_type=".wav"):
        """
        Generate single-speaker audio from text using TTS.
        """
        self.create_output_folders()
        
        return tts_generate_audio(user_input, voice, is_file, output_folder, False, output_file_type)

    def generate_multi_speaker_audio(self, folder_path):
        """
        Generate multi-speaker audio from previously processed text data.
        """
        
        print("Generating multi-speaker audio")
        
        return tts_generate_multi_speaker_audio(folder_path)
        
        
    def create_output_folders(self):
        """
        Create output folders in the parent directory of the current file if they have not already been created.
        """
        # Get the parent directory of the directory containing this file
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_file_dir)
        
        folders = ['multi_speaker_outputs', 'single_speaker_outputs']
        for folder in folders:
            path = os.path.join(parent_dir, folder)
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"Created folder: {path}")

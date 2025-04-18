import argparse
from session import Session

def main():
    parser = argparse.ArgumentParser(description="Process book text and generate audio using LLM.")
    
    # LLM arguments (local model)
    parser.add_argument("--llm_model_path", help="Path to the LLM.")
    parser.add_argument("--llm_model_type", default="default_type", help="Type of the model.")
    parser.add_argument("--llm_repo_id", default=None, help="Repository ID of the model.")
    parser.add_argument("--llm_context_length", type=int, default=2048, help="Context length for the model.")
    parser.add_argument("--llm_gpu_layers", type=int, default=0, help="Number of GPU layers.")
    parser.add_argument("--llm_temperature", type=float, default=0.7, help="Temperature setting for the model.")
    parser.add_argument("--llm_seed", type=int, default=-1, help="Seed for the LLM. Default (-1) is a random seed.")
    
    # LLM arguments (cloud-based)
    parser.add_argument("--cloud_llm_model_name", type=str, help="Cloud LLM model name.")
    parser.add_argument("--cloud_llm_api_key", type=str, help="API key for cloud LLM.")
    parser.add_argument("--cloud_llm_model_type", type=str, help="Model type for cloud LLM. OPEN_AI OR GEMINI")
    parser.add_argument("--cloud_llm_max_tokens", type=int, default=2048, help="Max tokens for cloud LLM.")
    
    # Identify characters
    parser.add_argument("--identify_characters_user_input", type=str, help="User input for identifying characters.")

    # Identify lines
    parser.add_argument("--identify_lines_user_input", type=str, help="User input for identifying lines.")

    # Audio generation
    parser.add_argument("--generate_audio_input", type=str, help="Text/file path for generating audio.")
    parser.add_argument("--generate_audio_voice", type=str, help="Voice for generating audio.")
    parser.add_argument("--generate_audio_output_folder", type=str, default="../outputs", help="Output folder for generated audio.")
    parser.add_argument("--is_file", type=bool, default=True, help="Input type (text or file). Default is True.")

    # Multi-speaker audio
    parser.add_argument("--multi_speaker_audio_folder_path", type=str, help="Folder path for multi-speaker audio generation.")
    
    args = parser.parse_args()
    
    session = Session()

    # Set LLM if needed (for character/line identification)
    if args.llm_model_path:
        session.set_and_load_llm(
            model_path=args.llm_model_path,
            model_type=args.llm_model_type,
            repo_id=args.llm_repo_id,
            context_length=args.llm_context_length,
            gpu_layers=args.llm_gpu_layers,
            temperature=args.llm_temperature,
            seed=args.llm_seed
        )
        print("LLM Model Loaded.")
    
    # Set Cloud LLM if needed
    if args.cloud_llm_model_name and args.cloud_llm_api_key and args.cloud_llm_model_type:
        session.set_cloud_llm(
            model_name=args.cloud_llm_model_name,
            api_key=args.cloud_llm_api_key,
            model_type=args.cloud_llm_model_type,
            max_tokens=args.cloud_llm_max_tokens
        )
        print("Cloud-based LLM Loaded.")
    
    # Identify characters in book (if needed)
    if args.identify_characters_user_input:
        result = session.indentify_book_characters(args.identify_characters_user_input, is_file=False)
        print("Identified Characters:", result)
    
    # Identify lines in book (if needed)
    if args.identify_lines_user_input:
        result = session.indentify_character_lines(args.identify_lines_user_input, is_file=False)
        print("Identified Character Lines:", result)
    
    # Generate audio (without needing LLM)
    if args.generate_audio_input and args.generate_audio_voice and args.generate_audio_output_folder:
        result = session.generate_audio(
            args.generate_audio_input,
            args.generate_audio_voice,
            args.generate_audio_output_folder,
            args.is_file,
            ".wav"  # Always ".wav" as output type
        )
        print("Generated Audio:", result)
    
    # Multi-speaker audio (without needing LLM)
    if args.multi_speaker_audio_folder_path:
        result = session.generate_multi_speaker_audio(args.multi_speaker_audio_folder_path)
        print("Multi-Speaker Audio:", result)
        
        
if __name__ == "__main__":
    main()

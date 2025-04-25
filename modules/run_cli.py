import argparse
import sys
from session import Session
from pathlib import Path

script_dir = Path(__file__).resolve().parent
outputs_path = script_dir / ".." / "single_speaker_outputs"

def main():
    parser = argparse.ArgumentParser(
        description="Process book text and generate audio using LLM.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
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

    # Identify lines
    parser.add_argument("--identify_lines_user_input", type=str, help="User input for identifying lines. Requires LLM.")
    parser.add_argument("--start_section", type=int, default=0, help="Start section index for line identification.")
    parser.add_argument("--end_section", type=int, default=-1, help="End section index for line identification.")
    parser.add_argument("--output_folder", type=str, help="Optional folder to store character line outputs.")
    parser.add_argument("--missing_narrator_max_retries", type=int, default=5, help="Max retries for missing narrator detection.")
    
    # Audio generation
    parser.add_argument("--generate_audio_input", type=str, help="Text/file path for generating audio.")
    parser.add_argument("--generate_audio_voice", type=str, help="Voice for generating audio.")
    parser.add_argument("--is_file", type=bool, default=True, help="Input type (text or file). Default is True.")

    # Multi-speaker audio
    parser.add_argument("--multi_speaker_audio_folder_path", type=str, help="Folder path for multi-speaker audio generation.")
    
    # Show help if no arguments are passed
    if len(sys.argv) == 1:
        print("\nNo arguments provided. Here's how to use this script:\n")
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()

    # Validation: If user wants to identify lines, LLM must be provided
    if args.identify_lines_user_input:
        local_llm_set = args.llm_model_path is not None
        cloud_llm_set = all([
            args.cloud_llm_model_name,
            args.cloud_llm_api_key,
            args.cloud_llm_model_type
        ])
        if not (local_llm_set or cloud_llm_set):
            parser.error(
                "To use --identify_lines_user_input, you must provide either local LLM arguments "
                "(--llm_model_path) or cloud LLM arguments (--cloud_llm_model_name, --cloud_llm_api_key, --cloud_llm_model_type)."
            )

    # Validation: local LLM params used without model path
    local_llm_params = [
        args.llm_model_type, args.llm_repo_id, args.llm_context_length,
        args.llm_gpu_layers, args.llm_temperature, args.llm_seed
    ]
    if any(p is not None and args.llm_model_path is None for p in local_llm_params):
        parser.error("Local LLM parameters provided without --llm_model_path. Please specify the model path.")

    # Validation: cloud LLM params used without model name
    cloud_llm_params = [args.cloud_llm_api_key, args.cloud_llm_model_type]
    if any(p is not None and args.cloud_llm_model_name is None for p in cloud_llm_params):
        parser.error("Cloud LLM parameters provided without --cloud_llm_model_name. Please specify the model name.")

    # Validation: identify_lines-dependent arguments used without main input
    identify_dependent_args = [
        ("--start_section", args.start_section != 0),
        ("--end_section", args.end_section != -1),
        ("--output_folder", args.output_folder is not None),
        ("--missing_narrator_max_retries", args.missing_narrator_max_retries != 5)
    ]
    if not args.identify_lines_user_input:
        used_args = [name for name, used in identify_dependent_args if used]
        if used_args:
            parser.error(
                f"The following arguments require --identify_lines_user_input: {', '.join(used_args)}"
            )

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
    
    # Identify lines in book (if needed)
    if args.identify_lines_user_input:
        output_folder = args.output_folder if args.output_folder else ""
        result = session.indentify_character_lines(
            user_input=args.identify_lines_user_input,
            is_file=args.is_file,
            output_folder=output_folder,
            start_section=args.start_section,
            end_section=args.end_section,
            missing_narrator_max_retries=args.missing_narrator_max_retries
        )
        print("Identified Character Lines:", result)
    
    # Generate single-speaker audio
    if args.generate_audio_input and args.generate_audio_voice:
        result = session.generate_audio(
            args.generate_audio_input,
            args.generate_audio_voice,
            str(outputs_path),
            args.is_file,
            ".wav"
        )
        print("Generated Audio:", result)
    
    # Generate multi-speaker audio
    if args.multi_speaker_audio_folder_path:
        result = session.generate_multi_speaker_audio(args.multi_speaker_audio_folder_path)
        print("Multi-Speaker Audio:", result)

if __name__ == "__main__":
    main()

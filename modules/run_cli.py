import argparse
import sys
from session import Session
from pathlib import Path
from text_generator import Model_Type  # <- Important: import Model_Type for enum conversion

script_dir = Path(__file__).resolve().parent
outputs_path = script_dir / ".." / "single_speaker_outputs"

def main():
    print("Processing...")

    parser = argparse.ArgumentParser(
        description="Process book text and generate audio using LLM.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # LLM arguments (local model)
    parser.add_argument("--llm_model_path", help="Path to the LLM.")
    parser.add_argument("--llm_model_type", default="LOCAL_FILE", help="Type of the model. Options: LOCAL_FILE, HUGGING_FACE, OPEN_AI.")
    parser.add_argument("--llm_repo_id", default=None, help="Repository ID of the model.")
    parser.add_argument("--llm_context_length", type=int, default=2048, help="Context length for the model.")
    parser.add_argument("--llm_gpu_layers", type=int, default=0, help="Number of GPU layers.")
    parser.add_argument("--llm_temperature", type=float, default=0.7, help="Temperature setting for the model.")
    parser.add_argument("--llm_seed", type=int, default=-1, help="Seed for the LLM. Default (-1) is a random seed.")

    # LLM arguments (cloud-based)
    parser.add_argument("--cloud_llm_model_name", type=str, help="Cloud LLM model name.")
    parser.add_argument("--cloud_llm_api_key", type=str, help="API key for cloud LLM.")
    parser.add_argument("--cloud_llm_model_type", type=str, help="Model type for cloud LLM. Options: OPEN_AI")
    parser.add_argument("--cloud_llm_max_tokens", type=int, default=2048, help="Max tokens for cloud LLM.")

    # Identify lines
    parser.add_argument("--identify_lines_input_text", type=str, help="Direct text input for identifying lines.")
    parser.add_argument("--identify_lines_input_file", type=str, help="File path input for identifying lines.")
    parser.add_argument("--start_section", type=int, default=0, help="Start section index for line identification.")
    parser.add_argument("--end_section", type=int, default=-1, help="End section index for line identification.")
    parser.add_argument("--output_folder", type=str, help="Optional folder to store character line outputs.")
    parser.add_argument("--missing_narrator_max_retries", type=int, default=5, help="Max retries for missing narrator detection.")

    # Audio generation
    parser.add_argument("--generate_audio_input_text", type=str, help="Direct text input for generating audio.")
    parser.add_argument("--generate_audio_input_file", type=str, help="File path input for generating audio.")
    parser.add_argument("--generate_audio_voice", type=str, help="Voice for generating audio.")

    # Multi-speaker audio
    parser.add_argument("--multi_speaker_audio_folder_path", type=str, help="Folder path for multi-speaker audio generation.")

    # Show help if no arguments are passed
    if len(sys.argv) == 1:
        print("\nNo arguments provided. Here's how to use this script:\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Fix model type to Model_Type enum (important!)
    try:
        args.llm_model_type = Model_Type[args.llm_model_type]
    except KeyError:
        print(f"Invalid model type '{args.llm_model_type}'. Valid options are: {[e.name for e in Model_Type]}")
        sys.exit(1)

    # Safety checks
    if args.generate_audio_input_text and args.generate_audio_input_file:
        parser.error("You cannot provide both --generate_audio_input_text and --generate_audio_input_file.")

    if args.identify_lines_input_text and args.identify_lines_input_file:
        parser.error("You cannot provide both --identify_lines_input_text and --identify_lines_input_file.")

    if (args.generate_audio_input_text or args.generate_audio_input_file) and not args.generate_audio_voice:
        parser.error("To generate audio, you must provide --generate_audio_voice along with text or file input.")

    if args.generate_audio_voice and not (args.generate_audio_input_text or args.generate_audio_input_file):
        parser.error("To generate audio, you must provide either --generate_audio_input_text or --generate_audio_input_file.")

    session = Session()

    # Set LLM if needed
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

    # Identify lines (if requested)
    if args.identify_lines_input_text or args.identify_lines_input_file:
        user_input = args.identify_lines_input_text if args.identify_lines_input_text else args.identify_lines_input_file
        is_file = args.identify_lines_input_file is not None

        output_folder = args.output_folder if args.output_folder else ""
        result = session.indentify_character_lines(
            user_input=user_input,
            is_file=is_file,
            output_folder=output_folder,
            start_section=args.start_section,
            end_section=args.end_section,
            missing_narrator_max_retries=args.missing_narrator_max_retries
        )
        print("Identified Character Lines:", result)

    # Generate audio (if requested)
    if args.generate_audio_input_text or args.generate_audio_input_file:
        user_input = args.generate_audio_input_text if args.generate_audio_input_text else args.generate_audio_input_file
        is_file = args.generate_audio_input_file is not None

        result = session.generate_audio(
            user_input=user_input,
            voice=args.generate_audio_voice,
            is_file=is_file,
            output_folder=None,
            output_file_type=".wav"
        )
        print("Generated Audio:", result)

    # Generate multi-speaker audio (if requested)
    if args.multi_speaker_audio_folder_path:
        result = session.generate_multi_speaker_audio(args.multi_speaker_audio_folder_path)
        print("Multi-Speaker Audio:", result)

if __name__ == "__main__":
    main()

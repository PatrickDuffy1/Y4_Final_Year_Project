import gradio as gr
from audio_generator import generate_audio_from_text, generate_audio_from_file
from os import listdir
from os.path import isfile, join

# Returns a list of all the voice file paths in the voices folder
def get_voices():
    
    directory_path = "./voices"
    file_paths = []
    
    # Loop through all of the files in the voices directory
    for file_path in listdir(directory_path):
    
        # Ignore anything that is a directory or text file
        if isfile(join(directory_path, file_path)) and file_path[-4:] != ".txt":
            
            # Add the file to the list of valid files
            file_paths.append(join(directory_path, file_path).replace("\\", "/"))
        
    return file_paths
    

# Generate the audio using the chosen text/file, and the chosen voice
def gradio_generate_audio(text, file, voice):
    
    # Use textbox as default. If there is no text in the textbox, use file, If there is neither, print message
    if text:
        audio = generate_audio_from_text(text, voice)
    elif file:
        audio = generate_audio_from_file(file.name, voice)
    else:
        return "Please provide either text or a file."
    
    return audio
    

demo = gr.Interface(
    fn=gradio_generate_audio,
    inputs=[
        "text", # Input box for text
        "file", # Input box for files
        # Dropdown menu for voices
        gr.Dropdown(
                choices=set(["./voices/voice_1.wav"] + get_voices()), # Get all of the available voices
                label="Voice", 
                value="./voices/voice_1.wav" # Default voice
            ),
        ],
    outputs=["audio"], # Output box for audio file
    allow_flagging="never",  # Disables the flagging functionality
)

# Run the interface
demo.launch()
    
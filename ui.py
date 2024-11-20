import gradio as gr
from audio_generator import test_function

# Generate the audio using the chosen text/file, and the chosen voice
def generate_audio(text, file, voice):
    
    test_function(text, file, voice)

    return audio
    

demo = gr.Interface(
    fn=generate_audio,
    inputs=[
        "text", # Input box for text
        "file", # Input box for files
        # Dropdown menu for voices
        gr.Dropdown(
                choices=["./voice_1.wav", "./voice_2.wav"],
                label="Voice", 
                value="./voice_1.wav" # Default voice
            ),
        ],
    outputs=["audio"], # Output box for audio file
)

# Run the interface
demo.launch()
    
import gradio as gr
from audio_generator import generate_audio

# Generate the audio using the chosen text/file, and the chosen voice
def gradio_generate_audio(text, file, voice):
    
    audio = generate_audio(text, file, voice)

    return audio
    

demo = gr.Interface(
    fn=gradio_generate_audio,
    inputs=[
        "text", # Input box for text
        "file", # Input box for files
        # Dropdown menu for voices
        gr.Dropdown(
                choices=["./voices/voice_1.wav", "./voices/voice_2.wav"],
                label="Voice", 
                value="./voices/voice_1.wav" # Default voice
            ),
        ],
    outputs=["audio"], # Output box for audio file
)

# Run the interface
demo.launch()
    
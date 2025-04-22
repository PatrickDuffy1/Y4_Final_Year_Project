from TTS.api import TTS
import torch

def load_tts_model(model_type):
    
    # Currently, only the 'coqui' model is supported
    if model_type == "coqui":
        return load_coqui_model()
        
    raise Exception("Invalid model type:", model_type)
    

# Load TTS model
def load_coqui_model():
    
    # Use cuda if available, otherwise use the cpu
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    print("Using device:", device)
    
    # Load TTS model
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    return tts
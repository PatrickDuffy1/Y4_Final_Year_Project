# Y4 Final Year Project - AI Audio Book Creator

## Description
The goal of the project is to generate audio books from files/book text where each character in the audio book has their own voice. 
Currently, there are a limited number of tools available to create audio books using AI Text To Speech, and little to none for creating an audio book with different voices for different characters. 
My aim in this project is to first use a Large Language Model (LLM) to identify characters in a book, identify their lines in the book, and choose a voice from a list of existing voices for the character.
Once that is done I then aim to use a Text To Speech (TTS) model to generate audio files of each character’s lines using the voice chosen for them. 
Finally, the audio files will be stitched together to create one audio file for the entire book. 

## Usage

## Cloning the Repository

Open Anaconda/Miniconda prompt and run the following command to clone the repository:

```bash
git clone https://github.com/PatrickDuffy1/Y4_Final_Year_Project
```

Navigate into the cloned repository:

```bash
cd Y4_Final_Year_Project
```

## Setting Up the Environment

1. Deactivate any existing conda environments:

   ```bash
   conda deactivate
   ```

2. Create a new environment with Python 3.9.0:

   ```bash
   conda create --name my_env_name python==3.9.0
   ```

3. Activate the new environment:

   ```bash
   conda activate my_env_name
   ```

## Installing Dependencies

1. Install CUDA toolkit:

   ```bash
   conda install -c conda-forge cudatoolkit
   ```

2. Install cuDNN:

   ```bash
   conda install -c conda-forge cudnn
   ```

3. Install PyTorch and related packages:

   ```bash
   conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
   ```

4. Install additional Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

Navigate to the `modules` directory:

```bash
cd modules
```

Run the main script:

```bash
python run.py
```

## Additional Information

- Ensure that you have the correct GPU drivers installed for CUDA support.
- Modify `my_env_name` to your preferred environment name if needed.

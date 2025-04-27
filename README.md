# AI Audiobook Generator

## Introduction

This project is an AI-driven system for generating both **single-speaker** and **multi-speaker** audiobooks entirely offline and locally. Unlike traditional audiobooks, where human narrators are hired (often at high cost), this system uses AI-based text-to-speech (TTS) technologies to automatically produce audiobook narrations without any human voice actors.

Users can choose between two audiobook generation modes:
- **Single-speaker:** A consistent synthetic narrator voice reads the entire book.
- **Multi-speaker:** Distinct synthetic voices are assigned to different characters, making the audiobook more immersive and expressive.

A key focus of this project is supporting full **local generation** — no internet connection is required after setup. This approach ensures user privacy, enhances affordability, and makes the tool more accessible for various needs, including for visually-impaired readers or users converting ebooks without official audiobook versions.

The multi-speaker generation feature is the core innovation of the system. By automatically identifying characters within a text and assigning each their own unique synthetic voice, the project addresses a major gap in audiobook availability: **multi-speaker productions are rare and expensive**, often reserved for premium or theatrical releases. This tool democratizes access to rich, character-driven audiobook experiences.

At the start of development, no comprehensive open-source solution for fully offline multi-speaker audiobook generation existed. While some commercial tools appeared during the project timeline, they were closed-source and provided no insight or assistance to the work here. As a result, the design and methodology of this system are based on original research and implementation.

In addition to the audiobook generation core, this project provides:
- A **Command Line Interface (CLI)** and a **User Interface (UI)** for ease of use.
- Support for **custom voice additions**, allowing users to expand the voice library.
- **Expressive tone adjustments**, aiming to bring characters and narration to life with emotion and context sensitivity.

Whether you're looking to convert your favorite ebooks into audiobooks, create accessible formats for users with reading difficulties, or simply explore the potential of modern AI TTS, this project offers a complete, open-source solution.

> **Important Note:**  
> This project **does not** include any pre-collected voice samples, **due to potential copyright restrictions**.  
> 
> To generate audiobooks, you must provide your own voice files and place them inside the `voices/` directory.  
> 
> See the **Choosing Voices** section below for recommendations on finding or creating high-quality voice samples.



## Screencast Link
https://youtu.be/h6gcs9kKOPk

## Usage

## Cloning the Repository

Assuming Anaconda/Miniconda is already installed.

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

## Additional Information

- Ensure that you have the correct GPU drivers installed for CUDA support.
- Modify `my_env_name` to your preferred environment name if needed.

## Running the Application

To start the project, assuming current directory is the root of the project, run:

```
python modules/run_ui.py
```

After a few seconds, the project window should open in your browser.  
If it doesn't, copy the URL displayed in the terminal (likely `http://127.0.0.1:7860`) and paste it into your browser's address bar.  
The UI is built with **Gradio**.

---

## Single-Speaker Audiobook Generator

Upon startup, you should land on the "Single Speaker Audiobook Generator" page. The "Single Speaker" tab at the top will be selected by default.

This page allows you to create an AI-narrated audiobook with a single narrator for the entire book. You can choose between:

- **Text input**: Paste your text directly.
- **File input**: Upload a file (`.txt` or `.epub`).

### Steps:

1. Enter your text or select a file.
2. Choose a voice from the dropdown menu (ensure you have voices in the `voices/` folder at the project root).
3. (If using a file) Optionally, name the output folder or select an existing folder to continue a previous generation.
4. Click **Generate Audio**.

> **Note:**  
> The first time you run the program, you'll be prompted in the terminal to accept the Coqui.ai user agreement (press `y` and `Enter`). This will initiate the download of the TTS model. Future runs will not require this step if the model is already downloaded.

### Performance:

- On an RTX 4090, generation achieves an average real-time factor of about **0.3** (i.e., a 3-minute audio clip takes slightly under 1 minute to generate).
- The TTS model consumes approximately **3GB of VRAM**.
- CPU generation is possible but significantly slower.

### Outputs:

- **If input was Text** → Single `.wav` file (timestamp as filename).
- **If input was a File** → Folder (timestamp or custom name) containing chapter-by-chapter `.wav` files (`0.wav`, `1.wav`, etc.).

Outputs are saved in the `single_speaker_outputs/` directory at the project root.

---

## Multi-speaker Audiobook Generator

The other three tabs at the top of the screen are for multi-speaker generation.

### Multi-speaker Generation Steps

** Load LLM → Identify lines → Assign voices → Generate multi-speaker audio.**

### 1. Loading a Model

Navigate to the **Load Model** tab. Here you can load a Language Model (LLM) in **GGUF format** using one of three methods:

- **Dropdown selection**: Choose a model located in the `models/` folder.
- **Absolute path**: Provide the full path to a model file.
- **HuggingFace**: Enter the model path (e.g., `google_gemma-3-27b-it-qat-Q4_K_M.gguf`) and the repository ID (e.g., `bartowski/google_gemma-3-27b-it-qat-GGUF`).

> The first time loading from HuggingFace, the model will be downloaded automatically.  
> Subsequent loads will use the cached model without downloading.

Additional options available on this page:

- **Context size** and **temperature**: Only modify if you understand the impact. (Default settings are optimized based on testing and detailed in the project dissertation.)
- **GPU layers to offload**: Depends on your GPU's VRAM. The more GPU layers offloaded to the GPU, the faster inference should be. The amount of layers that you can offload depends on the amount of VRAM your GPU has, and on the the number and size of the layers that the chosen LLM has.
- **Seed**: Use a fixed seed for reproducible outputs. A seed of `-1` means random.

Press the **Load Model** button to load the LLM.  
Load time depends on model size and storage type. For example, **Gemma 3 27B Q4_K_M** typically loads in under **10 seconds** from an internal SSD.



### 2. Character Line Identification

After the model is loaded, navigate to the **Line Identifier** tab.

You can input either:

- Text 
- A file (`.txt` or `.epub`)

#### If using an EPUB:

- You can specify the start and end sections.
  - **Start section**: Default is `0` (start from the beginning).
  - **End section**: Default is `-1` (continue to the end).
- Note that **section numbers** usually do **not match** book chapter numbers.  
  (Sections include front matter like the publisher's note, table of contents, etc.)

Example for "The Hobbit":
- Chapter 1 starts at section 9.
- To generate chapters 1 and 2, set:
  - Start section = `9`
  - End section = `11` (end section is exclusive)

Other options:

- **Output folder name**: Optional. (Works the same way as in single-speaker generation.)
- **Continue previous line identification**: Choose an existing folder from the dropdown.
- **Max Retries If No Narrator**: Default is `10`.
  - Some models occasionally miss narrator lines.
  - The program retries until successful or the max retries limit is hit.

> **Note:**  
> Some models, like Gemma 3, can occasionally miss narrator lines for a chunk and return no narrator at all.  
> When this happens, the program will retry that chunk until either the narrator lines appear, or the "Max Retries If No Narrator" limit is reached.
> 
> However, it is also possible that a chunk genuinely has no narrator lines — especially if the chunk size is small.  
> The size of the chunks and the style of the book can both influence whether narrator lines are present.  
> (Chunk size and its relationship to context size are discussed further in the dissertation.)
> 
> Because of this, setting a very high retry number is not always advisable.  
> The default value of **10 retries** is recommended unless you are certain adjustments are necessary.


Click **Identify Character Lines** to start the process. The output folder should open automatically upon completion.

#### Performance:

- Using **Gemma 3 27B Q4_K_M** with an **RTX 4090**:
  - "Harry Potter and the Philosopher's Stone" took around **3 hours**.
  - "The Hobbit" took slightly less than **4 hours**.

#### Outputs:

Located in `multi_speaker_outputs/`.  
The output folder will contain:

- `book_characters/` — character lists per chapter.
- `chapter_lines/` — dialogue lines and their assigned speakers per chapter.
- `merged_book_characters.json` — all characters merged across the book.

**Important:**  
- After line identification, **all characters** are set to `"unassigned"` voices.
- You must manually assign voice files (at minimum for the **Narrator**).
- Voice file paths must use **forward slashes** (`/`) not backslashes (`\`).

> Characters without assigned voices will default to the Narrator's voice.  
> (However, for a true multispeaker audiobook, it is recommended to assign voices individually, as if all voices default to the Narrator voice, it ends up being the same as the Single-Speaker generator)

---

### 3. Multi-Speaker Audio Generation

Navigate to the **Multi Speaker** tab.

Use the folder generated during Line Identification as the input.

- Choose the folder via dropdown or enter its absolute path.
- Ensure that the `merged_book_characters.json` file has the Narrator (at minimum) assigned a voice.

Start generation by clicking **Generate Multi-Speaker Audio**. The output folder should open automatically upon completion.

#### Performance:

- On an RTX 4090, generating the first chapter of "The Hobbit" took approximately **17 minutes**.

#### Outputs:

- A new `final_outputs/` folder will be created inside the same input directory.
- All output audio files (one per section) will be named `0.wav`, `1.wav`, etc.

---

## Running the Application (CLI Version)

In addition to the UI, the application can also be used via the command line (CLI).

To run the CLI version:

```
python modules/run_cli.py --help
```

Running with `--help` will display a list of available command-line arguments and usage instructions.

### Key Features:

- **Local or Cloud LLM Support**:  
  Specify either a local model path or use a cloud LLM (e.g., OpenAI, Gemini) via API key.
  
- **Line Identification**:  
  Identify speakers and narrators in text or EPUB files (see the **Line Identifier** section under the UI explanation for more about section numbering and retries).
  
- **Single-Speaker Audio Generation**:  
  Generate a `.wav` file (or chapter-by-chapter `.wav`s) from text or EPUBs using a selected voice (details same as UI section "Single Speaker Audiobook Generator").
  
- **Multi-Speaker Audio Generation**:  
  Generate multi-character audiobooks based on pre-identified character lines and assigned voices (details mirror the "Multi-Speaker Audio Generation" UI section).

> **Note:**  
> Voice file requirements, model loading behavior, and output folder structures are identical to the descriptions in the UI instructions above.  
> Refer to the UI sections for detailed behavior (e.g., retries if narrator lines are missing, character assignment rules).

---

## CLI Quick Reference

| Purpose | Example Command |
|:--------|:----------------|
| **Show help menu** | `python modules/run_cli.py --help` |
| **Generate single-speaker audio (text input)** | `python modules/run_cli.py --generate_audio_input_text "This is a sample text" --generate_audio_voice "voices/voice.wav"` |
| **Generate single-speaker audio (file input)** | `python modules/run_cli.py --generate_audio_input_file "path/to/book.epub" --generate_audio_voice "voices/voice.wav"` |
| **Identify character lines (local LLM)** | `python modules/run_cli.py --llm_model_path "models/model.gguf" --identify_lines_input_file "path/to/book.epub"` |
| **Identify character lines (cloud LLM)** | `python modules/run_cli.py --cloud_llm_model_name "gpt-4" --cloud_llm_api_key "your_api_key" --cloud_llm_model_type "OPEN_AI" --identify_lines_input_file "path/to/book.txt"` |
| **Generate multi-speaker audio** | `python modules/run_cli.py --multi_speaker_audio_folder_path "multi_speaker_outputs/folder_name"` |

---

## CLI Full Reference

| Argument | Description | Default | Required |
|:---------|:------------|:--------|:---------|
| --llm_model_path | Path to the local LLM model file. | None | Required if identifying lines locally |
| --llm_model_type | Type of the local model (Enum: depends on `Model_Type`. Options: LOCAL_FILE, HUGGING_FACE, OPEN_AI.). | "LOCAL_FILE" | No |
| --llm_repo_id | Repository ID of the model (if any). | None | No |
| --llm_context_length | Context length for the local model. | 2048 | No |
| --llm_gpu_layers | Number of GPU layers to offload for the local model. | 0 | No |
| --llm_temperature | Temperature setting for local model generation. | 0.7 | No |
| --llm_seed | Seed for reproducibility (use -1 for random). | -1 | No |
| --cloud_llm_model_name | Cloud LLM model name (e.g., "gpt-4"). | None | Required if identifying lines with a cloud LLM |
| --cloud_llm_api_key | API key for cloud LLM access. | None | Required if identifying lines with a cloud LLM |
| --cloud_llm_model_type | Cloud model type ("OPEN_AI" or "GEMINI"). | None | Required if identifying lines with a cloud LLM |
| --cloud_llm_max_tokens | Max tokens for cloud LLM responses. | 2048 | No |
| --identify_lines_input_text | Direct text input for line identification. | None | Required if identifying lines (either text or file must be given) |
| --identify_lines_input_file | File path input for line identification. | None | Required if identifying lines (either text or file must be given) |
| --start_section | Starting section index for EPUB line identification. | 0 | No |
| --end_section | Ending section index for EPUB line identification. | -1 | No |
| --output_folder | Optional folder name for character line outputs. | None | No |
| --missing_narrator_max_retries | Max retries if narrator lines are missing. | 5 | No |
| --generate_audio_input_text | Direct text input for audio generation. | None | Required if generating audio (either text or file must be given) |
| --generate_audio_input_file | File path input for audio generation. | None | Required if generating audio (either text or file must be given) |
| --generate_audio_voice | Voice file for generating audio. | None | Required if generating audio |
| --multi_speaker_audio_folder_path | Folder path for multi-speaker audio generation. | None | Required if generating multi-speaker audio |

> **Tip:**  
> If your path or filenames have spaces, enclose them in quotes (`" "`).

---

## Minimal CLI Examples

This section provides the **shortest, simplest** examples of how to use the CLI version.

(For full behavior details — like retries, narrator rules, output formats — refer to the equivalent UI sections.)

---

### 1. Generate Single-Speaker Audio (From Text)

```
python modules/run_cli.py --generate_audio_input_text "This is a simple book text" --generate_audio_voice "voices/voice.wav"
```

### 2. Generate Single-Speaker Audio (From File)

```
python modules/run_cli.py --generate_audio_input_file "path/to/your_book.epub" --generate_audio_voice "voices/voice.wav"
```

---

### 3. Identify Character Lines (With Local LLM)

```
python modules/run_cli.py --llm_model_path "models/your_model.gguf" --identify_lines_input_file "path/to/your_book.epub"
```

---

### 4. Identify Character Lines (With Cloud LLM)

```
python modules/run_cli.py --cloud_llm_model_name "gpt-4" --cloud_llm_api_key "your_api_key" --cloud_llm_model_type "OPEN_AI" --identify_lines_input_file "path/to/your_book.txt"
```

---

### 5. Generate Multi-Speaker Audio

```
python modules/run_cli.py --multi_speaker_audio_folder_path "multi_speaker_outputs/your_output_folder"
```

---

## Notes

- If you don't pass any arguments, the script will show the `--help` menu automatically.
- Always enclose file paths with spaces inside `"quotes"`.
- Voice files should be placed inside the `voices/` directory.
- Model files (for local LLMs) should be placed inside the `models/` directory.
- For cloud LLM usage, ensure your API keys are correct and have permission to access the specified model.

> **Important:**  
> Narrator assignment rules, fallback defaults, and output structures work exactly the same as described in the UI sections.


---

## Final Result

The generated `.wav` files (from either single or multi-speaker generation) can be:

- Played on your computer
- Transferred to an audiobook player

> **Tip:**  
> WAV files are uncompressed and large. It is advisable to convert them to a compressed format like `.mp3` to reduce storage space.


---

## Choosing an LLM

There is a wide variety of LLMs that can be used.  
The design of this program means **newer models** can be used without needing to modify the code.  
(You may need to update `llama-cpp-python`. If updates aren't available, manually rebuilding `llama.cpp` and copying the built files to `llama-cpp-python` should ensure newer model support, as, at the time of this project, `llama.cpp` is updated very regularly.)

Due to the fast pace of LLM development, current problems with the program may be solved in the (possibly near) future simply by using newer models. As of writing this, there are already multiple new LLMs which show potential for improving the program.

### Models Used During Testing:

- **Gemma 3 27B Q4_K_M**
- **Llama 3.3 70B Q4_K_M**

#### Notes:

- **Llama 3.3 70B** is older and larger.
- **No consumer GPU** currently fits all layers of **Llama 3.3 70B** at Q4_K_M quantization.
- **Gemma 3 27B** can offload entirely to a 24GB VRAM GPU.

Memory requirements:

- **Gemma 3 27B Q4_K_M** has a file size of ~16GB, meaning it needs ~16GB RAM at minimum.
- **Llama 3.3 70B Q4_K_M** has a file size of ~41GB, meaning it needs ~41GB RAM at minimum.

As LLMs evolve, both **quality** and **efficiency** are expected to improve.  
Smaller, better models will likely become available within a year.

---

## TTS (Text-To-Speech)

While the code currently uses **XTTSv2**, it can be adapted to newer models with minimal modifications.

> **Important:**  
> XTTSv2 and the company behind it have been deprecated.  
> Many newer TTS models show promise.
> Updating the TTS module and using a newer model is one possible way to improve quality in the future.

---

## Choosing Voices

No voices are included in this project due to potential copyright concerns.  
While voices can be sourced from public datasets (like on Kaggle), their quality may not always deliver ideal results.

> **Tip:**  
> High-quality sample audio significantly improves the quality of generated audiobooks.

**Important notes when choosing voice samples:**

- Voices with **high variability** (emotional range, tone shifts) generate the best outputs.
- **Monotone** original samples typically produce **monotone** generated audio.
- Audiobooks are often excellent sources for voices, as they tend to have:
  - High-quality audio
  - Natural voice variance
  - Clear enunciation
- However, the quality can depend on the individual narrator.

**Recommended voice sample length:**

- Between **20 seconds and 5 minutes**.
- Longer samples usually produce better results, but there are diminishing returns.
- Extremely long samples can also increase generation times.

**Usage:**

- Place your voice files inside the `voices/` directory at the project root.

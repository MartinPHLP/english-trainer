# english-trainer
english-trainer is a virtual speaking practice tool that uses LLM, LangChain, and Whisper.cpp to provide an interactive language learning experience. Users can engage in conversations with AI, receive corrections, and improve their English speaking skills.

## Features
- Automatic or manual context selection for dialogues
- Real-time speech recognition using Whisper.cpp
- AI-powered conversation partner using OpenAI's powerful language models
- Instant feedback and corrections on user's speech
- Simple keyboard controls for interaction
- Fast and cost-effective local speech-to-text conversion

## How It Works
english-trainer leverages local speech-to-text conversion using Whisper.cpp to make the program much faster and more cost-effective. This local processing handles the speech recognition part of the application.

For generating human-like responses and powering the conversational AI, the program utilizes OpenAI's powerful language models via their API. This combination allows for a responsive, intelligent, and natural-feeling conversation partner for language practice.

## Prerequisites

- Python 3.7+
- Git
- C++ compiler (for Whisper.cpp)
- OpenAI API key

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/MartinPHLP/english-trainer.git
   cd english-trainer
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Clone and set up Whisper.cpp:

   ```
   git clone https://github.com/ggerganov/whisper.cpp.git
   cd whisper.cpp
   bash ./models/download-ggml-model.sh base.en
   make
   cd ..
   ```

5. Set up environment variables:
   ```
   cp .example.env .env
   ```
   Edit the `.env` file and fill in your API keys. You can also modify the `WHISPER_OUTPUT_PATH` if needed.

## Usage

1. Run the application (command to be specified by the project owner)

2. Select the conversation context (automatic or manual)

3. Begin the dialogue:

   - Press SPACE once to start speaking
   - Press SPACE again to finish your current response
   - The AI will process your speech and respond accordingly

4. To exit the application, say "Exit program" after pressing space.

## Whisper.cpp Integration

The application uses Whisper.cpp for speech recognition. It is integrated as follows:

```python
command = f"{WHISPER_MAIN_PATH} -m {WHISPER_MODEL_PATH} -f {self.WAV_USER_PATH} -oj -of {os.getenv('WHISPER_OUTPUT_PATH')}"

# ... (execution of the command)

with open(os.getenv("WHISPER_OUTPUT_PATH") + ".json", "r") as file:
    output_json = json.load(file)
    user_text = output_json["transcription"][0]["text"]
```

Note that any compatibility issues are likely to be related to this integration.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

None

## Acknowledgements

- [LangChain](https://github.com/hwchase17/langchain)
- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)

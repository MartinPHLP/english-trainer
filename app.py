import re
import warnings

from dotenv import load_dotenv
from srcs.uihandler import UIHandler
from srcs.llmhandler import LLMHandler
from srcs.audiohandler import AudioHandler
from srcs.contextgenerator import ContextGenerator
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough

load_dotenv()
warnings.filterwarnings("ignore", category=DeprecationWarning)

def exit_program(inputs):
    if  "exit program" in inputs["user_input"].lower():
        print("Goodbye!")
        exit(0)

    return inputs

def main():
    ui = UIHandler()
    llm_handler = LLMHandler()
    audio_handler = AudioHandler()
    context_generator = ContextGenerator()

    ui.print_header()

    context, user_role, ai_role = context_generator.create_context()
    voice = llm_handler.determine_voice(ai_role)

    chain = (
        RunnablePassthrough.assign(
            user_input=lambda _: audio_handler.listen_and_transcribe(),
            voice=lambda _: voice
        )
        | RunnableLambda(lambda x: exit_program(x))
        | RunnableLambda(lambda x: {**x, **{"_": ui.display_input(x)}})
        | llm_handler.get_ai_response
        | llm_handler.check_and_correct
        | audio_handler.synthesize_speech
    )

    messages = llm_handler.initialize_messages(context, user_role, ai_role)

    while True:
        ui.prompt_user()

        result = chain.invoke({"messages": messages})
        messages = result["messages"]
        ui.display_response(result)

        if result["correction"]:
            audio_handler.play_audio(audio_handler.ERROR_SOUD_PATH)

        audio_handler.play_audio(audio_handler.SPEECH_OUTPUT_PATH)

        if len(messages) == 5:
            messages.pop(1)
            messages.pop(1)

if __name__ == "__main__":
    main()

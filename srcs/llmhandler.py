import random

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from srcs.output_models import GenderClassifier, EnglishBinaryClassifier, EnglishCorrector


class LLMHandler:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
        self.llm_corrector = ChatOpenAI(model="gpt-4o", temperature=0.3)
        self.setup_chains()

    def setup_chains(self):
        classifier_messages = [
            ("system", "You are a binary classifier. You take the last AI's response and the last user's response. If you find an error (grammar, English verbs, vocabulary) in the user's response, return_value must be 1, otherwise 0. You must ignore spaces, punctuation or capitalization errors."),
            ("human", "Here are the last messages: AI: {ai_response}. USER SENTENCE TO CLASSIFY: \"{user_input}\".")
        ]
        classifier_prompt = ChatPromptTemplate.from_messages(classifier_messages)
        classifier_output = self.llm_corrector.with_structured_output(EnglishBinaryClassifier).with_retry(stop_after_attempt=2)
        self.classifier = classifier_prompt | classifier_output

        corrector_messages = [
            ("system", "You are an English language corrector."),
            ("human", "Here's the context: AI sentence: \"{ai_response}\". USER sentence: \"{user_input}\". Correct the USER's sentence.")
        ]

        corrector_prompt = ChatPromptTemplate.from_messages(corrector_messages)
        self.corrector = corrector_prompt | self.llm_corrector.with_structured_output(EnglishCorrector).with_retry(stop_after_attempt=2)

    def get_ai_response(self, inputs):
        messages = inputs["messages"]
        user_input = inputs["user_input"]
        messages.append(HumanMessage(content=user_input))
        ai_response = self.llm.invoke(messages).content
        messages.append(AIMessage(content=ai_response))
        return {
            "messages": messages,
            "ai_response": ai_response,
            "user_input": user_input,
            "voice": inputs["voice"]
        }

    def check_and_correct(self, inputs):
        messages = inputs["messages"]
        ai_response =inputs["ai_response"]
        user_input =inputs["user_input"]
        correction = None

        classifier_result = self.classifier.invoke(
            {
                "ai_response": ai_response,
                "user_input": user_input
            }
        ).return_value

        if classifier_result == 1:
            corrector_result = self.corrector.invoke(
                {
                    "ai_response": ai_response,
                    "user_input": user_input
                }
            )
            correction = (
                f"Oops, you made a mistake !\n\nEXPLANATION : "
                f"{corrector_result.why}\nCORRECTED SENTENCE : \""
                f"{corrector_result.corrected_sentence}\"\n"
            )

        return {
            "messages": messages,
            "ai_response": ai_response,
            "user_input": user_input,
            "correction": correction,
            "voice": inputs["voice"]
        }

    def determine_voice(self, ai_role):
        gender = self.llm.with_structured_output(GenderClassifier).with_retry(stop_after_attempt=2).invoke([
            SystemMessage(content="You are a gender classifier. Determine the gender of the given character. Return 0 if the character is a female, 1 otherwise"),
            HumanMessage(content=f"Is {ai_role} a female character?")
        ]).gender

        if gender == 0:
            voice = random.choice(["nova", "shimmer"])

        else:
            voice = random.choice(["echo", "alloy", "fable", "onyx"])

        return voice

    def initialize_messages(self, context, user_role, ai_role):
        return [
            SystemMessage(content=f"You are a roleplay engine. In this story, you are '{ai_role}', and the context is:"
                f" {context}. Respond only as '{ai_role}' with short answers, adhering to their personality, speech,"
                f" and knowledge. The USER is '{user_role}', and you should interact with them"
                f" using only '{ai_role}''s text and style. Remain in character throughout.")
        ]

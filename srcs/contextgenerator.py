from langchain_openai import ChatOpenAI
from srcs.output_models import DialogContext
from langchain_core.messages import HumanMessage


class ContextGenerator:
    def __init__(self):
        self.llm_context = ChatOpenAI(model="gpt-4o-mini", temperature=1.9)

    def create_context(self):
        auto_context = input("Do you want an automatic context? (y/n): ").strip().lower()

        if auto_context == "y":
            while True:
                response = self.llm_context.with_structured_output(DialogContext).invoke([HumanMessage(content="Create a unique dialog context between two characters.")])
                self.print_context(response)

                if input("Are you satisfied with the context? (y/n): ").strip().lower() == "y":
                    return response.context, response.user, response.ai
        else:
            context = input("Write the dialog's context: ")
            user = input("USER: ")
            ai = input("AI: ")
            self.print_context(DialogContext(context=context, user=user, ai=ai))
            return context, user, ai

    def print_context(self, context):
        print("\n")
        print("╭────────────────────────────────────────╮")
        print("│ Context                                │")
        print("╰────────────────────────────────────────╯")
        print(f" {context.context} ")
        print("╭────────────────────────────────────────╮")
        print("│ User                                   │")
        print("╰────────────────────────────────────────╯")
        print(f" {context.user} ")
        print("╭────────────────────────────────────────╮")
        print("│ AI                                     │")
        print("╰────────────────────────────────────────╯")
        print(f" {context.ai} \n\n")

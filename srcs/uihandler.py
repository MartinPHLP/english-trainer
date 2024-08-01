from art import text2art


class UIHandler:
    def print_header(self):
        print("*************************************************************************************")
        print(text2art("english-trainer"))
        print("*************************************************************************************\n")

    def prompt_user(self):
        print("Press space to talk...")

    def display_input(self, result):
        print("\n╭───────────────────────────────────────────────╮")
        print("│                  User Input                   │")
        print("╰───────────────────────────────────────────────╯")
        print(f"{result['user_input']}\n")

    def display_response(self, result):
        if result['correction']:
            print("\n╭───────────────────────────────────────────────╮")
            print("│                  Correction                   │")
            print("╰───────────────────────────────────────────────╯")
            print(result['correction'])

        print("\n╭───────────────────────────────────────────────╮")
        print("│                   AI Response                 │")
        print("╰───────────────────────────────────────────────╯")
        print(f"{result['ai_response']}\n\n")

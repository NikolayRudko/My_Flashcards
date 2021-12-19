import io
import random
import argparse


class Flashcards:
    def __init__(self, output, import_file, export_file):
        self.cards = {}
        self.output = output
        self.import_file = import_file
        self.export_file = export_file

    def menu(self):
        if self.import_file is not None:
            self.import_cards(self.import_file)
        while True:
            self.my_print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
            command = input()
            self.my_print(command, console=False)
            if command == "add":
                self.add_card()
            elif command == "remove":
                self.remove_card()
            elif command == "import":
                self.import_cards()
            elif command == "export":
                self.export_cards()
            elif command == "ask":
                self.ask_cards()
            elif command == "exit":
                print('Bye bye!')
                if self.export_file is not None:
                    self.export_cards(self.export_file)
                break
            elif command == 'log':
                self.custom_log()
            elif command == "hardest card":
                self.hardest_cards()
            elif command == "reset stats":
                self.reset_stats()
            self.my_print('')

    def custom_log(self):
        self.my_print("File name:")
        file_name = input()
        self.my_print(file_name, console=False)
        with open(file_name, "w") as f:
            f.write(self.output.getvalue())
        print('The log has been saved.')

    def reset_stats(self):
        for i in self.cards.values():
            i[1] = 0
        self.my_print("Card statistics have been reset.")

    def hardest_cards(self):
        if len(self.cards) == 0:
            hardest_card = 0
        else:
            hardest_card = max([mistakes for definition, mistakes in self.cards.values()])
        if hardest_card == 0:
            self.my_print("There are no cards with errors.")
        else:
            hardest_card_dict = dict(filter(lambda elem: elem[1][1] == hardest_card, self.cards.items()))
            data = list(hardest_card_dict.values())
            if len(hardest_card_dict) == 1:
                name_hardest_card = next(iter(hardest_card_dict.keys()))
                self.my_print(f'The hardest card is "{name_hardest_card}". You have {hardest_card} errors answering it')
            else:
                str_terms = [f'"{term}"' for term, mistakes in data]
                hardest_card_str = ', '.join(str_terms)
                self.my_print(f"The hardest cards are {hardest_card_str}.")

    def add_card(self):
        self.my_print('The card:')
        term = input()
        self.my_print(term, console=False)
        while True:
            if term in self.cards.keys():
                self.my_print(f'The card "{term}" already exists. Try again:')
                term = input()
                self.my_print(term, console=False)
                continue
            break
        self.my_print('The definition of the card:')
        definition = input()
        self.my_print(definition, console=False)
        while True:
            definitions = [data[0] for data in self.cards.values()]
            if definition in definitions:
                self.my_print(f'The definition "{definition}" already exists. Try again:')
                definition = input()
                self.my_print(definition, console=False)
                continue
            break
        self.cards[term] = [definition, 0]
        self.my_print(f'The pair ("{term}":"{definition}") has been added')

    def remove_card(self):
        self.my_print('Which card?')
        term = input()
        self.my_print(term, console=False)
        try:
            self.cards.pop(term)
        except KeyError:
            self.my_print(f"Can't remove \"{term}\": there is no such card.")
        else:
            self.my_print('The card has been removed.')

    def import_cards(self, file_name=None):
        if file_name is None:
            self.my_print("File name:")
            file_name = input()
        self.my_print(file_name, console=False)
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    term, definition, mistakes = line.split()
                    self.cards[term] = [definition, int(mistakes)]
                if len(lines) > 0:
                    self.my_print(f"{len(lines)} cards have been loaded.")
        except FileNotFoundError:
            self.my_print('File not found.')

    def export_cards(self, file_name=None):
        if file_name is None:
            self.my_print("File name:")
            file_name = input()
        self.my_print(file_name, console=False)
        with open(file_name, 'w', encoding="utf-8") as file:
            for term, data in self.cards.items():
                file.write('{0} {1} {2}\n'.format(term, data[0], data[1]))
            self.my_print(f"{len(self.cards)} cards have been saved")

    def ask_cards(self):
        self.my_print("How many times to ask?")
        count = int(input())
        self.my_print(str(count), console=False)
        for _ in range(count):
            term = random.choice(list(self.cards.keys()))
            definition = self.cards[term][0]
            definitions = [data[0] for data in self.cards.values()]
            self.my_print(f'Print the definition of "{term}":')
            answer = input()
            self.my_print(answer, console=False)
            if answer == definition:
                self.my_print('Correct!')
            else:
                if answer in definitions:
                    index = definitions.index(answer)
                    list_terms = list(self.cards)
                    self.my_print(f'Wrong. The right answer is "{definition}", '
                                  f'but your definition is correct for "{list_terms[index]} card."')
                else:
                    self.my_print(f'Wrong. The right answer is "{definition}".')
                self.cards[term][1] += 1

    def my_print(self, message: str, console=True) -> None:
        if console:
            print(message)
        print(message, file=self.output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--import_from")
    parser.add_argument("--export_to")
    args = parser.parse_args()
    import_file = args.import_from
    export_file = args.export_to
    output = io.StringIO()
    my_cards = Flashcards(output, import_file, export_file)
    my_cards.menu()
    output.close()


if __name__ == "__main__":
    main()

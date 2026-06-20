# board.py — plik z klasą Board
from board_logic import BoardLogic

class Board:
    def __init__(self):
        # Lista talli kart
        self.deck_symbols = [
            "A♥", "2♥", "3♥", "4♥", "5♥", "6♥", "7♥", "8♥", "9♥", "10♥", "J♥", "Q♥", "K♥",
            "A♦", "2♦", "3♦", "4♦", "5♦", "6♦", "7♦", "8♦", "9♦", "10♦", "J♦", "Q♦", "K♦",
            "A♠", "2♠", "3♠", "4♠", "5♠", "6♠", "7♠", "8♠", "9♠", "10♠", "J♠", "Q♠", "K♠",
            "A♣", "2♣", "3♣", "4♣", "5♣", "6♣", "7♣", "8♣", "9♣", "10♣", "J♣", "Q♣", "K♣"
        ]

        # Słownik do porównywania wartości skrót-symbol
        self.suits = {
            "h": "♥",  # hearts
            "d": "♦",  # diamonds
            "s": "♠",  # spades
            "c": "♣"  # clubs
        }

        # Utworzenie stosów gry — odpowiednio stos rezerwowy, 7 stosów głównych, 4 stosy końcowe
        self.reserve_stack = []

        self.main_stack1 = []
        self.main_stack2 = []
        self.main_stack3 = []
        self.main_stack4 = []
        self.main_stack5 = []
        self.main_stack6 = []
        self.main_stack7 = []

        self.end_stack1 = []
        self.end_stack2 = []
        self.end_stack3 = []
        self.end_stack4 = []

        # Utworzenie list zawierających stosy główne i końcowe
        self.main_stacks = [self.main_stack1, self.main_stack2, self.main_stack3, self.main_stack4, self.main_stack5, self.main_stack6, self.main_stack7]
        self.end_stacks = [self.end_stack1, self.end_stack2, self.end_stack3, self.end_stack4]

        # Słownik do porównywania wartości kart
        self.card_values = {
            "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
            "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13
        }
        # Słownik ze skrótami do wszystkich stosów
        self.short_names = {
            "M1": self.main_stack1, "M2": self.main_stack2, "M3": self.main_stack3, "M4": self.main_stack4, "M5": self.main_stack5,
            "M6": self.main_stack6, "M7": self.main_stack7,
            "E1": self.end_stack1, "E2": self.end_stack2, "E3": self.end_stack3, "E4": self.end_stack4,
            "R": self.reserve_stack
        }

        # Indeks wyświetlanej karty w stosie rezerwowym
        self.reserve_index = 0

        self.logic = BoardLogic(self)


    def print_board(self, index):
        # Wyświetlanie stosów końcowych
        self.print_headers("Stosy końcowe")
        symbols = {"♥": self.end_stack1, "♦": self.end_stack2, "♠": self.end_stack3, "♣": self.end_stack4}
        for k, v in symbols.items():
            if not v:
                print("\t[" + k + "]\t", end="")
            else:
                print("\t" + str(v[-1]) + "\t", end="")
        print("\n")

        # Wyświetlanie stosu rezerwowego
        self.print_headers("Stos rezerwowy")
        for cart in self.reserve_stack:
            if self.reserve_stack.index(cart) != index:
                print("*", end="  ")
            else:
                print(cart, end="  ")
        print("\n\n")

        # Wyświetlanie stosów głównych
        self.print_headers("Stosy główne")
        for i in range(1, 8):
            print(("Stos " + str(i) + ":").ljust(11, " "), end="")
        print("")

        # Ustalenie wysokości maksymalnej wysokości
        max_height = max(len(self.main_stack1), len(self.main_stack2), len(self.main_stack3), len(self.main_stack4), len(self.main_stack5),
                         len(self.main_stack6), len(self.main_stack7))
        for i in range(max_height):
            for stack in self.main_stacks:
                if len(stack) > i:
                    # Jeśli
                    if i < len(stack) - 1:
                        # Jeśli nie jest to ostatnia karta w stosie
                        if stack[i].view:
                            # Jeśli karta ma atrybut view równy True, karta jest wyświetlana
                            print((str(stack[i])).ljust(11, " "), end="")
                        else:
                            print("*".ljust(11, " "), end="")
                    else:
                        print((str(stack[i])).ljust(11, " "), end="")
                        stack[i].view = True
                else:
                    print("   ".ljust(11, " "), end="")
            print("")


    def print_shortcuts(self):  # Funkcja wyświetlająca skróty stosowane w komendach
        self.print_headers("Skróty")
        shortcuts = {"M1": "Stos 1", "M2": "Stos 2", "M3": "Stos 3", "M4": "Stos 4", "M5": "Stos 5", "M6": "Stos 6",
                     "M7": "Stos 7",
                     "E1": "Stos końcowy 1", "E2": "Stos końcowy 2", "E3": "Stos końcowy 3", "E4": "Stos końcowy 4", }
        colors_shortcuts = {"Kier (♥)  -Kolor czerwony ": "h", "Karo (♦)  -Kolor czerwony": "d",
                            "Pik (♠)   -Kolor czarny ": "s", "Trefl (♣) -Kolor czarny": "c"}
        for k, v in shortcuts.items():
            print(k.ljust(5) + v)
        print("")
        for k, v in colors_shortcuts.items():
            print(v.ljust(5) + k)

    def print_help(self):  # Funkcja wyświetlająca pomoc
        self.print_headers("Pomoc")
        print("""
Gra pasjans - Wystarczy wpisać jedną z komend wyświetlonych na ekranie by grać!

Przenoś karty między stosami, tak aby na Stosach Końcowych (R1, R2,
R3 i R4) znalazły się karty ułożone w jednym kolorze w kolejności malejącej,
tzn. od Asa (A), przez numery 2-10, skończywszy na symbolach: Walet (J),
Królowa (Q) i Król (K).
W trakcie rozgrywki możesz wyświetlać do woli kolejne karty w stosie rezerwowym,
wystarczy użyć komendy flip lub f.
By wyjść z gry należy wprowadzić komendę exit lub e, jeśli chcemy rozpocząć grę
od nowa wystarczy komenda restart lub r. 
Wpisanie komendy akceptujemy klawiszem ENTER. W komendach nie musi być
uwzględniona wielkość liter. 
Miłej gry!""")
        input("\nNaciśnij klawisz ENTER by kontynuować")


    def print_commands(self):  # Funkcja wyświetlająca komendy
        self.print_headers("Komendy")
        commands = {"help": "Wyświetlenie pomocy",
                    "move X_X to YY": "Przeniesienie karty XX na stos YY",
                    "exit": "Wyjście i koniec gry",
                    "flip": "Pokazanie kolejnej karty w stosie rezerwowym",
                    "restart": "Zakończenie gry i rozpoczęcie nowej"}
        for k, v in commands.items():
            print(k.ljust(20, "_") + v)
        print("")

    def initialize_game(self):
        self.logic.initialize_game()

    def check_win(self):
        self.logic.check_win()

    def prepare_to_move(self, command: str):
        self.logic.prepare_to_move(command)

    def update_all_places(self):
        self.logic.update_all_places()

    @staticmethod
    def print_headers(text):  # Funkcja wyświetlająca nagłówki
        print(text.center(80, "-"))

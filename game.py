# coding=utf-8
# game.py — plik główny gry

import board, time, sys, random
from datetime import datetime
from thefuzz import process


board = board.Board()  # Utworzenie instancji klasy Board


def suggest_command(user_input, commands):
    best_match, score = process.extractOne(user_input, commands)
    if score >= 70:  # próg dopasowania
        return best_match
    return None

def main():  # Główna funkcja programu
    print("Pasjans".center(80, "="))  # Wyświetlenie nagłówka gry w konsoli
    while True:
        # Zmienna do obliczenia czasu gry
        start_time = datetime.now()

        # Czyszczenie stosu rezerwowego i wszystkich stosów gry
        board.reserve_stack.clear()
        for stack in board.main_stacks:
            stack.clear()
        for stack in board.end_stacks:
            stack.clear()

        reserve_index = 0  # Indeks wybranej karty w stosie rezerwowym (domyślnie pierwsza)

        # Inicjalizacja gry, wyświetlenie dostępnych komend i skrótów
        board.initialize_game()
        board.print_commands()
        board.print_shortcuts()
        time.sleep(2)  # Krótkie opóźnienie dla efektu

        while True:
            # Sprawdzenie warunku wygranej
            if board.check_win():
                end_time = datetime.now()
                delta = end_time - start_time
                print("Czas gry: " + str(delta).split('.')[0])  # Wyświetlenie czasu gry
                input("Naciśnij klawisz ENTER by rozpocząć nową grę\n")

            board.print_board(reserve_index)  # Wyświetlenie aktualnego stanu planszy

            # Aktualizacja atrybutu place dla każdej z kart

            board.update_all_places()
            # Pobranie komendy od użytkownika
            input_command = input("Wpisz komendę: ")
            input_command = input_command.upper().strip()

            if input_command == "":
                # Obsługa pustego wejścia
                print("Nie wpisano komendy")
                time.sleep(1)

            elif input_command == "HELP" or input_command[0] == "H":
                # Wyświetlenie pomocy, gdy wpisano HELP lub coś zaczynającego się na "H"
                board.print_help()

            elif input_command == "EXIT" or input_command[0] == "E":
                # Wyjście z gry po wyświetleniu podsumowania czasu
                end_time = datetime.now()
                delta = end_time - start_time
                print("Czas gry: " + str(delta).split('.')[0])
                print("Koniec gry".center(80, "="))
                time.sleep(5)
                sys.exit()

            elif input_command == "FLIP" or input_command[0] == "F":
                # Obsługa przewracania karty ze stosu rezerwowego
                # Jeśli nie jesteśmy na końcu stosu, idziemy dalej
                # W przeciwnym razie tasujemy stos i wracamy na początek
                if reserve_index < len(board.reserve_stack) - 1:
                    reserve_index += 1
                else:
                    random.shuffle(board.reserve_stack)
                    reserve_index = 0
                board.reserve_stack[reserve_index].view = True  # Ustawienie widoczności karty

            elif "MOVE " in input_command and " TO " in input_command:
                # Próba wykonania ruchu karty
                board.prepare_to_move(input_command)

            elif input_command == "RESTART" or input_command[0] == "R":
                # Restart gry — wyświetlenie informacji i przerwanie wewnętrznej pętli
                end_time = datetime.now()
                delta = end_time - start_time
                print("Czas gry: " + str(delta).split('.')[0])
                print("Ładowanie...")
                time.sleep(1)
                print("Nowa gra".center(80, "="))
                break

            else:

                main_commands = ["HELP", "EXIT", "FLIP", "RESTART", "MOVE"]
                main_word = input_command.split()[0] if input_command else ""

                suggestion = suggest_command(main_word, main_commands)
                if suggestion:
                    print(f"Nie znaleziono komendy: {input_command}")
                    print(f"Czy chodziło Ci o: {suggestion}?")
                else:
                    print("Brak komendy: " + input_command + " w liście istniejących komend")
                time.sleep(1)

            # Odświeżenie komend i skrótów oraz aktualizacja widoku
            board.print_commands()
            board.print_shortcuts()


# Wywołanie głównej funkcji programu, tylko jeśli plik uruchamiany bezpośrednio
if __name__ == "__main__":
    main()

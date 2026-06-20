# board_logic.py
import time
import random
from cart import Cart
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board

class BoardLogic:
    def __init__(self, board: 'Board'):
        # Referencja do instancji Board, pozwala na dostęp do wszystkich jej atrybutów
        self.board = board

    def initialize_game(self):
        # Utworzenie talii kart składającej się z obiektów klasy Cart,
        # symbol z listy symboli, place tymczasowo ustawione na None
        deck = [Cart(symbol, None) for symbol in self.board.deck_symbols]

        # Tasowanie kart w talii
        random.shuffle(deck)

        # Pomocnicze zmienne do rozdawania kart do stosów
        index = 0
        index2 = 1

        # Rozdawanie kart do głównych stosów, zgodnie z zasadami pasjansa
        for stack in self.board.main_stacks:
            while len(stack) < index2:
                stack.append(deck[index])
                index += 1
            index2 += 1

        # Pozostałe karty trafiają do stosu rezerwowego (reserve_stack)
        while index < len(deck):
            self.board.reserve_stack.append(deck[index])
            index += 1

        # Przydzielanie atrybutu 'place' każdej karcie, wskazującego na stos, w którym się znajduje
        for cart in self.board.reserve_stack:
            cart.place = self.board.reserve_stack

        for cart in deck:
            for stack in self.board.main_stacks:
                if cart in stack:
                    cart.place = stack
                    break

    def check_win(self):
        # Sprawdza, czy gracz wygrał — czyli czy we wszystkich stosach końcowych jest 13 kart
        if all(len(stack) == 13 for stack in self.board.end_stacks):
            print(("\n" + "$" * 80) * 10)
            print("WYGRAŁEŚ!".center(80, "$"))
            print(("$" * 80 + "\n") * 10)
            return True
        return False

    def normalize_card_input(self, user_input):
        # Normalizacja wejścia użytkownika dotyczącego karty
        # Usuwa podkreślenia, zmienia na małe litery, sprawdza poprawność symbolu
        user_input = user_input.replace("_", "").lower()

        if len(user_input) < 2:
            return None

        value_part = user_input[:-1].upper()  # Część wartości (np. '10', 'K', 'Q')
        suit_part = user_input[-1]             # Część koloru (np. 'h', 's')

        # Sprawdzenie, czy kolor należy do dozwolonych symboli w talii
        if suit_part not in self.board.suits:
            return None

        # Zwrócenie karty w standardowym formacie (np. '10H', 'QS')
        return value_part + self.board.suits[suit_part]

    def prepare_to_move(self, input_command):
        # Funkcja przygotowująca dane do ruchu karty
        # Oczekuje formatu: MOVE <karta> TO <stos>
        cart_name, new_place = input_command.replace("MOVE ", "").split(" TO ")
        new_place = new_place.upper()
        new_place = self.board.short_names.get(new_place)  # Pobranie referencji do stosu po skrócie


        if new_place is None:
            print("Brak podanej nazwy w stosach")
            return

        # Normalizacja nazwy karty podanej przez użytkownika
        normalized_name = self.normalize_card_input(cart_name)
        if normalized_name:
            cart_name = normalized_name
        cart_name = cart_name.strip()

        # Szukanie karty w stosach głównych i rezerwowym
        found_cart = None
        for stack in self.board.main_stacks + [self.board.reserve_stack]:
            for card in stack:
                if card.cart_symbol.upper() == cart_name.upper():
                    found_cart = card
                    break
            if found_cart:
                break

        if not found_cart:
            print("Nie znaleziono karty:", cart_name)
            return

        # Sprawdzenie, czy nowe miejsce to stos końcowy
        is_end = any(new_place is s for s in self.board.end_stacks)

        # Sprawdzenie, czy ruch jest dozwolony według reguł gry
        if found_cart.check_move(new_place, self.board):
            # Ruch pojedynczej karty, gdy jest na końcu stosu lub pochodzi z rezerwy
            if (found_cart.place.index(found_cart) == len(found_cart.place) - 1
                    or found_cart.place is self.board.reserve_stack):
                found_cart.move(new_place)

            # Ruch wielu kart (wiele kart odkrytych jednocześnie)
            elif all(card.view for card in found_cart.place[found_cart.place.index(found_cart):]):
                if is_end:
                    print("Na stosy końcowe nie można przenieść kilku kart jednocześnie")
                else:
                    found_cart.double_move(new_place)
            else:
                print("Błąd")
        else:
            print("Niespełnione warunki przenoszenia")
            time.sleep(2)

    def update_all_places(self):
        # Aktualizacja atrybutu 'place' dla wszystkich kart w każdym stosie
        for cart in self.board.reserve_stack:
            cart.place = self.board.reserve_stack

        for stack in self.board.end_stacks:
            for cart in stack:
                cart.place = stack

        for stack in self.board.main_stacks:
            for cart in stack:
                cart.place = stack

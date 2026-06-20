# cart.py - plik z klasą Cart

# Klasa karty
class Cart:
    def __init__(self, cart_symbol, place):
        self.cart_symbol = cart_symbol      # Nadanie symbolu karty (np. "A♥", "10♣")
        self.place = place                  # Przypisanie miejsca, w którym karta aktualnie się znajduje (np. stos)
        if len(cart_symbol) == 2:
            self.cart_number = cart_symbol[0]   # Jeśli symbol ma 2 znaki, pierwszy to wartość (np. "A"), drugi to kolor
            self.cart_color = cart_symbol[1]
        elif len(cart_symbol) == 3:
            self.cart_number = cart_symbol[:2]  # Jeśli symbol ma 3 znaki (np. "10♥"), dwa pierwsze to wartość
            self.cart_color = cart_symbol[2]    # Trzeci znak to kolor
        else:
            self.cart_number = "0"              # Jeśli symbol ma nieoczekiwaną długość, przypisywane są wartości domyślne
            self.cart_color = "0"

        self.view = False                   # Flaga informująca, czy karta ma być widoczna na planszy

    def __str__(self):                      # Metoda do reprezentacji karty jako napis (np. przy wypisywaniu na ekran)
        return self.cart_symbol

    def check_move(self, new_place, board):        # Metoda sprawdzająca, czy można przenieść kartę do wskazanego stosu
        if new_place in board.main_stacks:         # Przenoszenie do głównego stosu
            if new_place:
                # Sprawdzenie, czy kolor przenoszonej karty różni się od koloru ostatniej karty w stosie
                if (self.cart_color in ["♥", "♦"] and new_place[-1].cart_color not in ["♥", "♦"]) or \
                   (self.cart_color in ["♣", "♠"] and new_place[-1].cart_color not in ["♣", "♠"]):
                    # Sprawdzenie, czy wartość karty jest o 1 mniejsza niż wartość ostatniej karty w stosie
                    if board.card_values[self.cart_number] == board.card_values[new_place[-1].cart_number] - 1:
                        return True
            elif not new_place:
                # Do pustego stosu można przenieść tylko króla
                if self.cart_number == "K":
                    return True

        elif new_place in board.end_stacks:        # Przenoszenie do stosu końcowego

            if len(new_place) == 0:
                # Do pustego stosu końcowego można przenieść tylko asa
                return self.cart_number == "A"

            # Jeśli stos końcowy nie jest pusty, karta musi mieć ten sam kolor i być o 1 większa
            top = new_place[-1]
            return (self.cart_color == top.cart_color
                    and board.card_values[self.cart_number] == board.card_values[top.cart_number] + 1)

        elif new_place is board.reserve_stack:     # Próba przeniesienia do stosu rezerwowego
            print("Nie można przenosić kart do stosu rezerwowego")

        else:                                      # Jeśli docelowe miejsce nie jest znanym stosem
            print("Błędny stos")

        return False                               # W pozostałych przypadkach ruch jest niedozwolony

    def move(self, new_place):              # Metoda do przeniesienia jednej karty
        new_place.append(self)              # Dodanie karty do nowego stosu
        self.place.remove(self)             # Usunięcie karty z poprzedniego stosu
        self.place = new_place              # Aktualizacja atrybutu place na nowy stos

    def double_move(self, new_place):       # Przeniesienie wszystkich kart od bieżącej do końca stosu

        if self.place is None:              # Jeśli karta nie ma przypisanego stosu — błąd
            print("Błąd: Karta nie należy do żadnego stosu.")
            return

        try:
            index = self.place.index(self)  # Znalezienie indeksu bieżącej karty w jej stosie
        except ValueError:                  # Jeśli karta nie została znaleziona — błąd
            print("Błąd: Nie znaleziono karty w jej obecnym stosie.")
            return

        cards_to_move = self.place[index:]  # Lista kart do przeniesienia od bieżącej do końca stosu
        new_place.extend(cards_to_move)     # Dodanie ich do nowego stosu
        del self.place[index:]              # Usunięcie kart ze starego stosu

        # Ustawienie nowego miejsca (place) dla każdej przeniesionej karty
        for card in cards_to_move:
             card.place = new_place

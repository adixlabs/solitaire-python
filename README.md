# Solitaire (Klondike) – Python Console Game

## Project Overview

This project is a console-based implementation of the classic **Klondike Solitaire** game written in Python. The application allows the player to play Solitaire directly in the terminal, following the standard game rules.

The project includes:

* card movement validation,
* stock (reserve) pile handling,
* foundation piles,
* command suggestions for mistyped commands (fuzzy matching),
* game timer,
* restart functionality,
* simple text-based user interface.

---

# Project Structure

```text
.
├── game.py          # Main application entry point
├── board.py         # Board representation and user interface
├── board_logic.py   # Core game logic
├── cart.py          # Card class
└── README.md
```

---

# Requirements

* Python 3.10 or later

Required library:

```bash
pip install thefuzz
```

---

# Running the Game

From the project directory, run:

```bash
python game.py
```

---

# Game Rules

The objective is to move all 52 cards onto the four foundation piles.

## Foundation Piles

Each foundation pile must be built:

* starting with an Ace (A),
* ending with a King (K),
* using cards of the same suit.

Example:

```text
A♥
2♥
3♥
...
Q♥
K♥
```

---

## Tableau Piles

Cards on the tableau must be arranged:

* in descending order,
* with alternating colors (red/black).

Example:

```text
8♠
7♥
6♣
5♦
```

Only a King may be moved onto an empty tableau pile.

---

# Available Commands

| Command                 | Description                                |
| ----------------------- | ------------------------------------------ |
| `HELP`                  | Display help information                   |
| `MOVE <card> TO <pile>` | Move a card                                |
| `FLIP`                  | Reveal the next card from the reserve pile |
| `RESTART`               | Start a new game                           |
| `EXIT`                  | Quit the application                       |

Examples:

```text
MOVE AH TO E1
MOVE 10D TO M4
MOVE KS TO M1
```

---

# Pile Shortcuts

## Tableau Piles

```text
M1
M2
M3
M4
M5
M6
M7
```

## Foundation Piles

```text
E1
E2
E3
E4
```

## Suit Abbreviations

| Abbreviation | Suit       |
| ------------ | ---------- |
| h            | ♥ Hearts   |
| d            | ♦ Diamonds |
| s            | ♠ Spades   |
| c            | ♣ Clubs    |

Examples:

```text
AH
10D
QS
KC
```

---

# Features

* Random deck shuffling
* Automatic card dealing
* Move validation according to Solitaire rules
* Multiple-card movement (when allowed)
* Automatic card revealing
* Game timer
* Restart option
* Command suggestions for typos using fuzzy matching

---

# Project Architecture

## `game.py`

The application's entry point.

Responsibilities:

* starting the game,
* handling user input,
* processing commands,
* restarting the game,
* tracking play time.

---

## `board.py`

Contains the `Board` class responsible for the game state and console interface.

Responsibilities:

* creating all piles,
* displaying the board,
* showing available commands,
* displaying help,
* communicating with the game logic.

---

## `board_logic.py`

Implements the core game mechanics.

Responsibilities:

* initializing the game,
* shuffling and dealing cards,
* validating moves,
* checking the win condition,
* updating card locations,
* normalizing user input.

---

## `cart.py`

Represents a single playing card.

Provides methods for:

* validating moves,
* moving a single card,
* moving multiple cards.

---

# Winning the Game

The game is won when all four foundation piles contain all thirteen cards of their respective suits.

Once completed, the application displays a victory message along with the total game time.

---

# Author

Console implementation of the classic **Klondike Solitaire** game written in Python.


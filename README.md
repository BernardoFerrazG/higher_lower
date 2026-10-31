# Higher or Lower

[![CI](https://github.com/BernardoFerrazG/higher_lower/actions/workflows/ci.yml/badge.svg)](https://github.com/BernardoFerrazG/higher_lower/actions/workflows/ci.yml)

A terminal card game written in pure Python (no dependencies). You are shown a card and guess whether the next card from a shuffled 52-card deck will be **higher** or **lower**.

```
The first card is: 9 of Spades
Will the next card be higher or lower than 9 of Spades? (h/l): h
The next card is: Jack of Diamonds
Correct! +20
Score: 70
```

## Rules

- Ace is low (1), King is high (13).
- Each round you make 8 guesses; a correct guess is worth **+20**, a wrong one **−15**.
- **Ties lose**: if the next card has the same rank, neither guess is correct.
- You start with 50 points, and your score carries over between rounds.

## Running

Requires Python 3.10+.

```bash
python -m higher_lower                # play
python -m higher_lower --guesses 12   # longer rounds
python -m higher_lower --seed 7       # reproducible shuffle
```

## Design

```
higher_lower/
├── cards.py      # Card (immutable dataclass) and Deck
├── game.py       # Rules, scoring and the game loop
└── __main__.py   # command-line entry point
tests/            # pytest suite
```

- The game logic is separate from the terminal: `Game` takes injectable `ask` / `say` functions and a seeded random generator. Tests can therefore play complete scripted games without a keyboard.
- `Rules` is a frozen dataclass, so the scoring and round length can be changed in one place.
- Invalid answers are asked again **without** drawing a card. In the original version, a typo wasted a card.

## Tests

```bash
pip install pytest
pytest
```

The suite covers the deck (52 unique cards), card values, every guess/tie combination, scoring, input validation and seed reproducibility. CI runs it on every push.

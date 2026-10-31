import random

import pytest

from higher_lower import Card, Deck, Game, Rules, is_correct


def test_deck_has_52_unique_cards():
    deck = Deck()
    cards = [deck.draw() for _ in range(52)]
    assert len(set(cards)) == 52
    assert deck.draw() is None


def test_card_values():
    assert Card("Ace", "Spades").value == 1
    assert Card("10", "Hearts").value == 10
    assert Card("King", "Clubs").value == 13


@pytest.mark.parametrize(
    "guess, current, following, expected",
    [
        ("h", "5", "9", True),
        ("h", "9", "5", False),
        ("l", "9", "5", True),
        ("l", "5", "9", False),
        ("h", "7", "7", False),  # ties always lose
        ("l", "7", "7", False),
    ],
)
def test_is_correct(guess, current, following, expected):
    assert is_correct(guess, Card(current, "Spades"), Card(following, "Hearts")) is expected


def scripted_game(answers, rules=Rules(guesses_per_round=3), seed=0):
    answers = iter(answers)
    output = []
    game = Game(rules, rng=random.Random(seed), ask=lambda _: next(answers), say=output.append)
    return game, output


def test_invalid_answers_are_asked_again_without_consuming_a_card():
    game, output = scripted_game(["x", "h", "?", "l", "h", "n"])
    game.start()
    assert sum("Please answer" in line for line in output) == 2
    assert sum(line.startswith("The next card is") for line in output) == 3


def test_score_changes_by_reward_and_penalty():
    rules = Rules(starting_score=0, guesses_per_round=5, reward=20, penalty=15)
    game, output = scripted_game(["h"] * 5 + ["n"], rules=rules)
    game.start()
    right = sum(line.startswith("Correct") for line in output)
    wrong = sum(line.startswith("Wrong") for line in output)
    assert right + wrong == 5
    assert game.score == 20 * right - 15 * wrong


def test_same_seed_same_cards():
    outputs = []
    for _ in range(2):
        game, output = scripted_game(["h", "h", "h", "n"], seed=42)
        game.start()
        outputs.append(output)
    assert outputs[0] == outputs[1]

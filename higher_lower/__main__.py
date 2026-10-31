import argparse
import random

from .game import Game, Rules


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m higher_lower", description="Higher or Lower card game.")
    parser.add_argument("--guesses", type=int, default=Rules.guesses_per_round, help="guesses per round (max 51)")
    parser.add_argument("--seed", type=int, help="shuffle seed, for a reproducible game")
    args = parser.parse_args()

    if not 1 <= args.guesses <= 51:
        parser.error("--guesses must be between 1 and 51")

    try:
        Game(Rules(guesses_per_round=args.guesses), rng=random.Random(args.seed)).start()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")


if __name__ == "__main__":
    main()

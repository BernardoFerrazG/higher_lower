from deck import Deck
from card import Card


class Game:

    def __init__(self, score=50, num_cards=8):
        self.score = score
        self.deck = Deck()
        self.num_cards = num_cards


    def play_round(self):

        self.deck = Deck()
        self.deck.shuffle()
        current_card = self.deck.draw()
        print(f"The first card is: {current_card}")
        print()

        for _ in range(self.num_cards):
            guess = input(f"The next card is higher or lower than {current_card}? (answer with h or l): ").casefold()
            next_card = self.deck.draw()
            if not next_card:
                print("No more cards in the deck.")
                break

            print(f"The next card is: {next_card}")
            self.evaluate_guess(guess, current_card, next_card)
            print(f"Your score is: {self.score}")
            print()
            current_card = next_card

    def evaluate_guess(self, guess, current_card, next_card):

        if guess == 'h':
            if next_card.value > current_card.value:
                print("You got it right!!!")
                self.score += 20
            else:
                print("You were wrong, what a shame!")
                self.score -= 15
        elif guess == 'l':
            if next_card.value < current_card.value:
                print("You got it right!!!")
                self.score += 20
            else:
                print("You were wrong, what a shame!")
                self.score -= 15
        else:
            print("Invalid answer, please respond with 'h' or 'l'.")

    
    def play_again(self):
        while True:
            go_again = input('Do you want to play again? ("y" for yes, "n" for no) ').casefold()
            if go_again == 'n':
                print("Thanks for playing! Goodbye.")
                break
            elif go_again == 'y':
                self.play_round()
            else:
                print('Please respond with "y" or "n".')


    
    def start(self):
        
        print("Welcome to Higher or Lower")
        print("Guess if the next card will be higher or lower than the current card")
        print("If you guess correctly, you earn 20 points, but if you are wrong, you lose 15")
        print(f"You start with {self.score} points")
        print()


        while True:
            self.play_round()

            if not self.play_again():
                break



def main():
    game = Game()
    game.start()

main()   

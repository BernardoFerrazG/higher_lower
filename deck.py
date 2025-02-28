import random
from card import Card

class Deck:

    suits = ("Spades", "Clubs", "Diamonds", "Hearts")
    ranks = ("Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King")


    def __init__(self):
        self.cards = [Card(rank, suit, value+1)
                      for suit in Deck.suits
                      for value, rank in enumerate(Deck.ranks)]
        
    def shuffle(self):
        """shuffle cards"""
        random.shuffle(self.cards)

    def draw(self):
        """show the next card"""
        return self.cards.pop() if self.cards else None
    

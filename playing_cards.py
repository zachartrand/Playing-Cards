# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 12:29:47 2021

@author: Zach Chartrand <zachartrand999@gmail.com>

A module for playing cards.
"""

__all__ = ['PlayingCard', 'Deck', 'Hand', 'makeDeckInNewDeckOrder',
           'makeEuchreDeck', 'makePinochleDeck']

from typing import Iterable, List
from random import shuffle as _shuffle

VALUES = ['Joker', 'Ace', 'Two', 'Three', 'Four', 'Five', 'Six',
          'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']

SUITS = ['Clubs', 'Hearts', 'Spades', 'Diamonds']


def main():
    deck = makeDeckInNewDeckOrder()
    print("A deck of playing cards in American new deck order:\n")
    deck.print_cards()


class PlayingCard():
    """
    Class for Playing Card objects.

    Create a playing card as found in a poker deck. Requires a value
    and a suit upon creation.

    value can be either a string ('Ace', 'King') or an integer
    (1 = Ace, 13 = King).

    suit can be either a string ('Clubs', 'Diamonds') or an integer
    following the CHaSeD order (0 = Clubs, 1 = Hearts, 2 = Spades,
    3 = Diamonds).
    """
    def __init__(self, value: int or str, suit: int or str):
        if isinstance(value, int):
            if value > 13:
                raise ValueError("value must be between 0 and 13 (inclusive).")
            self.value = value
            self.value_name = VALUES[value]
        elif isinstance(value, str):
            if value.title() not in VALUES:
                raise ValueError(f"{value.title()} is not a valid playing card value.")
            self.value_name = value.title()
            self.value = VALUES.index(value.title())

        if isinstance(suit, int):
            if suit > 3:
                raise ValueError("suit must be between 0 and 3 (inclusive).")
            self.suit = suit
            self.suit_name = SUITS[suit]
        elif isinstance(suit, str):
            if suit.title() not in SUITS:
                raise ValueError("f{suit} is not a valid playing card suit.")
            self.suit_name = suit.title()
            self.suit = SUITS.index(suit.title())

        if self.value == 0:
            self.name = "Joker"
        else:
            self.name = " ".join((self.value_name, "of", self.suit_name))

    def __eq__(self, other) -> bool:
        """
        Return self == other.

        PlayingCards are considered equivalent if both their value and
        suit are identical.
        """
        if isinstance(other, PlayingCard):
            if (self.value, self.suit) == (other.value, other.suit):
                return True

        return False

    def __hash__(self) -> int:
        """Return hash(self)."""
        return hash((self.value, self.suit, self.name))

    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}('
                f"'{self.value_name}', '{self.suit_name})'")

    def __str__(self) -> str:
        """
        Return str(self).

        Return a human-readable string of the card's name
        (e.g. 'Ace of Spades').
        """
        return self.name

    def get_name(self) -> str:
        """
        Return a human-readable string of the card's name
        (e.g. 'Ace of Spades').
        """
        return self.name

    def get_value(self) -> int:
        """Return the card's value."""
        return self.value

    def get_suit(self) -> int:
        """Return the card's suit."""
        return self.suit

    def get_value_name(self) -> str:
        """Return the name of the card's value."""
        return self.value_name

    def get_suit_name(self) -> str:
        """Return the name of the card's suit."""
        return self.suit_name


class Deck():
    """
    Class for creating a deck of cards.

    Make a deck of any number of cards. Requires an iterable
    containing the PlayingCard objects you want in the deck. The first
    card in the iterable will be on top of the deck, the last on bottom.
    """
    def __init__(self, playing_cards: Iterable[PlayingCard]):
        self.cards = list(playing_cards)

    def __eq__(self, other) -> bool:
        """
        Return self == other.

        Two decks are considered equivalent if they have the exact same
        cards in the exact same order.
        """
        if isinstance(other, Deck):
            if len(self) == len(other):
                if self.get_list_of_cards() == other.get_list_of_cards():
                    return True

        return False

    def __len__(self) -> int:
        """
        Return len(self).

        Return the number of cards in the deck.
        """
        return len(self.cards)

    def get_cards(self) -> List[PlayingCard]:
        """
        Return the list of card objects that make up the deck.
        """
        return self.cards

    def get_list_of_cards(self, start: int = -1, stop: int = -1) -> List[str]:
        """
        Return a list of the names of the cards in the deck. By
        default, list all of the cards from top to bottom. If start
        is defined, show all the cards from that index to the end.
        If stop is defined, list all of the cards from the beginning
        to the stop index. If both are defined, this method will list
        the cards from start to stop.
        """
        listOfCards = []
        if (start, stop) == (-1, -1):
            for card in self.cards:
                listOfCards.append(card.get_name())
        else:
            if start == -1:
                cards = self.cards[:stop]
            elif stop == -1:
                cards = self.cards[start:]
            else:
                cards = self.cards[start:stop]

            for card in cards:
                listOfCards.append(card.get_name())

        return listOfCards

    def get_card_at(self, index: int) -> PlayingCard:
        """
        Return the playing card at the given index. The top card of
        the deck is at position 0 and the bottom card is at position
        [len(Deck) - 1].
        """
        return self.cards[index]

    def shuffle(self, n: int=1) -> None:
        """
        Shuffle the cards n times. By default, the deck is shuffled
        once.
        """
        if self.cards:
            for _ in range(n):
                _shuffle(self.cards)

    def cut(self, cards_off_top: int = -1) -> None:
        """
        Cut the deck.

        By default, the deck is cut in half, i.e. the top half is
        placed below the bottom half. If the cards_off_top parameter is
        set, that number of cards is cut off the top of the deck and
        placed on the bottom.
        """
        if cards_off_top == -1:
            cards_off_top = len(self) // 2

        self.cards = self.cards[cards_off_top:] + self.cards[:cards_off_top]

    def add_card(self, card: PlayingCard) -> None:
        """Add a PlayingCard to the Deck."""
        self.cards.append(card)

    def sort(self, *, key=lambda card: card.value, reverse=False) -> None:
        self.cards.sort(key=key, reverse=reverse)

    def deal_top_card(self) -> PlayingCard or None:
        """
        Deal the top card of the deck.

        Return the top card and remove it from the deck.
        """
        if self.cards:
            card = self.cards.pop(0)
            return card

        return None

    def bottom_deal(self) -> PlayingCard or None:
        """
        Deal the card from the bottom of the deck.

        Return the playing card at the last index and remove it from
        the deck.
        """
        if self.cards:
            card = self.cards.pop()
            return card

        return None

    def second_deal(self) -> PlayingCard or None:
        """
        Deal the second card in the deck.
        """
        if len(self) >= 2:
            card = self.cards.pop(1)
            return card

        return None

    def out_faro(self, number_of_cards_on_top: int = 0,
                 number_of_cards_on_bottom: int = 0) -> None:
        """
        Perform an out-faro shuffle on the deck.

        An out-faro is a perfect weave of the cards, alternating one
        card at a time between the two halves of the deck, with the top
        and bottom cards remaining on the top and bottom of the deck.

        By default, perform an out-faro on a perfectly cut deck (or as
        close as possible if the deck has an odd number of cards).
        If you wish to cut either the top half or bottom half a certain
        number of cards that isn't a perfect cut, populate either the
        number_of_cards_on_top or number_of_cards_on_bottom parameters
        with the number of cards you want to cut from the top or bottom
        of the deck, respectively.
        """
        if (number_of_cards_on_bottom, number_of_cards_on_top) == (0, 0):
            newDeck = [None for i in range(len(self))]
            for i, card in enumerate(self.cards):
                newPosition = i*2
                if newPosition >= len(self):
                    newPosition += 1
                    newPosition %= len(self)
                newDeck[newPosition] = card
        else:
            if number_of_cards_on_bottom == 0:
                number_of_cards_on_bottom = (
                    len(self) - number_of_cards_on_top)
            elif number_of_cards_on_top == 0:
                number_of_cards_on_top = (
                    len(self) - number_of_cards_on_bottom)

            topHalf = self.cards[:number_of_cards_on_top]
            bottomHalf = self.cards[-number_of_cards_on_bottom:]
            numberOfIterations = (
                len(topHalf) if len(topHalf) > len(bottomHalf)
                else len(bottomHalf))
            newDeck = []
            for i in range(numberOfIterations):
                try:
                    newDeck.append(topHalf[i])
                except:
                    pass
                try:
                    newDeck.append(bottomHalf[i])
                except:
                    pass

        self.cards = newDeck

    def in_faro(self, number_of_cards_on_top: int = 0,
                number_of_cards_on_bottom: int = 0) -> None:
        """
        Perform an in-faro shuffle on the deck.

        An in-faro is a perfect weave of the cards, alternating one
        card at a time between the two halves of the deck, with the top
        and bottom cards moving inward one position in the deck.

        See the Deck.out_faro() documentation for parameter
        information.
        """
        if (number_of_cards_on_bottom, number_of_cards_on_top) == (0, 0):
            newDeck = [None for i in range(len(self))]
            for i, card in enumerate(self.cards):
                newPosition = i*2 + 1
                if newPosition >= len(self):
                    newPosition -= 1
                    newPosition %= len(self)
                newDeck[newPosition] = card
        else:
            if number_of_cards_on_bottom == 0:
                number_of_cards_on_bottom = (
                    len(self) - number_of_cards_on_top)
            elif number_of_cards_on_top == 0:
                number_of_cards_on_top = (
                    len(self) - number_of_cards_on_bottom)

            topHalf = self.cards[:number_of_cards_on_top]
            bottomHalf = self.cards[-number_of_cards_on_bottom:]
            numberOfIterations = (
                len(topHalf) if len(topHalf) > len(bottomHalf)
                else len(bottomHalf))
            newDeck = []
            for i in range(numberOfIterations):
                try:
                    newDeck.append(bottomHalf[i])
                except:
                    pass
                try:
                    newDeck.append(topHalf[i])
                except:
                    pass

        self.cards = newDeck

    def print_cards(self) -> None:
        for i, card in enumerate(self.cards):
            print(i, card.get_name())


# Based this on Card.py Hand class from Think Python by Allen Downy.
class Hand(Deck):
    """A player's hand of PlayingCards."""
    def __init__(self, label='') -> None:
        self.cards = []
        self.label = label

    def __str__(self) -> str:
        if self.label:
            return f"{self.label} Hand ({len(self)} cards)"
        else:
            return f"Hand of {len(self)} cards."


def makeDeckInNewDeckOrder(mode: str="US") -> Deck:
    """
    Create and return a Deck object in New Deck Order (NDO).

    By default, return a deck in the NDO used by the U.S. Playing Card
    Company. By setting mode to 'European', return a deck in NDO used
    by European playing card companies like, e.g., Cartamundi.
    """
    suitOrder = dict(
        US = ("Hearts", "Clubs", "Diamonds", "Spades"),
        European = ("Spades", "Hearts", "Diamonds", "Clubs"),
    )
    if mode not in suitOrder.keys():
        raise ValueError("mode must be 'US' or 'European'.")

    deck = []
    for suit in suitOrder[mode][:2]:
        for value in range(1, 14):
            deck.append(PlayingCard(value, suit))
    for suit in suitOrder[mode][2:]:
        for value in reversed(range(1, 14)):
            deck.append(PlayingCard(value, suit))

    return Deck(deck)


def makeEuchreDeck() -> Deck:
    """
    Return a Euchre deck.

    Euchre uses cards from all suits valued from nine (9) to Ace high.
    """
    cards = []
    for suit in SUITS:
        for value in range(9, 14):
            cards.append(PlayingCard(value, suit))
        cards.append(PlayingCard(1, suit))

    return Deck(cards)


def makePinochleDeck() -> Deck:
    """
    Return a Pinochle deck.

    Pinochle uses a deck of cards made of two copies of each card from
    nine (9) to Ace high.
    """
    cards = []
    for suit in SUITS:
        for value in range(9, 14):
            for _ in range(2):
                cards.append(PlayingCard(value, suit))
        for _ in range(2):
            cards.append(PlayingCard(1, suit))

    return Deck(cards)


if __name__ == "__main__":
    main()

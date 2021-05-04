# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 12:29:47 2021

@author: Zach Chartrand <zachartrand999@gmail.com>
"""

__all__ = ['PlayingCard', 'Deck', 'makeDeckInNewDeckOrder', 'makeEuchreDeck']

from typing import Iterable, List
from random import shuffle as _shuffle

VALUES = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
    'Nine', 'Ten', 'Jack', 'Queen', 'King']

SUITS = ['Clubs', 'Hearts', 'Spades', 'Diamonds']


class PlayingCard():
    """
    Class for Playing Card objects.

    Creates a playing card as found in a poker deck. Requires a value
    and a suit upon creation.

    value can be either a string ('Ace', 'King') or an integer
    (1 = Ace, 13 = King).

    suit can be either a string ('Clubs', 'Diamonds') or an integer
    following the CHaSeD order (0 = Clubs, 1 = Hearts, 2 = Spades,
    3 = Diamonds).
    """
    def __init__(self, value: int or str, suit: int or str):
        if isinstance(value, int):
            self.value = value
            self.value_name = VALUES[value - 1]
        elif isinstance(value, str):
            self.value_name = value.title()
            self.value = VALUES.index(value.title())

        if isinstance(suit, int):
            self.suit = suit
            self.suit_name = SUITS[suit]
        elif isinstance(suit, str):
            self.suit_name = suit.title()
            self.suit = SUITS.index(suit.title())

        self.name = ' '.join((self.value_name, 'of', self.suit_name))

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
        return(f'{self.__class__.__name__}('
               f"'{self.value_name}', '{self.suit_name})'")

    def __str__(self) -> str:
        """
        Return str(self).

        Returns a human-readable string of the card's name
        (e.g. 'Ace of Spades').
        """
        return self.name

    def get_name(self) -> str:
        """
        Returns a human-readable string of the card's name
        (e.g. 'Ace of Spades').
        """
        return self.name

    def get_value(self) -> int:
        """Returns the card's value."""
        return self.value

    def get_suit(self) -> int:
        """Returns the card's suit."""
        return self.suit

    def get_value_name(self) -> str:
        """Returns the name of the card's value."""
        return self.value_name

    def get_suit_name(self) -> str:
        """Returns the name of the card's suit."""
        return self.suit_name


class Deck():
    """
    Class for creating a deck of cards.

    This can make a deck of any number of cards. Requires an iterable
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

        Returns the number of cards in the deck.
        """
        return len(self.cards)

    def get_cards(self) -> List[PlayingCard]:
        """
        Returns the list of card objects that make up the deck.
        """
        return self.cards

    def get_list_of_cards(self, start: int = -1, stop: int = -1) -> List[str]:
        """
        Returns a list of the names of the cards in the deck from top
        to bottom.
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
        Returns the playing card at the given index. The top card of
        the deck is at position 0 and the bottom card is at position
        [len(Deck) - 1].
        """
        return self.cards[index]

    def shuffle(self) -> None:
        """
        Shuffles the cards.
        """
        if self.cards:
            _shuffle(self.cards)

    def cut(self, cards_off_top: int = -1) -> None:
        """
        Cuts the deck.

        By default, the deck is cut in half, i.e. the top half is
        placed below the bottom half. If the cards_off_top parameter is
        set, that number of cards is cut off the top of the deck and
        placed on the bottom.
        """
        if cards_off_top == -1:
            cards_off_top = len(self) // 2

        self.cards = self.cards[cards_off_top:] + self.cards[:cards_off_top]

    def deal_top_card(self) -> PlayingCard or None:
        """
        Returns the top card and removes it from the deck.
        """
        if self.cards:
            card = self.cards[0]
            self.cards.remove(card)
            return card

        return None

    def out_faro(self, number_of_cards_on_top: int = 0,
                 number_of_cards_on_bottom: int = 0) -> None:
        """
        Performs an out-faro shuffle on the deck.

        An out-faro is a perfect weave of the cards, alternating one
        card at a time between the two halves of the deck, with the top
        and bottom cards remaining on the top and bottom of the deck.

        By default, this method performs an out-faro on a perfectly cut
        deck (or as close as possible if the deck has an odd number of
        cards). If you wish to cut either the top half or bottom half a
        certain number of cards that isn't a perfect cut, you can
        populate either the number_of_cards_on_top or
        number_of_cards_on_bottom parameters with the number of cards
        you want to cut from the top or bottom of the deck,
        respectively.
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
        Performs an in-faro shuffle on the deck.

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


def makeDeckInNewDeckOrder(mode: str='US') -> Deck:
    """
    Creates and returns a Deck object in New Deck Order (NDO).

    By default, this creates a deck in the NDO used by the U.S. Playing
    Card Company. By setting mode to 'European', you get a deck in NDO
    used by European playing card companies like, e.g., Cartamundi.
    """
    deck = []
    if mode == 'US':
        # Hearts
        for value in VALUES:
            deck.append(PlayingCard(value, 'Hearts'))
        # Clubs
        for value in VALUES:
            deck.append(PlayingCard(value, 'Clubs'))
        # Diamonds. Note: value order reverses.
        for value in reversed(VALUES):
            deck.append(PlayingCard(value, 'Diamonds'))
        # Spades
        for value in reversed(VALUES):
            deck.append(PlayingCard(value, 'Spades'))
    elif mode == 'European':
        # Spades
        for value in VALUES:
            deck.append(PlayingCard(value, 'Spades'))
        # Hearts
        for value in VALUES:
            deck.append(PlayingCard(value, 'Hearts'))
        # Diamonds. Note: value order reverses.
        for value in reversed(VALUES):
            deck.append(PlayingCard(value, 'Diamonds'))
        # Clubs
        for value in reversed(VALUES):
            deck.append(PlayingCard(value, 'Clubs'))
    else:
        raise ValueError("mode must be 'US' or 'European'")

    return Deck(deck)


def makeEuchreDeck() -> Deck:
    cards = []
    for suit in SUITS:
        for value in VALUES[8:]:
            cards.append(PlayingCard(value, suit))
        cards.append(PlayingCard(1, suit))

    return Deck(cards)

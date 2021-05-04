# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 01:28:39 2021

@author: Zach Chartrand
"""

from playing_cards import makeDeckInNewDeckOrder, Deck # , PlayingCard

def makeMnemonicaDeck() -> Deck:
    """
    Creates a deck in Mnemonica stack. For master wizards only.
    """
    deck = makeDeckInNewDeckOrder('European')
    for _ in range(4):
        deck.out_faro()
    topHalf, bottomHalf = deck.cards[:26], deck.cards[-26:]
    topHalf.reverse()
    deck.cards = topHalf + bottomHalf
    deck.out_faro(18)
    deck.cut(9)
    
    return deck

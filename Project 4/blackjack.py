#!/usr/bin/env python3
"""
Simple text-based Blackjack (21) in Python — cleaned & easy version
Run this file in VS Code (Python 3.8+). No extra libraries required.

Key fixes & simplifications from prior version:
- Bet is *reserved* when placed (subtracted from bankroll), and payouts return the bet + winnings.
- Blackjack pays 3:2 (handled correctly).
- Clearer, shorter code and comments for beginners.
- Uses OOP for Card, Deck, Hand, Chips.
"""

import random
from dataclasses import dataclass
from typing import List, Tuple

SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
RANKS = (
    "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Jack", "Queen", "King", "Ace"
)
VALUES = {
    "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
    "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11
}


@dataclass(frozen=True)
class Card:
    suit: str
    rank: str

    @property
    def value(self) -> int:
        return VALUES[self.rank]

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self) -> None:
        self.cards: List[Card] = [Card(s, r) for s in SUITS for r in RANKS]
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self) -> Card:
        if not self.cards:
            # rebuild and reshuffle when empty (keeps the game simple across rounds)
            self.__init__()
        return self.cards.pop()


class Hand:
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.cards: List[Card] = []
        self.value: int = 0
        self.aces_as_eleven: int = 0  # how many aces currently counted as 11

    def add_card(self, card: Card) -> None:
        self.cards.append(card)
        self.value += card.value
        if card.rank == "Ace":
            self.aces_as_eleven += 1
        self._adjust_for_aces()

    def _adjust_for_aces(self) -> None:
        # If bust and have an ace counted as 11, convert one ace from 11 to 1 (-10)
        while self.value > 21 and self.aces_as_eleven > 0:
            self.value -= 10
            self.aces_as_eleven -= 1

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value == 21

    def is_bust(self) -> bool:
        return self.value > 21

    def __str__(self) -> str:
        cards = ", ".join(str(c) for c in self.cards)
        return f"{self.owner} ({self.value}): {cards}"


@dataclass
class Chips:
    total: int = 100
    bet: int = 0

    def place_bet(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Bet must be positive.")
        if amount > self.total:
            raise ValueError("Bet cannot exceed your bankroll.")
        self.bet = amount
        # Reserve the bet by subtracting it from total now.
        self.total -= amount

    def win_regular(self) -> None:
        # Player gets back original bet + winnings equal to bet (1:1)
        self.total += 2 * self.bet
        self.bet = 0

    def win_blackjack(self) -> None:
        # Blackjack pays 3:2. Player should end up with original bet + 1.5*bet
        # After reserve, add back 2.5*bet = bet + 1.5*bet so total change is +1.5*bet
        self.total += int(2.5 * self.bet)
        self.bet = 0

    def push(self) -> None:
        # Return the bet (tie)
        self.total += self.bet
        self.bet = 0

    def lose(self) -> None:
        # Bet was already removed when placed; on loss we simply drop the bet.
        self.bet = 0


# -------------------- Small helper functions --------------------

def prompt_int(prompt: str) -> int:
    while True:
        try:
            val = int(input(prompt).strip())
            return val
        except ValueError:
            print("Please enter a valid integer.")


def prompt_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


def prompt_hit_or_stand() -> str:
    while True:
        ans = input("Hit or Stand? [h/s]: ").strip().lower()
        if ans in ("h", "hit"):
            return "hit"
        if ans in ("s", "stand"):
            return "stand"
        print("Choose 'h' (hit) or 's' (stand).")


# -------------------- Game logic --------------------

def deal_initial(deck: Deck, player_name: str) -> Tuple[Hand, Hand]:
    player_hand = Hand(player_name)
    dealer_hand = Hand("Dealer")
    # two cards each
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    return player_hand, dealer_hand


def show_table(player_hand: Hand, dealer_hand: Hand, hide_dealer: bool = True) -> None:
    print("-" * 50)
    if hide_dealer:
        # show dealer's second card only as the visible one and hide the first
        if dealer_hand.cards:
            print(f"Dealer (??): [Hidden], {dealer_hand.cards[1]}")
        else:
            print("Dealer: (no cards)")
    else:
        print(str(dealer_hand))
    print(str(player_hand))
    print("-" * 50)


def dealer_play(deck: Deck, dealer_hand: Hand) -> None:
    # Dealer hits until 17 or more (stands on soft 17)
    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal())


def settle(player_hand: Hand, dealer_hand: Hand, chips: Chips) -> str:
    player_bj = player_hand.is_blackjack()
    dealer_bj = dealer_hand.is_blackjack()

    if player_bj and dealer_bj:
        chips.push()
        return "Push — both have Blackjack."
    if player_bj:
        chips.win_blackjack()
        return "Blackjack! You win (3:2)."
    if dealer_bj:
        chips.lose()
        return "Dealer has Blackjack. You lose."

    if player_hand.is_bust():
        chips.lose()
        return "You busted — dealer wins."
    if dealer_hand.is_bust():
        chips.win_regular()
        return "Dealer busted — you win!"

    # compare totals
    if player_hand.value > dealer_hand.value:
        chips.win_regular()
        return "You win!"
    elif player_hand.value < dealer_hand.value:
        chips.lose()
        return "Dealer wins."
    else:
        chips.push()
        return "Push — it's a tie."


def play_round(deck: Deck, chips: Chips, player_name: str) -> None:
    print("\n--- New Round ---")
    print(f"Bankroll: {chips.total}")
    # take bet
    while True:
        amt = prompt_int("Enter bet amount: ")
        try:
            chips.place_bet(amt)
            break
        except ValueError as e:
            print(f"Invalid bet: {e}")

    # deal
    player_hand, dealer_hand = deal_initial(deck, player_name)
    show_table(player_hand, dealer_hand, hide_dealer=True)

    # check naturals
    if player_hand.is_blackjack() or dealer_hand.is_blackjack():
        show_table(player_hand, dealer_hand, hide_dealer=False)
        print(settle(player_hand, dealer_hand, chips))
        print(f"Bankroll now: {chips.total}")
        return

    # player turn
    while True:
        move = prompt_hit_or_stand()
        if move == "hit":
            player_hand.add_card(deck.deal())
            show_table(player_hand, dealer_hand, hide_dealer=True)
            if player_hand.is_bust():
                break
        else:
            break

    # dealer turn only if player not busted
    if not player_hand.is_bust():
        dealer_play(deck, dealer_hand)

    # reveal and settle
    show_table(player_hand, dealer_hand, hide_dealer=False)
    print(settle(player_hand, dealer_hand, chips))
    print(f"Bankroll now: {chips.total}")


def main() -> None:
    print("Welcome to Simple Blackjack!")
    name = input("Your name (press Enter for 'Player'): ").strip() or "Player"
    chips = Chips(total=100)
    deck = Deck()

    while chips.total > 0:
        play_round(deck, chips, name)
        if chips.total <= 0:
            print("You're out of chips. Game over.")
            break
        if not prompt_yes_no("Play another round? [y/n]: "):
            break

    print(f"Thanks for playing, {name}. You leave with {chips.total} chips.")


if __name__ == "__main__":
    main()

import random
import time
from termcolor import colored
import os
import replit
delay = 3


class card:
    def __init__(self, number, color):
        self.number = str(number)
        self.color = color


def draw(player):
    global deck, player1, player2, player3, player4, game

    if len(deck) < 1:
        deck.extend(discard)

    drawn = random.choice(deck)
    deck.remove(drawn)

    player.append(drawn)

    if game:
        if player == player1:
            print("\nPlayer 1 drew a " + read(drawn))
        elif player == player2:
            print("\nPlayer 2 drew a card")
        elif player == player3:
            print("\nPlayer 3 drew a card")
        elif player == player4:
            print("\nPlayer 4 drew a card")

        time.sleep(delay / 2)


def read(card):
    name = ""
    type = card.number
    suit = card.color

    if type == "wild" and suit != "z":
        name = colored("|wild|", suit)
    if suit == "z":
        name = colored("|", "blue") + colored("|", "yellow") + type + colored("|", "red") + colored("|", "green")
    else:
        name = colored("|" + type + "|", suit)

    return name


def printHand(hand):
    cards = ""
    hand.sort(key=lambda x: x.number)
    hand.sort(key=lambda x: x.color)
    for i in hand:
        cards = cards + read(i) + " "
    print(cards)


def endTurn():
    global lastCard
    global reverse
    global player
    global effect

    colors = ["blue", "green", "red", "yellow"]
    color = ""

    if effect == "reverse":
        effect = "none"

        if reverse:
            reverse = False
        else:
            reverse = True
        turn()

    elif effect == "skip":
        effect = "none"

        turn()
        print("\nPlayer " + str(player) + " was skipped.")
        time.sleep(delay)
        turn()

    elif effect == "wild":
        effect = "none"

        if player == 1:
            while color not in colors:
                color = input("Choose a new color: ").lower()
        else:
            color = random.choice(colors)

        print("The color has been changed to " + colored(color, color))
        time.sleep(delay)
        lastCard = card("wild", color)
        turn()

    elif effect == "+2":
        effect = "none"

        turn()
        if player == 1:
            draw(player1)
            draw(player1)

        elif player == 2:
            draw(player2)
            draw(player2)

        elif player == 3:
            draw(player3)
            draw(player3)

        elif player == 4:
            draw(player4)
            draw(player4)

        turn()

    elif effect == "+4":
        effect = "none"

        if player == 1:
            while color not in colors:
                color = input("Choose a new color: ").lower()
        else:
            color = random.choice(colors)

        print("The color has been changed to " + colored(color, color))
        time.sleep(delay)
        lastCard = card("+4", color)

        turn()
        if player == 1:
            draw(player1)
            draw(player1)
            draw(player1)
            draw(player1)
        elif player == 2:
            draw(player2)
            draw(player2)
            draw(player2)
            draw(player2)
        elif player == 3:
            draw(player3)
            draw(player3)
            draw(player3)
            draw(player3)
        elif player == 4:
            draw(player4)
            draw(player4)
            draw(player4)
            draw(player4)

        turn()

    else:
        effect = "none"
        turn()


def turn():
    global player

    if not reverse:
        player += 1
    else:
        player -= 1

    if player < 1:
        player = 4
    if player > 4:
        player = 1

    ui()


def play(card):
    global lastCard
    global effect

    if card.number == "skip":
        effect = "skip"
    elif card.number == "+2":
        effect = "+2"
    elif card.number == "reverse":
        effect = "reverse"
    elif card.number == "+4":
        effect = "+4"
    elif card.number == "wild":
        effect = "wild"

    if player == 1:
        player1.remove(card)
    elif player == 2:
        player2.remove(card)
    elif player == 3:
        player3.remove(card)
    elif player == 4:
        player4.remove(card)

    discard.append(card)
    random.shuffle(discard)

    lastCard = card


def check(card):
    global lastCard
    global effect

    if card.color == "z":
        return True
    elif lastCard.color == "z":
        return True
    elif lastCard.number == "wild" and card.color == lastCard.color:
        return True
    elif lastCard.number == card.number or card.color == lastCard.color:
        return True
    else:
        return False


def ui():
    global player, lastCard

    replit.clear()

    if player == 1:
        if not reverse:
            print("\n  -->")
        else:
            print("\n  <--")
    elif player == 2:
        if not reverse:
            print("\n             -->")
        else:
            print("\n             <--")
    elif player == 3:
        if not reverse:
            print("\n                        -->")
        else:
            print("\n                        <--")
    elif player == 4:
        if not reverse:
            print("\n                                   -->")
        else:
            print("\n                                   <--")

    print("player 1 | player 2 | player 3 | player 4")
    print(" " + str(len(player1)) + " cards   " + str(len(player2))
          + " cards    " + str(len(player3)) + " cards    "
          + str(len(player4)) + " cards")

    print("\nYour cards:")
    printHand(player1)

    print("\nLast card played was " + read(lastCard))


def think(p):
    global player
    global lastCard

    random.shuffle(p)

    pick = card("blank", "blank")
    invalid = True

    for i in p:
        if check(i):
            invalid = False
            pick = i

    time.sleep(delay)

    if invalid:
        draw(p)
    else:
        play(pick)
        print("\nPlayer " + str(player) + " played " + read(lastCard))
        time.sleep(delay)


deck = []

for j in range(2):
    for i in range(10):
        deck.append(card(i, "red"))

    for i in range(10):
        deck.append(card(i, "blue"))

    for i in range(10):
        deck.append(card(i, "green"))

    for i in range(10):
        deck.append(card(i, "yellow"))

    deck.append(card("skip", "yellow"))
    deck.append(card("reverse", "yellow"))
    deck.append(card("+2", "yellow"))
    deck.append(card("wild", "z"))
    deck.append(card("+4", "z"))

    deck.append(card("skip", "green"))
    deck.append(card("reverse", "green"))
    deck.append(card("+2", "green"))
    deck.append(card("wild", "z"))
    deck.append(card("+4", "z"))

    deck.append(card("skip", "blue"))
    deck.append(card("reverse", "blue"))
    deck.append(card("+2", "blue"))
    deck.append(card("wild", "z"))
    deck.append(card("+4", "z"))

    deck.append(card("skip", "red"))
    deck.append(card("reverse", "red"))
    deck.append(card("+2", "red"))
    deck.append(card("wild", "z"))
    deck.append(card("+4", "z"))

random.shuffle(deck)

# Start of Game
game = False
reverse = False
player = random.randint(1, 4)
discard = []
effect = "none"

player1 = []
player2 = []
player3 = []
player4 = []

for i in range(7):
    draw(player1)

for i in range(7):
    draw(player2)

for i in range(7):
    draw(player3)

for i in range(7):
    draw(player4)

draw(discard)
lastCard = discard[0]
print("\nStarting Card is " + read(lastCard))
time.sleep(delay)

turn()
game = True

# Main Game Loop
while game:

    if len(player1) < 1:
        print("\nYou win!")
        break
    elif len(player2) < 1:
        print("\nPlayer 2 won!")
        break
    elif len(player3) < 1:
        print("\nPlayer 3 won!")
        break
    elif len(player4) < 1:
        print("\nPlayer 4 won!")
        break

    if len(deck) < 1:
        deck = discard
        print("Deck is being reshuffled..")
        time.sleep(delay)

    # Player 1's player
    if player == 1:
        time.sleep(delay / 2)

        choice = input("\nWhat do you want to do? ").lower()

        invalid = True
        while invalid:
            if "draw" in choice:
                draw(player1)
                break

            pick = card("blank", "blank")

            for i in player1:
                if i.number in choice and check(i):
                    invalid = False
                    pick = i

            for i in player1:
                if i.color in choice and i.number in choice:
                    if check(i):
                        invalid = False
                        pick = i

            if invalid:
                choice = input("You can't play that card! Try again: ").lower()
            else:
                play(pick)
                print("\nYou played " + read(lastCard))
                time.sleep(delay / 2)

    # Player 2's player
    elif player == 2:
        think(player2)

    # Player 3's player
    elif player == 3:
        think(player3)

    # Player 4's player
    elif player == 4:
        think(player4)

    endTurn()

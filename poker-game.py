import random

class Card(object):
    """A card"""

    def __init__(self, suite, face):
        self._suite = suite
        self._face = face

    @property
    def face(self):
        return self._face

    @property
    def suite(self):
        return self._suite

    def __str__(self):
        if self._face == 1:
            face_str = 'A'
        elif self._face == 11:
            face_str = 'J'
        elif self._face == 12:
            face_str = 'Q'
        elif self._face == 13:
            face_str = 'K'
        else:
            face_str = str(self._face)
        return '%s%s' % (self._suite, face_str)

    def __repr__(self):
        return self.__str__()

class Poker(object):
    """A deck of cards"""

    def __init__(self):
        self._cards = [Card(suite, face) 
                       for suite in '♠♥♣♦'
                       for face in range(1, 14)]
        self._current = 0

    @property
    def cards(self):
        return self._cards

    def shuffle(self):
        """Shuffle (random out of order)"""
        self._current = 0
        random.shuffle(self._cards)

    @property
    def next(self):
        """Licensing"""
        card = self._cards[self._current]
        self._current += 1
        return card

    @property
    def has_next(self):
        """No cards"""
        return self._current < len(self._cards)

class Player(object):
    """Player"""

    def __init__(self, name):
        self._name = name
        self._cards_on_hand = []

    @property
    def name(self):
        return self._name

    @property
    def cards_on_hand(self):
        return self._cards_on_hand

    def get(self, card):
        """Draw"""
        self._cards_on_hand.append(card)

    def arrange(self, card_key):
        """The player sorts the cards in his hand"""
        self._cards_on_hand.sort(key=card_key)

    
def score_on_hands(cards_on_hand):
    """Return the points of the player's hand type and the points of the largest card"""
    score = 0
    straightCount = 0
    max_card = 0
    suite_dict = {}
    face_dict = {}
    transfer_dict = {'A':1,'J':11,'Q':12,'K':13}
    card_face = []
    '''Circulate the player's hand, build a list of points and a suit dict'''
    for index in range(len(cards_on_hand)):
        if str(cards_on_hand[index])[1] in transfer_dict:
            card_face.append(transfer_dict.get(str(cards_on_hand[index])[1]))
        elif str(cards_on_hand[index])[1] == '1':
            card_face.append(10)
        else:
            card_face.append(int(str(cards_on_hand[index])[1]))
        suite_dict[str(cards_on_hand[index])[0]] = 1
    '''Because 1 can be treated as 1 or 14, so if 1 exists, add 14 to the end of the list to calculate flush'''
    if 1 in card_face:
        card_face.append(14)

    '''Check straight, if it is straight, straight should be 4'''
    for face in range(len(card_face)-1):
        if card_face[face] +1 == card_face[face+1] :
            straightCount +=1

    '''Detect the number of cards of the same number'''
    for face in card_face:

        if face not in face_dict:
            face_dict[face] = 1
        else:
            face_dict[face] += 1

    '''Store the maximum number of points'''
    max_card = card_face[len(card_face)-1]

    '''Calculate player score'''
    if straightCount == 4:
        score+= 8

    if len(suite_dict) == 1:
        score+= 9

    for values in face_dict.values():
        if values == 2:
            score += 3
        elif values == 3:
            score += 7
        elif values == 4:
            score += 11

    return (score, max_card)


# Sorting rules-sort according to the number of points and then according to the suit
def get_key(card):
    #return (card.suite, card.face)
    return (card.face, card.suite)

def main():
    p = Poker()
    p.shuffle()
    winner = {'Winner':0,'score':0,'max':0}
    players = [Player('Achanakmar'), Player('Bhopali Surma'), Player('Chikara Colonel'), Player('Daru Kala')]  # Chork Panauti
    for _ in range(5):
        for player in players:
            player.get(p.next)

    for player in players:
        print(player.name + ':', end=' ')
        player.arrange(get_key)
        print(player.cards_on_hand)
        if score_on_hands(player.cards_on_hand)[0] == 0:
            print('high card')
        elif score_on_hands(player.cards_on_hand)[0] ==3:
            print('one pair')
        elif score_on_hands(player.cards_on_hand)[0] ==6:
            print('two pair')
        elif score_on_hands(player.cards_on_hand)[0] ==7:
            print('three of a kind')
        elif score_on_hands(player.cards_on_hand)[0] ==8:
            print('straight')
        elif score_on_hands(player.cards_on_hand)[0] ==9:
            print('flush')
        elif score_on_hands(player.cards_on_hand)[0] ==10:
            print('full house')
        elif score_on_hands(player.cards_on_hand)[0] ==11:
            print('four of a kind')
        elif score_on_hands(player.cards_on_hand)[0] ==17 and score_on_hands(player.cards_on_hand)[1] != 14:
            print('straight flush')
        elif score_on_hands(player.cards_on_hand)[0] ==17 and score_on_hands(player.cards_on_hand)[1] == 14:
            print('royar flush!!!')

        if score_on_hands(player.cards_on_hand)[0] >  winner['score']:
            winner['Winner'] = player.name 
            winner['score'] = score_on_hands(player.cards_on_hand)[0]
            winner['max'] = score_on_hands(player.cards_on_hand)[1]

        elif score_on_hands(player.cards_on_hand)[0] == winner['score']:
            if score_on_hands(player.cards_on_hand)[1] > winner['max']:
                winner['Winner'] = player.name 
                winner['score'] = score_on_hands(player.cards_on_hand)[0]
                winner['max'] = score_on_hands(player.cards_on_hand)[1]

    print('winner is ',winner['Winner'])

if __name__ == '__main__':
    main()
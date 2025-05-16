import random
import math
import db
# Card values
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}
conn=db.create_connection("BlackJack.db")
decks=3
# Starting balance and bet amount
STARTING_BALANCE = 500
bet_amount = [50, 50, 50, 10, 70, 100] 
NAMES=["MG","RMG","OSC","FIB","LAB","CC"]
WIN_BET_MODIFIER= [.5,2,bet_amount[2],1,[10,20,30,40,50,60]]
LOSS_BET_MODIFIER = [2,.5,bet_amount[2],10,[10,20,30,40,50,60]]
past_rounds = ["Win","Win","Win","Win","Win","Win"]
running_count=0   
out_players=[False,False,False,False,False,False]

def fibinacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibinacci(n-1) + fibinacci(n-2)
    
def labouchere(won):
   
    if len(WIN_BET_MODIFIER[4]) >1: 
        bet=WIN_BET_MODIFIER[4][0]+WIN_BET_MODIFIER[4][-1]
        if won == "Win":
            WIN_BET_MODIFIER[4].pop() 
            WIN_BET_MODIFIER[4].pop(0)
        else:
            WIN_BET_MODIFIER[4].append(WIN_BET_MODIFIER[4][0]+WIN_BET_MODIFIER[4][-1])
        return bet
    out_players[4]=True
    return 0
    
def card_counting(cards :str,count: int): 
    high=['10','J','Q','K','A']
    low=['2','3','4','5','6']
    
    if cards[0:2].strip() in high:
        count-=1
    elif cards[0:2].strip() in low: 
        count+=1
    return count
    
# Create a deck of cards
def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']*decks
    ranks = list(CARD_VALUES.keys())
    return [f"{rank} of {suit}" for rank in ranks for suit in suits]

# Calculate hand value
def calculate_hand_value(hand):
    value = sum(CARD_VALUES[card.split()[0]] for card in hand)
    aces = sum(1 for card in hand if card.startswith('A'))
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# AI decision to hit or stand
def ai_decision(hand):
    return calculate_hand_value(hand) < 18

def edit_bet():
    for i in range(len(bet_amount)):
        
        if i ==1 or i==0:
            if past_rounds[i] == "Win":
                bet_amount[i] = math.ceil(bet_amount[i] * WIN_BET_MODIFIER[i])
            elif past_rounds[i] == "Lose":
                bet_amount[i] = math.ceil(bet_amount[i] * LOSS_BET_MODIFIER[i])
        if i ==2:
            if past_rounds[i] == "Win":
                bet_amount[i] = bet_amount[i] + WIN_BET_MODIFIER[i]
            elif past_rounds[i] == "Lose":
                bet_amount[i] = bet_amount[i] - LOSS_BET_MODIFIER[i]
        if i ==3:
            if past_rounds[i] == "Win":
                bet_amount[i] = bet_amount[i] + fibinacci(WIN_BET_MODIFIER[i])
                WIN_BET_MODIFIER[i] += 2
            elif past_rounds[i] == "Lose":
                bet_amount[i] = 10
                WIN_BET_MODIFIER[i] = 10
        if i ==4:
            bet_amount[i] = labouchere(past_rounds[i])
        if i ==5:
            bet_amount[i] =min(2000,math.ceil( 2**(running_count)/decks))
        bet_amount[i] = max(50,min(balances[f"AI {i+1}"],bet_amount[i]))
        bet_amount[i] = min(2000,bet_amount[i])
        
    for i in range (len(bet_amount)):
        if balances[f"AI {i+1}"] ==0:
            out_players[i]=True
            print(f"AI {i+1} is out of money")
            bet_amount[i] = 0
    
            
            
# Play a round of Blackjack
def play_blackjack(balances,deck):
    global running_count
    players = {f"AI {i+1}": [] for i in range(6)}
    dealer= []
    
    # Deduct bets from each player's balance
    for player in players:
        balances[player] -= bet_amount[int(player[-1])-1]
 
    # Initial deal
    for _ in range(2):
        for player in players:
            temp=deck.pop()
            players[player].append(temp)
            running_count=card_counting(temp,running_count)
        temp=deck.pop()
        dealer.append(temp)
        running_count=card_counting(temp,running_count)

    # AI players' turns
    for player, hand in players.items():
        while ai_decision(hand):
            temp=deck.pop()
            hand.append(temp)
            running_count=card_counting(temp,running_count)

    # Dealer's turn
    while calculate_hand_value(dealer) < 17:
        temp=deck.pop()
        dealer.append(temp)
        running_count=card_counting(temp,running_count)

    if len(deck)<28:
        return True #checks if there is enough cards in the deck to play the game  
    # Determine results
    dealer_value = calculate_hand_value(dealer)
    print(f"Dealer's hand: {dealer} (Value: {dealer_value})")
    for player, hand in players.items():
        player_value = calculate_hand_value(hand)
        print(f"{player}'s hand: {hand} (Value: {player_value})")
        if player_value > 21:
            print(f"{player} busts!")
            past_rounds[int(player[-1])-1] = "Lose"
        elif dealer_value > 21 or player_value > dealer_value:
            print(f"{player} wins!")
            past_rounds[int(player[-1])-1] = "Win"
        elif player_value == dealer_value:
            print(f"{player} ties with the dealer!")
            past_rounds[int(player[-1])-1] = "Tie"
        else:
            print(f"{player} loses!")
            past_rounds[int(player[-1])-1] = "Lose"
        
    
    
        # Display balances
    print(f"\nRC: {running_count} Player balances:")
    for player, balance in balances.items():
        balance=max(0,balance)
        print(f"{player}: ${balance} ")
     
    for i in range (len(bet_amount)):
        if past_rounds[i] == "Win":
            balances[f"AI {i+1}"] += bet_amount[i] * 2
        if past_rounds[i] == "Tie":
            balances[f"AI {i+1}"] += bet_amount[i] 
           
        db.insert_db(conn,"Handwise",["Player","Bet","Result","Balance"],[NAMES[i],bet_amount[i],past_rounds[i],balances[f"AI {i+1}"]])
# Main game loop
if __name__ == "__main__":
    balances = {f"AI {i+1}": STARTING_BALANCE for i in range(6)}
    deck = create_deck()
    
    random.shuffle(deck)
    i=0
    while i<10:
            i+=1
        # try:
            print(len(deck))
            if play_blackjack(balances,deck):
                i-=1
                print("Deck is empty, reshuffling...")
                running_count=0
                for j in range(len(bet_amount)):
                    balances[f"AI {j+1}"] +=bet_amount[j] 
                deck = create_deck()
                continue
            
            random.shuffle(deck)
            edit_bet()
            temp=[]
            print(f"Trialwise: {i}")
            for player in balances:
                temp.append(balances[player])
            db.insert_db(conn,"Trialwise",["Martingale","Reverse Martingale","Oscar's Grind","Fibonanci","Labouchere","Card Counting"],[*temp])
        # except Exception as e:
        #     print(e)
        #     i-=1
            
        
    

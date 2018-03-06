# Deal two cards to the user, compute the sum, and display it to the user.
import random


# get card value
def deal_card():
    card = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    card_value = random.choice(card)
    return card_value


# get player scores
def get_player_score():
    player_card1 = deal_card()
    player_card2 = deal_card()
    player_score = player_card1 + player_card2
    print('Your hand of two cards has a total value of: ', player_score)
    HS_flag = input(('Would you like to take another card? (Y/N): '))
    while not (HS_flag == 'Y' or HS_flag == 'N'):
        HS_flag = input(('Would you like to take another card? (Y/N): '))
    while HS_flag == 'Y':
        player_score += deal_card()
        print('Your hand of two cards has a total value of: ', player_score)
        if player_score > 21:
            print('You BUSTED with a total value of ', player_score, end='\n')
            print('** You Lose. **')
            break
        HS_flag = input(('Would you like to take another card? (Y/N): '))
        while not (HS_flag == 'Y' or HS_flag == 'N'):
            HS_flag = input(('Would you like to take another card? (Y/N): '))
    return player_score


# get computer score
def get_dealer_score():
    dealer_card1 = deal_card()
    dealer_card2 = deal_card()
    dealer_sum = dealer_card1 + dealer_card2
    while dealer_sum < 16:
        dealer_sum += deal_card()
    return dealer_sum


# print result
def result_print(player_score, dealer_score):
    print('You have stopped taking more cards with a hand value of ', player_score)
    print('The dealer was dealt a hand with a value of ', dealer_score, end='\n')


# make comparision and give the result
def check_result(player_score, dealer_score):
    if dealer_score > 21:
        print('The dealer BUSTED with a value of ', dealer_score)
        print('** You Win **')
    elif player_score <= dealer_score:
        result_print(player_score, dealer_score)
        print('** You Lose. **')
    elif player_score > dealer_score:
        result_print(player_score, dealer_score)
        print('** You Win. **')



def main() -> object:
    continue_flag = 'Y'
    while not (continue_flag == 'Y' or continue_flag == 'N'):
        continue_flag = input('Would you like to play again? (Y/N)')
    while continue_flag == 'Y':
        print("Let's start our game blackjack!")
        player_score = get_player_score()
        dealer_score = get_dealer_score()
        if (player_score <= 21) and (dealer_score <= 21):
            check_result(player_score, dealer_score)
        continue_flag = input('Would you like to play again? (Y/N)')
        while not (continue_flag == 'Y' or continue_flag == 'N'):
            continue_flag = input('Would you like to play again? (Y/N)')

main()

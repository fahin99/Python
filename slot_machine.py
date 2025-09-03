import random

def spin_row():
    symbols= ['🍒', '🍋' ,'🍉' ,'🔔' ,'⭐']
    results= []
    for symbol in range(3):
        results.append(random.choice(symbols))
    return results
    #return [random.choice(symbols) for _ in range(3)]

def print_row(row):
    print("*************")
    print(" | ".join(row))
    print("*************")

def get_payout(row, bet):
    if row[0]==row[1]==row[2]:
        if row[0]=='🍒': return bet*3
        elif row[0]=='🍋': return bet*4
        elif row[0]=='🍉': return bet*5
        elif row[0]=='🔔': return bet*10
        elif row[0]=='⭐': return bet*20
    return 0

def main():
    balance=100
    print("******************************")
    print("    Welcome to Python Slots   ")
    print("    Symbols: 🍒 🍋 🍉 🔔 ⭐  ")
    print("******************************")
    while balance > 0:
        print(f"\nCurrent Balance: ${balance}")
        bet=input("Place your bet amount: ")
        if not bet.isdigit():
            print("Please enter a number")
            continue
        else:
            bet=int(bet)
            if bet > balance:
                print("Insufficient funds")
                continue
            elif bet <= 0:
                print("Bet must be greater than 0")
                continue
            balance-=bet
            row=spin_row()
            print("Spinning...\n")
            print_row(row)
            payout=get_payout(row, bet)
            if payout>0:
                print(f"You won ${payout}")
            else:
                print("\nSorry, you lost this round")
                if balance==0:
                    print("\nYou cannot play anymore. Quitting...")
                    break
            balance+=payout
            play_again=input("Do you want to play again? (y/n): ").upper()
            if play_again != "Y":
                break


if __name__=="__main__":
    main()
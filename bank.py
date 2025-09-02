#novice bank script
def balance_show(balance):
    print(f"Your balance is ${balance:.2f}")

def deposit():
    amount=float(input("Enter amount to deposit: "))
    if amount <= 0:
        print("\nInvalid amount")
        return 0
    else:
        print(f"\nDeposit successful")
        return amount

def withdraw(balance):
    amount=float(input("Enter amount to withdraw: "))
    if amount <= 0 or amount>balance:
        print("\nInvalid amount")
        return 0
    else:
        print(f"\nWithdraw successful")
        return amount

def main():
    balance=0
    running=True
    print("----------------Welcome to the Bank----------------")
    while running:
        print("-----------------------------------------------------")
        print("1. Show balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")
        print("Enter your choice(1-4):", end="")
        choice = int(input())
        if choice==1:
            print()
            balance_show(balance)
        elif choice==2:
            balance+=deposit()
            balance_show(balance)
        elif choice==3:
            balance-=withdraw(balance)
            balance_show(balance)
        elif choice==4:
            print("Exiting...")
            running=False
        else:
            print("\nInvalid choice")
        print()

if __name__=="__main__":
    main()
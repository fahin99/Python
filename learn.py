mode=input("Enter mode:")
if mode=="calc":
# compound interest calculator
    print("nothing")

#cart
elif mode=="cart":
    foods=[]
    prices=[]
    total=0
    while True:
        food=input("\nEnter the name of the food(press 'q' to quit): ")
        if food.lower() == 'q':
            print("\nStopping taking input")
            break
        else:
            price=input(f"Enter the price of {food}: $")
            foods.append(food)
            prices.append(float(price))
    print("\n----------Your Cart----------")
    count=0
    for food in foods:
        print(f"The price of {food} is ${prices[count]:.2f}")
        total+=prices[count]
        count+=1
    print(f"\nTotal: ${total:.2f}")
    print("---------------------------------")

#dice
#● ┌ ─ ┐ │ └ ┘
elif mode=="dice":
    import random
    '''
    "┌────────────┐"
    "│            │"
    "│            │"
    "│            │"
    "└────────────┘"
    '''
    dice_art={
        1: (
            "┌────────────┐",
            "│            │",
            "│      ●     │",
            "│            │",
            "└────────────┘"),
        2: (
            "┌────────────┐",
            "│ ●          │",
            "│            │",
            "│          ● │",
            "└────────────┘"),
        3: (
            "┌────────────┐",
            "│ ●          │",
            "│      ●     │",
            "│          ● │",
            "└────────────┘"),
        4: (
            "┌────────────┐",
            "│ ●        ● │",
            "│            │",
            "│ ●        ● │",
            "└────────────┘"),
        5: (
            "┌────────────┐",
            "│ ●        ● │",
            "│     ●      │",
            "│ ●        ● │",
            "└────────────┘"),
        6: (
            "┌────────────┐",
            "│ ●    ●   ● │",
            "│            │",
            "│ ●    ●   ● │",
            "└────────────┘"),
    }
    dice=[]
    total=0
    num_of_dice=int(input("Enter the number of dice: "))
    for die in range(num_of_dice):
        dice.append(random.randint(1,6))
        # for show in dice_art.get(dice[die]):
        #     print(show)
    for line in range(5):
        for die in dice:
            print(dice_art.get(die)[line], end="")
        print()
    for die in dice:
        total+=die
    print(f"\nTotal: {total}")
else:
    print("Invalid option")
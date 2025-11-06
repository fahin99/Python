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

import threading
import time

print()
def walk_dog(name):
    time.sleep(6)
    print(f"Finished walking {name}.")

def trash_dump():
    time.sleep(4)
    print("Trash has been dumped.")
    
def wash_dishes():
    time.sleep(2)
    print("Dishes are cleaned.")

chore1=threading.Thread(target=walk_dog, args=("Scooby",))
chore1.start()
chore2=threading.Thread(target=trash_dump)
chore2.start()
chore3=threading.Thread(target=wash_dishes)
chore3.start()
chore3.join()
chore1.join()
chore2.join()

print("\nAll chores are done!\n")

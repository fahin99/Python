import time
import datetime
import pygame

def set_alarm(alarm_time):
    print(f"Alarm set for {alarm_time}")
    sound_file="D:/OneDrive/Documents/Python/alarm/alarm.mp3"
    running=True
    while running:
        current_time=datetime.datetime.now().strftime("%H:%M:%S")
        # print(f"Current time: {current_time}", end="\r")
        print(current_time)
        if current_time==alarm_time:
            print("WAKE UP! 😭😮‍💨")
            pygame.mixer.init()
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
        time.sleep(1)
        
if __name__ == "__main__":
    alarm_time = input("Set the alarm time (HH:MM:SS): ")
    set_alarm(alarm_time)
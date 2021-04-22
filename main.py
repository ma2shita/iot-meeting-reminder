import gcalendar
import drawImage
import showOnEpaper
import datetime
from pygame import mixer
import time

startTime = remindTime = datetime.datetime.now()

def notify():
    mixer.init()
    mixer.music.load('notification.mp3')
    mixer.music.play(1)

def task():
    schedule = gcalendar.getEvent()
    global startTime, remindTime
    startTime = schedule['time']
    # startTime = startTime.replace(tzinfo=None)
    print(startTime.tzinfo)
    startStr = startTime.strftime('%H:%M')
    # remind = schedule['time'] - datetime.time(0, 15, 0, 0)
    
    remindTime = schedule['time'] - datetime.timedelta(0, 0, 0, 0, 15, 0, 0)
    remindStr = remindTime.strftime('%H:%M')
    # print(type(start), type(remind))
    event = schedule['event']
    if(event != 'No Event'):
        drawImage.newImage(remindStr, startStr, event)
        showOnEpaper.show(event)
    else:
        showOnEpaper.show(event)

def main():
    while True:
        global startTime, remindTime
        dt_now = datetime.datetime.now(startTime.tzinfo)
        if(dt_now > startTime):
            notify()
            time.sleep(60)
            task()
        elif(remindTime < dt_now and dt_now < remindTime + datetime.timedelta(0, 0, 0, 0, 1, 0, 0)):
            notify()
        time.sleep(60)
        

if __name__ == "__main__":
    main()
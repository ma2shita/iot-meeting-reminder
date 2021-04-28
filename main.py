import gcalendar
import drawImage
import showOnEpaper
import datetime
from pygame import mixer
import time

import pytz


def notify():
    mixer.init()
    mixer.music.load('decision47.mp3')
    mixer.music.play(1)
    time.sleep(5)


def remind():
    mixer.init()
    mixer.music.load('tirin1.mp3')
    mixer.music.play(1)
    time.sleep(5)

def schedules():
    schedule = gcalendar.getEvent()
    currentStartTime = schedule['time']
    currentRemindTime = currentStartTime - datetime.timedelta(0, 0, 0, 0, 15, 0, 0)
    currentEvent = schedule['event']

    nextStartTime = schedule['nextTime']
    nextRemindTime = nextStartTime - datetime.timedelta(0, 0, 0, 0, 15, 0, 0)
    nextEvent = schedule['nextEvent']
    return currentStartTime, currentRemindTime, currentEvent, nextStartTime, nextRemindTime, nextEvent

def display(startTime, remindTime, eventName):
    if(eventName != "No Event"):
        startStr = startTime.strftime('%H:%M')
        remindStr = remindTime.strftime('%H:%M')
        drawImage.newImage(remindStr, startStr, eventName)
        showOnEpaper.show(eventName)
    else:
        showOnEpaper.show(eventName)

def main():
    dispStartTime, dispRemindTime, dispEvent, _, _, _ = schedules()
    display(dispStartTime, dispRemindTime, dispEvent)

    while True:
        tzinfo = pytz.timezone('Asia/Tokyo')
        dt_now = datetime.datetime.now(tzinfo)
        if(dispEvent == 'No Event'):
            time.sleep(datetime.timedelta(hours=1).seconds)
            print('No Event')
            dispStartTime, dispRemindTime, dispEvent, _, _, _ = schedules()
        elif(dt_now < dispRemindTime):
            print('dt_now < RemindTime')
            time.sleep((dispRemindTime - dt_now).seconds)
            remind()
            time.sleep(1)
        elif(dispRemindTime < dt_now and dt_now < dispStartTime):
            print('RemindTime < dt_now < StartTime')
            time.sleep((dispStartTime - dt_now).seconds)
            notify()
            time.sleep(1)
        elif(dispStartTime < dt_now):
            print('StartTime < dt_now')
            time.sleep(120) #ePaperの更新まで2分待つ
            _, _, _, dispStartTime, dispRemindTime, dispEvent = schedules()
            display(dispStartTime, dispRemindTime, dispEvent)
            

if __name__ == "__main__":
    main()


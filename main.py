import gcalendar
import drawImage
import showOnEpaper
import datetime
from pygame import mixer
import time

import pytz

startTime = remindTime = datetime.datetime.now()
eventName = ''
nextTime = ''
nextEvent = ''


def notify():
    mixer.init()
    mixer.music.load('notification.mp3')
    mixer.music.play(1)


def remind():
    mixer.init()
    mixer.music.load('remind.mp3')
    mixer.music.play(1)

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

def task():
    schedule = gcalendar.getEvent()
    global startTime, remindTime, eventName, nextEvent
    startTime = schedule['time']
    # startTime = startTime.replace(tzinfo=None)
    # print(startTime.tzinfo)

    startStr = startTime.strftime('%H:%M')
    # remind = schedule['time'] - datetime.time(0, 15, 0, 0)
    
    remindTime = schedule['time'] - datetime.timedelta(0, 0, 0, 0, 15, 0, 0)
    remindStr = remindTime.strftime('%H:%M')
    # print(type(start), type(remind))

    event = eventName = schedule['event']
    
    nextTime = schedule['nextTime']
    nextEvent = schedule['nextEvent']
    

    if(event != 'No Event'):
        drawImage.newImage(remindStr, startStr, event)
        showOnEpaper.show(event)
    else:
        showOnEpaper.show(event)

def main():
    while True:
        global startTime, remindTime, eventName
        tzinfo = pytz.timezone('Asia/Tokyo')
        dt_now = datetime.datetime.now(tzinfo)
        # dt_now = datetime.datetime.now()
        # startTime = startTime.replace(tzinfo=None)
        # notify()
        task()
        print(type)
        if(remindTime < dt_now):
            timeToRemind = datetime.timedelta(seconds=0)
        else:
            timeToRemind = remindTime - dt_now

        timeToStart = startTime - dt_now
        
        # if(timeToRemind < dt_now):
        #     timeToRemind = datetime.timedelta(seconds=0)
        
        print(timeToStart.seconds)
        time.sleep(timeToRemind.seconds)
        notify()
        time.sleep((timeToStart - timeToRemind).seconds)
        notify()
        # if(nextTime is not None):
        #     time.sleep()
        
        # if(dt_now > startTime and eventName != 'No Event'):
        #     notify()
        #     time.sleep(1)
        #     task()
        # elif(remindTime < dt_now and dt_now < remindTime + datetime.timedelta(0, 0, 0, 0, 1, 0, 0)):
        #     notify()
        # time.sleep(60)
        
def temp():
    dispStartTime, dispRemindTime, dispEvent, _, _, _ = schedules()
    display(dispStartTime, dispRemindTime, dispEvent)
    # dispRemindTime = ''
    # dispStartTime = ''
    # dispEvent = ''
    while True:
        tzinfo = pytz.timezone('Asia/Tokyo')
        dt_now = datetime.datetime.now(tzinfo)
        if(dispEvent == 'No Event'):
            time.sleep(datetime.timedelta(hours=1).seconds)
            print('noevent')
            dispStartTime, dispRemindTime, dispEvent, _, _, _ = schedules()
        elif(dt_now < dispRemindTime):
            print('dtnow < disptime')
            time.sleep((dispRemindTime - dt_now).seconds)
            remind()
            time.sleep(1)
        elif(dispRemindTime < dt_now and dt_now < dispStartTime):
            print('disptime < dtnow < dispstart')
            time.sleep((dispStartTime - dt_now).seconds)
            notify()
            time.sleep(1)
        elif(dispStartTime < dt_now):
            print('dispstart < dtnow')
            time.sleep(5)
            _, _, _, dispStartTime, dispRemindTime, dispEvent = schedules()
            # if(dispEvent != 'No Event'):
            display(dispStartTime, dispRemindTime, dispEvent)
            # time.sleep((dispStartTime - dt_now))


if __name__ == "__main__":
    temp()


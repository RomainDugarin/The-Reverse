import time, calendar, asyncio


@asyncio.coroutine
def periodic():
    #Periodic
    sleep = 1300
    lastShow = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(calendar.timegm(time.gmtime())))
    nextShow = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime( calendar.timegm(time.gmtime())+sleep ))
    while True:
        print("Last show : " + lastShow)
        print("Next show : " + nextShow)
        #if heure actuelle >= prochaine event
        if time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(calendar.timegm(time.gmtime()))) >= nextShow:
            lastShow = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(calendar.timegm(time.gmtime())))
            nextShow = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime( calendar.timegm(time.gmtime())+sleep ))
            print("On est a la bonne heure. heure actuelle : " + lastShow)
        else:
            print("Pas maintenant. heure actuelle : " + time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(calendar.timegm(time.gmtime()))))
        #Periodic time
        yield from asyncio.sleep(10)



def stop():
    task.cancel()

task = asyncio.Task(periodic())
loop = asyncio.get_event_loop()
loop.call_later(86400, stop)

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
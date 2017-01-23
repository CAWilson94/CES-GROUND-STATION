import requests
from scheduler.models import TLE, AzEl, NextPass, Mission
import math, ephem
from datetime import date, datetime, timedelta


class Services():
    def getAzElTLE(self, tleEntry, dateTime):

        # getObserver preferences file AK
        observer = _Helper.getObserver(self, dateTime);

        try:
            sat = ephem.readtle(tleEntry.name, tleEntry.line1, tleEntry.line2)  # necessary?
        except ValueError:
            return "Format of TLEEntry is incorrect (getAzElTLE)"

        sat.compute(observer)
        return AzEl(0, sat.az, sat.alt)


    def getAzElTLENow(self, tleEntry):
        return Services.getAzElTLE(self, tleEntry, datetime.now())


    def getAzElForPeriod(self, tleEntry, riseTime, setTime, period):
        azelProgress = []
        i = 0
        for timestamp in _Helper.timeSpan(riseTime, setTime, delta=timedelta(seconds=period)):
            azel = Services.getAzElTLE(self, tleEntry, timestamp)
            i += 1  # change azel id? AK
            azelProgress.append(azel)
        return azelProgress


    def getNextPass(self, tleEntry, dateTime):
        observer = _Helper.getObserver(self, dateTime);
        try:
            sat = ephem.readtle(tleEntry.name, tleEntry.line1, tleEntry.line2)
        except ValueError:
            return "Format of TLEEntry is incorrect (getNextPass)"

        details = observer.next_pass(sat)

        riseTime = _Helper.roundMicrosecond(details[0])
        setTime = _Helper.roundMicrosecond(details[4])
        duration = setTime - riseTime
        # riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth
        return NextPass(0, riseTime, setTime, duration, details[3], details[1], details[5])


    def findMissionById(index):
        try:
            mission = Mission.objects.get(id=index)
        except Mission.DoesNotExist:
            mission = None
        return mission

    def findMissionByName(name):
        try:
            mission = Mission.objects.get(name=name)
        except Mission.DoesNotExist:
            mission = None
        return mission

    def findMissionsByTLE(TLE):
        try:
            mission_list = Mission.objects.filter(TLE=TLE)
        except Mission.DoesNotExist:
            mission_list = None
        return mission_list


    def findMissionsByStatus(status):
        try:
            mission_list = Mission.objects.filter(status=status)
        except Mission.DoesNotExist:
            mission_list = None
        return mission_list


    def findMissionsByPriority(priority):
        try:
            mission_list = Mission.objects.filter(priority=priority)
        except Mission.DoesNotExist:
            mission_list = None
        return mission_list

    def findMissionsByCurrentNumberOfPasses(current_num_passes):
        try:
            mission_list = Mission.objects.filter(current_num_passes=current_num_passes)
        except Mission.DoesNotExist:
            mission_list = None
        return mission_list

    def findMissionsByMaxNumberOfPasses(max_num_passes):
        try:
            mission_list = Mission.objects.filter(max_num_passes=max_num_passes)
        except Mission.DoesNotExist:
            mission_list = None
        return mission_list

    def saveOrUpdate(mission):
        try:
            Mission.objects.update_or_create(mission)
            return True
        except Mission.DoesNotExist:
            return False

    def removeMissionByName(name):
        try:
            Mission.objects.filter(name=name).delete()
            return True
        except Mission.DoesNotExist:
            return False


    def updateTLE():
        """
        Retrieves TLE data from external source, checks format and places in db
        """
        requestsObject = requests.get("http://celestrak.com/NORAD/elements/cubesat.txt")
        tle = requestsObject.text

        # splits text into one list with format:  AK
        # name, line1, line2, name, line1, line2
        tleArray = tle.split('\r\n')

        # remove errant empty entry
        if tleArray[len(tleArray) - 1] == '':
            del tleArray[len(tleArray) - 1]
        if len(tleArray) % 3 != 0:
            print("major error")  # TODO: raisemassive error AK

        checkedTLEArray = _Helper.checkTLEFormat(tleArray)

        i = 0
        while i <= (len(checkedTLEArray) - 3):
            name = _Helper.adder(checkedTLEArray[i]).strip()
            try:
                tleEntry = TLE.objects.get(name=name)
                pass  # what does pass do?
            except TLE.DoesNotExist as e:
                # create new entry in db
                newTLE = TLE(name=name, line1=checkedTLEArray[i + 1], line2=checkedTLEArray[i + 2])
                newTLE.save()
            else:
                # update existing
                tleEntry.line1 = checkedTLEArray[i + 1]
                tleEntry.line2 = checkedTLEArray[i + 2]
                tleEntry.save()
            i += 3


class _Helper():
    # Helper Functions
    def adder(stringsep):  # nicer way? AK
        """
        Adds up the split strings of the satellite name
        """
        string = ""
        for x in stringsep:
            string = string + x
        return (string)


    def checkTLEFormat(tleArray):
        """
        Checks the format of the each TLE line to make sure it is in the correct format
        """
        i = 0
        badEntriesArray = []  # needs an iterator
        while i <= (len(tleArray) - 3):
            try:
                ephem.readtle(tleArray[i], tleArray[i + 1], tleArray[i + 2])
            except ValueError:
                # print ("Bad entry ",tleArray[i]) #put in log
                badEntriesArray.append(tleArray[i])
                badEntriesArray.append(tleArray[i + 1])
                badEntriesArray.append(tleArray[i + 2])
            i += 3

        goodEntriesArray = [entry for entry in tleArray if entry not in badEntriesArray]
        return goodEntriesArray

    def getObserver(self, datetime):
        observer = ephem.Observer();
        observer.lat = math.radians(55.8667)
        observer.long = math.radians(-4.4333)
        observer.date = ephem.Date(datetime)
        return observer

    def timeSpan(startTime, endTime, delta):  # timedelta(days=1)):
        # returns iterator of timestamps in from start to end AK
        currentTime = startTime
        while currentTime < endTime:
            yield currentTime
            currentTime += delta
            # from stackoverflow

    def roundMicrosecond(ephemDate):
        dateTime = ephemDate.datetime()
        ms = dateTime.microsecond / 1000000
        msRound = int(round(ms, 0))
        dateTime = dateTime + timedelta(seconds=msRound) - timedelta(microseconds=dateTime.microsecond)
        return dateTime
		



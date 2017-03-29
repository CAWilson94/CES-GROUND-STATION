from random import randint
from datetime import timedelta
from scheduler.models import NextPass
from scheduler.schedulerHelper import SchedulerHelper
from scheduler.MOT.schedulerInterface import MOT

# mins added to the end of the conflict period
CONFLICT_PADDING = timedelta(minutes=1)
# minimum lengh of pass to fill in the conflict window once a sat is chosen.
MIN_SUB_PASS_LEN = timedelta(minutes=3)

DEBUG = False

DEBUG_LEVEL = 1

orderOfPasses = []

class MOTRuleBased(MOT):

    def _passAsStr(self, nextPass):
        return (nextPass.tle.name + "(" + str(nextPass.mission.priority) + "): "  
            + str(nextPass.riseTime.strftime('%H:%M:%S')) + " -> " + str(nextPass.setTime.strftime('%H:%M:%S')))

    def _lastIndex(self, list, value):
        index = 0
        temp = orderOfPasses[::-1]
        while(index < len(temp)):
            if(temp[index].tle.name == value.tle.name):
                return len(temp) - index
            index += 1
        return -1

    # def _getPassesFromMissions(self, missions):
    #     passes = []

    #     dateNow = datetime.now()

    #     print("Total missions: " + str(len(missions)))
    #     i = 0
    #     for m in missions:
    #         i += 1
    #         print("Finding passes for the next 36 hours, found: " + str(len(passes)) + ", now looking at " + str(i) + " : " + m.TLE.name)

    #         tleEntry = m.TLE
    #         try:
    #             nextPass = Services.getNextPass(self, tleEntry, dateNow)
    #             nextPass.tle = tleEntry
    #             nextPass.mission = m
    #             passes.append(nextPass)
    #             if(DEBUG and DEBUG_LEVEL >= 4):
    #                 print(nextPass.__str__() + "\n")

    #             while(nextPass.setTime < (dateNow + timedelta(hours=36))):
    #                 time = nextPass.setTime + timedelta(minutes=1)
    #                 try:
    #                     nextPass = Services.getNextPass(self, tleEntry, time)
    #                     nextPass.tle = tleEntry
    #                     nextPass.mission = m
    #                     passes.append(nextPass)
    #                     if(DEBUG and DEBUG_LEVEL >= 4):
    #                         print(nextPass.__str__() + "\n")
    #                 except ValueError: 
    #                     break
    #         except ValueError: 
    #                 print("No pass was found for " + tleEntry.name + " over groundstation in the next 36 hours.")
    #     return passes

    # General checking if the pass is within conflicting time period
    def _conflicts(self, periodStart, periodEnd, passToCheck):
        if(passToCheck.riseTime >= periodStart and passToCheck.riseTime <= periodEnd):
            return True
        else:
            return False


    # Rule 1
    # Filter out low priority
    def _filterPriority(self, conflicting):
        if(conflicting):
            highestPriority = conflicting[0].mission.priority
            #print("Highest Priority: " + str(highestPriority))
            filtered = []

            for sat in conflicting:
                if(sat.mission.priority == highestPriority):
                    filtered.append(sat)
                    #print("Added " + sat.())

                if(sat.mission.priority > highestPriority):
                    filtered = []
                    highestPriority = sat.mission.priority
                    filtered.append(sat)
                    #print("Found new highest: " + str())

            if(filtered):
                return filtered

        return conflicting


    # Rule 2
    # Pick ones which haven't been picked yet
    def _filterByUnpicked(self, conflicting):
        if(conflicting):
            neverPicked = []
            for sat in conflicting:
                unpicked = True
                for aPass in orderOfPasses:
                    if(aPass.tle.name == sat.tle.name):
                        unpicked = False

                if(unpicked):
                    neverPicked.append(sat)
            if(neverPicked):
                return neverPicked

        return None


    # Rule 3
    # Pick the oldest one
    def _filterByOldest(self, conflicting):
        if(conflicting):
            oldestPass = conflicting[0]
            oldest = [oldestPass]
            oldestLastIndex = self._lastIndex(orderOfPasses, oldestPass)

            index = 0
            while(index < len(conflicting)):
                current = conflicting[index]
                currentLastIndex = self._lastIndex(orderOfPasses, current)
                if(currentLastIndex < oldestLastIndex):
                    oldest = [conflicting[index]]  # reset oldest list
                    oldestPass = current
                    oldestLastIndex = currentLastIndex
                elif(currentLastIndex == oldestLastIndex):
                    oldest.append(conflicting[index])
                index += 1

            return oldest
        return None

    """
        Rules for filtering the list of conflicts down to one satellite. 
            1. Highest Priority first
            2. The one that hasn't been looked at at all
            3. The one hasn't been looked at in the longest time
            4. The one that comes first chronologically
            5. Randomly chosen

        
        Rule 1: Filter by priority
            if only one is found with a higher priority
                add to order
            if more than one are found of the higher priority
                apply rule 2
            if none are found
                apply rule 2
        Rule 2: Filter by whether it has been picked at all. 
            if only one hasn't been picked before
                add it to order
            if more than one is found that hasn't been picked before
                apply rule 4
            if none are found that weren't picked before
                apply rule 3
        Rule 3: Find one which hasn't been picked in the longest time. 
            add it to the order
        Rule 4: Choose a radom one
            add it to the order

        Later change Rule 4 to:
        Rule 4.1: Find the one which leaves the lagest gap between the 
                  start or the end of the pass
            if one found
                add it to the order
            else 
                apply original Rule 4
            
    """
    def _findNext(self, conflicting, startTime, endTime):
        #print("There were : " + str(len(conflicting)) + " conflicts found:")
        if(conflicting):
            temp = conflicting
            chosen = temp[0]

            # Rule 1
            temp = self._filterPriority(temp)
            if(len(temp) == 1):
                if(DEBUG and DEBUG_LEVEL >= 3):
                    print(
                        "Only one found with highest priority, returning: " + self._passAsStr(temp[0]))
                return temp[0]

            unpicked = self._filterByUnpicked(temp)
            if(unpicked is not None):
                if(len(unpicked) == 1):
                    if(DEBUG and DEBUG_LEVEL >= 3):
                        print(
                            "Only one found which wasn't picked before, returning: " + self._passAsStr(unpicked[0]))
                    return unpicked[0]
                elif(len(unpicked) > 1):

                    if(DEBUG and DEBUG_LEVEL >= 4):
                        print("Unpicked:")
                        for sat in unpicked:
                            print(self._passAsStr(sat))
                    returning = unpicked[randint(0, len(unpicked) - 1)]
                    if(DEBUG and DEBUG_LEVEL >= 3):
                        print(
                            "Multiple not picked before, reurning random one: " + self._passAsStr(returning))
                    return returning
                    # Implement this when dealing with partial conflicts too.
                    # return filterByTimeSaved(temp, startTime, endTime)
                else:
                    print("No unpicked found")

            oldest = self._filterByOldest(temp)
            if(len(oldest) == 1):
                if(DEBUG and DEBUG_LEVEL >= 3):
                    print("One oldest found, returning it: " +
                          self._passAsStr(oldest[0]))
                return oldest[0]
            elif(len(oldest) > 1):

                if(DEBUG and DEBUG_LEVEL >= 4):
                    print("Oldest:")
                    for sat in oldest:
                        print(self._passAsStr(sat))

                returning = oldest[randint(0, len(oldest) - 1)]
                if(DEBUG and DEBUG_LEVEL >= 3):
                    print("Multiple oldest found, returning random one: " +
                          self._passAsStr(returning))
                return returning

        if(DEBUG and DEBUG_LEVEL >= 3):
            print("*** Returning first item in conflicts ***")
        return conflicting[0]

    # Looks for passes before the chosen one to fill the window
    def _fillBeforeChosen(self, conflicts, chosen):
        if(chosen in conflicts):
            del conflicts[conflicts.index(chosen)]

        conflicts.sort(key=lambda x: x.riseTime, reverse=False)

        startTime = conflicts[0].riseTime
        endTime = chosen.riseTime - CONFLICT_PADDING

        counter = 0
        for sat in conflicts:
            if(sat.riseTime > endTime):
                del conflicts[conflicts.index(sat)]
            counter += 1

        if(conflicts):
            bestFit = conflicts[0]
            bestTime = 0
            if(bestFit.setTime < endTime):
                bestTime = bestFit.setTime - bestFit.riseTime
            else:
                bestTime = endTime - bestFit.riseTime

            for sat in conflicts:
                satPeriod = 0
                if(sat.setTime < endTime):
                    satPeriod = sat.setTime - sat.riseTime
                else:
                    satPeriod = endTime - sat.riseTime

                if(satPeriod > bestTime):
                    bestTime = satPeriod
                    bestFit = sat

            if(bestTime > MIN_SUB_PASS_LEN):
                start = bestFit.riseTime
                end = bestFit.riseTime + bestTime
                duration = end - start

                return NextPass(tle=bestFit.tle, mission=bestFit.mission, riseTime=start, setTime=end, duration=duration,
                                    maxElevation=bestFit.maxElevation, riseAzimuth=bestFit.riseAzimuth, setAzimuth=bestFit.setAzimuth)
            else:
                if(DEBUG and DEBUG_LEVEL >= 2):
                    print("Nothing found before")
                return None
        else:
            if(DEBUG and DEBUG_LEVEL >= 2):
                print("Nothing found before")
            return None

    # Looks for passes after the chosen one to fill the window
    def _fillAfterChosen(self, conflicts, chosen):

        if(chosen in conflicts):
            del conflicts[conflicts.index(chosen)]

        conflicts.sort(key=lambda x: x.riseTime, reverse=False)

        startTime = chosen.setTime + CONFLICT_PADDING
        endTime = conflicts[len(conflicts) - 1].setTime

        counter = 0
        for sat in conflicts:
            if(sat.setTime > startTime):
                del conflicts[conflicts.index(sat)]
            counter += 1

        if(conflicts):
            bestFit = conflicts[0]
            bestTime = 0
            if(bestFit.riseTime > startTime):
                bestTime = bestFit.setTime - bestFit.riseTime
            else:
                bestTime = bestFit.setTime - startTime

            for sat in conflicts:
                satPeriod = 0
                if(bestFit.riseTime > startTime):
                    satPeriod = sat.setTime - sat.riseTime
                else:
                    satPeriod = sat.setTime - startTime

                if(satPeriod > bestTime):
                    bestTime = satPeriod
                    bestFit = sat

            if(bestTime > MIN_SUB_PASS_LEN):
                start = bestFit.setTime - bestTime
                end = bestFit.setTime
                duration = end - start

                return NextPass(tle=bestFit.tle, mission=bestFit.mission, riseTime=start, setTime=end, duration=duration,
                                    maxElevation=bestFit.maxElevation, riseAzimuth=bestFit.riseAzimuth, setAzimuth=bestFit.setAzimuth)
            else:
                if(DEBUG and DEBUG_LEVEL >= 2):
                    print("Nothing found after")
                return None
        else:
            if(DEBUG and DEBUG_LEVEL >= 2):
                print("Nothing found after")
            return None

    # Fills the conflict window with partial passes
    def _fillConflictWindow(self, conflicts, chosen):
        localSchedule = []
        localSchedule.append(chosen)

        satBefore = self._fillBeforeChosen(conflicts[:], chosen)
        if(satBefore is not None):
            localSchedule.append(satBefore)

        satAfter = self._fillAfterChosen(conflicts[:], chosen)
        if(satAfter is not None):
            localSchedule.append(satAfter)

        localSchedule.sort(key=lambda x: x.riseTime, reverse=False)

        return localSchedule

    # Returns a list of passes with no conflicts
    def find(self, missions, usefulTime):

        # Useful time not needed in rulebased, however kept for easy change to Hill Climber schedulers.

        passes = SchedulerHelper.getPassesFromMissions(self, missions)
        # Sort from earliest first
        passes.sort(key=lambda x: x.riseTime, reverse=False)

        if(DEBUG and DEBUG_LEVEL >= 2):
            print("Passes: " + str(len(passes)))
            print("Sorted list")
            for aPass in passes:
                print(self._passAsStr(aPass))

        if(DEBUG and DEBUG_LEVEL >= 1):
            print("")

        i = 0
        conflictsNum = 0

        # for each satellites
        while(i < len(passes)):
            j = i + 1
            # find time window of conflic
            conflicting = []
            periodStart = passes[i].riseTime
            periodEnd = passes[i].setTime + CONFLICT_PADDING

            while(j < len(passes)):
                # find all satellites which start in the time window.
                if(self._conflicts(periodStart, periodEnd, passes[j])):
                    conflicting.append(passes[j])
                    if(passes[j].setTime > periodEnd):
                        periodEnd = passes[j].setTime + CONFLICT_PADDING
                    j += 1
                else:
                    break
            # if any were found
            if(conflicting):
                conflicting.append(passes[i])
                conflicting.sort(key=lambda x: x.riseTime, reverse=False)

                if(DEBUG and DEBUG_LEVEL >= 2):
                    print("Conflicts")
                    for x in range(len(conflicting)):
                        print(self._passAsStr(conflicting[x]))
                    print("---------")

                # resolve the conflict
                nextPass = self._findNext(conflicting, periodStart, periodEnd)

                filledWindow = self._fillConflictWindow(conflicting, nextPass)
                #nextPass = findNextRandomly(conflicting)
                if(DEBUG and DEBUG_LEVEL >= 1):
                    for sat in filledWindow:
                        print("Added: " + self._passAsStr(sat) + " from conflict res.")
                # append to the order
                for sat in filledWindow:
                    orderOfPasses.append(sat)
                conflictsNum += 1
                # skip alland DEBUG_LEVEL >= 1 sats which were conflicting
                # change this to find conflicts from end of sat selected to end of
                # conflict window for sats > 4 mins
                i = j
            else:
                # no conflicts add and move on to next sat
                if(DEBUG and DEBUG_LEVEL >= 1):
                    print("Added: " + self._passAsStr(passes[i]))
                orderOfPasses.append(passes[i])

                i = i + 1

        if(DEBUG and DEBUG_LEVEL >= 1):
            print("Num of conflicts resolved: " + str(conflictsNum))

        return orderOfPasses
#
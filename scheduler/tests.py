from .services import Services, _Helper
from scheduler.TLEServices import TLE_Services
from scheduler.missionServices import mission_services
from .models import TLE, AzEl, NextPass, Mission
from django.test import TestCase
from datetime import date, datetime, timedelta
import ephem
# Create your tests here. 

class TLEServicesTests(TestCase):
    def test_FindById_is_correct(self):
        t1 = TLE(id = '0',
                name="EYESAT-1 (AO-27)",
                 line1="1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
                 line2="2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")

        t2 = TLE(name='TIANWANG 1A (TW-1A)',
                 line1='1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                 line2='2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858')

        t3 = TLE(name='SWISSCUBE',
                 line1='1 35932U 09051B   17012.34187112  .00000118  00000-0  37698-4 0  9992',
                 line2='2 35932  98.4726 148.2822 0007800  18.8768 341.2717 14.55942386387640')

        print(repr(t1))
        t1.save()
        t2.save()
        t3.save()
        
        tleEntry = TLE_Services.findTLEById(0)
        print(repr(shouldBe))
        """
        shouldBe = TLE(id = '0',"EYESAT-1 (AO-27)",
                "1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
                "2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")

        print(repr(shouldBe))

        tleEntry1 = TLE_Services.findTLEById(1)
        shouldBe1 = TLE('1',"TIANWANG 1A (TW-1A)",
                 "1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998",
                 "2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858")

        tleEntry2 = TLE_Services.findTLEById(2)
        shouldBe2 = TLE('2',"SWISSCUBE",
                 "1 35932U 09051B   17012.34187112  .00000118  00000-0  37698-4 0  9992",
                 "2 35932  98.4726 148.2822 0007800  18.8768 341.2717 14.55942386387640")
        """
        self.assertIs(tleEntry == (t1), True)
       #self.assertIs(tleEntry1 == (shouldBe1), True)
       #self.assertIs(tleEntry2 == (shouldBe2), True)

"""
    def test_FindByName_is_correct(self):

         t1 = TLE(name="EYESAT-1 (AO-27)",
                 line1="1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
                 line2="2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")

        t2 = TLE(name='TIANWANG 1A (TW-1A)',
                 line1='1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                 line2='2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858')
        t3 = TLE(name='SWISSCUBE',
                 line1='1 35932U 09051B   17012.34187112  .00000118  00000-0  37698-4 0  9992',
                 line2='2 35932  98.4726 148.2822 0007800  18.8768 341.2717 14.55942386387640')
        t1.save()
        t2.save()
        t3.save()
        tleEntry = TLE_Services.findTLEByName("NANOSATC-BR1")
        shouldBe = TLE(name ="NANOSATC-BR1",
                        line1 ='1 40024U 14033Q   17021.95106765  .00000421  00000-0  50647-4 0  9994',
                        line2 ='2 40024  97.9211 293.9798 0013770  65.7971 294.4683 14.89043048140788',)
        self.assertIs(tleEntry == (shouldBe), True)

    def test_saveTLE_is_correct(self):
        tleEntry = TLE_Services.findTLEByName("NANOSATC-BR1")
        shouldBe = TLE('45', "NANOSATC-BR1",
                        '1 40024U 14033Q   17021.95106765  .00000421  00000-0  50647-4 0  9994',
                        '2 40024  97.9211 293.9798 0013770  65.7971 294.4683 14.89043048140788',)
        self.assertIs(tleEntry == (shouldBe), True)

    def test_removeTLE_is_correct(self):
        tleEntry = TLE_Services.findTLEByName("NANOSATC-BR1")
        shouldBe = TLE('45', "NANOSATC-BR1",
                        '1 40024U 14033Q   17021.95106765  .00000421  00000-0  50647-4 0  9994',
                        '2 40024  97.9211 293.9798 0013770  65.7971 294.4683 14.89043048140788',)
        self.assertIs(tleEntry == (shouldBe), True)
"""
class pyephemTests(TestCase):
    def test_getazeldata_is_correct1(self):
        # test needs to be updated in roughly early 2018 to a newer time if datetime
        # is too far from the epoch of the satellite: 11/01/17
        tleEntry = TLE('0', 'EYESAT-1 (AO-27)',
                       '1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991',
                       '2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061', )
        # azel = Services.getAzElTLE(self, tleEntry ,datetime(2017,1,1,12,0,0))
        azel = Services.getAzElTLE(self, tleEntry, datetime(2017, 1, 1, 12, 0, 0))
        # degrees minutes seconds -> decimal degrees -> radians
        shouldBe = AzEl(0, 4.355794429779053, -1.4003942012786865)
        self.assertIs(shouldBe == (azel), True)

        # self.assertIs(shouldBe.elevation == azel.elevation,True)

    def test_getazeldata_is_correct2(self):
        # test needs to be updated in roughly early 2018 to a newer time if datetime
        # is too far from the epoch of the satellite: 17/01/17
        tleEntry = TLE('0', 'PROMETHEUS 2-3',
                       '1 41855U 16067H   17017.17439223 -.00000035  00000-0  22910-5 0  9998',
                       '2 41855  97.9660  92.6242 0012070  83.3470 276.9124 14.95885483  9917', )
        azel = Services.getAzElTLE(self, tleEntry, datetime(2017, 6, 6, 12, 0, 0))
        shouldBe = AzEl(0, 3.1872448921203613, -1.5055859088897705)
        self.assertIs(shouldBe == (azel), True)

    # self.assertIs(shouldBe.elevation == azel.elevation,True)

    def test_getazeldata_is_correct3(self):
        # test needs to be updated in roughly early 2018 to a newer time if datetime
        # is too far from the epoch of the satellite: 17/01/17
        tleEntry = TLE('0', 'PROMETHEUS 2-3',
                       '1 41855U 16067H   17017.17439223 -.00000035  00000-0  22910-5 0  9998',
                       '2 41855  97.9660  92.6242 0012070  83.3470 276.9124 14.95885483  9917', )
        azel = Services.getAzElTLE(self, tleEntry, datetime(2017, 6, 6, 12, 0, 0))
        shouldBe = AzEl(0, 3.18724345421203613, -1.5055834588897705)
        self.assertIs(shouldBe == azel, False)

    def test_getAzElForPeriod_is_correct(self):
        tleEntry = TLE('0', 'PROMETHEUS 2-3',
                       '1 41855U 16067H   17017.17439223 -.00000035  00000-0  22910-5 0  9998',
                       '2 41855  97.9660  92.6242 0012070  83.3470 276.9124 14.95885483  9917', )
        # tleEntry, riseTime, setTime, period in seconds
        azelList = Services.getAzElForPeriod(self, tleEntry, datetime(2017, 6, 6, 12, 2, 42),
                                             datetime(2017, 6, 6, 12, 9, 2), 30)
        shouldBe = []
        shouldBe.append(AzEl(0, 0.8919017910957336, -1.534958004951477))
        shouldBe.append(AzEl(0, 0.7173821926116943, -1.5194507837295532))
        shouldBe.append(AzEl(0, 0.6259355545043945, -1.5030969381332397))
        shouldBe.append(AzEl(0, 0.570842981338501, -1.4863852262496948))
        shouldBe.append(AzEl(0, 0.5344333648681641, -1.4694904088974))
        shouldBe.append(AzEl(0, 0.5087897181510925, -1.4524891376495361))
        shouldBe.append(AzEl(0, 0.4898819625377655, -1.4354195594787598))
        shouldBe.append(AzEl(0, 0.4754546880722046, -1.4183026552200317))
        shouldBe.append(AzEl(0, 0.46415090560913086, -1.4011510610580444))
        shouldBe.append(AzEl(0, 0.4551066756248474, -1.383972406387329))
        shouldBe.append(AzEl(0, 0.4477463364601135, -1.3667718172073364))
        shouldBe.append(AzEl(0, 0.4416716694831848, -1.3495526313781738))
        shouldBe.append(AzEl(0, 0.43659859895706177, -1.3323169946670532))
        self.assertIs(len(shouldBe) == len(azelList), True)

        for val in shouldBe:
            self.assertIs(val in azelList, True)

    def test_getAzElForPeriod_is_incorrect(self):
        tleEntry = TLE('0', 'PROMETHEUS 2-3',
                       '1 41855U 16067H   17017.17439223 -.00000035  00000-0  22910-5 0  9998',
                       '2 41855  97.9660  92.6242 0012070  83.3470 276.9124 14.95885483  9917', )
        # tleEntry, riseTime, setTime, period in seconds
        azelList = Services.getAzElForPeriod(self, tleEntry, datetime(2017, 6, 6, 12, 2, 42),
                                             datetime(2017, 6, 6, 12, 9, 2), 30)
        shouldBe = []
        shouldBe.append(AzEl(0, 0.8919017913454357336, -1.534958004951477))
        shouldBe.append(AzEl(0, 0.71738214353116943, -1.5194507837295532))
        shouldBe.append(AzEl(0, 0.6259355545043945, -1.5030969381332397))
        shouldBe.append(AzEl(0, 0.570842981338501, -1.4863852262496948))
        shouldBe.append(AzEl(0, 0.53443336486341641, -1.4694904088974))
        shouldBe.append(AzEl(0, 0.5087897181510925, -1.4524891376495361))
        shouldBe.append(AzEl(0, 0.48988196253745655, -1.4354195594787598))
        shouldBe.append(AzEl(0, 0.4754546880722046, -1.4183026552200317))
        shouldBe.append(AzEl(0, 0.46415090560913086, -1.4011510610580444))
        shouldBe.append(AzEl(0, 0.4551066756248474, -1.383972406387329))
        shouldBe.append(AzEl(0, 0.4477463364601135, -1.3667718172073364))
        shouldBe.append(AzEl(0, 0.4416716694831848, -1.3495526313781738))
        shouldBe.append(AzEl(0, 0.4365985989570617, -1.3323169946670532))

        self.assertIs(len(shouldBe) == len(azelList), True)

        badEntry = False
        for val in shouldBe:
            if val not in azelList:
                badEntry = True
        self.assertIs(badEntry, True)


    def test_makeNextPassDetails_is_correct(self):
        tleEntry = TLE('0', 'TIANWANG 1A (TW-1A)',
                       '1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                       '2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858', )
        dateTime = datetime(2017, 6, 6, 12, 0, 0)
        nextPass = Services.getNextPass(self, tleEntry, dateTime)

        # riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth
        riseTime = datetime(2017, 6, 6, 16, 21, 24)
        setTime = datetime(2017, 6, 6, 16, 24, 22)
        duration = timedelta(0, 178)
        maxElevation = 0.01104038581252098
        riseAzimuth = 0.8570818901062012
        setAzimuth = 0.3221415579319

        shouldBe = NextPass(0, riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth)

        self.assertIs(shouldBe == nextPass, True)


    def passtest_makeNextPassDetails_is_incorrect(self):
        tleEntry = TLE('0', 'TIANWANG 1A (TW-1A)',
                       '1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                       '2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858', )
        dateTime = datetime(2017, 6, 6, 12, 0, 0)
        nextPass = Services.getNextPass(self, tleEntry, dateTime)

        # riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth
        riseTime = datetime(2017, 6, 6, 16, 21, 24)
        setTime = datetime(2017, 8, 6, 16, 24, 22)
        duration = timedelta(0, 178)
        maxElevation = 0.05104038581252098
        riseAzimuth = 0.8570818901062012
        setAzimuth = 0.3221415579319

        shouldBe = NextPass(0, riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth)

        self.assertIs(shouldBe.riseAzimuth == nextPass.riseAzimuth, False)


class HelperMethodsTests(TestCase):
    def test_datespan_is_correct(self):
        timestamp = _Helper.timeSpan(datetime(2017, 6, 6, 12, 2, 42), datetime(2017, 6, 6, 12, 9, 42), 31)

        # look further into testing   get a mocker involved?

    def test_roundMicrosecond_is_correct(self):
        dt = ephem.Date('2017/6/6 12:02:42.345345')
        roundedMicrosecond = _Helper.roundMicrosecond(dt)
        shouldBe = datetime(2017, 6, 6, 12, 2, 42)
        self.assertIs(shouldBe == roundedMicrosecond, True)


class UpdateTLETests(TestCase):
    # data gets pulled in from website, check first few entries are sane? requests job?
    # gets parsed
    # put in db 	#gets taken out

    def test_data_from_celestrak_is_valid(self):
        tleArray = [
            'EYESAT-1 (AO-27)',
            '1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991',
            '2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061',
            'CUTE-1 (CO-55)',
            '1 27844U 03031E   17012.57520683  .00000056  00000-0  44979-4 0  9997',
            '2 27844  98.6913  23.8380 0010757  79.0163 281.2224 14.22008047702203',
            'CUBESAT XI-IV (CO-57)',
            '1 27848U 03031J   17011.75882937  .00000044  00000-0  39844-4 0  9995',
            '2 27848  98.7007  23.2239 0010701  89.1852 271.0552 14.21626517701976',
            'mostwrong',
            '1 wowsowrong1231',
            '2 couldi34v beanym34orew2 3rong',
            'M-CUBED & EXP-1 PRIME',
            '1 37855U 11061F   17011.86088514  .00001922  00000-0  10927-3 0  9993',
            '2 37855 101.7157 163.8757 0183039 182.8914 177.1254 15.02379487283316',
            'SWISSCUBE',
            '1 35932U 09051B   17012.34187112  .00000118  00000-0  37698-4 0  9992',
            '2 35932  98.4726 148.2822 0007800  18.8768 341.2717 14.55942386387640',
            'TIANWANG 1A (TW-1A)',
            '1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
            '2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858',
            'madeupsat',
            '1 41895U 98067KR   7012.47827931  .00011364  00000-0  17301-3 0  9999',
            '2 41895  51.6434  94.4040 0005661  96.0874 264.0617 15.55009568  3716',
            'madeupsat1',
            '1 41895U 98067KR    012.47827931  .00011364  00000-0  17301-3 0  9999',
            '2 41895  51.6434  94.4040 0005661  96.0874 264.0617 15.55009568  3716',
            'madeupsat2',
            '1 41895U 98067KR     12.47827931  .00011364  00000-0  17301-3 0  9999',
            '2 41895  51.6434  94.4040 0005661  96.0874 264.0617 15.55009568  3716',
            'madeupsat3',
            '1 41895U 98067KR     2.47827931  .00011364  00000-0  17301-3 0  9999',
            '2 41895  51.6434  94.4040 0005661  96.0874 264.0617 15.55009568  3716',
            'madeupsat4',
            '1 41895U 98067KR     2.47827931  .00011364  00000-0  17301-3 0  9999',
            '2 41895  51.6434  04.4040 0005661  96.0874 264.0617 15.55009568  3716',
            'madeupsat5',
            '1 41895U 98067KR     2.47827931  .00011364  00000-0  17301-3 0  9999',
            '2 41895  51.6434  4.4040 0005661  96.0874 264.0617 15.55009568  3716', ]

        checkedArray = _Helper.checkTLEFormat(tleArray)
        # print(checkedArray)
        shouldBe = [
            'EYESAT-1 (AO-27)',
            '1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991',
            '2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061',
            'CUTE-1 (CO-55)',
            '1 27844U 03031E   17012.57520683  .00000056  00000-0  44979-4 0  9997',
            '2 27844  98.6913  23.8380 0010757  79.0163 281.2224 14.22008047702203',
            'CUBESAT XI-IV (CO-57)',
            '1 27848U 03031J   17011.75882937  .00000044  00000-0  39844-4 0  9995',
            '2 27848  98.7007  23.2239 0010701  89.1852 271.0552 14.21626517701976',
            'M-CUBED & EXP-1 PRIME',
            '1 37855U 11061F   17011.86088514  .00001922  00000-0  10927-3 0  9993',
            '2 37855 101.7157 163.8757 0183039 182.8914 177.1254 15.02379487283316',
            'SWISSCUBE',
            '1 35932U 09051B   17012.34187112  .00000118  00000-0  37698-4 0  9992',
            '2 35932  98.4726 148.2822 0007800  18.8768 341.2717 14.55942386387640',
            'TIANWANG 1A (TW-1A)',
            '1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
            '2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858',
        ]

        self.assertIs(shouldBe == checkedArray, True)


class missionTests(TestCase):

    def test_findMissionById1(self):
        t1 = TLE(name="EYESAT-1 (AO-27)",
                 line1="1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
                 line2="2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")

        t2 = TLE(name='TIANWANG 1A (TW-1A)',
                 line1='1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                 line2='2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858')

        t1.save()
        t2.save()
        mission1 = Mission(id=1, name="Mission1", TLE=t1, status="Finished", priority=3, max_num_passes=3,
                           current_num_passes=1)
        mission2 = Mission(id=2, name="Mission2", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=2)
        mission3 = Mission(id=3, name="Mission3", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=3)
        mission1.save()
        mission2.save()
        mission3.save()

        testValue0 = mission_services.findMissionById(0)
        self.assertIs(testValue0 == mission1, False)
        self.assertIs(testValue0 == mission2, False)
        self.assertIs(testValue0 == mission3, False)

        testValue1 = mission_services.findMissionById(1)
        self.assertIs(testValue1 == mission1, True)
        self.assertIs(testValue1 == mission2, False)
        self.assertIs(testValue1 == mission3, False)

        testValue2 = mission_services.findMissionById(2)
        self.assertIs(testValue2 == mission1, False)
        self.assertIs(testValue2 == mission2, True)
        self.assertIs(testValue2 == mission3, False)

        testValue3 = mission_services.findMissionById(3)
        self.assertIs(testValue3 == mission1, False)
        self.assertIs(testValue3 == mission2, False)
        self.assertIs(testValue3 == mission3, True)


    def test_findMissionByName(self):
        t1 = TLE(name="EYESAT-1 (AO-27)",
                 line1="1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
                 line2="2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")
        t2 = TLE(name='TIANWANG 1A (TW-1A)',
                 line1='1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                 line2='2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858')
        t1.save()
        t2.save()
        mission1 = Mission(id=1, name="Mission1", TLE=t1, status="Finished", priority=3, max_num_passes=3,
                           current_num_passes=1)
        mission2 = Mission(id=2, name="Mission2", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=2)
        mission3 = Mission(id=3, name="Mission3", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=3)
        mission1.save()
        mission2.save()
        mission3.save()

        testValue0 = mission_services.findMissionByName('Mission0')
        self.assertIs(testValue0 == mission1, False)
        self.assertIs(testValue0 == mission2, False)
        self.assertIs(testValue0 == mission3, False)

        testValue1 = mission_services.findMissionByName('Mission1')
        self.assertIs(testValue1 == mission1, True)
        self.assertIs(testValue1 == mission2, False)
        self.assertIs(testValue1 == mission3, False)

        testValue2 = mission_services.findMissionByName('Mission2')
        self.assertIs(testValue2 == mission1, False)
        self.assertIs(testValue2 == mission2, True)
        self.assertIs(testValue2 == mission3, False)

        testValue3 = mission_services.findMissionByName('Mission3')
        self.assertIs(testValue3 == mission1, False)
        self.assertIs(testValue3 == mission2, False)
        self.assertIs(testValue3 == mission3, True)


    def test_findMissionsByTLE(self):
        t1 = TLE(name="EYESAT-1 (AO-27)",
                 line1="1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
                 line2="2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")

        t2 = TLE(name='TIANWANG 1A (TW-1A)',
                 line1='1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                 line2='2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858')
        t3 = TLE(name='SWISSCUBE',
                 line1='1 35932U 09051B   17012.34187112  .00000118  00000-0  37698-4 0  9992',
                 line2='2 35932  98.4726 148.2822 0007800  18.8768 341.2717 14.55942386387640')
        t1.save()
        t2.save()
        t3.save()
        mission1 = Mission(id=1, name="Mission1", TLE=t1, status="Finished", priority=3, max_num_passes=3,
                           current_num_passes=1)
        mission2 = Mission(id=2, name="Mission2", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=2)
        mission3 = Mission(id=3, name="Mission3", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=3)
        mission1.save()
        mission2.save()
        mission3.save()

        testValue1 = mission_services.findMissionsByTLE(t1)
        self.assertIs(mission1 in testValue1, True)
        self.assertIs(mission2 in testValue1, False)
        self.assertIs(mission3 in testValue1, False)

        testValue2 = mission_services.findMissionsByTLE(t2)
        self.assertIs(mission1 in testValue2, False)
        self.assertIs(mission2 in testValue2, True)
        self.assertIs(mission3 in testValue2, True)

        testValue3 = mission_services.findMissionsByTLE(t3)
        self.assertIs(mission1 in testValue3, False)
        self.assertIs(mission2 in testValue3, False)
        self.assertIs(mission3 in testValue3, False)


    def test_findMissionsByStatus(self):
        t1 = TLE(name="EYESAT-1 (AO-27)", line1="1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
                 line2="2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")

        t2 = TLE(name='TIANWANG 1A (TW-1A)',
                 line1='1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                 line2='2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858')
        t1.save()
        t2.save()
        mission1 = Mission(id=1, name="Mission1", TLE=t1, status="Finished", priority=3, max_num_passes=3,
                           current_num_passes=1)
        mission2 = Mission(id=2, name="Mission2", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=2)
        mission3 = Mission(id=3, name="Mission3", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=3)
        mission1.save()
        mission2.save()
        mission3.save()

        testValue1 = mission_services.findMissionsByStatus('Finished')
        self.assertIs(mission1 in testValue1, True)
        self.assertIs(mission2 in testValue1, False)
        self.assertIs(mission3 in testValue1, False)

        testValue2 = mission_services.findMissionsByStatus('Tracked')
        self.assertIs(mission1 in testValue2, False)
        self.assertIs(mission2 in testValue2, True)
        self.assertIs(mission3 in testValue2, True)

        testValue3 = mission_services.findMissionsByStatus('Pending')
        self.assertIs(mission1 in testValue3, False)
        self.assertIs(mission2 in testValue3, False)
        self.assertIs(mission3 in testValue3, False)


    def test_findMissionsByPriority(self):
        t1 = TLE(name="EYESAT-1 (AO-27)",
                 line1="1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
                 line2="2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")

        t2 = TLE(name='TIANWANG 1A (TW-1A)',
                 line1='1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                 line2='2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858')
        t1.save()
        t2.save()
        mission1 = Mission(id=1, name="Mission1", TLE=t1, status="Finished", priority=3, max_num_passes=3,
                           current_num_passes=1)
        mission2 = Mission(id=2, name="Mission2", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=2)
        mission3 = Mission(id=3, name="Mission3", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=3)
        mission1.save()
        mission2.save()
        mission3.save()

        testValue1 = mission_services.findMissionsByPriority(1)
        self.assertIs(mission1 in testValue1, False)
        self.assertIs(mission2 in testValue1, True)
        self.assertIs(mission3 in testValue1, True)

        testValue2 = mission_services.findMissionsByPriority(2)
        self.assertIs(mission1 in testValue2, False)
        self.assertIs(mission2 in testValue2, False)
        self.assertIs(mission3 in testValue2, False)

        testValue3 = mission_services.findMissionsByPriority(3)
        self.assertIs(mission1 in testValue3, True)
        self.assertIs(mission2 in testValue3, False)
        self.assertIs(mission3 in testValue3, False)


    def test_findMissionsByCurrentNumberOfPasses(self):
        t1 = TLE(name="EYESAT-1 (AO-27)",
                 line1="1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
                 line2="2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")

        t2 = TLE(name='TIANWANG 1A (TW-1A)',
                 line1='1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                 line2='2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858')
        t1.save()
        t2.save()
        mission1 = Mission(id=1, name="Mission1", TLE=t1, status="Finished", priority=3, max_num_passes=3,
                           current_num_passes=1)
        mission2 = Mission(id=2, name="Mission2", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=2)
        mission3 = Mission(id=3, name="Mission3", TLE=t2, status="Tracked", priority=1, max_num_passes=3,
                           current_num_passes=3)
        mission1.save()
        mission2.save()
        mission3.save()

        testValue0 = mission_services.findMissionsByCurrentNumberOfPasses(0)
        self.assertIs(mission1 in testValue0, False)
        self.assertIs(mission2 in testValue0, False)
        self.assertIs(mission3 in testValue0, False)

        testValue1 = mission_services.findMissionsByCurrentNumberOfPasses(1)
        self.assertIs(mission1 in testValue1, True)
        self.assertIs(mission2 in testValue1, False)
        self.assertIs(mission3 in testValue1, False)

        testValue2 = mission_services.findMissionsByCurrentNumberOfPasses(2)
        self.assertIs(mission1 in testValue2, False)
        self.assertIs(mission2 in testValue2, True)
        self.assertIs(mission3 in testValue2, False)

        testValue3 = mission_services.findMissionsByCurrentNumberOfPasses(3)
        self.assertIs(mission1 in testValue3, False)
        self.assertIs(mission2 in testValue3, False)
        self.assertIs(mission3 in testValue3, True)


    def test_findMissionsByMaxNumberOfPasses(self):
        t1 = TLE(name="EYESAT-1 (AO-27)",
                 line1="1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
                 line2="2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")

        t2 = TLE(name='TIANWANG 1A (TW-1A)',
                 line1='1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                 line2='2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858')
        t1.save()
        t2.save()
        mission1 = Mission(id=1, name="Mission1", TLE=t1, status="Finished", priority=3, max_num_passes=3,
                           current_num_passes=1)
        mission2 = Mission(id=2, name="Mission2", TLE=t2, status="Tracked", priority=1, max_num_passes=2,
                           current_num_passes=2)
        mission3 = Mission(id=3, name="Mission3", TLE=t2, status="Tracked", priority=1, max_num_passes=4,
                           current_num_passes=3)
        mission1.save()
        mission2.save()
        mission3.save()

        testValue1 = mission_services.findMissionsByMaxNumberOfPasses(1)
        self.assertIs(mission1 in testValue1, False)
        self.assertIs(mission2 in testValue1, False)
        self.assertIs(mission3 in testValue1, False)

        testValue2 = mission_services.findMissionsByMaxNumberOfPasses(2)
        self.assertIs(mission1 in testValue2, False)
        self.assertIs(mission2 in testValue2, True)
        self.assertIs(mission3 in testValue2, False)

        testValue3 = mission_services.findMissionsByMaxNumberOfPasses(3)
        self.assertIs(mission1 in testValue3, True)
        self.assertIs(mission2 in testValue3, False)
        self.assertIs(mission3 in testValue3, False)

        testValue4 = mission_services.findMissionsByMaxNumberOfPasses(4)
        self.assertIs(mission1 in testValue4, False)
        self.assertIs(mission2 in testValue4, False)
        self.assertIs(mission3 in testValue4, True)

    def test_removeMissionByName(self):
        t1 = TLE(name="EYESAT-1 (AO-27)",
                 line1="1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
                 line2="2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")

        t2 = TLE(name='TIANWANG 1A (TW-1A)',
                 line1='1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
                 line2='2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858')
        t1.save()
        t2.save()
        mission1 = Mission(id=1, name="Mission1", TLE=t1, status="Finished", priority=3, max_num_passes=3,
                           current_num_passes=1)
        mission2 = Mission(id=2, name="Mission2", TLE=t2, status="Tracked", priority=1, max_num_passes=2,
                           current_num_passes=2)
        mission3 = Mission(id=3, name="Mission3", TLE=t2, status="Tracked", priority=1, max_num_passes=4,
                           current_num_passes=3)
        mission1.save()
        mission2.save()
        mission3.save()

        self.assertIs(mission1 == mission_services.findMissionByName('Mission1'), True)

        mission_services.removeMissionByName("Mission1")
        self.assertIs(mission_services.findMissionByName('Mission1') == mission1, False)


    # def test_SaveOrUpdate(self):
    #     t1 = TLE(name="EYESAT-1 (AO-27)",
    #              line1="1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991",
    #              line2="2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061")
    #
    #     t2 = TLE(name='TIANWANG 1A (TW-1A)',
    #              line1='1 40928U 15051D   17012.78841078  .00002327  00000-0  71003-4 0  9998',
    #              line2='2 40928  97.2476  51.3649 0014522  42.3053  46.5607 15.34836540 72858')
    #     t1.save()
    #     t2.save()
    #     mission1 = Mission(id=1, name="Mission1", TLE=t1, status="Finished", priority=3, max_num_passes=3,
    #                        current_num_passes=1)
    #     mission2 = Mission(id=2, name="Mission2", TLE=t2, status="Tracked", priority=1, max_num_passes=2,
    #                        current_num_passes=2)
    #     mission3 = Mission(id=3, name="Mission3", TLE=t2, status="Tracked", priority=1, max_num_passes=4,
    #                        current_num_passes=3)
    #     mission1.save()
    #     mission2.save()
    #     mission3.save()
    #
    #     Services.removeMissionByName("Mission1")
    #     self.assertIs(Services.findMissionByName('Mission1') == mission1, False)
    #     Services.saveOrUpdate(mission1)
    #     self.assertIs(Services.findMissionByName('Mission1') == mission1, True)
    #     mission1 = Mission(id=1, name="Mission_1", TLE=t1, status="Finished", priority=3, max_num_passes=3,
    #                        current_num_passes=1)
    #     Services.saveOrUpdate(mission1)
    #     self.assertIs(Services.findMissionByName('Mission1') == mission1, False)
    #     self.assertIs(Services.findMissionByName('Mission_1') == mission1, True)












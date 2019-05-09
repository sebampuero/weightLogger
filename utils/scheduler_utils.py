import schedule
from common.database import Database
from utils.email_utils import Emailer
from utils.led_utils import Led
import datetime
import time


class SchedulerUtils(object):

    @staticmethod
    def weight_was_not_logged():
        if Database.getLastEntry() is not None:
            last_entry_id, last_entry_ts = Database.getLastEntry()
            if datetime.datetime.fromtimestamp(float(last_entry_ts)).strftime('%j') != datetime.datetime.fromtimestamp(float(time.time())).strftime('%j'):
                #Emailer.send_email()
                return True
            else:
                return False
        else:
            return False


    @staticmethod
    def init_schedule():
        print("Scheduler has started")
        #schedule.every().day.at("8:00").do(SchedulerUtils.check_if_weight_was_not_logged)
        #schedule.every().day.at("10:00").do(SchedulerUtils.check_if_weight_was_not_logged)
        #schedule.every().day.at("14:00").do(SchedulerUtils.check_if_weight_was_not_logged)
        #schedule.every().day.at("18:00").do(SchedulerUtils.check_if_weight_was_not_logged)
        #run in another thread
        led = Led()
        while True:
            if int(datetime.datetime.fromtimestamp(time.time()).strftime('%H')) > 6:
                if SchedulerUtils.weight_was_not_logged():
                    for i in range(0,60):
                        led.turnOnLed()
                        time.sleep(1)
                        led.turnOffLed()
                        time.sleep(1)
                else:
                    pass
            #schedule.run_pending()
            time.sleep(30)

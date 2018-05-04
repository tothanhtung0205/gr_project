# -*- coding=utf-8 -*-
# author = "tungtt"

import schedule
import time

def job():
    print("I'm working...")

schedule.every(1).seconds.do(job)
schedule.every().day.at("11:37").do(job)
schedule.run_pending()

while(1):
    schedule.run_pending()


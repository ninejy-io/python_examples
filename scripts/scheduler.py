import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

# add job
def my_job():
    print(time.time())

scheduler = BlockingScheduler()  # 阻塞
# scheduler = BackgroundScheduler()  # 非阻塞

# scheduler.add_job(my_job, 'interval', seconds=2)
# scheduler.start()
'''
scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', seconds=3)
def my_job():
    print(time.time())

scheduler.start()
'''

'''
# remove job
job = scheduler.add_job(my_job, 'interval', seconds=1)
job.remove()

scheduler.add_job(my_job, 'interval', seconds=2, id='my_job_id')
scheduler.remove_job('my_job_id')
'''

'''
# pause/resume job
scheduler.pause()
scheduler.pause_job()

scheduler.resume()
scheduler.resume_job()
'''

'''
# get job list
scheduler.add_job(my_job, 'interval', seconds=2, id='123')
print(scheduler.get_job(job_id='123'))
print(scheduler.get_jobs())
'''

'''
# shutdown scheduler
scheduler.shutdown()
scheduler.shutdown(wait=False)
'''


scheduler.add_job(my_job, 'cron', year=2018, month=3, day=13, hour=13, minute=50, second=3)
scheduler.add_job(my_job, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
scheduler.add_job(my_job, 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2018-03-23')
scheduler.add_job(my_job, 'cron', second='*/5')

scheduler.add_job(my_job, 'interval', days=3, hours=17, minutes=23, seconds=27)

from datetime import date, datetime
def my_job2(text):
    print(text)
scheduler.add_job(my_job, 'date', run_date=date(2018, 3, 15), args=['text'])
scheduler.add_job(my_job, 'date', run_date=datetime(2018, 3, 15, 10, 20, 10), args=['text'])
scheduler.start()

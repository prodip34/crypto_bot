import schedule
import time
import subprocess

def job():
    subprocess.run(["python", "bot.py"])

schedule.every(3).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
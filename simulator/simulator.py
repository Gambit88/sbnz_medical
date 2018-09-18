import requests
import time
import random

patientId = 2

for i in range(0,15):
    print("waiting")
    time.sleep(10)
    print("sending")
    r = requests.post('http://localhost:8000/monitoring/'+str(patientId)+'/',
    data = {'heartratebeat':random.randint(50,90),'oxygenlevel':random.randint(60,100),'liquidlevel':random.randint(0,50)})
    print("sent")
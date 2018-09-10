import requests
import time
import random

patientId = 4

for i in range(0,15):
    time.sleep(120)
    r = requests.post('http://localhost:8000/monitoring/'+patientId+'/',
    data = {'heartratebeat':random.randint(50,90),'oxygenlevel':random.randint(60,100),'liquidlevel':random.randint(0,50)})
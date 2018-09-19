import requests
import time
import random

patientId = 2

def sim1():
	for i in range(0,15):
		print("Waiting...")
		time.sleep(10)
		hb = random.randint(50,160)
		ol = random.randint(60,100)
		ll = random.randint(0,50)
		print("Sending:")
		print("Heartbeat(per minute): "+str(hb)+" Oxygen: "+str(ol)+" Liquid: "+str(ll))
		r = requests.post('http://localhost:8000/monitoring/'+str(patientId)+'/',
		data = {'heartratebeat':hb,'oxygenlevel':ol,'liquidlevel':ll})
		print("Sent!")
		
def sim2():
	print("Waiting...")
	time.sleep(10)
	hb = 160
	ol = 50
	ll = 10
	print("Sending:")
	print("Heartbeat(per minute): "+str(hb)+" Oxygen: "+str(ol)+" Liquid: "+str(ll))
	r = requests.post('http://localhost:8000/monitoring/'+str(patientId)+'/',
	data = {'heartratebeat':hb,'oxygenlevel':ol,'liquidlevel':ll})
	print("Sent!")
	print("Waiting...")
	time.sleep(10)
	hb = 165
	ol = 49
	ll = 0
	print("Sending:")
	print("Heartbeat(per minute): "+str(hb)+" Oxygen: "+str(ol)+" Liquid: "+str(ll))
	r = requests.post('http://localhost:8000/monitoring/'+str(patientId)+'/',
	data = {'heartratebeat':hb,'oxygenlevel':ol,'liquidlevel':ll})
	print("Sent!")
	print("Waiting...")
	time.sleep(10)
	hb = 150
	ol = 55
	ll = 0
	print("Sending:")
	print("Heartbeat(per minute): "+str(hb)+" Oxygen: "+str(ol)+" Liquid: "+str(ll))
	r = requests.post('http://localhost:8000/monitoring/'+str(patientId)+'/',
	data = {'heartratebeat':hb,'oxygenlevel':ol,'liquidlevel':ll})
	print("Sent!")
	
sim2()
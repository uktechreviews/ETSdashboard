#!/usr/bin/env python

import time
import fourletterphat
from gpiozero import LED
from gpiozero import Button
import os
from time import sleep
import json
import subprocess

b1 =Button(25)
b2 =Button(12)
b3 =Button(23)
#b4 =Button(12)
b5 =Button(7)
b6 =Button(8)

led1 = LED(21)
led2 = LED(20)
led3 = LED(16)
led4 = LED(19)
#led5 = LED(26)
led6 = LED(18)
led7 = LED(15)
led8 = LED(14)
led9 = LED(6)
led10 = LED(13)
led11 = LED(5)
led12 = LED(11)
led13 = LED(9)
led14 = LED(10)
led15 = LED(22)
led16 = LED(27)
led17 = LED(17)
led18 = LED(4)

subprocess.run(["rm", "telemetry"])

def test_leds_on():
	led1.on()
	led2.on()
	led3.on()
	led4.on()
#	led5.on()
	led6.on()
	led7.on()
	led8.on()
	led9.on()
	led10.on()
	led11.on()
	led12.on()
	led13.on()
	led14.on()
	led15.on()
	led16.on()
	led17.on()
	led18.on()

def test_leds_off():
	led1.off()
	led2.off()
	led3.off()
	led4.off()
#	led5.off()
	led6.off()
	led7.off()
	led8.off()
	led9.off()
	led10.off()
	led11.off()
	led12.off()
	led13.off()
	led14.off()
	led15.off()
	led16.off()
	led17.off()
	led18.off()

clock = False
game = False
link = False

print ("Checking LEDs")
fourletterphat.print_str("****")
fourletterphat.show()
test_leds_on()
sleep(1)
test_leds_off()
fourletterphat.clear()

while True:
	led15.off()
	if clock == False and game == False:
		fourletterphat.clear()
		fourletterphat.show()
		led14.on()
		sleep(0.5)
		led14.off()
		sleep(0.5)

	if b1.is_pressed:
		led14.off()
		clock = True
		if game != False:
			game = False
		fourletterphat.clear()
		str_time = time.strftime("%H%M")
		fourletterphat.print_number_str(str_time)
		fourletterphat.set_decimal(1, int(time.time() % 2))
		fourletterphat.show()
	else:
		clock = False
	if b2.is_pressed:
		test_leds_on()
	else:
		test_leds_off()
	if b3.is_pressed:
		led14.off()
		if link !=True:
			led9.on()
		else:
			led9.off()
		print(clock)
		if clock != True:
			game = True
			led10.on()
		if game !=False:
			subprocess.run(["rm", "telemetry"])
			subprocess.run(["wget", "http://192.168.0.43:25555/api/ets2/telemetry","--timeout=5","--tries=1"])
			try:
				f = open('telemetry')
			except FileNotFoundError:
				print ("No connection to server - will keep trying while in game mode")
				fourletterphat.print_str("DATA")
				fourletterphat.show()
				link = False
				continue
			link = True
			data = json.load(f)
			speed = int(data['truck']['speed'])
			print(speed)
			if speed == 0:
				speed_display = "STOP"
			if speed >0:
				speed_display = str(speed)
			if speed <0:
				speed_display = str(speed)
				speed_display = (speed_display[1:])
				speed_display = ("R"+ speed_display)
			fourletterphat.print_str(speed_display)
			fourletterphat.show()
			engine_status = data['truck']['engineOn']
			electric_status = data['truck']['electricOn']
			wipers = data['truck']['wipersOn']
			oil = data['truck']['oilPressureWarningOn']
			water = data['truck']['waterTemperatureWarningOn']
			battery = data['truck']['batteryVoltageWarningOn']
			lights_high = data['truck']['lightsBeamHighOn']
			lights_low = data['truck']['lightsBeamLowOn']
			if wipers == True:
				led15.on()
			#else:
	#			led15.off()
			if lights_low == True:
				led16.on()
				if lights_high == True:
					led17.on()
				else:
					led17.off()
			else:
				led16.off()
			if engine_status == True:
				led1.on()
			else:
				led1.off()
			if electric_status == True:
				led2.on()
			else:
				led2.off()
			if oil == True or water == True or battery == True:
				led8.on()
			else:
				led8.off()
			if oil == True:
				led4.on()
			else:
				led4.off()
			if water == True:
				led3.on()
			else:
				led3.off()
			cruise = data['truck']['cruiseControlOn']
			print ("cruise " + str(cruise))
			if cruise == True:
				led7.on()
			else:
				led7.off()
			sleep(0.5)
	else:
		game = False

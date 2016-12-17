from utime import sleep_ms
import machine


# -- Configuration -- #
# Selected pin to send out the pwm signal
SIGNAL_PIN = machine.Pin(5, machine.Pin.OUT)
# Global signal pwm object, duty cycle is set later
signal = machine.PWM(SIGNAL_PIN, freq=1000, duty = 0)


# -- Functions -- #
# Clipping function for 'exp', and 'lin'
def clip(value, a, b):
	# returns the value clipped to a and b
	# clip( 11, 0, 10 ) 	returns 10
	# clip( 5, 1, 8 )		returns 5
	# clip( -1.0, 0, 5.7 )	returns 0
	# etc...
	if value < a:
		return a
	elif value > b:
		return b
	else:
		return value

# Exponential setting
def exp(pct):
	# Human perception is usually logarithmic,
	# In this case we can better differentiate if the intensity
	# is low. This sets an exponential function on the logarithmic one
	# thus the perception will be kind of linear. "kind of" is good enough here
	# returned value is in the range of 1-1024
	pct = clip(pct, 0, 100)
	
	duty = round(2**(pct/10))
	return duty
	
# Linear setting
def lin(pct):
	# returns intensity value linearly
	# returned value is in the range of 1-1024
	pct = clip(pct, 0, 100)
	
	duty = round(pct*(1024/100))
	return duty
	
# Fade in -  Fade out animation
def fade(func, intensity, ms):
	# Intensity form is:
	# 		- [0,x] in case of static
	# 		- [y, x] in case of other animation
 	d=-intensity[1]
	while True:
		if d > intensity[1]:
			d=-intensity[1]
		elif abs(d) < intensity[0]:
			d = intensity[0]
		signal.duty(func(abs(d)))
		d = d + 1
		
		# Set delay so that every animation lasts the same time
		sleep_ms(round(ms/(intensity[1] - intensity[0]))) 
		
# Blinking animation
def blink(func, intensity, ms):
	# Uses MIN and MAX from the intensity to pulse between them
	rms = round(ms/2)
	while True:
		signal.duty(func(intensity[1]))
		sleep_ms(rms)
		signal.duty(func(intensity[0]))
		sleep_ms(rms)

# Static animation
def static(func, intensity, ms):
	# Calls the function 'func' with intensity 'intensity'
	signal.duty(func(intensity[1]))
	
#============================================================
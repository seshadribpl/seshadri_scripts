import pyowm
owm = pyowm.OWM('cc09309e3b53bd99266d9e712fc709f5')
reg = owm.city_id_registry()
obs = owm.weather_at_id(1269843)

w = obs.get_weather()
print w

rain = w.get_rain()
humidity = w.get_humidity()
temperature = w.get_temperature

print w.get_sunrise_time('iso')

fc = owm.three_hours_forecast('Hyderabad,IN')
f = fc.get_forecast()

print len(f)
for item in f:
	print item

lst = f.get_weathers()
fc.will_have_rain()
from pyowm import OWM

# Cache provider to be used
from pyowm.caches.lrucache import LRUCache
cache = LRUCache()

owm = OWM('cc09309e3b53bd99266d9e712fc709f5')
reg = owm.city_id_registry()
obs = owm.weather_at_id(1269843)


print obs.get_reception_time(timeformat='iso')

w = obs.get_weather()

if w.get_rain():
    print 'it is going to rain'
else:
    print 'no rain'


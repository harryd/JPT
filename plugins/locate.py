#!/usr/bin/python

import GeoIP
import re
import socket
import sys
from irc.commands import commandHandler

def get_ip(hostmask):
	if re.search(r'[0-9]+(?:\.[0-9]+){3}', hostmask) != None:
		ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', hostmask)[0]
	else:
		ip = socket.gethostbyname(hostmask)
	return ip

def host2country(host):
	try:
		ip = get_ip(host)
	except:
		return ['Cant get IP from host: %s' % host, False]
	else:
		gi = GeoIP.open("/usr/share/GeoIP/GeoLiteCity.dat",GeoIP.GEOIP_STANDARD)
		gir = gi.record_by_addr(ip)
		#gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
		#loc = gi.country_name_by_addr(ip)
		
		if gir == None:
			return ['Unknown location for ip: %s' % ip, False]
		else:
			return ['%s, %s, %s' % (gir['city'],gir['region_name'], gir['country_name']), True]


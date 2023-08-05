#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import requests
import json
import logging

__version__ = '0.0.1'
_LOGGER = logging.getLogger(__name__)

class Mower(object):

	def __init__(self, host, pin):
		self.host = host
		self.pin = pin
		self.state = ""
		self.battery = ""
		self.error = ""
		_LOGGER.debug('Host: <%s>, PIN: <%s>', host, pin)

	def parseError(self, errorArray):
		_LOGGER.debug(errorArray)
		if errorArray[0]:
			return 'blade blocked'
		elif errorArray[1]:
			return 'repositioning error'
		elif errorArray[3]:
			return 'blade blocked'
		elif errorArray[4]:
			return 'outside wire stopped'
		elif errorArray[5]:
			return 'mower lifted'
		elif errorArray[6]:
			return 'unspecified error'
		elif errorArray[7]:
			return 'unspecified error'
		elif errorArray[8]:
			return 'unspecified error'
		elif errorArray[9]:
			return 'collision sensor blocked'
		elif errorArray[10]:
			return 'mower tilted'
		elif errorArray[11]:
			return 'charge error'
		elif errorArray[12]:
			return 'battery error'
		else:
			return 'none'


	def parseStatus(self, statusArray):
		_LOGGER.debug(statusArray)
		if (statusArray[5] == 1) and (statusArray[13] == 0):
			return 'charging'		
		if (statusArray[5] == 1) and (statusArray[13] == 1):
			return 'charging completed'
		if statusArray[14]:
			return 'manual stop'
		if statusArray[15]:
			return 'going home'
		else:
			return 'mowing'
		

	def start(self):
		try:
			r = requests.post('http://' + self.host + '/jsondata.cgi', auth=('admin', self.pin), data='[["settaggi",11,1]]', timeout=7)
		except:
			_LOGGER.warning('Could not connect to Landroid')
			self.connected = False
		else:
			response_json = r.json()
			if(response_json['allarmi']):
				_LOGGER.info('Landroid started')


	def stop(self):
		try:
			r = requests.post('http://' + self.host + '/jsondata.cgi', auth=('admin', self.pin), data='[["settaggi",12,1]]', timeout=7)
		except:
			_LOGGER.warning('Could not connect to Landroid')
			self.connected = False
		else:
			response_json = r.json()
			if(response_json):
				_LOGGER.info('Landroid stopped')


	def update(self):
		try:
			_LOGGER.info('Updating')
			r = requests.get('http://' + self.host + '/jsondata.cgi', auth=('admin', self.pin), timeout=7)
		except:
			_LOGGER.warning('Could not connect to Landroid')
			self.connected = False
		else:
			response_json = r.json()
			_LOGGER.debug(response_json)
			self.connected = True
			self.numbrOfRuns =  response_json['CntProg']
			self.battery = response_json['perc_batt']
			self.error = self.parseError(response_json['allarmi'])
			self.state = self.parseStatus(response_json['settaggi'])
			return True

	def __str__(self):
		return 'Host: %s\nConnected: %r\nState: %s\nBattery: %s\nError: %s' % (
			self.host,
			self.connected,
			self.state,
			self.battery,
			self.error)

def read_credentials():
	"""Read credentials from file."""
	from os.path import join, dirname, expanduser
	for directory in [dirname(argv[0]),
					expanduser('~')]:
		try:
			with open(join(directory, '.landroid.conf')) as config:
				return dict(x.split(': ')
							for x in config.read().strip().splitlines()
							if not x.startswith('#'))
		except (IOError, OSError):
			continue
	return {}

def main():
	"""Main method."""
	if '-v' in argv:
		logging.basicConfig(level=logging.INFO)
	elif '-vv' in argv:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.ERROR)

	mower = Mower(**read_credentials())
	mower.update()
	print(mower)

if __name__ == '__main__':
	main()



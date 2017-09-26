# Script to count the number of files in a directory and upload the result to Datadog using 
# the DD agent running on the host
# Author: Seshadri Kothandaraman 26 Sep 2017

# stdlib
import os

# project
from checks import AgentCheck
from utils.subprocess_output import get_subprocess_output

class dirCheck(AgentCheck):
	''' This check counts the number of files in a directory
	WARNING: the user that dd-agent runs as must have sudo access for accessing and listing the directory.
	However, sudo is not needed if running the dd-agent as root. Also, it is not recommended.
	YAML config options:
	'directory' - the value of the directory which you want to examine
	'subdirs' - the subdirs that you would like to count
	'''

	def check(self, instance):
		config = self._get_config(instance)

		directory = config['directory']
		subdirs = config['subdirs']
		tags = config['tags']

		self._get_subdir_count(directory, subdirs, tags)

	def _get_config(self, instance):
		directory = instance.get('directory', None)
		subdirs = instance.get('subdirs', None)
		tags = instance.get('tags', [])
		if not subdirs or not directory:
			raise Exception('missing required yaml config entry')

		instance_config = {

		  'directory': directory,
		  'subdirs': queues,
		  'tags': tags,
		}

		return instance_config

	def _get_subdir_count(self, directory, subdirs, tags):
		for subdir in subdirs:
			subdir_path = os.path.join(directory, subdir)
			if not os.path.exists(subdir_path):
				raise Exception('%s does not exist' % subdir_path)

			count = 0
			if os.geteuid() == 0:
				# not recommended to run dd-agent as root
				count = sum(len(files) for root, dirs, files in os.walk(subdir_path))

			else:
				# check if dd-agent can run as sudo
				test_sudo = os.system('setsid sudo -l < /dev/null')
				if test_sudo == 0:
					output, _, _ = get_subprocess_output(['sudo', 'find', subdir_path, '-type', 'f'], self.log, False)
					count = len(output.splitlines())

				else:
					raise Exception('The dd-agent user does not have sudo access')

			# generate an individually-tagged metric
			self.gauge('countfiles.subdir.size', count, tags = tags + ['queue:%s' %queue, 'instance:%s' % os.path.basename(directory)])

			# these can be retrieved in a single graph statement 
			# example: 
			# sum:countfiles.subdir.size{instance:countfiles,subdir:dota,host:hostname.domain.tld}



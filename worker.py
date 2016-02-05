#!/usr/bin/python
"""Build a worker and give the worker jobs and roles"""
__version__ = '0.2a'
__author__ = 'Nicholas Porter'

import json
import os
import shutil
import time

from optparse import OptionParser


class Worker(object):
	"""Making of the essentials needed to describe a Worker.
	Standard usage:

		import worker
		jobs = {'Programmer': 'makes programs'}
		a = worker.Worker(jobs)

	If you feel inclined to set the name just set it as a string.

		workername = 'Jill'
		a = worker.Worker(jobs, name=workername)

	name -- Defaulted to John.
	jobs -- Dictionary of jobs and roles. jobs are the key, roles are the value.
	"""

	def __init__(self, name='John', jsonfile='settings.json', verbose=False):
		"""

		:type jsonfile:  string filename of json in currect working directory
		:rtype: object
		"""
		self.name = name
		self.json_file, self.json_bak = self.json_set(jsonfile, verbose)
		f1 = open(self.json_file, 'r')
		self.verbose = verbose
		self.jobs = json.load(f1)

	def add_job(self, thejob, therole):
		"""When you need to add a job along with its corresponding role.
		This is the simple function.
		input_new_job() takes user input directly from the console.

		thejob -- Is the new job.
		therole -- The role of the new job.

		:param thejob: str. The new job to add
		:param therole: str. Role of the new job

		"""
		if self.verbose:
			print 'Adding job "{0}" with the role "{1}".'.format(thejob,
			                                                     therole)
		self.jobs[thejob] = therole

	def ask_to_save_jobs(self):
		"""Prompt for user to save or not to save jobs
		"""
		if self.verbose:
			print self.jobs
		h = str(raw_input('Do you want to save this to file? (y/n): '))
		if h is 'y':
			self.save_jobs()
		else:
			print "Didn't save."

	def input_new_job(self):
		"""Prompts user for a new job and corresponding roles."""
		newjob = str(raw_input("What's the job?: "), )
		new_role = str(raw_input("What's the job do?: "), )
		self.add_job(newjob, new_role)
		self.ask_to_save_jobs()

	@staticmethod
	def json_set(jsonfile, verbose):
		"""
		Set the settings file saved in JSON format.
		:param verbose: bool, if you want verbose for debugging.
		:param jsonfile: string of filename for json file in current path
		"""
		json_file = os.path.join(os.getcwd(), '{0}'.format(jsonfile))
		json_bak = os.path.join(os.getcwd(), '.{0}.bak'.format(jsonfile))
		if not os.path.exists(json_file):
			if os.path.exists(json_bak):
				shutil.copy(json_bak, json_file)
			else:
				jsonjobs = {'Programmer': 'makes programs'}
				f = open(json_file, 'w')
				json.dump(jsonjobs, f)
				shutil.copy(json_file, json_bak)
				f.close()
		else:
			f = open(json_file, 'r')
			try:
				jsonjobs = json.load(f)
				if verbose:
						print jsonjobs
			except ValueError:
				f.close()
				f = open(json_file, 'w')
				jsonjobs = {'Programmer': 'makes programs'}
				json.dump(jsonjobs, f)
				shutil.copy(json_file, json_bak)
				f.close()
		return json_file, json_bak

	def menu(self):
		print '\b\b----------------------'
		print 'MENU'
		print '----------------------'
		print ' (a)dd new job'
		print ' (r)emove job'
		print ' (q)uit'
		print '----------------------'
		i = str(raw_input('What would you like to do?: '), )
		if i.lower() == 'a' or i.lower() == 'add':
			self.input_new_job()
		elif i.lower() == 'q' or i.lower() == 'quit':
			self.ask_to_save_jobs()
			exit()
		elif i.lower() == 'r' or i.lower() == 'remove':
			self.remove_job()
		else:
			pass

	def print_info(self):
		"""Print off the information in a nice format."""
		print 'This is {0}.'.format(self.name)
		print 'A little bit about {0}:'.format(self.name)
		for job in self.jobs:
			print ' {0} is a {1}. Where {0} {2}'.format(self.name, job,
			                                            self.jobs[job])

	def remove_job(self):
		"""Interactive menu to remove jobs."""
		while True:
			print "Jobs:"
			for job in self.jobs:
				print ' ', job
			h = str(raw_input('What job would you like to remove?: '), )
			if h in self.jobs:
				del self.jobs[h]
				if self.verbose:
					print self.jobs
				break
			else:
				print 'That is not a job.'
		self.ask_to_save_jobs()

	def run(self, pause):
		while True:
			try:
				self.print_info()
				time.sleep(pause)
			except KeyboardInterrupt:
				self.menu()

	def save_jobs(self):
		"""Save jobs to json file.
		The filename will be settings.json
		"""
		f1 = open(self.json_file, 'w')
		json.dump(self.jobs, f1)
		f1.close()


if __name__ == "__main__":
	usage = '%prog [options]'
	version = '%prog v0.2a'
	changelog = '''
	+++ 0.2a +++
	Change format to JSON instead of importing over .py file.
	Cleaner, more efficient, and I know should've been my go to
	before I even started.

	+++ 0.1a +++
	import class from personal file, add stuff to class,
	then export it over the original personal file'''

	p = OptionParser(usage=usage, version=version)
	p.add_option('-n', '--name',
	             help='Change name of worker.')
	p.add_option('-s', '--settings-file',
	             help='Name of settings file.(current path only)')
	p.add_option('-v', '--verbose', action='store_true',
	             help='Extra output for debugging')
	p.add_option('--changelog', action='store_true',
	             help='Output Version and Changelog')
	options, args = p.parse_args()
	if options.changelog:
		p.print_version()
		print changelog
		exit()

	a = Worker(verbose=options.verbose)
	a.run(2)

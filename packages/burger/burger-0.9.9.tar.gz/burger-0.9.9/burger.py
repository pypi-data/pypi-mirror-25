#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013-2017 by Rebecca Ann Heineman becky@burgerbecky.com

# It is released under an MIT Open Source license. Please see LICENSE
# for license details. Yes, you can use it in a
# commercial title without paying anything, just give me a credit.
# Please? It's not like I'm asking you for money!

#
# Includes
#

import os
import shutil
import stat
import errno
import subprocess
import platform
import sys
import string
from cStringIO import StringIO

#
## \mainpage Burgerlib Python Index
#
# A set of subroutines used by the Burgerlib
# based scripts written in Python.
#
# \par List of Classes
#
# \li \ref burger
# \li \ref burger.node
# \li \ref burger.interceptstdout
#
#
# To use the library:
#
# \code
# # Import the burger libary
# import burger
# \endcode
#
# To install type in 'pip install -U burger' from your shell.
#
# The source can be found at github at https://github.com/burgerbecky/pyburger
#
# Email becky@burgerbecky.com for comments, bugs or coding suggestions.
#

#
## \package burger
# A set of subroutines used by the Burgerlib based scripts
# written in Python.
#
# For higher level tools like makeprojects, burgerclean and
# burgerbuild, common subroutines were collected and
# placed in this module for reuse.
#

#
# Describe this module
#

## Current version of the library
__version__ = '0.9.9'

## Author's name
__author__ = 'Rebecca Ann Heineman <becky@burgerbecky.com>'

## Name of the module
__title__ = 'burger'

## Summary of the module's use
__summary__ = 'Burger Becky\'s shared python library.'

## Home page
__uri__ = 'http://burgerbecky.com'

## Email address for bug reports
__email__ = 'becky@burgerbecky.com'

## Type of license used for distribution
__license__ = 'MIT License'

## Copyright owner
__copyright__ = 'Copyright 2013-2017 Rebecca Ann Heineman'

#
## Items to import on "from burger import *"
#

__all__ = [
	'__version__',
	'__author__',
	'__title__',
	'__summary__',
	'__uri__',
	'__email__',
	'__license__',
	'__copyright__',
	'interceptstdout',
	'getsdksfolder',
	'createfolderifneeded',
	'deletefileifpresent',
	'converttoarray',
	'TrueFalse',
	'truefalse',
	'TRUEFALSE',
	'converttowindowsslashes',
	'converttolinuxslashes',
	'converttowindowsslasheswithendslash',
	'node',
	'hostmachine',
	'fixcsharp',
	'getwindowshosttype',
	'getmachosttype',
	'whereisdoxygen',
	'whereisp4',
	'perforceedit',
	'comparefiles',
	'comparefiletostring',
	'makeversionheader',
	'iscodewarriormacallowed',
	'isthesourcenewer',
	'copyfileifneeded',
	'copyfileandcheckoutifneeded',
	'copydirectoryifneeded',
	'shutilreadonlycallback',
	'deletedirectory',
	'traversedirectory',
	'encapsulatepath'
]

#
## Handy class for capturing stdout from tools and
# python itself
#
# How to use this to capture text sent out stdout
#
# \code
# from burger import interceptstdout
#
# with interceptstdout() as output:
#    do_somethingthatprints()
#
# print output
# \endcode
#

class interceptstdout(list):

	## Constructor
	def __init__(self):
		# Saved copy of sys.stdout
		self._stdout = None

		# cStringIO to redirect output to
		self._stringio = None
		super(interceptstdout, self).__init__()

	## Invoked on "with" which intercepts all future stdout
	def __enter__(self):

		self._stdout = sys.stdout
		self._stringio = StringIO()
		sys.stdout = self._stringio
		return self

	## Disconnect the stdout and store the items into a list
	def __exit__(self, *args):

		# Restore stdout on exit

		self.extend(self._stringio.getvalue().splitlines())
		sys.stdout = self._stdout

#
## Return the path of the BURGER_SDKS folder
#
# If the environment variable BURGER_SDKS is set,
# return the pathname it contains. Otherwise,
# print a warning and return None.
#

def getsdksfolder():
	sdks = os.getenv('BURGER_SDKS')
	if sdks is None:
		print 'The environment variable "BURGER_SDKS" is not set'
	return sdks

#
## Given a pathname to a folder, detect if the folder exists,
# if not, create it.
#
# \param foldername A string object with the pathname
#

def createfolderifneeded(foldername):
	if not os.path.isdir(foldername):
		os.makedirs(foldername)

#
## Given a pathname to a file, detect if a file exists. If so, delete it.
#
# \param filename A string object with the filename
#

def deletefileifpresent(filename):
	if os.path.isfile(filename):
		os.remove(filename)

#
## Convert a string to a string array (list)
#
# If the input is already a list, return the list as is.
# Otherwise, convert the string to a single entry list.
# If the input is None, return an empty list.
#
# \param inputarray A list or string object
# \return The original input if it was a list, or a list with the input object as a single entry
#

def converttoarray(inputarray):
	# If empty, return an empty array
	if inputarray is None:
		inputarray = []
	elif not isinstance(inputarray, list):
		# Convert a single entry into an array
		inputarray = [inputarray]
	return inputarray

#
## Convert the input into a boolean and return the string 'True' or 'False'
#
# If the input was a string of 'False' (Case insensitive comparision),
# this function will return 'False'
#
# \param item Object to convert to a bool before converting into a string
# \return 'True' or 'False'
# \sa truefalse() or TRUEFALSE()
#

def TrueFalse(item):
	# Test if it's the string 'False'
	if isinstance(item, (str, unicode)):
		if item.upper() == 'FALSE':
			return 'False'
	return str(bool(item))

#
## Convert the input into a boolean and return the lower case string 'true' or 'false'
#
# If the input was a string of 'False' (Case insensitive comparision),
# this function will return 'False'
#
# \param item Object to convert to a bool before converting into a string
# \return 'true' or 'false'
# \sa TRUEFALSE() or TrueFalse()
#

def truefalse(item):
	return TrueFalse(item).lower()

#
## Convert the input into a boolean and return the upper case string 'TRUE' or 'FALSE'
#
# If the input was a string of 'False' (Case insensitive comparision),
# this function will return 'False'
#
# \param item Object to convert to a bool before converting into a string
# \return 'TRUE' or 'FALSE'
# \sa truefalse() or TrueFalse()
#

def TRUEFALSE(item):
	return TrueFalse(item).upper()

#
## Convert a filename from linux/mac to windows format
#
# Convert all '/' characters into '\' characters
#
# \param item A string object that text substitution will occur
#

def converttowindowsslashes(item):
	return item.replace('/', '\\')

#
## Convert a filename from windows to linux/mac format
#
# Convert all '\' characters into '/' characters
#
# \param item A string object that text substitution will occur
#

def converttolinuxslashes(item):
	return item.replace('\\', '/')

#
## Convert a filename to a format used by Visual Studio
#
# Convert all '/' characters into '\' characters and
# append a '\' if one is not present in the final string
#
# \param item A string object that text substitution will occur
#

def converttowindowsslasheswithendslash(item):
	item = converttowindowsslashes(item)
	if not item.endswith('\\'):
		item.append('\\')
	return item

#
## Node class for creating directory trees
# Needed for some projects that have to store
# file entries in nested trees
#

class node(object):

	## Create a node with an initial value
	#
	# \param value Object to be the value of this node
	# \param children Array of nodes to be added as children to this one
	#
	def __init__(self, value, children=None):

		if children is None:
			children = []

		## Value contained in this node
		self.value = value
		## Array of children nodes to this node
		self.children = children

	## Convert to string function for node tree
	def __repr__(self, level=0):
		ret = '\t'*level+repr(self.value)+'\n'
		for child in self.children:
			ret += child.__repr__(level+1)
		return ret

#
## Return the high level operating system's name
#
# Return the machine this script is running on, 'windows', 'macosx',
# 'linux' or 'unknown'
#

def hostmachine():

	# Only windows reports as NT

	if os.name == 'nt':
		return 'windows'

	# BSD and GNU report as posix

	if os.name == 'posix':

		# MacOSX is the Darwin kernel

		if platform.system() == 'Darwin':
			return 'macosx'

		# Assume linux (Tested on Ubuntu and Red Hat)

		return 'linux'

	# Surrender Dorothy

	return 'unknown'

#
## Convert pathname to execute a C# exe file
#
# C# applications can launch as is on Windows platforms,
# however, on Mac OSX and Linux, it must be launched
# from mono. Determine the host machine and if not
# windows, automatically prepend "mono" to
# the application's name to properly launch it
#
# This will also encase the name in quotes in case there are
# spaces in the pathname
#
# \param csharpapplicationpath Pathname string to update
#

def fixcsharp(csharpapplicationpath):
	if hostmachine() != 'windows':
		csharpapplicationpath = 'mono "' + csharpapplicationpath + '"'
	else:
		csharpapplicationpath = '"' + csharpapplicationpath + '"'
	return csharpapplicationpath

#
## Return windows host type (32 or 64 bit)
#
# Return False if the host is not Windows, 'x86' if it's a 32 bit host
# and 'x64' if it's a 64 bit host, and possibly 'arm' if an arm host
#

def getwindowshosttype():

	# Not windows?

	if os.name != 'nt':
		return False

	# Test the CPU for the type

	machine = platform.machine()
	if machine == 'AMD64':
		return 'x64'
	return 'x86'

#
## Return Mac OSX host type (PowerPC/Intel)
#
# Return False if the host is not Mac OSX. 'ppc' if it's a Power PC based
# system, 'x86' for Intel (Both 32 and 64 bit)
#

def getmachosttype():

	# Mac/Linux?
	if os.name != 'posix':
		return False

	# Not linux?

	if platform.system() != 'Darwin':
		return False

	#
	# Since it's a mac, query the Mac OSX cpu type
	# using the MacOSX python extensions
	#

	version, _, cpu = platform.mac_ver()
	if cpu == 'x86' or cpu == 'x86_64':
		return 'x86'

	if cpu == 'PowerPC':
		return 'ppc'

	# default to PowerPC
	return 'ppc'

#
## Return the location of Doxygen's executable
#
# Look for an environment variable DOXYGEN and
# determine if the executable resides there, if
# so, return the string to the path
#
# If running on a MacOSX client, look in the Applications
# folder for a copy of Doxygen.app and return the
# pathname to the copy of doxygen that resides within
#
# If it cannot be determined that doxygen is installed,
# the string 'doxygen' is returned expecting
# that the executable is in the PATH
#

def whereisdoxygen():

	# Is Doxygen installed on windows?

	if getwindowshosttype() != False:

		# Try the environment variable

		doxygenpath = os.path.expandvars('${DOXYGEN}\\bin\\doxygen.exe')
		if doxygenpath != None:
			if not os.path.isfile(doxygenpath):
				doxygenpath = None

		# Try 64 bit version or native 32 bit version
		if doxygenpath is None:
			doxygenpath = os.path.expandvars('${ProgramFiles}\\doxygen\\bin\\doxygen.exe')
			if doxygenpath != None:
				if not os.path.isfile(doxygenpath):
					doxygenpath = None

		# Try 32 bit version on 64 bit system

		if doxygenpath is None:
			doxygenpath = os.path.expandvars('${ProgramFiles(x86)}\\doxygen\\bin\\doxygen.exe')
			if doxygenpath != None:
				if not os.path.isfile(doxygenpath):
					doxygenpath = None

		if doxygenpath is None:
			print 'Doxygen needs to be installed to build documentation!'

		return doxygenpath

	# MacOSX has it hidden in the application
	elif getmachosttype() != False:
		doxygenpath = '/Applications/Doxygen.app/Contents/Resources/doxygen'
		if not os.path.isfile(doxygenpath):
			print 'Doxygen needs to be installed in your Applications folder to build documentation!'
			return None
		return doxygenpath

	# None of the above
	return 'doxygen'

#
## Return the location of the p4 executable
#
# Note: This returns the string in a format that is used
# to call p4 from a shell, so on Windows clients it may
# be encased in quotes to allow spaces in the full pathname
#
# If it cannot be determined that p4 is installed,
# the string 'p4' is returned expecting
# that the executable is in the PATH
#

def whereisp4():

	# Is Perforce installed on windows?

	if getwindowshosttype() != False:

		# Try the environment variable

		perforcepath = os.path.expandvars('${PERFORCE}\\p4.exe')
		if perforcepath != None:
			if not os.path.isfile(perforcepath):
				perforcepath = None

		# Try 64 bit version or native 32 bit version
		if perforcepath is None:
			perforcepath = os.path.expandvars('${ProgramFiles}\\Perforce\\p4.exe')
			if perforcepath != None:
				if not os.path.isfile(perforcepath):
					perforcepath = None

		# Try 32 bit version on 64 bit system

		if perforcepath is None:
			perforcepath = os.path.expandvars('${ProgramFiles(x86)}\\Perforce\\p4.exe')
			if perforcepath != None:
				if not os.path.isfile(perforcepath):
					perforcepath = None

		if perforcepath is None:
			print 'Perforce needs to be installed for source control!'
			return None

		return '"' + perforcepath + '"'

	#
	# Is the path set for Linux or Mac OSX?

	perforcepath = os.getenv('PERFORCE')
	if perforcepath != None:
		return '"' + os.path.join(perforcepath, 'p4') + '"'


	# Use the local copy of the p4 client (Universal binary)

	#if hostmachine() == 'macosx':
	#	return '"' + os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'macosx','bin'),'p4') + '"'

	# Assume it's in the PATH on other systems
	return 'p4'

#
## Given a list of files, checkout (Edit) them in perforce
#
# Pass either a single string or a string list of pathnames
# of files to checkout in perforce using the 'p4 edit' command
#
# \param files list or string object of file(s) to checkout
#

def perforceedit(files):

	# Get the p4 executable

	perforce = whereisp4()
	# Not found?
	if perforce is None:
		return 10

	if not isinstance(files, list):
		files = [files]

	for file in files:
		cmd = perforce + ' edit "' + os.path.abspath(file) + '"'
		error = subprocess.call(cmd, shell=True)
		if error != 0:
			return error
	return 0

#
## Compare text files for equality
#
# Check if two text files are the same length,
# and then test the contents to verify equality
# If both are true, then return True
# Otherwise return False
#
# \param filename1 string object with the pathname of the file to test
# \param filename2 string object with the pathname of the file to test against
#

def comparefiles(filename1, filename2):

	# Are they the same size?

	try:
		f1size = os.path.getsize(filename1)
		f2size = os.path.getsize(filename2)
	except:
		return False

	# Not the same size?
	if f1size != f2size:
		return False

	# Do a data compare as a text file

	try:
		f1 = open(filename1, 'r')
		fileOneLines = f1.readlines()
		f1.close()

	except:
		f1.close()
		return False

	try:
		f2 = open(filename2, 'r')
		fileTwoLines = f2.readlines()
		f2.close()

	except:
		f2.close()
		return False

	# Compare the file contents

	x = 0
	for i in fileOneLines:
		if i != fileTwoLines[x]:
			return False
		x += 1

	# It's a match!

	return True

#
## Compare text file and a string for equality
#
# Check if a text file is the same as a string
# by loading the text file and
# testing line by line to verify the equality
# of the contents
# If they are the same, return True
# Otherwise return False
#
# \param filename string object with the pathname of the file to test
# \param string string object to test against
#

def comparefiletostring(filename, string):

	#
	# Do a data compare as a text file
	#

	f1 = None
	try:
		f1 = open(filename, 'r')
		fileOneLines = f1.readlines()
		f1.close()

	except:
		if f1 != None:
			f1.close()
		return False

	#
	# Compare the file contents taking into account
	# different line endings
	#

	fileTwoLines = string.getvalue().splitlines(True)
	f1size = len(fileOneLines)
	f2size = len(fileTwoLines)

	#
	# Not the same size?
	#

	if f1size != f2size:
		return False

	x = 0
	for i in fileOneLines:
		if i != fileTwoLines[x]:
			return False
		x += 1

	# It's a match!

	return True

#
## Create a C header with the perforce version
#
# This function assumes version control is with perforce!
#
# Get the last change list and create a header
# with this information (Only modify the output file if
# the contents have changed)
#
# \param workingdir string with the path of the folder to obtain the perforce version for
# \param outputfilename string with the path of the generated header
#

def makeversionheader(workingdir, outputfilename):

	# Check if perforce is installed
	p4exe = whereisp4()
	if p4exe is None:
		return 10

	# Create the header guard
	headerguard = os.path.basename(outputfilename).upper()
	headerguard = headerguard.replace(' ', '_')
	headerguard = '__' + headerguard.replace('.', '_') + '__'

	# Work filename
	p4tempfilename = 'p4tempfilename1234.h'
	p4temppathname = os.path.join(workingdir, p4tempfilename)

	#
	# Get the last change list
	# Parse "Change 3361 on 2012/05/15 13:20:12 by burgerbecky@burgeroctocore 'Made a p4 change'"
	# -m 1 / Limit to one entry
	# -t / Display the time
	# -l / Print out the entire changelist description
	#

	cmd = p4exe + ' changes -m 1 -t -l ...#have > ' + p4tempfilename
	error = subprocess.call(cmd, cwd=workingdir, shell=True)
	if error != 0:
		# Uh oh...
		deletefileifpresent(p4temppathname)
		print 'Error in calling ' + cmd
		return error

	#
	# Parse out the file contents
	#

	p4tempfp = open(p4temppathname, 'r')
	tempdata = p4tempfp.read().strip()
	p4tempfp.close()
	p4changes = tempdata.split(' ')

	#
	# Get the p4 client
	# Parse "P4CLIENT=burgeroctocore (config)"
	#

	cmd = p4exe + ' set P4CLIENT > ' + p4tempfilename
	error = subprocess.call(cmd, cwd=workingdir, shell=True)
	if error != 0:
		# The P4CLIENT query failed!
		deletefileifpresent(p4temppathname)
		print 'Error in calling ' + cmd
		return error

	#
	# Parse out the P4CLIENT query
	#

	p4tempfp = open(p4temppathname, 'r')
	tempdata = p4tempfp.read().strip()
	p4tempfp.close()
	p4clients = tempdata.split(' ')
	p4clients = p4clients[0].split('=')

	#
	# Get the p4 user
	# Parse "P4USER=burgerbecky (config)"
	#

	cmd = p4exe + ' set P4USER > ' + p4tempfilename
	error = subprocess.call(cmd, cwd=workingdir, shell=True)
	if error != 0:
		# The P4USER query failed!
		deletefileifpresent(p4temppathname)
		print 'Error in calling ' + cmd
		return error

	#
	# Parse out the P4USER query
	#

	p4tempfp = open(p4temppathname, 'r')
	tempdata = p4tempfp.read().strip()
	p4tempfp.close()
	os.remove(p4temppathname)
	p4users = tempdata.split(' ')
	p4users = p4users[0].split('=')

	#
	# Name of the temp work file
	#

	tempheaderfile = os.path.join(workingdir, 'versioninfo1234.h')
	fp = open(tempheaderfile, 'w')

	#
	# Write out the header
	#

	fp.write( \
		'/***************************************\n'
		'\n'
		'\tThis file was generated by a call to\n'
		'\tburger.makeversionheader() from a build\n'
		'\tpython script\n'
		'\n'
		'***************************************/\n'
		'\n'
		'#ifndef ' + headerguard + '\n'
		'#define ' + headerguard + '\n'
		'\n')

	if len(p4changes) > 4:
		fp.write('#define P4_CHANGELIST ' + p4changes[1] + '\n')
		fp.write('#define P4_CHANGEDATE "' + p4changes[3] + '"\n')
		fp.write('#define P4_CHANGETIME "' + p4changes[4] + '"\n')

	if len(p4clients) > 1:
		fp.write('#define P4_CLIENT "' + p4clients[1] + '"\n')

	if len(p4users) > 1:
		fp.write('#define P4_USER "' + p4users[1] + '"\n\n#endif\n')
	fp.close()

	#
	# Check if the file is different than what's already stored on
	# the drive
	#

	if os.path.isfile(outputfilename) != True or \
		comparefiles(tempheaderfile, outputfilename) != True:
		print 'Copying ' + tempheaderfile + ' -> ' + outputfilename
		try:
			shutil.copyfile(tempheaderfile, outputfilename)
		except IOError, e:
			os.remove(tempheaderfile)
			print e
			return 2

	#
	# Clean up
	#

	os.remove(tempheaderfile)
	return 0

#
## True if this machine can run Codewarrior for Mac OS Carbon
#
# Return True if CodeWarrior for Mac OS can be run
# on a PowerPC compatible Mac
#

def iscodewarriormacallowed():

	# Test if a mac

	if hostmachine() == 'macosx':
		# Get the Mac OS version number
		version, _, cpu = platform.mac_ver()

		# Convert 10.5.8 to 10.5

		digits = version.split('.')

		# Snow Leopard (10.6) supports Rosetta
		# Lion (10.7) and Mountain Lion (10.8) do not

		if float(digits[0]) == 10:
			if float(digits[1]) < 7:
				return True

	# Can't run, not a mac or Power PC native or emulation isn't supported
	return False

#
## Return True if the source file is newer then the destination file
#
# Check the modification times of both files to determine if the
# source file is newer
#
# Return True if there is no destination file
#
# \param src string pathname of the file to test
# \param dest string pathname of the file to test against
#
# \return False if not newer, True if newer, 2 if there is no source file
#

def isthesourcenewer(src, dest):
	# It's an error if there is no source file
	try:
		srctime = os.path.getmtime(src)
	except:
		return 2

	# If there is a destination file, check the modification times
	try:
		desttime = os.path.getmtime(dest)
	except:
		return True

	# Is the source newer?
	if srctime <= desttime:
		return False
	return True

#
## Copy a file only if newer
#
# Copy a file only if the destination is
# missing or is older than the source file
#
# \param src string pathname of the file to copy from
# \param dest string pathname of the file to copy to
#
# \return Returns 0 if no error otherwise non-zero
#

def copyfileifneeded(src, dest):

	# If there is a destination file, check the modification times

	if isthesourcenewer(src, dest) is True:

		# Copy the file

		print 'Copying ' + src + ' -> ' + dest
		try:
			shutil.copyfile(src, dest)
		except IOError, e:
			print e
			return 2
	return 0

#
## Copy a file only if newer being aware of Perforce
#
# Copy a file only if needed and check out the destination file before the copy
# operation
#
# \param src string pathname of the file to copy from
# \param dest string pathname of the file to copy to
#

def copyfileandcheckoutifneeded(src, dest):

	if isthesourcenewer(src, dest) is True:

		# Alert perforce that the file is to be modified

		perforceedit(dest)

		# Copy the file

		print 'Copying ' + src + ' -> ' + dest
		try:
			shutil.copyfile(src, dest)
		except IOError, e:
			print e
			return 2
	return 0

#
## Copy all of the files in a directory into a new directory
#
# Copy all files in a directory into a new directory,
# creating any necessary directories in the process
#
# It will skip files with specific extensions
#
# \note This is a recursive function
#
# \param src string pathname of the directory to copy from
# \param dest string pathname of the directory to copy to
# \param exceptionlist optional list object of file extensions to ignore during copy
#

def copydirectoryifneeded(src, dest, exceptionlist=None):

	if exceptionlist is None:
		exceptionlist = []

	#
	# Make sure the output folder exists
	#

	createfolderifneeded(dest)

	name_list = os.listdir(src)
	for base_name in name_list:
		skip = False
		for item in exceptionlist:
			if base_name.endswith(item):
				skip = True
		if skip is False:
			file_name = os.path.join(src, base_name)

			# Handle the directories found
			if os.path.isdir(file_name):
				# Recursive!
				error = copydirectoryifneeded(file_name, os.path.join(dest, base_name), exceptionlist)
			else:
				error = copyfileifneeded(file_name, os.path.join(dest, base_name))

			if error != 0:
				return error

	return 0

#
## Subroutine for shutil.rmtree() to delete read only files
#
# shutil.rmtree() raises an exception if there are read
# only files in the directory being deleted. Use this
# callback to allow read only files to be disposed of
#
# \code
# import burger
# import shutil
#
# shutil.rmtree(PATH_TO_DIRECTORY,onerror = burger.shutilreadonlycallback)
# \endcode
#
# \note This is a callback function
#
# \param func Not used
# \param path pathname of the file that is read only
# \param exception_info Information about the exception
#

def shutilreadonlycallback(func, path, exception_info):
	exctype, value = exception_info[:2]

	# File not found? Ignore
	if value.args[0] == errno.ENOENT:
		return

	#
	# Read only?
	# EACCESS for Linux/MacOSX, EIO for Windows
	#

	if value.args[0] == errno.EACCES or value.args[0] == errno.EIO:
		# Mark as writable
		os.chmod(path, stat.S_IWRITE)
		# Try again to get rid of the file
		os.unlink(path)

#
## Recursively delete a directory
#
# Delete a directory and all of the files and directories
# within.
#
# \param path Pathname of the directory to delete
# \param deletereadonly True if read only files are to be deleted as well
#

def deletedirectory(path, deletereadonly=False):
	if deletereadonly is False:
		return shutil.rmtree(path, ignore_errors=True)
	return shutil.rmtree(path, onerror=shutilreadonlycallback)

#
## Find executable tool directory
#
# For allowing builds on multiple operating system hosts,
# it's necessary to query what is the host operating system
# and glean out which folder to find a executable compiled
# for that specific host
#
# \param toolfolder Pathname to the folder that contains the executables
# \param toolname Bare name of the tool (Windows will append '.exe')
# \param encapsulate False if a path is requested, True if it's quoted
#		to be used as a string to be sent to command line shell
# \return Full pathname to the tool to execute
#

def gettoolpath(toolfolder, toolname, encapsulate=False):
	host = hostmachine()

	# Macosx uses fat binaries
	if host == 'macosx':
		exename = os.path.join(toolfolder, 'macosx', toolname)

	# Linux is currently just 64 bit Intel, will have to update
	# as more platforms are supported
	elif host == 'linux':
		exename = os.path.join(toolfolder, 'linux', toolname)

	# Windows supports 32 and 64 bit Intel
	elif host == 'windows':
		exename = os.path.join(toolfolder, 'windows', getwindowshosttype(), toolname + '.exe')
	else:

	# On unknown platforms, assume the tool is in the path for the fallback
		exename = toolname

	# Encase in quotes to handle spaces in filenames

	if encapsulate is True:
		exename = '"' + exename + '"'
	return exename

#
## Create a list of all copies of a file following a directory
#
# Starting with a working directory, test if a file exists
# and if so, inserted it into a list. The list will be
# starting from the root with the last entry
# being at the workingdirectory
#
# \param workingdir string with the path of the folder to obtain the perforce version for
# \param filename string with the path of the generated header
# \return List of pathnames (With filename appended)
#

def traversedirectory(workingdir, filename):

	dirlist = []

	# Convert into a unpacked pathname
	tempdir = os.path.abspath(workingdir)

	# Loop
	while 1:
		# Is the file here?
		temppath = os.path.join(tempdir, filename)
		if os.path.isfile(temppath):
			# Insert at the beginning
			dirlist.insert(0, temppath)
		# Pop a folder
		tempdir2 = os.path.dirname(tempdir)
		# Already at the top of the directory?
		if tempdir2 is None or tempdir2 == tempdir:
			break
		# Use the new folder
		tempdir = tempdir2

	# Return the list of files
	return dirlist


_WINDOWSSAFESET = frozenset(string.ascii_letters + string.digits + '_-.:\\')
_LINUXSAFESET = frozenset(string.ascii_letters + string.digits + '@%_-+=:,./')

#
## Quote a pathname for use in the native system shell
#
# On windows platforms, if the path has a space or other
# character that could confuse COMMAND.COM, the string
# will be quoted, and for other platforms, it will
# be quoted using rules that work best for BASH.
# This will also quote if the path has a ';' which
# could be used to confuse bash.
#
# \param input string with the path to encapsulate
# \return Input string or input properly quoted
#

def encapsulatepath(input):
	# Windows version
	if getwindowshosttype():
		# Force to windows slashes
		temp = converttowindowsslashes(input)
		# break if not a safe string
		for item in temp:
			if item not in _WINDOWSSAFESET:
				break
		else:
			# Safe string
			if not temp:
				return '""'
			return temp
		# Quote the string
		return '"' + temp.replace('"', '^"') + '"'

	# Force to linux slashes
	temp = converttolinuxslashes(input)
	for item in temp:
		if item not in _LINUXSAFESET:
			break
	else:
		if not temp:
			return "''"
		return temp
	# Enquote the string for Linux or MacOSX
	return "'" + temp.replace("'", "'\"'\"'") + "'"

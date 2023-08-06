#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import re
import os
import array

from .AbstractPatternMatcher import AbstractPatternMatcher
from .PathPatternMatcher import PathPatternMatcher
from .PathPatternsMatcher import PathPatternsMatcher





def createPatternMatcher(patternOrListOfPatterns):
	if patternOrListOfPatterns is None:
		return None
	if isinstance(patternOrListOfPatterns, AbstractPatternMatcher):
		return patternOrListOfPatterns
	if isinstance(patternOrListOfPatterns, str):
		return PathPatternMatcher(patternOrListOfPatterns)
	if isinstance(patternOrListOfPatterns, list):
		for e in patternOrListOfPatterns:
			if not isinstance(e, str):
				raise Exception("Invalid data type specified in list!")
		return PathPatternsMatcher(patternOrListOfPatterns)
	raise Exception("Invalid data type specified!")
#



#
# Recursively get all files and directories. If a filter is specified the filter is taken into account.
#
# @param		str bRecursive				The base path that defines the starting point for the search.
# @param		bool bRecursive				If <c>True</c> (= the default) a recursive search will be performed.
# @param		misc relDirPathFilter		A filter specifying which directories to ignore.
# @param		misc relFilePathFilter		A filter specifying which files to ignore.
# @return		tuple						Returns a tuple containing:
#											* a list of directory paths relative to the search base directory
#											* a list of file paths relative to the search base directory
#
def getFilesAndDirs(searchBaseDirPath, relDirPathFilter, relFilePathFilter, bRecursive = True, bSwallowExceptions = True):
	relDirPathFilter = createPatternMatcher(relDirPathFilter)
	relFilePathFilter = createPatternMatcher(relFilePathFilter)

	files = []
	dirs = []

	paths = [ os.path.abspath(searchBaseDirPath) ]
	i = 0
	while i < len(paths):
		currentAbsPath = paths[i]
		i += 1

		pattern = currentAbsPath
		if not pattern.endswith("/"):
			pattern += "/"
		patternLength = len(pattern)

		entryNames = None
		if bSwallowExceptions:
			try:
				entryNames = os.listdir(currentAbsPath)
			except:
				pass
		else:
			entryNames = os.listdir(currentAbsPath)

		if entryNames is not None:
			for entryName in entryNames:
				absPath = pattern + entryName
				relPath = absPath[patternLength:]
				if os.path.isdir(absPath):
					if relDirPathFilter is not None:
						if relDirPathFilter.checkMatch(relPath):
							continue
					dirs.append(relPath)
					if bRecursive:
						paths.append(absPath)
				else:
					if relFilePathFilter is not None:
						if relFilePathFilter.checkMatch(relPath):
							continue
					files.append(relPath)

	return (dirs, files)
#



#
# Recursively get all directories. If a filter is specified the filter is taken into account.
#
# @param		str searchBaseDirPath		The base path that defines the starting point for the search.
# @param		bool bRecursive				If <c>True</c> (= the default) a recursive search will be performed.
# @param		misc relDirPathFilter		A filter specifying which directories to accept.
# @return		list						Returns a list of directory paths relative to the search base directory
#
def getMatchedFilesAndDirs(searchBaseDirPath, relDirPathFilter, relFilePathFilter, relDirPathMatcher, relFilePathMatcher,
	bRecursive = True, bSwallowExceptions = True, bExactMatch = False, bSortFiles = True, bSortDirs = True):

	assert relDirPathMatcher is not None
	assert relFilePathMatcher is not None
	assert isinstance(bRecursive, bool)
	assert isinstance(bSwallowExceptions, bool)
	relDirPathMatcher = createPatternMatcher(relDirPathMatcher)
	relFilePathMatcher = createPatternMatcher(relFilePathMatcher)
	relDirPathFilter = createPatternMatcher(relDirPathFilter)
	relFilePathFilter = createPatternMatcher(relFilePathFilter)

	dirs = []
	files = []

	searchBaseDirPath = os.path.abspath(searchBaseDirPath)
	searchBaseDirPathWithSlash = "/" if searchBaseDirPath == '/' else searchBaseDirPath + "/"
	searchBaseDirPathWithSlashLength = len(searchBaseDirPathWithSlash)

	paths = [ searchBaseDirPath ]
	i = 0
	while i < len(paths):
		currentAbsPath = paths[i]
		i += 1

		currentRelBasePath = currentAbsPath[searchBaseDirPathWithSlashLength:]

		entryNames = None
		if bSwallowExceptions:
			try:
				entryNames = os.listdir(currentAbsPath)
			except:
				pass
		else:
			entryNames = os.listdir(currentAbsPath)

		if entryNames is not None:
			# print(currentAbsPath)
			for entryName in entryNames:
				relEntryPath = os.path.join(currentRelBasePath, entryName)
				absEntryPath = searchBaseDirPathWithSlash + relEntryPath
				if os.path.isdir(absEntryPath):
					if relDirPathFilter is not None:
						if relDirPathFilter.checkMatch(relEntryPath):
							# print("-- Skipping: " + relEntryPath)
							continue
					# print("-- Checking match: " + relEntryPath)
					if relDirPathMatcher.checkMatch(relEntryPath):
						# print("-- Accepted: " + relEntryPath)
						dirs.append(relEntryPath)
						if bExactMatch:
							continue
					if bRecursive:
						paths.append(absEntryPath)
				else:
					if relFilePathFilter is not None:
						if relFilePathFilter.checkMatch(relEntryPath):
							# print("-- Skipping: " + relEntryPath)
							continue
					# print("-- Checking match: " + relEntryPath)
					if relFilePathMatcher.checkMatch(relEntryPath):
						# print("-- Accepted: " + relEntryPath)
						files.append(relEntryPath)

	if bSortDirs:
		dirs.sort()
	if bSortFiles:
		files.sort()

	return (dirs, files)
#



#
# Recursively get all directories. If a filter is specified the filter is taken into account.
#
# @param		str searchBaseDirPath		The base path that defines the starting point for the search.
# @param		bool bRecursive				If <c>True</c> (= the default) a recursive search will be performed.
# @param		misc relDirPathFilter		A filter specifying which directories to accept.
# @return		list						Returns a list of directory paths relative to the search base directory
#
def getMatchedDirs(searchBaseDirPath, relDirPathFilter, relDirPathMatcher,
	bRecursive = True, bSwallowExceptions = True, bExactMatch = False, bSortDirs = True):

	assert relDirPathMatcher is not None
	assert isinstance(bRecursive, bool)
	assert isinstance(bSwallowExceptions, bool)
	relDirPathMatcher = createPatternMatcher(relDirPathMatcher)
	relDirPathFilter = createPatternMatcher(relDirPathFilter)

	dirs = []

	searchBaseDirPath = os.path.abspath(searchBaseDirPath)
	searchBaseDirPathWithSlash = "/" if searchBaseDirPath == '/' else searchBaseDirPath + "/"
	searchBaseDirPathWithSlashLength = len(searchBaseDirPathWithSlash)

	paths = [ searchBaseDirPath ]
	i = 0
	while i < len(paths):
		currentAbsPath = paths[i]
		i += 1

		currentRelBasePath = currentAbsPath[searchBaseDirPathWithSlashLength:]

		entryNames = None
		if bSwallowExceptions:
			try:
				entryNames = os.listdir(currentAbsPath)
			except:
				pass
		else:
			entryNames = os.listdir(currentAbsPath)

		if entryNames is not None:
			# print(currentAbsPath)
			for entryName in entryNames:
				relEntryPath = os.path.join(currentRelBasePath, entryName)
				absEntryPath = searchBaseDirPathWithSlash + relEntryPath
				if os.path.isdir(absEntryPath):
					if relDirPathFilter is not None:
						if relDirPathFilter.checkMatch(relEntryPath):
							# print("-- Skipping: " + relEntryPath)
							continue
					# print("-- Checking match: " + relEntryPath)
					if relDirPathMatcher.checkMatch(relEntryPath):
						# print("-- Accepted: " + relEntryPath)
						dirs.append(relEntryPath)
						if bExactMatch:
							continue
					if bRecursive:
						paths.append(absEntryPath)
				else:
					pass

	if bSortDirs:
		dirs.sort()

	return dirs
#



#
# Recursively get all directories. If a filter is specified the filter is taken into account.
#
# @param		str searchBaseDirPath		The base path that defines the starting point for the search.
# @param		bool bRecursive				If <c>True</c> (= the default) a recursive search will be performed.
# @param		misc relDirPathFilter		A filter specifying which directories to accept.
# @return		list						Returns a list of directory paths relative to the search base directory
#
def getMatchedFiles(searchBaseDirPath, relDirPathFilter, relFilePathMatcher,
	bRecursive = True, bSwallowExceptions = True, bExactMatch = False, bSortDirs = True):

	assert relFilePathMatcher is not None
	assert isinstance(bRecursive, bool)
	assert isinstance(bSwallowExceptions, bool)
	relFilePathMatcher = createPatternMatcher(relFilePathMatcher)
	relDirPathFilter = createPatternMatcher(relDirPathFilter)

	files = []

	searchBaseDirPath = os.path.abspath(searchBaseDirPath)
	searchBaseDirPathWithSlash = "/" if searchBaseDirPath == '/' else searchBaseDirPath + "/"
	searchBaseDirPathWithSlashLength = len(searchBaseDirPathWithSlash)

	paths = [ searchBaseDirPath ]
	i = 0
	while i < len(paths):
		currentAbsPath = paths[i]
		i += 1

		currentRelBasePath = currentAbsPath[searchBaseDirPathWithSlashLength:]

		entryNames = None
		if bSwallowExceptions:
			try:
				entryNames = os.listdir(currentAbsPath)
			except:
				pass
		else:
			entryNames = os.listdir(currentAbsPath)

		if entryNames is not None:
			# print(currentAbsPath)
			for entryName in entryNames:
				relEntryPath = os.path.join(currentRelBasePath, entryName)
				absEntryPath = searchBaseDirPathWithSlash + relEntryPath
				if os.path.isdir(absEntryPath):
					if relDirPathFilter is not None:
						if relDirPathFilter.checkMatch(relEntryPath):
							# print("-- Skipping: " + relEntryPath)
							continue
					# print("-- Checking match: " + relEntryPath)
					if bRecursive:
						paths.append(absEntryPath)
				else:
					if relFilePathMatcher.checkMatch(relEntryPath):
						# print("-- Accepted: " + relEntryPath)
						files.append(relEntryPath)
						if bExactMatch:
							continue

	if bSortDirs:
		files.sort()

	return files
#



def glob(pathOrPaths, bSwallowExceptions = True, bSortResults = True, bRecursive = False):
	if isinstance(pathOrPaths, list):
		ret = []
		for path in pathOrPaths:
			ret.extend(__glob(path, bSwallowExceptions, False, bRecursive))
	else:
		ret = __glob(pathOrPaths, bSwallowExceptions, False, bRecursive)

	if bSortResults:
		ret.sort()

	return ret
#



def __glob(path, bSwallowExceptions = True, bSortResults = True, bRecursive = False):
	if not path.startswith('/'):
		raise Exception("Not an absolute path pattern!")

	elements = path.split('/')
	elements = elements[1:]
	p = ""
	n = 0
	while n < len(elements):
		element = elements[n]
		if len(element) == 0:
			raise Exception("Not a valid path pattern!")
		if (element.find("*") >= 0) or (element.find("?") >= 0):
			break
		else:
			p += "/" + element
		n += 1
	searchBaseDirPath = p
	searchBaseDirPathWithSlash = "/" if searchBaseDirPath == '/' else searchBaseDirPath + "/"
	searchBaseDirPathWithSlashLength = len(searchBaseDirPathWithSlash)
	relPatternMatcher = createPatternMatcher(path[len(p) + 1:])

	ret = []
	paths = [ searchBaseDirPath ]
	i = 0
	while i < len(paths):
		currentAbsPath = paths[i]
		i += 1

		currentRelBasePath = currentAbsPath[searchBaseDirPathWithSlashLength:]

		entryNames = None
		if bSwallowExceptions:
			try:
				entryNames = os.listdir(currentAbsPath)
			except:
				pass
		else:
			entryNames = os.listdir(currentAbsPath)

		if entryNames is not None:
			for entryName in entryNames:
				relEntryPath = os.path.join(currentRelBasePath, entryName)
				absEntryPath = searchBaseDirPathWithSlash + relEntryPath
				if os.path.isdir(absEntryPath):
					if relPatternMatcher.checkMatch(relEntryPath):
						ret.append(absEntryPath)
						if bRecursive:
							paths.append(absEntryPath)
					else:
						paths.append(absEntryPath)
				else:
					if relPatternMatcher.checkMatch(relEntryPath):
						ret.append(absEntryPath)

	if bSortResults:
		ret.sort()

	return ret
#












#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import re



from .AbstractPatternMatcher import AbstractPatternMatcher






class PathPatternsMatcher(AbstractPatternMatcher):

	def __init__(self, pathPatterns):
		self.__pathPatterns = []
		for pathPattern in pathPatterns:
			self.__pathPatterns.append(re.compile(self._compilePathPatternToRegExStr(pathPattern)))

	def checkMatch(self, relPath):
		for pathPattern in self.__pathPatterns:
			# print("CHECKING: " + relPath + " AGAINST " + str(pathPattern))
			result = pathPattern.match(relPath)
			# print(result)
			if result != None:
				return True
		return False







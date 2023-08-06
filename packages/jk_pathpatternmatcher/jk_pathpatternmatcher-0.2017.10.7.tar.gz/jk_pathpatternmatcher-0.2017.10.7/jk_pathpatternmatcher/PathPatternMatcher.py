#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import re



from .AbstractPatternMatcher import AbstractPatternMatcher






class PathPatternMatcher(AbstractPatternMatcher):

	def __init__(self, pathPattern):
		self.__pathPattern = re.compile(self._compilePathPatternToRegExStr(pathPattern))

	def checkMatch(self, relPath):
		result = self.__pathPattern.match(relPath)
		return result != None




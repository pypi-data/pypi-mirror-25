#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import re







class AbstractPatternMatcher(object):

	__REGEX_REPLACEMENT_MAP = {
		'^': '\\^',
		'?': '\\?',
		'$': '\\$',
		'.': '\\.',
		'+': '\\+',
		'*': '\\*',
		'|': '\\|',
		'(': '\\(',
		')': '\\)',
		'[': '\\[',
		']': '\\]',
		'{': '\\{',
		'}': '\\}',
		'\\': '\\\\',
	}



	def __addPartToRegex(self, p):
		regexStr = ""
		for c in p:
			repC = AbstractPatternMatcher.__REGEX_REPLACEMENT_MAP.get(c, None)
			if repC != None:
				regexStr += repC
			else:
				regexStr += c
		return regexStr
	#



	def _compilePathPatternToRegExStr(self, pathPattern):
		regexStr = "^"
		bNeedsSlash = False
		for p in pathPattern.split('/'):
			if bNeedsSlash:
				regexStr += "/"
			else:
				bNeedsSlash = True
			if p == '**':
				regexStr += ".+"
				continue
			if p == '*':
				regexStr += "[^/]+"
				continue
			p = p.split('*')
			if len(p) == 1:
				regexStr += self.__addPartToRegex(p)
			elif len(p) > 1:
				bAddStar = False
				for p2 in p:
					if bAddStar:
						bAddStar = True
					else:
						regexStr += "[^/]*"
					regexStr += self.__addPartToRegex(p2)
			else:
				raise Exception("Invalid pattern specified: " + pathPattern)
		# print(pathPattern + "  =>  " + regexStr)
		return regexStr
	#



	def checkMatch(self, relPath):
		raise Exception("Not implemented!")
	#



#




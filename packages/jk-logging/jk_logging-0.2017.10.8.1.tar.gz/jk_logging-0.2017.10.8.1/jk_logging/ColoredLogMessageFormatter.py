#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import datetime


from .EnumLogLevel import EnumLogLevel
from .AbstractLogMessageFormatter import AbstractLogMessageFormatter





def _createLogMsgTypeColorMap():
	logLevelToColorDict = {
		EnumLogLevel.TRACE: '\033[90m',
		EnumLogLevel.DEBUG: '\033[90m',
		EnumLogLevel.NOTICE: '\033[90m',
		EnumLogLevel.STDOUT: '\033[97m',
		EnumLogLevel.INFO: '\033[37m',
		EnumLogLevel.WARNING: '\033[93m',
		EnumLogLevel.ERROR: '\033[91m',
		EnumLogLevel.STDERR: '\033[91m',
		EnumLogLevel.EXCEPTION: '\033[91m',
		EnumLogLevel.SUCCESS: '\033[92m',
	}
	return logLevelToColorDict





#
# This is a default formatter for log messages. It produces human readable output for log messages.
#
class ColoredLogMessageFormatter(AbstractLogMessageFormatter):


	LOG_LEVEL_TO_COLOR_MAP = _createLogMsgTypeColorMap()
	RESET_COLOR = '\033[0m'



	def __init__(self, bIncludeIDs = False, fillChar = "\t"):
		self.__fillChar = fillChar
		self.__indentBuffer = fillChar
		self.__includeIDs = bIncludeIDs



	#
	# Create and return a string representation of the specified log entry.
	#
	# @param		list logEntryStruct			A log entry structure. See <c>AbstractLogger._logi()</c> for a detailed description.
	# @return		str							Returns the string representation of the log message.
	#
	def format(self, logEntryStruct):
		sID = str(logEntryStruct[1]) if (logEntryStruct != None) else "-"
		indentationLevel = logEntryStruct[2]
		while indentationLevel > len(self.__indentBuffer):
			self.__indentBuffer += self.__fillChar
		sIndent = self.__indentBuffer[0:indentationLevel]
		sParentID = str(logEntryStruct[3]) if (logEntryStruct != None) else "-"
		sTimeStamp = "[" + datetime.datetime.fromtimestamp(logEntryStruct[4]).strftime('%Y-%m-%d %H:%M:%S') + "]"
		sLogType = AbstractLogMessageFormatter.LOG_LEVEL_TO_STR_MAP[logEntryStruct[5]]

		s = sIndent + ColoredLogMessageFormatter.LOG_LEVEL_TO_COLOR_MAP[logEntryStruct[5]]
		if self.__includeIDs:
			s += "(" + sParentID + "|" + sID + ") "
		s += sTimeStamp + " "

		if logEntryStruct[0] == "txt":
			sLogMsg = logEntryStruct[6]
			return s + sLogType + ":  " + sLogMsg + ColoredLogMessageFormatter.RESET_COLOR
		elif logEntryStruct[0] == "ex":
			sExClass = logEntryStruct[6]
			sLogMsg = logEntryStruct[7]
			ret = []
			ret.append(s + " "  + sLogType + ":  " + sExClass + ": " + sLogMsg + ColoredLogMessageFormatter.RESET_COLOR)
			if logEntryStruct[8] != None:
				for (stPath, stLineNo, stModuleName, stLine) in logEntryStruct[8]:
					ret.append(s + " STACKTRACE:  " + stPath + ":" + str(stLineNo) + " " + stModuleName + "    # " + stLine)
			return ret
		elif logEntryStruct[0] == "desc":
			sLogMsg = logEntryStruct[6]
			return s + sLogType + ":  " + sLogMsg + ColoredLogMessageFormatter.RESET_COLOR
		else:
			raise Exception()




COLOR_LOG_MESSAGE_FORMATTER = ColoredLogMessageFormatter()









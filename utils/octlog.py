# -*- coding: utf-8 -*-

import sys

sys.path.append("../")

EV_LEVEL_EMERG = 0
EV_LEVEL_ALERT = 1
EV_LEVEL_CRIT = 2
EV_LEVEL_ERROR = 3
EV_LEVEL_WARN = 4
EV_LEVEL_NOTIFY = 5
EV_LEVEL_INFO = 6
EV_LEVEL_DEBUG = 7

event_level = {
	EV_LEVEL_EMERG: "Emerg",
	EV_LEVEL_ALERT: "Alert",
	EV_LEVEL_CRIT: "Crit",
	EV_LEVEL_ERROR: "Error",
	EV_LEVEL_WARN: "Warn",
	EV_LEVEL_NOTIFY: "Notify",
	EV_LEVEL_INFO: "Info",
	EV_LEVEL_DEBUG: "Debug"
}

def get_debug_level(mod):
	return EV_LEVEL_DEBUG

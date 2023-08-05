#!/usr/bin/env python3
'''
Anime module for Nielsen.
'''

import logging
import re
from .config import CONFIG


def generate_filename(info):
	'''Returns a filename based on information in the provided dictionary with
	the following keys:
		- series: Series name
		- episode: Episode number
		- title: Episode title (if found/enabled)
		- tags: Sub group, resolution, version, etc.
		- extension: File extension
	Filename variants:
		[HorribleSubs] Drifters - 01v2 [720p].mkv
	Transformed filename:
		Drifters -01- Fight Song [HorribleSubs 720p v2].mkv
	'''

	patterns = [
		# [HorribleSubs] Drifters - 01v2 [720p].mkv
		re.compile(r"(?P<group>\[.+\])\s+(?P<series>.+)\s+-\s+(?P<episode>\d{2,})(?P<version>v\d)?\s+(?P<resolution>\[.*\])?\.+(?P<extension>\w+)$"),
	]

	tags = re.compile(r"(1080p|720p|HDTV|WEB|PROPER|REPACK|RERIP).*", re.IGNORECASE)

	filename = '{0} -{1}- {2} [{3}].{4}'.format(info['series'],
		info['episode'], info['title'], info['tags'], info['extension'])

	return filename

# vim: tabstop=4 softtabstop=4 shiftwidth=4 noexpandtab

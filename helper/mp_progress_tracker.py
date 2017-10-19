# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
from progressbar import *


class mpProgressTracker:

	def __init__(self, title='', total=0, interval=.1):
		widgets = [title, ': ', Percentage(), ' ', Bar(marker='*',left='[',right=']'), ' ', ETA()]
		self.pbar = ProgressBar(widgets=widgets, maxval=total)
		self.total = total
		self.interval = interval

	def track(self, job):
		self.pbar.start()
		while not job.ready():
			self.pbar.update(self.total - job._number_left)
			time.sleep(self.interval)
		self.pbar.finish()




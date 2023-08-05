
import os, sys, time
from PyQt5.QtWidgets import QApplication
from tweetypy.config import configure, flush_queue
from tweetypy.mainwin import MainWin

def main():
	config = configure()
	try:
		if config['data-files']['log-file']:
			sys.stdout = open(config['data-files']['log-file'], 'w')
	except KeyError:
		pass
	print(f' INFO: TweetyPy started on {time.asctime(time.localtime())}')
	print(' INFO: Version 1.0.0 "Ain\'t She Tweet"')
	print(' INFO: Copyright 2017 Jesse McClure')
	print(' INFO: License: MIT')
	app = QApplication(sys.argv)
	args = sys.argv[1:]
	files = [arg for arg in args if os.path.isfile(arg)]
	flags = [arg for arg in args if arg[0] == '-']
	other = [arg for arg in args if arg not in files + flags]
	# TODO create logger
	if flags:
		print(' WARN: ignoring unrecognized flags: ', flags)
	if other:
		print(' WARN: ignoring unrecognized arguments: ', other)
	flush_queue()
	win = MainWin(files, config)
	return app.exec_()


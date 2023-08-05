
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import qApp, QAction, QFileDialog, QLabel, QMenuBar, QMainWindow, QWidget
from tweetypy.spectrogram import Spectrogram


class MainWin(QMainWindow):
	def __init__(self, files, config):
		super().__init__()
		self.files = files
		self.data = []
		self.saved = True
		self.config = config
		self.setGeometry(0, 0, 800, 600)
		self.setWindowTitle("TweetyPy")
		self.setWindowIcon(QIcon('web.png'))	# TODO FIXME
		if self.config['main-window']['maximized']:
			self.setWindowState(Qt.WindowMaximized)
		self.init_calls()
		self.init_actions()
		self.init_menubar()
		self.init_toolbar()
		self.init_statusbar()
		self.init_body()
		self.show()
		self.spect = None
		# Spectrograms are sized relative to parent window.  The timer allows
		# the window manager to adjust the parent window prior to this sizing.
		if self.files:
			QTimer.singleShot(20,self.next_spectrogram)

	# TODO handle drag & drop of sound files to add to queue
	# and update window title

	def action_unknown(self):
		print(' WARN: unknown action binding')

	def action_add_songs(self):
		fnames, kind = QFileDialog.getOpenFileNames(self, 'Select Audio Files', '', "Audio (*.wav)")
		if not fnames:
			return
		self.files += fnames
		if self.spect:
			self.setWindowTitle(f'TweetyPy: {self.spect.data["name"]} [+{len(self.files)} more]')
		else:
			self.next_spectrogram()

	def action_save(self):
		fname, kind = QFileDialog.getSaveFileName(self, 'Save data file', '', 'Data files (*.txt *.csv)')
		if not fname:
			return
		with open(fname, 'w') as f:
			f.write(self.config['data-files']['header'])
			for data in self.data:
				f.write(self.config['data-files']['format'].format(**data)) # TODO needs testing
		self.saved = True

	def init_calls(self):
		self.calls = {
			'add_songs': self.action_add_songs,
			'fit': lambda: self.spect.fit() if self.spect else None,
			'mode_normal': lambda: self.spect.mode_normal() if self.spect else None,
			'mode_cursor': lambda: self.spect.mode_cursor() if self.spect else None,
			'mode_eraser': lambda: self.spect.mode_eraser() if self.spect else None,
			'next_song': self.next_spectrogram,
			'undo': lambda: self.spect.undo() if self.spect else None,
			#'prev_song':
			'quit': self.close,
			'unknown': self.action_unknown,
		}

	def init_body(self):
		self.body = QWidget()
		self.body.setBackgroundRole(QPalette.AlternateBase)
		self.body.setAutoFillBackground(True)
		self.body.setContentsMargins(10,10,10,10)
		self.setCentralWidget(self.body)

	def init_actions(self):
		self.actions = dict()
		for act in self.config['actions']:
			pix = QPixmap()
			pix.loadFromData(act['icon'])
			a = QAction(QIcon(pix), act['menu'], self)
			a.setShortcut(act['shortcut'])
			a.setStatusTip(act['statustip'])
			if act['name'] in self.calls:
				a.triggered.connect(self.calls[act['name']])
			else:
				a.triggered.connect(self.calls['unknown'])
			self.actions[act['name']] = a

	def init_menubar(self):
		def add_menu(menu, entry):
			if type(entry) is list:
				for e in entry:
					add_menu(menu, e)
			elif type(entry) is dict and 'name' in entry and 'items' in entry:
				sub = menu.addMenu(entry['name'])
				add_menu(sub, entry['items'])
			elif type(entry) is str and entry in self.actions:
				menu.addAction(self.actions[entry])
			elif type(entry) is str and entry == 'bar':
				menu.addSeparator()
		conf = self.config['main-window']
		if 'menu' in conf and type(conf['menu']) is list:
			bar = self.menuBar()
			add_menu(bar, conf['menu'])

	def init_statusbar(self):
		self.statusbar = self.statusBar()
		self.status_text = QLabel()
		self.statusBar().addPermanentWidget(self.status_text)

	def init_toolbar(self):
		for bar in self.config['main-window']['toolbars']:
			toolbar = self.addToolBar(bar['name'])
			toolbar.setVisible(bar['visible'])
			toolbar.setToolButtonStyle(bar['style'])
			for item in bar['items']:
				if item == 'bar':
					toolbar.addSeparator()
				elif item in self.actions:
					toolbar.addAction(self.actions[item])
				else:
					print(f' WARN: unknown toolbar item "{item}"')

	def closeEvent(self, e):
		if self.spect and not self.spect.stored:
			print(' DATA: ' + ' '.join(map(str, self.spect.data.values())))
			self.data.append(self.spect.data)
			self.saved = False
		if not self.saved:
			self.action_save()

	def next_spectrogram(self):
		if self.spect and not self.spect.stored:
			print(' DATA: ' + ' '.join(map(str, self.spect.data.values())))
			self.data.append(self.spect.data)
			self.spect.close()
			self.saved = False
		if self.files:
			self.fname = self.files.pop(0)
			self.spect = Spectrogram(self.fname, self.body, self.config['spectrogram'])
			self.spect.mouseOver.connect(self.update_status)
			title = f'TweetyPy: {self.spect.data["name"]}'
			if self.files:
				title += f' [+{len(self.files)} more]'
			self.setWindowTitle(title)
		else:
			self.fname = None
			self.spect = None

	def update_status(self, x, y):
		self.status_text.setText(f'FEX: {self.spect.data["fex"]:.3}   {x:0.3}s {y:0.1}KHz')



import os, site, tempfile, yaml
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

_queue = []

def configure():
	files = []
	for fname in [ 'icons.yaml', 'actions.yaml', 'menu.yaml', 'config.yaml' ]:
		files += [os.path.join(p, 'tweetypy', fname) for p in site.getsitepackages()]
		if 'XDG_CONFIG_HOME' in os.environ:
			files += [os.path.join(os.environ['XDG_CONFIG_HOME'], 'tweetypy', fname)]
		elif 'HOME' in os.environ:
			files += [os.path.join(os.environ['HOME'], '.config', 'tweetypy', fname)]
		elif 'APPDATA' in os.environ:
			files += os.path.join(os.environ['APPDATA'], 'tweetypy', fname)
		elif 'USERPROFILE' in os.enviorn:
			files += os.path.join(os.environ['USERPROFILE'], 'AppData', 'tweetypy', fname)
		files += [os.path.join(os.getcwd(), fname)]

	# Color constants
	Window = QColor(QPalette.Window).name()
	Background = QColor(QPalette.Background).name()
	WindowText = QColor(QPalette.WindowText).name()
	Foreground = QColor(QPalette.Foreground).name()
	Base = QColor(QPalette.Base).name()
	AlternateBase = QColor(QPalette.AlternateBase).name()
	ToolTipBase = QColor(QPalette.ToolTipBase).name()
	ToolTipText = QColor(QPalette.ToolTipText).name()
	Text = QColor(QPalette.Text).name()
	Button = QColor(QPalette.Button).name()
	ButtonText = QColor(QPalette.ButtonText).name()
	BrightText = QColor(QPalette.BrightText).name()
	Highlight =  QColor(QPalette.Highlight).name()
	# Icon style constants
	IconOnly = Qt.ToolButtonIconOnly
	TextOnly = Qt.ToolButtonTextOnly
	TextBesideIcon = Qt.ToolButtonTextBesideIcon
	TextUnderIcon = Qt.ToolButtonTextUnderIcon
	FollowStyle = Qt.ToolButtonFollowStyle
	# Misc constants
	TempFile = os.path.join(tempfile.gettempdir(), 'tweetypy.log')

	conf = f"""
constants:

   Window: &Window {Window}
   Background: &Background {Background}
   WindowText: &WindowText {WindowText}
   Foreground: &Foreground {Foreground}
   Base: &Base {Base}
   AlternateBase: &AlternateBase {AlternateBase}
   ToolTipBase: &ToolTipBase {ToolTipBase}
   ToolTipText: &ToolTipText {ToolTipText}
   Text: &Text {Text}
   Button: &Button {Button}
   ButtonText: &ButtonText {ButtonText}
   BrightText: &BrightText {BrightText}
   Highlight: &Highlight {Highlight}

   IconOnly: &IconOnly {IconOnly}
   TextOnly: &TextOnly {TextOnly}
   TextBesideIcon: &TextBesideIcon {TextBesideIcon}
   TextUnderIcon: &TextUnderIcon {TextUnderIcon}
   FollowStyle: &FollowStyle {FollowStyle}

   TempFile: &TempFile {TempFile}
"""

	for fname in files:
		global _queue
		if (os.path.isfile(fname)):
			with open(fname, 'r') as fin:
				_queue += [f' INFO: read config from {fname}']
				conf += fin.read()
	return yaml.load(conf)

def flush_queue():
	for line in _queue:
		print(line)


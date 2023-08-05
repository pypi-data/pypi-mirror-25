
import os, wave
from numpy import *
from scipy.signal import spectrogram
from PyQt5.QtCore import pyqtSignal, Qt, QPoint, QRect
from PyQt5.QtGui import QColor, QImage, QPainter, QPainterPath
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QWidget

class Spectrogram(QWidget):

	mouseOver = pyqtSignal(float, float)

	def __init__(self, fname, parent, config):
		super().__init__(parent)
		print(f' INFO: processing {fname}')
		self.conf = config
		self.setMouseTracking(True)
		self.setGeometry(parent.contentsRect())
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.data = {
			'name': os.path.basename(fname),
			'path': fname,
			'pex': 0.0,
			'tex': 0.0,
			'fex': 0.0,
			'notes': ''}
		self.stored = False
		self.init_fft()
		if self.amp is None:
			parent.next_spectrogram()
			self.close()
			return
		self.init_calculations()
		self.init_image()
		self.fit()
		self.eraser = self.init_eraser(10, 200)
		self.eraser.maxheight = 200
		self.cursorX = self.init_cursor(1, self.height() * 4)
		self.cursorY = self.init_cursor(self.width() * 4, 1)
		self.show()

	def init_fft(self):
		fft = self.conf['fft']
		try:
			with wave.open(self.data['path'], 'rb') as song:
				channels, bs, samprate, nsamp, comp, compnam  = song.getparams()
				data = fromstring(song.readframes(nsamp), dtype=uint16)
		except wave.Error:
			print(f' WARN: skipping \"{self.data["path"]}\": not a wave file.')
			return None
		f, t, amp = spectrogram(data, samprate, fft['window-function'],
				fft['window'], fft['overlap'], detrend=False, mode='psd' )
		self.freq = f
		self.time = t
		self.amp = amp

	def init_calculations(self):
		calc = self.conf['calculations']
		bot = argmax(self.freq > calc['high-pass'])
		top = argmin(self.freq < calc['low-pass'])
		self.freq = self.freq[bot:top]
		self.amp = self.amp[bot:top,:]

		self.thresh = self.amp.max() / 10**(calc['threshold'] / 10.0)
		self.thresh = 255.0 - self.thresh * 255.0 / self.amp.max()
		self.amp = 255.0 - self.amp * 255.0 / self.amp.max()

		arr = asarray(self.amp.flat)
		per = 100 * (arr <= self.thresh).sum() / len(arr)
		msg = f'{per:.2}%% of signal is above the threshold.'
		if per > 35.0:
			print(f' WARN: {msg}  Consider using a lower threshold.')
		elif per < 5.0:
			print(f' WARN: {msg}  Consider using a higher threshold.')
		else:
			print(f' INFO: {msg}')

	def init_image(self):
		colors = self.conf['colors']
		self.amp = flipud(self.amp)
		self.amp_back = copy(self.amp)
		self.freq = flipud(self.freq)
		self.imgdata = array(self.amp, uint8)
		h, w = self.imgdata.shape
		self.freq /= 1000.0
		self.image = QImage(self.imgdata.tobytes(), w, h, w, QImage.Format_Grayscale8)
		if colors['invert']:
			self.image.invertPixels()

	def init_cursor(self, w, h):
		cursor = QWidget(self)
		cursor.setAttribute(Qt.WA_TransparentForMouseEvents)
		effect = QGraphicsOpacityEffect(cursor)
		effect.setOpacity(0.4)
		cursor.setGraphicsEffect(effect)
		cursor.setGeometry(0, 0, w, h)
		cursor.setAutoFillBackground(True)
		p = cursor.palette()
		p.setColor(cursor.backgroundRole(), QColor(self.conf['colors']['cursor']))
		cursor.setPalette(p)
		cursor.hide()
		return cursor

	def init_eraser(self, w, h):
		eraser = QWidget(self)
		eraser.setAttribute(Qt.WA_TransparentForMouseEvents)
		effect = QGraphicsOpacityEffect(eraser)
		effect.setOpacity(0.4)
		eraser.setGraphicsEffect(effect)
		eraser.setGeometry(0, 0, w, h)
		eraser.setAutoFillBackground(True)
		p = eraser.palette()
		p.setColor(eraser.backgroundRole(), QColor(self.conf['colors']['eraser']))
		eraser.setPalette(p)
		eraser.hide()
		return eraser

	def fit(self):
		s = self.image.size()
		asp = s.width() / (s.height() * self.conf['scale-ratio'])
		if self.size().height() * asp > self.size().width():
			self.resize(self.width(), self.width() / asp)
		else:
			self.resize(self.height() * asp, self.height())

	def mode_normal(self):
		self.unsetCursor()
		self.eraser.hide()
		self.cursorX.hide()
		self.cursorY.hide()

	def mode_cursor(self):
		self.setCursor(Qt.BlankCursor)
		self.eraser.hide()
		self.cursorX.show()
		self.cursorY.show()

	def mode_eraser(self):
		self.setCursor(Qt.BlankCursor)
		self.cursorX.hide()
		self.cursorY.hide()
		self.eraser.show()

	def undo(self):
		copyto(self.amp, self.amp_back)
		self.update()

	def paintEvent(self, e):
		# TODO refactor this rats nest
		qp = QPainter(self)
		qp.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
		qp.drawImage(self.contentsRect(), self.image, self.image.rect())
		r = QRect(0, 0, self.width() - 1, self.height() - 1)
		qp.setPen(QColor(self.conf['colors']['border']))
		qp.drawRect(r)
		path = QPainterPath()
		pfreq, ptime, pex, tex = 0.0, 0.0, 0.0, 0.0
		qp.setPen(QColor(self.conf['colors']['line']))
		for x, y in enumerate(argmin(self.amp, 0)):
			if self.amp[y,x] > self.thresh:
				continue
			t, f = self.time[x], self.freq[y]
			if self.conf['calculations']['log10-freq']:
				f = log10(f)
			if pfreq == 0.0:
				path.moveTo(x * self.sx, y * self.sy)
			else:
				path.lineTo(x * self.sx, y * self.sy)
				pex += sqrt((f - pfreq)**2 + (t - ptime)**2)
				tex += t - ptime
			ptime, pfreq = t, f
		qp.drawPath(path)
		self.data['pex'] = pex
		self.data['tex'] = tex
		try:
			self.data['fex'] = pex / tex
		except ZeroDivisionError:
			self.data['fex'] = 0.0
		#self.fexChanged.emit() # TODO replace this?

	def resizeEvent(self, e):
		self.sx = self.width() / self.image.width()
		self.sy = self.height() / self.image.height()

	def mousePressEvent(self, e):
		if self.cursorX.isVisible():
			pass
		elif self.eraser.isVisible():
			copyto(self.amp_back, self.amp)
			pass
		elif e.button() == Qt.MiddleButton:
			self.fit()
		else:
			self.__pos = self.pos()
			self.__size = self.size()
			self.__epos = self.mapToParent(e.pos())

	def mouseMoveEvent(self, e):
		# TODO refactor this rats nest
		# TODO add eraser size changes
		y = e.pos().y()
		if y < self.eraser.maxheight / 2.0:
			fixed = y * 2.0
		elif y > self.height() - self.eraser.maxheight / 2.0:
			fixed = (self.height() - y) * 2.0
		else:
			fixed = self.eraser.maxheight
		self.eraser.setFixedHeight(int(clip(fixed,0,self.eraser.maxheight)))
		x = e.pos().x() - self.eraser.width() / 2.0
		y = e.pos().y() - self.eraser.height() / 2.0
		self.eraser.move(x, y)

		x = e.pos().x()
		y = e.pos().y()
		self.cursorX.move(x, 0)
		self.cursorY.move(0, y)
		s = self.imgdata.shape
		x = clip(int(s[1] * e.pos().x() / self.width()), 0, self.time.size)
		y = clip(int(s[0] * e.pos().y() / self.height()), 0, self.freq.size)
		self.mouseOver.emit(self.time[x], self.time[y])
		if e.buttons() and self.cursorX.isVisible():
			self.mouseCursorEvent(e)
		elif e.buttons() and self.eraser.isVisible():
			self.mouseEraseEvent(e)
		elif e.buttons():
			self.mouseNormalEvent(e)

	def mouseCursorEvent(self, e):
		pass

	def mapToImgdata(self, x, y):
		s = self.imgdata.shape
		x *= s[1] / self.width()
		y *= s[0] / self.height()
		x = int(clip(x, 0, s[1]))
		y = int(clip(y, 0, s[0]))
		return x, y

	def mouseEraseEvent(self, e):
		w = self.eraser.width()
		h = self.eraser.height()
		x = e.pos().x() - w / 2.0
		y = e.pos().y() - h / 2.0
		x1, y1 = self.mapToImgdata(x, y)
		x2, y2 = self.mapToImgdata(x + w, y + h)
		self.amp[y1:y2,x1:x2] = 255.0
		self.update(x, 0, w, self.height())
		self.stored = False

	def mouseNormalEvent(self, e):
		if e.buttons() == Qt.LeftButton:
			diff = self.mapToParent(e.pos()) - self.__epos + self.__pos
			self.move(diff)
		elif e.buttons() == Qt.RightButton:
			diff = self.mapToParent(e.pos()) - self.__epos
			w = self.__size.width() + diff.x()
			h = self.__size.height() + diff.y()
			self.resize(w, h)

	def mouseReleaseEvent(self, e):
		self.cursorX.resize(1, self.height() * 4)
		self.cursorY.resize(self.width() * 4, 1)
		self.update(self.contentsRect())


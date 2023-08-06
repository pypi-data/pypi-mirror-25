#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets


class FixedWidget(QtWidgets.QWidget):
    def _fixWindow(self):
        self.resize(0, 0)
        geometry = self.geometry()
        self.setFixedSize(geometry.width(), geometry.height())

    def fixWindow(self):
        QtCore.QTimer.singleShot(0, self._fixWindow)

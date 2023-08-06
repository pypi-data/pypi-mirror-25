#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from PyQt5 import QtCore, QtNetwork
import auxygen
from ..controller.config import Config


class Pilatus(QtCore.QObject):
    sigScanStepReady = QtCore.pyqtSignal()
    sigExperimentFinished = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.logger = auxygen.devices.logger.Logger('Dectris')
        self.scanCbfName = ''
        self.guiStarted = False
        self.timestamp = None
        self.energy = None
        self.address = None
        self.createSocket()

    def setGuiStarted(self):
        self.guiStarted = True

    # noinspection PyUnresolvedReferences
    def createSocket(self):
        self.socket = QtNetwork.QTcpSocket(self)
        self.socket.setProxy(QtNetwork.QNetworkProxy(QtNetwork.QNetworkProxy.NoProxy))
        self.socket.connected.connect(self.sendFirstRequest)
        self.socket.readyRead.connect(self.readResponse)
        self.socket.disconnected.connect(self.serverHasStopped)
        self.socket.error.connect(self.serverHasError)

    def setConfig(self):
        self.separator = chr(int(Config.Separator)).encode('ascii')
        self.readout1 = float(Config.Readout1)
        self.readout2 = float(Config.Readout2)
        self.thresholdTimeout = float(Config.ThresholdTimeout or 60)
        if self.address and self.address != Config.DetAddress:
            self.connectDetector()
        self.setEnergy()

    def connectDetector(self):
        self.stop()
        if Config.DetAddress:
            try:
                host, port = Config.DetAddress.split(':')
                port = int(port)
            except (IndexError, ValueError):
                self.logger.error(f'Detector address "{Config.DetAddress}" is not correct, connection is not possible')
            else:
                self.address = Config.DetAddress
                self.createSocket()
                self.socket.connectToHost(host, port)

    def serverHasError(self):
        msg = self.socket.errorString()
        self.logger.error(f'Cannot connect to Pilatus. Message: {msg}')
        self.stop()

    def send(self, cmd):
        if not self.guiStarted:
            return
        if self.isConnected():
            self.socket.write(f'{cmd}\n'.encode(encoding='ascii', errors='ignore'))
        else:
            self.logger.error('Detector is not connected, check the camserver')

    def readResponse(self):
        data = self.socket.readAll()
        for s in bytes(data).split(self.separator):
            s = s.strip().decode(errors='ignore')
            if not s:
                continue
            self.logger.info(s)
            if self.scanCbfName and self.scanCbfName in s:
                self.scanCbfName = ''
                self.sigScanStepReady.emit()
            if '7 OK' in s:
                self.sigExperimentFinished.emit()

    def serverHasStopped(self):
        self.logger.warn('Dectris Pilatus server has been stopped')
        self.stop()

    def sendFirstRequest(self):
        self.send(f'Imgpath {Config.ServerDir}')
        self.logger.info('Connected to the Dectris Pilatus camera')
        self.emptyExposure()

    def abort(self):
        self.send('K')

    def stop(self):
        self.socket.disconnectFromHost()

    def emptyExposure(self):
        self.initExperiment(0.1, 1)
        self.shot('_empty.cbf')

    def setEnergy(self, energy=None):
        if energy:
            self.energy = energy * 1e3
        if Config.AdjustThreshold and self.energy:
            timestamp = time.time()
            if self.timestamp is None:
                self.timestamp = timestamp
                self.send(f'SetEnergy {self.energy}')
                self.logger.info(f'Setting energy for the camera: {self.energy:.0f} eV')
            else:
                if timestamp - self.timestamp >= self.thresholdTimeout:
                    self.timestamp = None
                    QtCore.QTimer.singleShot(0, self.setEnergy)
                else:
                    QtCore.QTimer.singleShot(1000, self.setEnergy)

    def initExperiment(self, expPeriod, nframes, settings=None):
        readoutTime = self.readout2 if nframes > 1 and expPeriod > 15 else self.readout1
        self.send(f'ExpTime {expPeriod - readoutTime:f}')
        self.send(f'ExpPeriod {expPeriod:f}')
        self.send(f'NImages {nframes:d}')
        for s in settings or {}:
            self.send(f'MXSettings {s} {settings[s]}')

    def exposure(self, cbfName):
        self.send(f'ExtMTrigger {cbfName}')

    def shot(self, cbfName):
        self.send(f'Exposure {cbfName}')

    def scanShot(self, cbfName=''):
        if cbfName:
            self.shot(cbfName)
        self.scanCbfName = cbfName

    def isConnected(self):
        return self.socket.state() == self.socket.ConnectedState

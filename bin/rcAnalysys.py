#!/usr/bin/env python3

import argparse
import os
import re
import sys
import sqlite3
from PySide2.QtWidgets import (QPushButton, QGroupBox, QVBoxLayout, QHBoxLayout, QRadioButton, QComboBox, QWidget,
                               QApplication,QFileDialog,
                               QLabel, QLineEdit)
from PySide2.QtCore import Slot




class RcAnalysisGui(QWidget):
    def __init__(self ):
        super(RcAnalysisGui, self).__init__()


        self.__mainLayout = QVBoxLayout()
        self.__mainRunWidges = {}

        self.__selectGroup = QGroupBox("select sql database")
        self.__selectGroup.setLayout(QHBoxLayout())

        self.__selectWidget = QPushButton("browse")
        self.__selectWidget.clicked.connect(self.selectFile)
        self.__selectGroup.layout().addWidget(self.__selectWidget)

        self.__sqlPath = QLineEdit()
        self.__sqlPath.setReadOnly(True)
        self.__selectGroup.layout().addWidget(self.__sqlPath)
        self.__mainLayout.addWidget(self.__selectGroup)

        # add netA/netB gui
        self.__netA = SelectNet("netA", [])
        self.__netB = SelectNet("netB", [])
#        self.netA = self.__netA
#        self.netB = self.__netB
        self.__mainLayout.addWidget(self.__netA)
        self.__mainLayout.addWidget(self.__netB)

        self.__resultGroup = QGroupBox("results")
        self.__resultGroup.setLayout(QHBoxLayout())

        self.__runWidget = QPushButton("report coupling")
        self.__runWidget.clicked.connect(self.checkCoupling)
        self.__resultGroup.layout().addWidget(self.__runWidget)

        self.__coupVal = QLineEdit()
        self.__coupVal.setReadOnly(True)
        self.__resultGroup.layout().addWidget(self.__coupVal)

        self.__plotNetAWidget = QPushButton("plot netA")
        self.__plotNetAWidget.clicked.connect(lambda: self.plotNet("netA"))
        self.__resultGroup.layout().addWidget(self.__plotNetAWidget)

        self.__clearNetAWidget = QPushButton("clear netA")
        self.__clearNetAWidget.clicked.connect(lambda: self.clearNet("netA"))
        self.__resultGroup.layout().addWidget(self.__clearNetAWidget)

        self.__plotNetBWidget = QPushButton("plot netB")
        self.__plotNetBWidget.clicked.connect(lambda: self.plotNet("netB"))
        self.__resultGroup.layout().addWidget(self.__plotNetBWidget)

        self.__clearNetBWidget = QPushButton("clear netB")
        self.__clearNetBWidget.clicked.connect(lambda: self.clearNet("netB"))
        self.__resultGroup.layout().addWidget(self.__clearNetBWidget)
        self.__mainLayout.addWidget(self.__resultGroup)

        self.setLayout(self.__mainLayout)
        title = f"rc analysis"
        self.setWindowTitle(title)
        self.show()

    @Slot()
    def selectFile(self):
#        app = QApplication([])
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        sqlFile, _ = QFileDialog.getOpenFileName(
            None,
            "QFileDialog.getOpenFileName()",
            "",
            "All Files (*);;Python Files (*.py)",
            options=options,
        )
        self.__sqlPath.setText(sqlFile)

        # initializa sqlite connect
        self.__conn = sqlite3.connect(sqlFile)
        self.__c = self.__conn.cursor()
        self.__cnets = self.__c.execute("SELECT NETNAME from TNETNAME")
        self.__nets = list(map(lambda x: x[0], self.__cnets))
        self.__netA.setNets(self.__nets)
        self.__netB.setNets(self.__nets)
#        self.__netA.__net.clear()
#        self.__netA.__net.additems(self.__nets)


    @ Slot()
    def checkCoupling(self):
        netA = self.__netA.getNet()
        netB = self.__netB.getNet()
        self.__c.execute(
            f'SELECT  NETA,SEGA,NETB,SEGB,VALUE from TC WHERE (NETA = "{netA}" AND NETB = "{netB}") OR (NETA = "{netB}" AND NETB = "{netA}")')
        coupNets = self.__c.fetchall()
        self.__netAPts = []
        self.__netBPts = []
        cTotal = 0
        self.__coupVal.setText(f'{str(cTotal)}f')
        for (net1, net1_seg, net2, net2_seg, capVal) in coupNets:
            #            print(netA,segA,netB,segB,capVal)
            if net1 == netA:
                netA_seg = net1_seg
                netB_seg = net2_seg
            if net2 == netA:
                netA_seg = net2_seg
                netB_seg = net1_seg
            self.getCoor(netA, netA_seg, self.__netAPts)
            self.getCoor(netB, netB_seg, self.__netBPts)
            cTotal = cTotal + capVal
            cTotal = round(cTotal,5)
            self.__coupVal.setText(f'{str(cTotal)}f')

    @Slot()
    def plotNet(self, text):
        if text == "netA":
            pts = self.__netAPts
            layer = 'list("y1" "drawing")'
        if text == "netB":
            pts = self.__netBPts
            layer = 'list("y2" "drawing")'
        for pt in pts:
            print(f'ODEplotHilight(list({pt}) {layer})',file=sys.stdout,flush=True)


    @Slot()
    def clearNet(self, text):
        print("ODEclearHilight()",flush=True)

    #            self.__c.execute(
    #                f'SELECT COOR from TR WHERE (NETA = "{netA}" AND SEGA = "{segA}") OR (NETB = "{netA}" AND SEGB = "{segA}")')
    #            resACoors = self.__c.fetchall()
    #            for coor in resACoors:
    #                print(coor)

    #            self.__c.execute(f'SELECT COOR from TR WHERE (NETA = "{netB}" AND SEGA = "{segB}") OR (NETB = "{netB}" AND SEGB = "{segB}")')
    #            resB = self.__c.fetchall()
    #            print("R2 is :",list(resB))

    def getCoor(self, net, seg, pts):
        self.__c.execute(
            f'SELECT COOR from TR WHERE (NETA = "{net}" AND SEGA = "{seg}") OR (NETB = "{net}" AND SEGB = "{seg}")')
        coors = self.__c.fetchall()
        for coor in coors:
            pts.append(coor[0])


#        print(list(coupNets))

class SelectNet(QGroupBox):
    def __init__(self, netAB, nets):
        QGroupBox.__init__(self, f"{netAB}")
        self.__netGroup = QGroupBox(netAB)
        self.__mainLayout = QVBoxLayout()

        self.__net = QComboBox()
        self.__net.addItems(nets)
        self.__nets = []

        self.__netInput = QLineEdit()
        self.__netInput.textChanged.connect(self.updatePath)
        self.__mainLayout.addWidget(self.__netInput)

        self.__mainLayout.addWidget(self.__net)

        self.setLayout(self.__mainLayout)

    #        self.__netGroup.setLayout(self.__mainLayout)

    def setNets(self,nets):
        self.__net.clear()
        self.__net.addItems(nets)
        self.__nets = nets

    def getNet(self):
        return self.__net.currentText()

    def updatePath(self, netPartial):
        matchNets = []
        for net in self.__nets:
            if re.search(f"{netPartial}", net):
                matchNets.append(net)
        self.__net.clear()
        self.__net.addItems(matchNets)


app = QApplication()
gui = RcAnalysisGui()
app.exec_()

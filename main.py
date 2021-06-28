# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import PyQt5
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QLabel
import glob
import os
from utils import *
import json

_translate = QtCore.QCoreApplication.translate
#device = torch.device("cpu")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 1200)


        self.tab_im = []
        self.path = ""
        self.output = ""
        self.i = 0

        self.X = None
        self.Y = None
        self.img = None
        self.bboxes = None

        self.labels = {}

        self.size_full = (765, 1360)
        self.size_head = (400, 600)
        self.size_eyes = (200, 300)

        self.size = (800, 800)

        self.r = 0

        self.checked = None
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")


        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addStretch()

        self.progress = QtWidgets.QLabel("")
        self.progress.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.progress)

        self.looking = QtWidgets.QCheckBox("Looking")
        self.not_looking = QtWidgets.QCheckBox("Not looking")
        self.dont_know = QtWidgets.QCheckBox("Can't say")

        self.group = QtWidgets.QButtonGroup()
        self.group.addButton(self.looking)
        self.group.addButton(self.not_looking)
        self.group.addButton(self.dont_know)

        self.looking.setObjectName("Looking")
        self.verticalLayout.addWidget(self.looking)

        self.not_looking.setObjectName("Not looking")
        self.verticalLayout.addWidget(self.not_looking)

        self.dont_know.setObjectName("Can't say")
        self.verticalLayout.addWidget(self.dont_know)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)


        self.horizontalLayout.addLayout(self.verticalLayout)
        self.kps = False
        self.photo = QtWidgets.QLabel(self.centralwidget)
        #self.photo.setMaximumSize(QtCore.QSize(self.size[0], self.size[1]))
        self.photo.setText("")
        self.photo.setPixmap(QtGui.QPixmap(""))
        #self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.horizontalLayout.addWidget(self.photo)
        self.legend = QtWidgets.QLabel(self.centralwidget)
        self.legend = QtWidgets.QLabel(self.centralwidget)
        self.legend.setPixmap(QtGui.QPixmap(""))
        self.horizontalLayout.addWidget(self.legend)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1125, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)


        self.menubar.addAction(self.menuFile.menuAction())
        self.last_x, self.last_y = None, None
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.click)
        self.pushButton_4.clicked.connect(self.click_back)

        self.pushButton.setShortcut(QtGui.QKeySequence("d"))
        self.pushButton_4.setShortcut(QtGui.QKeySequence("a"))

        self.looking.setShortcut(QtGui.QKeySequence("i"))
        self.not_looking.setShortcut(QtGui.QKeySequence("o"))
        self.dont_know.setShortcut(QtGui.QKeySequence("p"))


        self.actionOpen.triggered.connect(self.click_directory)
        self.group.buttonClicked.connect(self.checked_button)


    def show_im(self, im):
        im_size = cv2.imread(im).shape
        if 'body' in self.type:
            im_size = self.size_full
        elif 'head' in self.type:
            im_size = self.size_head
        else:
            im_size = self.size_eyes
        pixmap = QtGui.QPixmap(im)
        pixmap = pixmap.scaled(im_size[1], im_size[0], QtCore.Qt.KeepAspectRatio)
        self.photo.setPixmap(pixmap)
        #self.photo.setMaximumSize(QtCore.QSize(im_size[1], im_size[0]))


    def click_directory(self):
        self.kps = False
        self.path = str(QFileDialog.getExistingDirectory(self.menuFile, "Select Directory"))
        self.type = self.path.split('/')[-1]
        self.tab_im = sorted(glob.glob(self.path+'/*.jpg'))+sorted(glob.glob(self.path+'/*.png'))
        legend_file = [im for im in self.tab_im if 'legend' in im]
        if len(legend_file) > 0:
            legend_path = legend_file[0]
            self.tab_im.remove(legend_path)
            legend_pixmap = QtGui.QPixmap(legend_path)
            self.kps = True
            self.legend.setPixmap(legend_pixmap)
        else:
            self.legend.setPixmap(QtGui.QPixmap())

        self.output = self.path.split('/')[-1]
        # Add file txt file to select images and filter list
        self.i = 0
        self.checked = None
        if len(self.tab_im) > 0:
            #self.photo.setPixmap(QtGui.QPixmap(self.tab_im[self.i]))
            self.show_im(self.tab_im[self.i])
            self.img = self.tab_im[self.i].split('/')[-1]
            self.progress.setText(f'Progress: {self.i+1}/{len(self.tab_im)}')



    def checked_button(self):
        if self.group.checkedButton() == self.looking:
            self.checked = 1
        elif self.group.checkedButton() == self.not_looking:
            self.checked = 0
        elif self.group.checkedButton() == self.dont_know:
            self.checked = -1
        self.click()


    def reset_buttons(self):
        self.group.setExclusive(False)
        for button in self.group.buttons():
            button.setChecked(False)
        self.group.setExclusive(True)

    def click(self):
        if self.checked == None:
            alert = QtWidgets.QMessageBox()
            alert.setText('Please select a label before moving on.')
            alert.exec_()
        else:
            if len(self.tab_im) != 0:
                self.labels[self.img] = self.checked
                if self.i < len(self.tab_im)-1:
                    self.i += 1
                    self.show_im(self.tab_im[self.i])

                else:
                    self.i = 0
                    alert = QtWidgets.QMessageBox()
                    alert.setText('Thanks! You labeled all the images! You can quit the application.')
                    with open(f'labels/{self.output}.json', 'w', encoding='utf-8') as f:
                        json.dump(self.labels, f)
                    alert.exec_()
                    self.show_im(self.tab_im[self.i])

                self.X = None
                self.Y = None
                self.img = self.tab_im[self.i].split('/')[-1]
                self.bboxes = None
                self.checked = None
                self.progress.setText(f'Progress: {self.i+1}/{len(self.tab_im)}')
                self.reset_buttons()


    def click_back(self):

        if len(self.tab_im) != 0:
            #self.labels[self.img] = self.checked
            if self.i == 0:
                self.i += len(self.tab_im)-1
            else:
                self.i -= 1
            self.show_im(self.tab_im[self.i])
            self.X = None
            self.Y = None
            self.img = self.tab_im[self.i].split('/')[-1]
            self.bboxes = None
            self.checked = None
            self.progress.setText(f'Progress: {self.i+1}/{len(self.tab_im)}')
            self.reset_buttons()



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Looking or not: Human performance", "Looking or not: Human performance"))
        self.pushButton.setText(_translate("MainWindow", "Next Image"))
        self.pushButton_4.setText(_translate("MainWindow", "Previous Image"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))


if __name__ == "__main__":
    import sys
    import os
    if not os.path.exists('labels'):
        os.makedirs('labels')
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowIcon(QtGui.QIcon('logo.png'))
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

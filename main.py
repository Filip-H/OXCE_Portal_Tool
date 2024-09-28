import sys


import yaml
from PyQt6.QtGui import QIntValidator

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QComboBox, QSlider, QGridLayout, QLabel, QPushButton, \
    QMessageBox




def updateSlider(object):
    object.slider_label.setText(f'Number of aliens: {object.slider.value()}')

def addList(combobox):
    with open('spawners.yml', 'r') as spawnerfile:
        spawnerlist = yaml.safe_load(spawnerfile)

        for spawners in spawnerlist:
            combobox.addItem(str(spawners))




def portalButtonClick(object):
    try:
        x = int(object.lineX.text())
    except ValueError:
        MainWindow.Coordswarning(window)
        return
    try:
        y = int(object.lineY.text())
    except ValueError:
        MainWindow.Coordswarning(window)
        return
    try:
        z = int(object.lineZ.text())
    except ValueError:
        MainWindow.Coordswarning(window)
        return

    object.lineX.setEnabled(False)
    object.lineY.setEnabled(False)
    object.lineZ.setEnabled(False)
    object.portalButton.setEnabled(False)
    object.active = True
    yamlfunctions.createPortal(object.name,x,y,z)

def resetClick(list):
    for object in list:
        if object.active:
            object.lineX.clear()
            object.lineY.clear()
            object.lineZ.clear()
            object.lineX.setEnabled(True)
            object.lineY.setEnabled(True)
            object.lineZ.setEnabled(True)
            object.portalButton.setEnabled(True)





class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('OXCE Unit Spawner')
        self.setGeometry(500, 200, 800, 200)

        self.savePath = QLineEdit(self,placeholderText = "insert savefile path", clearButtonEnabled=True)

        self.spawnButton = QPushButton('Spawn Aliens')


        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.savePath,0,0,1,3,alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.spawnButton,6,4,1,3,alignment=Qt.AlignmentFlag.AlignBottom)

        alpha = portal(1, self, layout,"alpha")
        bravo = portal(2, self, layout,"bravo")
        charlie = portal(3, self, layout,"charlie")
        delta = portal(4, self, layout, "delta")
        echo = portal(5,self, layout, "echo")

        portalList = [alpha,bravo,charlie,delta,echo]
        self.spawnButton.clicked.connect(lambda: yamlfunctions.spawnClick(portalList))

        self.spawnButton = QPushButton('Reset Portals')
        self.spawnButton.clicked.connect(lambda: resetClick(portalList))
        layout.addWidget(self.spawnButton,0,3,alignment=Qt.AlignmentFlag.AlignTop)

        self.show()

    def Coordswarning(object):
        QMessageBox.warning(object,'Error','Invalid Input')
    def PathWarning(object):
        QMessageBox.warning(object,'Error','Invalid Path')

class portal():

    def __init__(self, gridY, window, layout, name):

            self.gridY = gridY
            self.window = window
            self.layout = layout
            self.name = name
            self.active = False

            onlyInt = QIntValidator()
            onlyInt.setRange(0, 999)

            self.lineX = QLineEdit(window, placeholderText="x")
            self.lineX.setValidator(onlyInt)
            self.lineY = QLineEdit(window, placeholderText="y")
            self.lineY.setValidator(onlyInt)
            self.lineZ = QLineEdit(window, placeholderText="z")
            self.lineZ.setValidator(onlyInt)

            self.portalButton = QPushButton('Spawn Portal')

            self.portalButton.clicked.connect(lambda: portalButtonClick(self))

            self.slider = QSlider(Qt.Orientation.Horizontal, window)
            self.slider.setRange(0, 20)
            self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)

            self.slider_label = QLabel('Number of aliens: 0', window)
            self.slider.valueChanged.connect(lambda: updateSlider(self))


            self.combobox = QComboBox(window)
            addList(self.combobox)


            layout.addWidget(self.lineX, gridY, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.lineY, gridY, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.lineZ, gridY, 2, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.portalButton, gridY, 3, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.slider, gridY, 4, alignment=Qt.AlignmentFlag.AlignRight)
            layout.addWidget(self.slider_label, gridY, 5, alignment=Qt.AlignmentFlag.AlignRight)
            layout.addWidget(self.combobox, gridY, 6, alignment=Qt.AlignmentFlag.AlignRight)

class yamlfunctions():
    def createPortal(name,x,y,z):
        try:
            with open(window.savePath.text(), 'r') as savefile:
                data = list(yaml.safe_load_all(savefile))
                saveGame = data[1]
                battleGame = saveGame.get('battleGame')
                units = battleGame.get('units')
                idList = []
                for targets in units:
                    targetId = targets.get('id')
                    idList.append(targetId)
                maxId = max(idList)
                maxId = maxId + 1
                coords = [x,y,z]

                with open('templates.yml','r') as templatefile:
                    templatelist = yaml.safe_load(templatefile)
                    template = templatelist[0]
                    template['id']  = maxId
                    template['position'] = coords
                    units.append(template)
        except FileNotFoundError:
            MainWindow.PathWarning(window)
        try:
            with  open(window.savePath.text(), 'w') as savefile:
                yaml.Dumper.ignore_aliases = lambda *args: True
                yaml.dump_all(data, savefile)
        except FileNotFoundError:
            MainWindow.PathWarning(window)
    def spawnClick(portals):
        for objects in portals:
            if objects.active:
                try:
                    with open(window.savePath.text(), 'r') as savefile:
                        data = list(yaml.safe_load_all(savefile))
                        saveGame = data[1]
                        battleGame = saveGame.get('battleGame')
                        items = battleGame.get('items')
                        idList = []
                        for targets in items:
                            targetId = targets.get('id')
                            idList.append(targetId)
                        maxId = max(idList)
                        maxId = maxId + 1

                        x = int(objects.lineX.text())
                        y = int(objects.lineY.text())
                        z = int(objects.lineZ.text())
                        coords = [x,y,z]

                        with open('templates.yml', 'r') as templatefile:
                            templatelist = yaml.safe_load(templatefile)
                            template = templatelist[1]
                            template['position'] = coords
                            template['type'] = objects.combobox.currentText()
                            count = 0
                            while count < objects.slider.value():
                                template['id'] = int(maxId)
                                items.append(dict(template))
                                maxId = maxId + 1
                                count = count + 1
                except FileNotFoundError:
                    MainWindow.PathWarning(window)
                try:
                    with  open(window.savePath.text(), 'w') as savefile:
                        yaml.Dumper.ignore_aliases = lambda *args: True
                        yaml.dump_all(data, savefile)
                except FileNotFoundError:
                    MainWindow.PathWarning(window)






if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())

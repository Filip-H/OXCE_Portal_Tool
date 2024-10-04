import sys
import yaml

from playsound import playsound
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
    yamlfunctions.createPortal(object.name,x,y,z, object)

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
            object.slider.setValue(0)
            object.active = False
    playsound('Sounds/note.wav')


def singleReset(object):
    if object.active:
        object.lineX.clear()
        object.lineY.clear()
        object.lineZ.clear()
        object.lineX.setEnabled(True)
        object.lineY.setEnabled(True)
        object.lineZ.setEnabled(True)
        object.portalButton.setEnabled(True)
        object.slider.setValue(0)
        object.active = False
        playsound('Sounds/note.wav')
        return

    playsound('Sounds/error.wav')




class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('OXCE Unit Spawner')
        self.setGeometry(500, 200, 1000, 200)

        self.savePath = QLineEdit(self,placeholderText = "insert savefile path", clearButtonEnabled=True)

        self.spawnButton = QPushButton('Spawn Aliens')


        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.savePath,0,0,1,3,alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.spawnButton,21,4,1,3,alignment=Qt.AlignmentFlag.AlignBottom)

        a = portal(1, self, layout,"a")
        b = portal(2, self, layout,"b")
        c = portal(3, self, layout,"c")
        d = portal(4, self, layout, "d")
        e = portal(5,self, layout, "e")
        f = portal(6,self, layout, "f")
        g = portal(7,self, layout, "g")
        h = portal(8,self, layout, "h")
        i = portal(9,self, layout, "i")
        j = portal(10,self, layout, "j")
        k = portal(11,self, layout, "k")
        m = portal(12,self, layout, "m")
        n = portal(13,self, layout, "n")
        o = portal(14,self, layout, "o")
        p = portal(15,self, layout, "p")
        q = portal(16,self, layout, "q")
        r = portal(17,self, layout, "r")
        s = portal(18,self, layout, "s")
        t = portal(19,self, layout, "t")
        u = portal(20,self, layout, "u")


        portalList = [a,b,c,d,e,f,g,h,i,j,k,m,n,o,p,q,r,s,t,u]
        self.spawnButton.clicked.connect(lambda: yamlfunctions.spawnClick(portalList))

        self.resetButton = QPushButton('Reset Portals')
        self.resetButton.clicked.connect(lambda: resetClick(portalList))
        layout.addWidget(self.resetButton,0,3,alignment=Qt.AlignmentFlag.AlignTop)

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
            self.slider.setRange(0, 8)
            self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)

            self.slider_label = QLabel('Number of aliens: 0', window)
            self.slider.valueChanged.connect(lambda: updateSlider(self))


            self.combobox = QComboBox(window)
            addList(self.combobox)

            self.resetButton =  QPushButton('Reset')
            self.resetButton.clicked.connect(lambda: singleReset(self))

            self.singleSpawnButton = QPushButton('Spawn')
            self.singleSpawnButton.clicked.connect(lambda: yamlfunctions.singleSpawn(self))


            layout.addWidget(self.lineX, gridY, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.lineY, gridY, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.lineZ, gridY, 2, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.portalButton, gridY, 3, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.slider, gridY, 4, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.slider_label, gridY,5, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.combobox, gridY,6, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.resetButton, gridY,7, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.singleSpawnButton, gridY, 8, alignment=Qt.AlignmentFlag.AlignLeft)

class yamlfunctions():
    def createPortal(name,x,y,z, object):
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
            singleReset(object)
            return
        try:
            with  open(window.savePath.text(), 'w') as savefile:
                yaml.Dumper.ignore_aliases = lambda *args: True
                yaml.dump_all(data, savefile)
                playsound('Sounds/note.wav')
        except FileNotFoundError:
            MainWindow.PathWarning(window)
            singleReset(object)
            return
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
                    return
                try:
                    with  open(window.savePath.text(), 'w') as savefile:
                        yaml.Dumper.ignore_aliases = lambda *args: True
                        yaml.dump_all(data, savefile)
                except FileNotFoundError:
                    MainWindow.PathWarning(window)
                    return
        playsound('Sounds/note.wav')

    def singleSpawn(object):
            if object.active:
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

                        x = int(object.lineX.text())
                        y = int(object.lineY.text())
                        z = int(object.lineZ.text())
                        coords = [x,y,z]

                        with open('templates.yml', 'r') as templatefile:
                            templatelist = yaml.safe_load(templatefile)
                            template = templatelist[1]
                            template['position'] = coords
                            template['type'] = object.combobox.currentText()
                            count = 0
                            while count < object.slider.value():
                                template['id'] = int(maxId)
                                items.append(dict(template))
                                maxId = maxId + 1
                                count = count + 1
                except FileNotFoundError:
                    MainWindow.PathWarning(window)
                    return
                try:
                    with  open(window.savePath.text(), 'w') as savefile:
                        yaml.Dumper.ignore_aliases = lambda *args: True
                        yaml.dump_all(data, savefile)
                        playsound('Sounds/note.wav')
                        return
                except FileNotFoundError:
                    MainWindow.PathWarning(window)
                    return

            playsound('Sounds/error.wav')
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())

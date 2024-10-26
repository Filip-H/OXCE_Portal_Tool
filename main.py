import sys
from http.cookiejar import debug

import yaml

from playsound import playsound
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QComboBox, QSlider, QGridLayout, QLabel, QPushButton, \
    QMessageBox

colourlist = ['QPushButton {background-color: blue;}','QPushButton {background-color: red;}','QPushButton {background-color: green;}','QPushButton {background-color: purple;}','QPushButton {background-color: brown;}','QPushButton {background-color: gray;}','QPushButton {background-color: black;}']

with open("config.yml", 'r') as configfile:
    configdata = yaml.safe_load(configfile)
    defaultpath = configdata['defaultPath']

with open("translation.yml", 'r') as translationfile:
    translations = yaml.safe_load(translationfile)

with open('spawners.yml', 'r') as spawnerfile:
    spawners = yaml.safe_load(spawnerfile)
    spawnerlist = []
    try:
        spawnerlist.extend(spawners['single'])
    except TypeError:
        print('no single spawners')

    try:
        spawnerlist.extend(spawners['recurring'])
    except TypeError:
        print('no recurring spawners')
    safeSpawnerList = list(spawnerlist)
    for x in range(0,len(spawnerlist)):
        if spawnerlist[x] in translations:
            spawnerlist[x] = translations[spawnerlist[x]]
    reversetranslation = dict(translations)
    reversetranslation = {v: k for k, v in reversetranslation.items()}



def updateSlider(portal):
    portal.slider_label.setText(f'Number of aliens: {portal.slider.value()}')

def addList(combobox):

        for spawners in spawnerlist:
            combobox.addItem(str(spawners))

def portalButtonClick(portal):
    if portal.active == False:
        try:
            x = int(portal.lineX.text())
        except ValueError:
            MainWindow.Coordswarning(window)
            return
        try:
            y = int(portal.lineY.text())
        except ValueError:
            MainWindow.Coordswarning(window)
            return
        try:
            z = int(portal.lineZ.text())
        except ValueError:
            MainWindow.Coordswarning(window)
            return

        portal.lineX.setEnabled(False)
        portal.lineY.setEnabled(False)
        portal.lineZ.setEnabled(False)
        portal.portalButton.setEnabled(False)
        portal.active = True
        yamlfunctions.createPortal(portal.name,x,y,z, portal)
        return
    playsound('Sounds/error.wav')

def resetClick(list):
    for portal in list:
        if portal.active:
            portal.lineX.clear()
            portal.lineY.clear()
            portal.lineZ.clear()
            portal.lineX.setEnabled(True)
            portal.lineY.setEnabled(True)
            portal.lineZ.setEnabled(True)
            portal.portalButton.setEnabled(True)
            portal.slider.setValue(0)
            portal.active = False
            portal.id = 0
            portal.colorNumber = 0
            portal.singleSpawnButton.setStyleSheet('QPushButton {background-color: white;}')
    window.portalNumber = 0
    playsound('Sounds/note.wav')


def singleReset(portal):
    if portal.active:
        portal.lineX.clear()
        portal.lineY.clear()
        portal.lineZ.clear()
        portal.lineX.setEnabled(True)
        portal.lineY.setEnabled(True)
        portal.lineZ.setEnabled(True)
        portal.portalButton.setEnabled(True)
        portal.slider.setValue(0)
        portal.active = False
        portal.id = 0
        portal.colorNumber = 0
        playsound('Sounds/note.wav')
        portal.singleSpawnButton.setStyleSheet('QPushButton {background-color: white;}')
        return
    playsound('Sounds/error.wav')




class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('OXCE Unit Spawner')
        self.setGeometry(500, 200, 1000, 200)

        self.savePath = QLineEdit(self,placeholderText = "insert savefile path", clearButtonEnabled=True)
        self.savePath.setText(defaultpath)

        self.spawnButton = QPushButton('Spawn Aliens')
        self.portalNumber = 0


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

    def Coordswarning(window):
        QMessageBox.warning(window,'Error','Invalid Input')
    def PathWarning(window):
        QMessageBox.warning(window,'Error','Invalid Path')

class portal():

    def __init__(self, gridY, window, layout, name):

            self.gridY = gridY
            self.window = window
            self.layout = layout
            self.name = name
            self.active = False
            self.id = 0
            self.colorNumber = 0

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
            self.singleSpawnButton.clicked.connect(lambda: yamlfunctions.singleSpawn(self,True))


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
    def createPortal(name,x,y,z, portal):
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
                    tags = template['tags']
                    portal.id = maxId
                    template['id']  = maxId
                    template['position'] = coords
                    tags['PortalNo'] = window.portalNumber
                    portal.colorNumber = int(window.portalNumber % 7)
                    portal.singleSpawnButton.setStyleSheet(colourlist[portal.colorNumber])
                    window.portalNumber = window.portalNumber + 1
                    units.append(template)

        except FileNotFoundError:
            MainWindow.PathWarning(window)
            singleReset(portal)
            return
        try:
            with  open(window.savePath.text(), 'w') as savefile:
                yaml.Dumper.ignore_aliases = lambda *args: True
                yaml.dump_all(data, savefile)
                playsound('Sounds/note.wav')
        except FileNotFoundError:
            MainWindow.PathWarning(window)
            singleReset(portal)
            return

    def spawnClick(portals):
        for objects in portals:
            yamlfunctions.singleSpawn(objects,False)
        playsound('Sounds/note.wav')

    def singleSpawn(portal, playSound):
            if portal.active:
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

                        x = int(portal.lineX.text())
                        y = int(portal.lineY.text())
                        z = int(portal.lineZ.text())
                        coords = [x,y,z]
                        blockedTiles = yamlfunctions.getBlockedTiles(data)
                        spawnPos = yamlfunctions.getSpawnPos(coords)

                        blockedSpawns = 0

                        for tiles in spawnPos:
                            if tiles in blockedTiles:
                                blockedSpawns = blockedSpawns + 1

                        blockedSpawns = blockedSpawns + yamlfunctions.getLiveGrenadeCount(data, coords)
                        freeSpawns = 8-blockedSpawns



                        with open('templates.yml', 'r') as templatefile:
                            templatelist = yaml.safe_load(templatefile)
                            template = templatelist[1]
                            template['position'] = coords
                            selectedType = portal.combobox.currentText()
                            if selectedType in reversetranslation.keys():
                                selectedType = reversetranslation[selectedType]
                            template['type'] = selectedType
                            tags = template['tags']
                            tags['GrenX'] = coords[0]
                            tags['GrenY'] = coords[1]
                            tags['GrenZ'] = coords[2]
                            count = 0
                            while count < portal.slider.value():
                                if selectedType in spawners['recurring']:
                                    metaSave = data[0]
                                    turn = int(metaSave['turn']) % 10
                                    for grenadeCount in range (0,50):
                                        template['id'] = int(maxId)
                                        if count >= freeSpawns and grenadeCount == 0:
                                            template['fuseTimer'] = 2
                                        elif grenadeCount != 0:
                                            template['fuseTimer'] = (2*10*grenadeCount)-(turn*2)
                                        tags['PortalId'] = portal.id
                                        items.append(dict(template))
                                        maxId = maxId + 1
                                else:
                                    template['id'] = int(maxId)
                                    if count >= freeSpawns:
                                        template['fuseTimer'] = 2
                                    tags['PortalId'] = portal.id
                                    items.append(dict(template))
                                    maxId = maxId + 1
                                count = count + 1
                                template['fuseTimer'] = 0

                except FileNotFoundError:
                    MainWindow.PathWarning(window)
                    return

                try:
                    with  open(window.savePath.text(), 'w') as savefile:
                        yaml.Dumper.ignore_aliases = lambda *args: True
                        yaml.dump_all(data, savefile)
                        if playSound:
                            playsound('Sounds/note.wav')
                        portal.slider.setValue(0)
                        return
                except FileNotFoundError:
                    MainWindow.PathWarning(window)
                    return
            if playSound:
                playsound('Sounds/error.wav')

    def getSpawnPos(coords):
            referencePos = list(coords)
            referencePos[0] = referencePos[0] -1
            referencePos[1] = referencePos[1] -1
            spawnPos = []
            for i in range(0, 3):
                for k in range(0, 3):
                    pos = list(referencePos)
                    pos[0] = pos[0] + i
                    pos[1] = pos[1] + k
                    spawnPos.append(list(pos))

            spawnPos.remove(list(coords))

            return spawnPos

    def getLiveGrenadeCount(data, coords):

        saveGame = data[1]
        battleGame = saveGame.get('battleGame')
        items = battleGame.get('items')
        liveGrenadeCount = 0
        for grenades in items:

            if grenades['type'] in safeSpawnerList:
                try:
                    if grenades['fuseTimer'] == 0:
                        position = grenades['position']
                        if position == coords:
                            liveGrenadeCount = liveGrenadeCount + 1
                except KeyError:
                    print("No Fuse Active")
        return liveGrenadeCount
    def getBlockedTiles(data):
            saveGame = data[1]
            battleGame = saveGame.get('battleGame')

            blockedTiles = []
            units = battleGame.get('units')
            for blocks in units:
                position = blocks['position']
                blockedTiles.append(list(position))
            return blockedTiles




if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())

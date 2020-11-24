import sys
import os
import pickle
import copy
from library import * #CLASSES, PIECES, MONUMENTS, GEMS, GEMS_MAGIC, GEMS_SECRET, MATS_BRONZE, MATS_SILVER, MATS_GOLD, MATS_OTHER
from servant import Servant

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
#from library_ui import Ui_MainWindow
from PyQt5 import uic

sys.path.append('.')
ui_path = os.path.dirname(os.path.abspath(__file__))
Ui_MainWindow, MainBaseClass = uic.loadUiType(os.path.join(ui_path, 'library.ui') )
Ui_CostumeWindow, CostumeBaseClass = uic.loadUiType(os.path.join(ui_path, 'costume.ui') )
Ui_ServantListWindow, ServantListBaseClass = uic.loadUiType(os.path.join(ui_path, 'servant_list.ui') )

class CostumeWindow( CostumeBaseClass ):

    def __init__( self ):
        # run parent initialization
        super().__init__()
        #self.setAttribute(qtc.Qt.WA_DeleteOnClose)

        self.ui = Ui_CostumeWindow()
        self.ui.setupUi(self)
        
        self.mats     = [ (self.ui.mat1, self.ui.mat1_qty ), (self.ui.mat2, self.ui.mat2_qty ),\
                          (self.ui.mat3, self.ui.mat3_qty ), (self.ui.mat4, self.ui.mat4_qty ) ]

        self.populateMats()

    def populateMats( self ):
        for entry in self.mats:
            entry[0].addItems(MATS_BRONZE)
            entry[0].addItems(MATS_SILVER)
            entry[0].addItems(MATS_GOLD)

    def saveCostume( self ):
        costume = self.getCostumeData()        
        current_servant.addCostume(costume)

    def resetFields( self ):
        for entry in self.mats:
            entry[0].setCurrentIndex( 0 )
            entry[1].setValue( 0 )
        self.ui.costume_name_txt.clear()


    def loadCostume( self, costume_name ):
        costume = None
        for searching in current_servant.costumes:
            if( searching[COSTUME_NAME] == costume_name):
                costume = searching
        
        if ( costume == None ):
            return
        
        self.ui.costume_name_txt.insert( costume[COSTUME_NAME] )
        self.ui.mat1.setCurrentText( costume[COSTUME_MATS_01][0] )
        self.ui.mat1_qty.setValue( costume[COSTUME_MATS_01][1] )
        self.ui.mat2.setCurrentText( costume[COSTUME_MATS_02][0] )
        self.ui.mat2_qty.setValue( costume[COSTUME_MATS_02][1] )
        self.ui.mat3.setCurrentText( costume[COSTUME_MATS_03][0] )
        self.ui.mat3_qty.setValue( costume[COSTUME_MATS_03][1] )
        self.ui.mat4.setCurrentText( costume[COSTUME_MATS_04][0] )
        self.ui.mat4_qty.setValue( costume[COSTUME_MATS_04][1] )


    def getCostumeData( self ):
        name = self.ui.costume_name_txt.displayText()
        mat1 = self.ui.mat1.currentText()
        mat1_qty = self.ui.mat1_qty.value()
        mat2 = self.ui.mat2.currentText()
        mat2_qty = self.ui.mat2_qty.value()
        mat3 = self.ui.mat3.currentText()
        mat3_qty = self.ui.mat3_qty.value()
        mat4 = self.ui.mat4.currentText()
        mat4_qty = self.ui.mat4_qty.value()

        costume = { COSTUME_NAME:name, COSTUME_MATS_01:( mat1, mat1_qty ), COSTUME_MATS_02:( mat2, mat2_qty ),\
                        COSTUME_MATS_03:( mat3, mat3_qty ), COSTUME_MATS_04:( mat4, mat4_qty ) }
        return costume

    def done( self ):
        self.saveCostume()
        self.close()

    def cancel ( self ):
        self.close()

    def closeEvent( self, event ):
        self.resetFields()
        w.costumeWindowOpen = False

class ServantListWindow( ServantListBaseClass ):

    def __init__( self ):
        # run parent initialization
        super().__init__()
        #self.setAttribute(qtc.Qt.WA_DeleteOnClose)

        self.ui = Ui_ServantListWindow()
        self.ui.setupUi(self)

        self.ui.deleteServantButton.clicked.connect(self.deleteServant)

    def updateServantList( self ):
        self.ui.servantList.clear()
        servants_keys = list(servants.keys())
        servants_keys.sort()
        for servant in servants_keys:
            display = "{0:03d}".format(servants[servant].servant_id) + ": " + servants[servant].name
            self.ui.servantList.addItem(display)
    
        #self.ui.servantList.sortItems()

    def deleteServant( self ):
        
        del_servant = self.ui.servantList.currentItem().text()
        del_servant_id = int(del_servant[0:3])
        
        del servants[del_servant_id]
        self.ui.servantList.takeItem(self.ui.servantList.currentRow())
        saveServants(servants)
        #self.updateServantList()

class FGOC( MainBaseClass ):

    def __init__( self, *args, **kwargs ):
        # run parent initialization
        super().__init__( *args, **kwargs )

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # rarity
        self.current_rarity = 5
        self.saveExit = False

        self.rarity_dict = { 1:self.ui.star1, 2:self.ui.star2, 3:self.ui.star3, 4:self.ui.star4, 5:self.ui.star5,\
                             self.ui.star1:1, self.ui.star2:2, self.ui.star3:3, self.ui.star4:4, self.ui.star5:5 }

        self.lowRarityQty = { 1:2 , 2:3 , 3:4 , 4:4, 5:5 }
        self.highRarityQty = { 1:4 , 2:6 , 3:8 , 4:10, 5:12 }

        # group ascension materials combo boxes & quantity boxes (SpinBoxes)
        self.asc_mats     = [ (self.ui.asc1_mat_1, self.ui.asc1_qt_1 ), (self.ui.asc1_mat_2, self.ui.asc1_qt_2 ),\
                              (self.ui.asc2_mat_1, self.ui.asc2_qt_1 ), (self.ui.asc2_mat_2, self.ui.asc2_qt_2 ), (self.ui.asc2_mat_3, self.ui.asc2_qt_3 ),\
                              (self.ui.asc3_mat_1, self.ui.asc3_qt_1 ), (self.ui.asc3_mat_2, self.ui.asc3_qt_2 ), (self.ui.asc3_mat_3, self.ui.asc3_qt_3 ),\
                              (self.ui.asc4_mat_1, self.ui.asc4_qt_1 ), (self.ui.asc4_mat_2, self.ui.asc4_qt_2 ), (self.ui.asc4_mat_3, self.ui.asc4_qt_3 ) ]
        self.pieces_indexes     = ( 0, 2 )
        self.monuments_indexes  = ( 5, 8 )

        # group skill materials combo boxes & quantity boxes (SpinBoxes)
        self.sk_mats        = [ (self.ui.sk1_mat_1, self.ui.sk1_qt_1 ), (self.ui.sk1_mat_2, self.ui.sk1_qt_2 ),\
                                (self.ui.sk2_mat_1, self.ui.sk2_qt_1 ), (self.ui.sk2_mat_2, self.ui.sk2_qt_2 ),\
                                (self.ui.sk3_mat_1, self.ui.sk3_qt_1 ), (self.ui.sk3_mat_2, self.ui.sk3_qt_2 ),\
                                (self.ui.sk4_mat_1, self.ui.sk4_qt_1 ), (self.ui.sk4_mat_2, self.ui.sk4_qt_2 ),\
                                (self.ui.sk5_mat_1, self.ui.sk5_qt_1 ), (self.ui.sk5_mat_2, self.ui.sk5_qt_2 ),\
                                (self.ui.sk6_mat_1, self.ui.sk6_qt_1 ), (self.ui.sk6_mat_2, self.ui.sk6_qt_2 ),\
                                (self.ui.sk7_mat_1, self.ui.sk7_qt_1 ), (self.ui.sk7_mat_2, self.ui.sk7_qt_2 ),\
                                (self.ui.sk8_mat_1, self.ui.sk8_qt_1 ), (self.ui.sk8_mat_2, self.ui.sk8_qt_2 ) ]  
        self.gems_indexes        = ( 0, 2  )
        self.gems_magic_indexes  = ( 4, 6  )
        self.gems_secret_indexes = ( 8, 10 )

        self.sk_names       = [ self.ui.sk_name_1, self.ui.sk_name_2, self.ui.sk_name_3 ]

        self.populateFields()        

        # buttons
        self.ui.clearButton.clicked.connect(self.clearServant)
        self.ui.rarityButtons.buttonClicked.connect(self.getRarity)
        self.ui.ascResetButton.clicked.connect(self.resetAscMats)
        self.ui.skResetButton.clicked.connect(self.resetSkMats)
        self.ui.viewServantsButton.clicked.connect(self.viewServantList)
        self.ui.saveServantButton.clicked.connect(self.saveServant)
        self.ui.saveExitButton.clicked.connect(self.saveAndExit)
        self.ui.exitButton.clicked.connect(self.exit)

        # costume list updater

        # class change trigger
        self.ui.class_select.currentIndexChanged.connect(self.classChanged)

        # set up costume window
        self.costumeWindowOpen = False
        self.costumeWindow = CostumeWindow()
        self.servantListWindow = ServantListWindow()

        self.costumeWindow.ui.doneButton.clicked.connect( self.costumeFinished )
        self.costumeWindow.ui.cancelButton.clicked.connect( self.costumeCanceled )

        
        self.servantListWindow.ui.editServantButton.clicked.connect(self.loadServant)
        self.servantListWindow.ui.cancelButton.clicked.connect(self.servantListClosed)

        self.ui.costumeAddButton.clicked.connect( self.addCostume )
        self.ui.costumeEditButton.clicked.connect( self.editCostume )
        self.ui.costumeDeleteButton.clicked.connect( self.delCostume )

        self.show()

    def populateFields( self ):

        # class
        self.ui.class_select.addItems( CLASSES )

        # ascension materials

        count = 0
        for entry in self.asc_mats:
            entry[0].addItem("NONE")
            if ( count in self.pieces_indexes ):
                entry[0].addItems(PIECES)
            elif ( count in self.monuments_indexes ):
                entry[0].addItems(MONUMENTS)

            entry[0].addItems(MATS_BRONZE)
            entry[0].addItems(MATS_SILVER)
            entry[0].addItems(MATS_GOLD)

            entry[0].addItem("Ruler")

            count += 1
        
        # skill materials

        count = 0
        for entry in self.sk_mats:
            entry[0].addItem("NONE")
            if ( count in self.gems_indexes  ):
                entry[0].addItems(GEMS)
            elif ( count in self.gems_magic_indexes ):
                entry[0].addItems(GEMS_MAGIC)
            elif ( count in self.gems_secret_indexes  ):
                entry[0].addItems(GEMS_SECRET)
            
            entry[0].addItems(MATS_BRONZE)
            entry[0].addItems(MATS_SILVER)
            entry[0].addItems(MATS_GOLD)
            if ( count < 12 ):
                entry[0].addItem("Ruler")
            
            count+=1

    def classChanged(self):
        self.populateStatues()
        self.populateGems()

    def populateStatues(self):
        
        if ( self.current_rarity == 0 ):
            return

        low_qty  = self.lowRarityQty.get( self.current_rarity )

        if ( self.ui.class_select.currentText() in CLASSES[0:7] ):
            class_index = CLASSES.index( self.ui.class_select.currentText() )
            index = 0
            high_qty = self.highRarityQty.get( self.current_rarity )
            
            # populate names
            low = True

            for entry in self.asc_mats:
                if ( index in self.pieces_indexes or index in self.monuments_indexes ):

                    if( index in self.pieces_indexes ):
                        entry[0].setCurrentText(PIECES[class_index])
                    else:
                        entry[0].setCurrentText(MONUMENTS[class_index])

                    if (low):
                        entry[1].setValue(low_qty)
                    else:
                        entry[1].setValue(high_qty)
                    
                    low = not low

                index += 1

        # ruler special case
        elif ( self.ui.class_select.currentText() == RULER ):
            for entry in self.asc_mats:
                entry[0].setCurrentText("Ruler")
                entry[1].setValue(low_qty)

    def populateGems( self ):

        if (self.current_rarity == 0 ):
            return

        
        low_qty  = self.lowRarityQty.get( self.current_rarity )

        # standard classes (saber-berserker)

        if ( self.ui.class_select.currentText() in CLASSES[0:7]):
            class_index = CLASSES.index( self.ui.class_select.currentText() )
            high_qty = self.highRarityQty.get( self.current_rarity )
            index = 0                    
            low = True

            # populate names
            for entry in self.sk_mats[0:12]:
                if ( index in self.gems_indexes or\
                     index in self.gems_magic_indexes or\
                     index in self.gems_secret_indexes ):

                    if ( index in self.gems_indexes ):
                        entry[0].setCurrentText(GEMS[class_index])
                    elif ( index in self.gems_magic_indexes ):
                        entry[0].setCurrentText(GEMS_MAGIC[class_index])
                    else:
                        entry[0].setCurrentText(GEMS_SECRET[class_index])

                    if (low):
                        entry[1].setValue(low_qty)
                    else:
                        entry[1].setValue(high_qty)

                    low = not low

                index += 1
        
        # ruler special case
        elif ( self.ui.class_select.currentText() == RULER ):
            for entry in self.sk_mats[0:12]:
                entry[0].setCurrentText("Ruler")
                entry[1].setValue(low_qty)

    def getRarity( self ):
        button = self.ui.rarityButtons.checkedButton()
        """
        if ( button == None ):
            self.current_rarity = 0
        elif ( button == self.ui.star1):
            self.current_rarity = 1
        elif ( button == self.ui.star2):
            self.current_rarity = 2
        elif ( button == self.ui.star3):
            self.current_rarity = 3
        elif ( button == self.ui.star4):
            self.current_rarity = 4
        elif ( button == self.ui.star5):
            self.current_rarity = 5
        """
        self.current_rarity = self.rarity_dict[button]
        self.classChanged()

    def inSubList(self, top_list, item ):
        for sub_list in top_list:
            if ( item in sub_list ):
                return True
        return False

    def subListIndex(self, top_list, item):
        for sub_list in top_list:
            if ( item in sub_list ):
                return top_list.index(sub_list)
        return -1

    def saveServant( self ):
        
        self.updateCurrentServant()

        servants[current_servant.servant_id] = copy.deepcopy(current_servant)

        saveServants(servants)

    def viewServantList( self ):
        self.servantListWindow.updateServantList()
        self.servantListWindow.show()
    
    def servantListClosed(self):
        self.servantListWindow.hide()

    def loadServant( self ): 
        self.servantListClosed()
        self.clearServant()
        
        new_servant = self.servantListWindow.ui.servantList.currentItem().text()
        new_servant_id = int(new_servant[0:3])
        
        found = False

        if( new_servant_id in servants.keys() ):
            current_servant = copy.deepcopy( servants[new_servant_id] )
            found = True
        
        if ( not found ):
            return

        # name
        self.ui.name_txt.insert(current_servant.name)

        # rarity
        self.rarity_dict[current_servant.rarity].setChecked(True)

        # class
        self.ui.class_select.setCurrentText(current_servant.servant_class)

        # ID
        self.ui.id_num.setValue(current_servant.servant_id)
        
        # wiki name
        self.ui.wiki_txt.insert(current_servant.wiki_name)

        # ascensions
        level = 0
        index = 0
        for asc in self.asc_mats:
            if ( level == 0):
                asc[0].setCurrentText(current_servant.asc_mats[level][index % 2][0] )
                asc[1].setValue(current_servant.asc_mats[level][index % 2][1] )
                index += 1
                if ( index == 2 ):
                    level += 1
            else:
                asc[0].setCurrentText(current_servant.asc_mats[level][(index + 1 ) % 3][0] )
                asc[1].setValue(current_servant.asc_mats[level][(index + 1) % 3][1] ) 
                index += 1
                if ( index % 3 == 2):
                    level += 1


        # skill names
        index = 0
        for skill in self.sk_names:
            skill.insert(current_servant.skill_names[index])
            index += 1

        # skill materials
        level = 0
        index = 0
        for skill in self.sk_mats:
            skill[0].setCurrentText(current_servant.skill_mats[level][index % 2][0] )
            skill[1].setValue(current_servant.skill_mats[level][index % 2][1] )
            index += 1
            if ( index % 2 == 0 ):
                level += 1

        # costumes <--- issue here
        self.updateCostumeList()

    def updateCurrentServant( self ):
        current_servant.name = self.ui.name_txt.displayText()
        current_servant.servant_id = self.ui.id_num.value()
        current_servant.servant_class = self.ui.class_select.currentText()
        current_servant.wiki_name = self.ui.wiki_txt.displayText()
        current_servant.rarity = self.current_rarity

        skill_names = []
        for name in self.sk_names:
            skill_names.append( name.displayText() )

        current_servant.skill_names = skill_names

        asc_list = []
        sk_list = []
            
        index = 0

        if (current_servant.servant_class == RULER ):
            if(self.current_rarity == 5):
                asc_list = RULER_5_ASC
                sk_list  = RULER_5_SK
            else:
                asc_list = RULER_4_ASC
                sk_list  = RULER_4_SK
            
            for skill in self.sk_mats[6:]:
                if ( index % 2 == 0 ):
                    first = ( skill[0].currentText(), skill[1].value() )
                else:
                    sk_list.append( (first, ( skill[0].currentText(), skill[1].value() ) ) )                  
                index += 1
        else:
            for skill in self.sk_mats:
                if ( index % 2 == 0 ):
                    first = ( skill[0].currentText(), skill[1].value() )
                else:
                    sk_list.append( (first, ( skill[0].currentText(), skill[1].value() ) ) )
                index += 1
            
            index = 0
            for asc in self.asc_mats:
                if(index == 0):
                    first = ( asc[0].currentText(), asc[1].value() ) 
                elif(index == 1):                
                    asc_list.append( (first, ( asc[0].currentText(), asc[1].value() ) ) )
                elif( index % 3 == 2 ):
                    first = ( asc[0].currentText(), asc[1].value() )
                elif( index % 3 == 0 ):
                    second =  ( asc[0].currentText(), asc[1].value() )
                else:                
                    asc_list.append( ( first, second, ( asc[0].currentText(), asc[1].value() ) ) )

                index += 1

        current_servant.skill_mats = sk_list
        current_servant.asc_mats = asc_list

    def clearServant( self ):       
        
        # name
        self.ui.name_txt.clear()

        # rarity
        self.ui.star5.setChecked(True)

        # class
        self.ui.class_select.setCurrentIndex(0)

        # ID
        self.ui.id_num.setValue(0)
        
        # wiki name
        self.ui.wiki_txt.clear()

        # ascensions
        self.resetAscMats()

        # skill names
        for skill in self.sk_names:
            skill.clear()

        # skill materials
        self.resetSkMats()

        self.getRarity()
        self.updateCostumeList()
        current_servant.reset()

    def addCostume( self ):
        if( self.costumeWindowOpen ):
            return
        self.costumeWindow.show()
        self.costumeWindowOpen = True

    def editCostume( self ):
        if( self.costumeWindowOpen ):
            return
        if (self.ui.costumes_list.currentItem() != None):
            self.costumeWindow.loadCostume( self.ui.costumes_list.currentItem().text() )
            self.costumeWindow.show()        
            self.costumeWindowOpen = True

    def delCostume( self ):
        delete_target = self.ui.costumes_list.currentItem().text()
        if (delete_target != None):
            current_servant.delCostume( delete_target )
            self.updateCostumeList()        

    def costumeFinished ( self ):
        self.costumeWindow.done()
        self.updateCostumeList()
        self.costumeWindowOpen = False

    def costumeCanceled ( self ):
        self.costumeWindow.cancel()
        self.costumeWindowOpen = False

    def updateCostumeList ( self ):
        self.ui.costumes_list.clear()
        for costume in current_servant.costumes:
            self.ui.costumes_list.addItem( costume[COSTUME_NAME] )
        self.ui.costumes_list.sortItems()     

    def resetAscMats( self ):
        for asc in self.asc_mats:
            asc[0].setCurrentIndex(0)
            asc[1].setValue(0)

    def resetSkMats( self ):
        for skill in self.sk_mats:
            skill[0].setCurrentIndex(0)
            skill[1].setValue(0)

    def saveAndExit( self ):
        self.saveExit = True
        self.close()

    def exit( self ):
        self.saveExit = False
        self.close()

    def closeEvent( self, event ):
        if ( self.saveExit ):
            self.saveServant()
        qtw.QApplication.closeAllWindows()

# GLOBAL FUNCTIONS

def loadServants(servant_list):

    try:
        servant_list = pickle.load( open( SERVANT_LIBRARY, "rb" ) )
    except:
        return servant_list

    return servant_list

def saveServants(servant_list):

    pickle.dump( servant_list , open( SERVANT_LIBRARY, "wb" ) )

if __name__ == '__main__':

    servants = {}
    current_servant = Servant()

    servants = loadServants(servants)    

    app = qtw.QApplication( sys.argv )

    w = FGOC()

    sys.exit( app.exec_() )
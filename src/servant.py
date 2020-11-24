# File: servant.py
# The class file for servants in the FGO companion app
import localization as loc

class Servant():

    def __init__( self ):
        self.name           = ""
        self.servant_id     = -1
        self.rarity         = 0
        self.servant_class  = ""
        self.skill_names    = []
        self.skill_mats     = []
        self.asc_mats       = []
        self.wiki_name      = ""
        self.costume_names  = []
        self.costumes       = []

    def reset( self ):  
        self.name           = ""
        self.servant_id     = -1
        self.rarity         = 0
        self.servant_class  = ""
        self.skill_names    = []
        self.skill_mats     = []
        self.asc_mats       = []
        self.wiki_name      = ""
        self.costume_names  = []
        self.costumes       = []

    def wikiUpdate( self, updated_servant ):
        if (self.name           == updated_servant.name             and\
            self.servant_id     == updated_servant.servant_id       and\
            self.rarity         == updated_servant.rarity           and\
            self.servant_class  == updated_servant.servant_class    and\
            self.skill_names    == updated_servant.skill_names      and\
            self.skill_mats     == updated_servant.skill_mats       and\
            self.asc_mats       == updated_servant.asc_mats         and\
            self.costumes       == updated_servant.costumes):
            return False
        
        self.name           = updated_servant.name
        self.servant_id     = updated_servant.servant_id
        self.rarity         = updated_servant.rarity
        self.servant_class  = updated_servant.servant_class
        self.skill_names    = updated_servant.skill_names
        self.skill_mats     = updated_servant.skill_mats
        self.asc_mats       = updated_servant.asc_mats
        self.costumes       = updated_servant.costumes

        return True


    def addCostume( self , new_costume ):
        self.delCostume( new_costume[0] )
        self.costumes.append( new_costume )

    def delCostume( self , target_costume ):
        for costume in self.costumes:
            if ( costume[0] == target_costume ):
                self.costumes.remove( costume )
                return
                
        
class ownedServant(Servant):

    def __init__ (self, original = None):
        if ( original == None ):
            self.priority        = False
            self.level           = 1
            self.ascension       = 0
            self.skill1          = 1
            self.skill2          = 1
            self.skill3          = 1
            self.fou             = 0
            self.fou_gold        = 0
            self.grail           = 0


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
            self.costumes       == updated_servant.costumes         and\
            len( self.costume_names ) == len(updated_servant.costume_names) ):

            return False
        
        self.name           = updated_servant.name
        self.servant_id     = updated_servant.servant_id
        self.rarity         = updated_servant.rarity
        self.servant_class  = updated_servant.servant_class
        self.skill_names    = updated_servant.skill_names
        self.skill_mats     = updated_servant.skill_mats
        self.asc_mats       = updated_servant.asc_mats
        self.costumes       = updated_servant.costumes

        if ( len(self.costume_names) != len(self.costumes) ):
            if( len(self.costume_names) < len(self.costumes) ):
                new_names = len(self.costumes) - len(self.costume_names)
                while( new_names > 0 ):
                    self.costume_names.append("New Costume")
                    new_names -= 1

        return True

    def update( self, updated_servant ):
        if(     self.name           == updated_servant.name             and\
                self.wiki_name      == updated_servant.wiki_name        and\
                self.servant_id     == updated_servant.servant_id       and\
                self.rarity         == updated_servant.rarity           and\
                self.servant_class  == updated_servant.servant_class    and\
                self.skill_names    == updated_servant.skill_names      and\
                self.skill_mats     == updated_servant.skill_mats       and\
                self.asc_mats       == updated_servant.asc_mats         and\
                self.costumes       == updated_servant.costumes         and\
                self.costume_names  == updated_servant.costume_names ):

                return False

        self.name           = updated_servant.name
        self.wiki_name      = updated_servant.wiki_name
        self.servant_id     = updated_servant.servant_id
        self.rarity         = updated_servant.rarity
        self.servant_class  = updated_servant.servant_class
        self.skill_names    = updated_servant.skill_names
        self.skill_mats     = updated_servant.skill_mats
        self.asc_mats       = updated_servant.asc_mats
        self.costumes       = updated_servant.costumes
        self.costume_names  = updated_servant.costume_names

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

    def __init__ (self, original = None, base = False):
        if ( original == None or base ):
            self.priority        = False
            self.level           = 1
            self.ascension       = 0
            self.skill1          = 1
            self.skill2          = 1
            self.skill3          = 1
            self.fou             = 0
            self.fou_gold        = 0
            self.grail           = 0

        if ( not original ):
            super().__init__()

        if ( original ):

            self.name           = original.name
            self.wiki_name      = original.wiki_name
            self.servant_id     = original.servant_id
            self.rarity         = original.rarity
            self.servant_class  = original.servant_class
            self.skill_names    = original.skill_names
            self.skill_mats     = original.skill_mats
            self.asc_mats       = original.asc_mats
            self.costumes       = original.costumes
            self.costume_names  = original.costume_names

        if ( base ):            
            self.user_name          = ""
            self.user_skill_names   = ""
            self.user_costume_names = ""

        if ( not base ):

            self.user_name          = original.name
            self.user_skill_names   = original.name
            self.user_costume_names = original.name
        

    def ownedUpdate(self, updated_servant, base = False):

        baseUpdate = self.update(updated_servant)

        if ( base ):
            if ( not baseUpdate):
                return False
            else:
                return True
        else:
            if (    self.user_name          == updated_servant.user_name            and\
                    self.user_skill_names   == updated_servant.user_skill_names     and\
                    self.user_costume_names == updated_servant.user_costume_names ):
                    if ( not baseUpdate):
                        return False

            self.user_name          = updated_servant.user_name
            self.user_skill_names   = updated_servant.user_skill_names
            self.user_costume_names = updated_servant.user_costume_names

        return True

    def reset(self):
        # base servant
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

        # owned servant
        self.priority        = False
        self.level           = 1
        self.ascension       = 0
        self.skill1          = 1
        self.skill2          = 1
        self.skill3          = 1
        self.fou             = 0
        self.fou_gold        = 0
        self.grail           = 0

        self.user_name          = self.name
        self.user_skill_names   = self.skill_names
        self.user_costume_names = self.costume_names

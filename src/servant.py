# File: servant.py
# The class file for servants in the FGO companion app

class Servant():
    name            = ""
    rarity          = 0
    skill_one       = []
    skill_two       = []
    skill_three     = []
    skills = [ skill_one, skill_two, skill_three ]
    ascension_materials_one   = []
    ascension_materials_two   = []
    ascension_materials_three = []
    ascension_materials_four  = []
    wiki_links      = []

    # Accessors
    def getName ( self ):
        return self.name
    
    def getRarity ( self ):
        return self.rarity

    # Modifiers

    def setName ( self, name ):
        self.name = name
        
    def setRarity ( self, rarity ):
        self.rarity = rarity
    
    def addWiki ( self, wiki_link ):
        self.wiki_links.append(wiki_link)

    
class ownedServant(Servant):
    priority        = False
    level           = 1
    ascension       = 0
    fou             = 0
    fou_gold        = 0
    grail           = 0

    # Accessors
    
    def getPriority ( self ):
        return self.priority
    
    def getLevel ( self ):
        return self.level
    
    def getAscension ( self ):
        return self.ascension
    
    def getFou ( self ):
        return self.fou
    
    def getFouGold ( self ):
        return self.fou_gold
    
    def getGrail ( self ):
        return self.grail
    
    def getSkill ( self , skill_id ):
        return self.skills[skill_id]
    
    def getSkills ( self ):
        return self.skills

    # Modifiers
        
    def setLevel ( self, level ):
        self.level = level
        
    def setAscension ( self, ascension ):
        self.ascension = ascension
        
    def addFou ( self, fou ):
        self.fou += fou
        
    def addFouGold ( self, fou_gold ):
        self.fou_gold += fou_gold
        
    def addGrail ( self ):
        self.grail += 1
        
    def setSkill ( self, skill_id, skill_lvl ):
        
    def incAscension ( self, name ):
        
    def togglePriority ( self ):
        self.priority = not self.priority

# populate servant library from wiki data

import localization as loc 
import pickle
from copy import deepcopy
from servant import Servant
import sys


#####################
# Wiki Dictionaries #
#####################

PIECE_SABER             = "Saber Piece"
PIECE_ARCHER            = "Archer Piece"
PIECE_LANCER            = "Lancer Piece"
PIECE_RIDER             = "Rider Piece"
PIECE_CASTER            = "Caster Piece"
PIECE_ASSASSIN          = "Assassin Piece"
PIECE_BERSERKER         = "Berserker Piece"

MONUMENT_SABER          = "Saber Monument"
MONUMENT_ARCHER         = "Archer Monument"
MONUMENT_LANCER         = "Lancer Monument"
MONUMENT_RIDER          = "Rider Monument"
MONUMENT_CASTER         = "Caster Monument"
MONUMENT_ASSASSIN       = "Assassin Monument"
MONUMENT_BERSERKER      = "Berserker Monument"

GEM_SABER               = "Shining Gem Of Swords"
GEM_ARCHER              = "Shining Gem Of Bows"
GEM_LANCER              = "Shining Gem Of Lances"
GEM_RIDER               = "Shining Gem Of Cavalry"
GEM_CASTER              = "Shining Gem Of Spells"
GEM_ASSASSIN            = "Shining Gem Of Killing"
GEM_BERSERKER           = "Shining Gem Of Madness"

GEM_MAGIC_SABER         = "Magic Gem Of Swords"
GEM_MAGIC_ARCHER        = "Magic Gem Of Bows"
GEM_MAGIC_LANCER        = "Magic Gem Of Lances"
GEM_MAGIC_RIDER         = "Magic Gem Of Cavalry"
GEM_MAGIC_CASTER        = "Magic Gem Of Spells"
GEM_MAGIC_ASSASSIN      = "Magic Gem Of Killing"
GEM_MAGIC_BERSERKER     = "Magic Gem Of Madness"

GEM_SECRET_SABER        = "Secret Gem Of Swords"
GEM_SECRET_ARCHER       = "Secret Gem Of Bows"
GEM_SECRET_LANCER       = "Secret Gem Of Lances"
GEM_SECRET_RIDER        = "Secret Gem Of Cavalry"
GEM_SECRET_CASTER       = "Secret Gem Of Spells"
GEM_SECRET_ASSASSIN     = "Secret Gem Of Killing"
GEM_SECRET_BERSERKER    = "Secret Gem Of Madness"

BRONZE_00   = "Hero'S Proof"
BRONZE_01   = "Unlucky Bone"
BRONZE_02   = "Dragon Fang"
BRONZE_03   = "Void'S Refuse"
BRONZE_04   = "Chains Of The Fool"
BRONZE_05   = "Stinger Of Certain Death"
BRONZE_06   = "Magical Cerebrospinal Fluid"
BRONZE_07   = "Night-Weeping Iron Stake"
BRONZE_08   = "Stimulus Gunpowder"

SILVER_00   = "Yggdrasil Seed"
SILVER_01   = "Ghost Lantern"
SILVER_02   = "Octuplet Twin Crystals"
SILVER_03   = "Snake Jewel"
SILVER_04   = "Phoenix Plume"
SILVER_05   = "Infinity Gear"
SILVER_06   = "Forbidden Page"
SILVER_07   = "Homunculus Baby"
SILVER_08   = "Meteoric Horseshoe"
SILVER_09   = "Medal Of Great Knight"
SILVER_10   = "Seashell Of Reminiscence"
SILVER_11   = "Kotan Magatama"
SILVER_12   = "Permafrost Ice Crystal"
SILVER_13   = "Giant'S Ring"
SILVER_14   = "Aurora Steel"
SILVER_15   = "Ancient Bell Of Tranquility"
SILVER_16   = "Arrowhead Of Maledictions"
SILVER_17   = "Crown Of Radiant Silver"
SILVER_18   = "Divine Spiricle Vein"

GOLD_00     = "Talon Of Chaos"
GOLD_01     = "Heart Of A Foreign God"
GOLD_02     = "Dragon'S Reverse Scale"
GOLD_03     = "Spirit Root"
GOLD_04     = "Warhorse'S Immature Horn"
GOLD_05     = "Bloodstone Tear"
GOLD_06     = "Black Tallow"
GOLD_07     = "Lamp Of Demon Sealing"
GOLD_08     = "Scarab Of Wisdom"
GOLD_09     = "Primordial Lanugo"
GOLD_10     = "Cursed Beast Cholecyst"
GOLD_11     = "Bizarre Godly Wine"
GOLD_12     = "Dawnlight Reactor Core"
GOLD_13     = "Tsukumo Mirror"
GOLD_14     = "Genesis Egg"
GOLD_15     = "Comet Shard"
GOLD_16     = "Fruit Of Longevity"

OTHER_00    = "QP"
OTHER_01    = "Crystallized Lore"
OTHER_02    = "Holy Grail"
OTHER_03    = "Chaldea Visionary Flames"


WIKI_MATS_ALL=  { PIECE_SABER: 100, PIECE_ARCHER: 101, PIECE_LANCER: 102, PIECE_RIDER: 103, PIECE_CASTER: 104, PIECE_ASSASSIN: 105, PIECE_BERSERKER: 106,\
                 \
                 MONUMENT_SABER: 200, MONUMENT_ARCHER: 201, MONUMENT_LANCER: 202, MONUMENT_RIDER: 203, MONUMENT_CASTER: 204, MONUMENT_ASSASSIN: 205, MONUMENT_BERSERKER: 206,\
                 \
                 GEM_SABER: 300, GEM_ARCHER: 301, GEM_LANCER: 302, GEM_RIDER: 303, GEM_CASTER: 304, GEM_ASSASSIN: 305, GEM_BERSERKER: 306,\
                 \
                 GEM_MAGIC_SABER: 400, GEM_MAGIC_ARCHER: 401, GEM_MAGIC_LANCER: 402, GEM_MAGIC_RIDER: 403, GEM_MAGIC_CASTER: 404, GEM_MAGIC_ASSASSIN: 405, GEM_MAGIC_BERSERKER: 406,\
                 \
                 GEM_SECRET_SABER: 500, GEM_SECRET_ARCHER: 501, GEM_SECRET_LANCER: 502, GEM_SECRET_RIDER: 503, GEM_SECRET_CASTER: 504, GEM_SECRET_ASSASSIN: 505, GEM_SECRET_BERSERKER: 506,\
                 \
                 BRONZE_00: 600, BRONZE_01: 601, BRONZE_02: 602, BRONZE_03: 603, BRONZE_04: 604, BRONZE_05: 605, BRONZE_06: 606, BRONZE_07: 607, BRONZE_08: 608,\
                 \
                 SILVER_00: 700, SILVER_01: 701, SILVER_02: 702, SILVER_03: 703, SILVER_04: 704, SILVER_05: 705, SILVER_06: 706, SILVER_07: 707, SILVER_08: 708, SILVER_09: 709,\
                 SILVER_10: 710, SILVER_11: 711, SILVER_12: 712, SILVER_13: 713, SILVER_14: 714, SILVER_15: 715, SILVER_16: 716, SILVER_17: 717, SILVER_18: 718,\
                 \
                 GOLD_00: 800, GOLD_01: 801, GOLD_02: 802, GOLD_03: 803, GOLD_04: 804, GOLD_05: 805, GOLD_06: 806, GOLD_07: 807, GOLD_08: 808, GOLD_09: 809,\
                 GOLD_10: 810, GOLD_11: 811, GOLD_12: 812, GOLD_13: 813, GOLD_14: 814, GOLD_15: 815, GOLD_16: 816,\
                 \
                 OTHER_00: 900, OTHER_01: 901, OTHER_02: 902, OTHER_03: 903 }



def cleanMatsLine( line ):
   
    try:            
        line = line.strip('|')     
        line = line.strip()        # clears outside whitespace
        asc_num = line[0:2]
        level = int(asc_num[0]) 
        line = line.strip(asc_num)
        line = line.replace('=', '')     
        line = line.replace('Inum|', '')    
        line = line.replace('inum|', '')  
        line = line.replace( '{', '')
        line = line.replace( '}', '')
        line = line.strip()
        if ( "|" in line):
            mats = line.split('|')
        else:
            mats = False
    except:
        print("Failed to Clean Material Line:")
        print(line)        
        sys.exit("Line Cleaning Failed | Check Source File")

    try:
        mats[0] = mats[0].replace('_', ' ')
        mats[0] = WIKI_MATS_ALL[ mats[0].strip().title() ]
    except:
        if ( mats ):
            mats[0] = 923
        else:
            mats = [-1]

    if ( len(mats) == 2 ):
        mats[1] = int( mats[1].strip() )
    else:
        return level, [-1,-1]

    return (level, mats )

def cleanSkillName( skill ):   
    
    try:
        skill = skill[ ( skill.rfind('{{:') + 3 ) : ]
        skill = skill.replace('}', '')
        skill = skill.replace('|-|', '')
        skill = skill.strip()
        skill = skill.replace('|', ' ')
    except:
        print("Failed to Clean Skill Name:")
        print(skill)        
        sys.exit("Line Cleaning Failed | Check Source File")

    return skill

def readWikiFile():
        
    with open('wiki_servants.txt', 'r', errors='replace') as f:
        wiki = f.readlines()


    for line in wiki:
        line = line.strip()

    return wiki

def resetFound( found_tags ):    
    found_tags[0]           = False
    found_tags[1]           = False
    found_tags[2]           = False
    found_tags[3]           = False
    found_tags[4]           = False
    found_tags[5]           = False
    found_tags[6]           = False
    found_tags[7]           = False

def addID(line, servant):
    try:
        line = line.replace('|', '')
        line = line.replace('=', '')
        line = line.replace('id', '')
        line = line.strip()
    except:
        print("Failed to Clean ID:")
        print(line)        
        sys.exit("Line Cleaning Failed | Check Source File")
        
    servant.servant_id = int(line)

def addRarity(line, servant):
    try:
        line = line.replace('|', '')
        line = line.replace('=', '')
        line = line.replace('stars', '')
        line = line.strip()
    except:
        print("Failed to Clean Rarity:")
        print(line)        
        sys.exit("Line Cleaning Failed | Check Source File")
    servant.rarity = int(line)

def addClass(line, servant):
    try:
        line = line.replace('|', '')
        line = line.replace('=', '')
        line = line.replace('class', '')
        line = line.replace('Gold', '')
        line = line.replace('Silver', '')
        line = line.replace('Bronze', '')
        line = line.strip()
    except:
        print("Failed to Clean Class:")
        print(line)        
        sys.exit("Line Cleaning Failed | Check Source File")

    servant.servant_class = line

def addSkillNames( wiki, index, servant):
    
    skill = wiki[index]
    index += 1
    line = wiki[index]
    
    while ( "Second Skill" not in line):
        skill += line
        index += 1
        line = wiki[index]
    
    skill = cleanSkillName( skill )
    servant.skill_names.append( skill[:] )
    skill = ""

    index += 1
    line = wiki[index]

    while ( "Third Skill" not in line):
        skill += line
        index += 1
        line = wiki[index]
    
    skill = cleanSkillName( skill )
    servant.skill_names.append( skill[:] )
    skill = ""

    
    index += 1
    line = wiki[index]

    while ( "tabber>" not in line):
        skill += line
        index += 1
        line = wiki[index]
    
    skill = cleanSkillName( skill )
    servant.skill_names.append( skill[:] )

    return index

def addAscensionMats ( wiki, index, servant ):
    
    finished_ascensions = False
    current_mats = []
    current_level = 1

    while ( not finished_ascensions ):
        line = wiki[index]

        if( 'qp' not in line ):
            level, mats = cleanMatsLine( line )

            if ( mats[0] == -1 ):
                index += 1
                continue
        else:
            servant.asc_mats.append( deepcopy(current_mats) )
            finished_ascensions = True
            break

        if ( level == current_level ):
            current_mats.append( deepcopy(mats) )
        elif ( level > 4 ):
            servant.asc_mats.append( deepcopy(current_mats) )
            finished_ascensions = True
            index = addCostumes(wiki, index, servant)
            break             
        else:                
            servant.asc_mats.append( deepcopy(current_mats) )
            current_mats = []
            current_mats.append( deepcopy(mats) )
            current_level += 1

        index += 1

    return index

def addCostumes( wiki, index, servant ):

    current_mats = []
    current_level = 5
    finished_costumes = False

    while ( not finished_costumes ):
        line = wiki[index]

        if( 'qp' not in line ):
            level, mats = cleanMatsLine( line )

            if ( mats[0] == -1 ):
                index += 1
                continue
        else:
            servant.costumes.append( deepcopy(current_mats) )
            servant.costume_names.append("Costume " + str( current_level - 4 ) )
            finished_costumes = True
            break

        if ( level == current_level ):
            current_mats.append( deepcopy(mats)) 
        else:                
            servant.costumes.append( deepcopy(current_mats) )
            servant.costume_names.append("Costume " + str( current_level - 4 ) )
            current_mats = []
            current_mats.append( deepcopy(mats) )
            current_level += 1

        index += 1   

    return index

def addSkillMats( wiki, index, servant):

    current_mats = []
    current_level = 1
    finished_skills = False
    
    while ( not finished_skills ):
        line = wiki[index]

        if ( "Lore" in line or "lore" in line or "qp" in line ):
            servant.skill_mats.append( deepcopy(current_mats) )
            finished_skills = True
            break
        
        level, mats = cleanMatsLine( line )

        if ( mats[0] == -1 ):
            index += 1
            continue

        if ( level == current_level ):
            current_mats.append( deepcopy(mats) )
        else:
            servant.skill_mats.append( deepcopy(current_mats) )
            current_mats = []
            current_mats.append( deepcopy(mats) )
            current_level += 1

        index += 1

    return index

def updateAllServants( servants ):

    wiki = readWikiFile()

    added = 0
    updated = 0

    current_servant = Servant()

    index = 0

    skip = False

    found_name = False
    found_id = False
    found_rarity = False
    found_class = False
    found_id = False
    found_skill_names = False
    found_ascensions = False
    found_skills = False

    #found_tags = [found_name, found_id, found_rarity, found_class, found_id, found_skill_names, found_ascensions, found_skills ]

    while ( index < len(wiki) ):
        
        # if everything was found, skip ahead to find "NEXT!SERVANT"
        skip = ( found_name and found_id and found_rarity and found_class and\
                 found_id and found_skill_names and found_ascensions and found_skills)

        line = wiki[index]

        if ( skip and ("NEXT!SERVANT" not in line) ):
            index += 1
            continue

        if ( "NEXT!SERVANT" in wiki[index] ):
            
            if( current_servant.servant_id != -1 ):
                if( current_servant.servant_id in servants ):
                    if( servants[current_servant.servant_id].wikiUpdate(current_servant) ):
                        updated += 1
                else:
                    servants[current_servant.servant_id] = deepcopy(current_servant)
                    added += 1

            #print( "Added: ( {0:03d} ) ".format(current_servant.servant_id) + current_servant.name)
            skip = False

            found_name = False
            found_id = False
            found_rarity = False
            found_class = False
            found_id = False
            found_skill_names = False
            found_ascensions = False
            found_skills = False

            current_servant.reset()

            index += 1
            continue
        
        # if servant not complete, continue filling values

        if ( not found_name ):
            if ( len( line.strip() ) > 1 ):
                current_servant.name = line
                found_name = True
            index += 1
            continue
        
        if ( not found_id ):
            if ( "|id =" in line or "| id =" in line or "|id=" in line or "| id=" in line ):
                addID( line, current_servant )

                found_id = True
                index += 1
                continue

        if ( not found_rarity ):
            if ( "|stars =" in line or "| stars =" in line or "|stars=" in line or "| stars=" in line ):
                addRarity( line, current_servant )

                found_rarity = True
                index += 1
                continue

        if ( not found_class ):
            if ( "|class =" in line or "| class =" in line or "|class=" in line or "| class=" in line ):
                addClass( line, current_servant )

                found_class = True
                index += 1
                continue
        
        if ( not found_skill_names):
            if ( "First Skill" in line):
                index = addSkillNames ( wiki, index, current_servant )

                found_skill_names = True
                continue


        if ( not found_ascensions ):
            if ( "{{ascension" in line or "{{ ascension" in line or "{{Ascension" in line or "{{ Ascension" in line):
                found_ascensions = True
                index = addAscensionMats(wiki, index + 1, current_servant)
                index += 1
                continue
        

        if ( not found_skills ):
            if ( "{{skillreinforcement" in line or "{{ skillreinforcement" in line or "{{Skillreinforcement" in line or "{{ Skillreinforcement" in line ):
                index = addSkillMats(wiki, index + 1, current_servant) + 1

                found_skills = True
                continue
  
        # ITERATOR
        index += 1
    
    print()
    print("Servants Added:", added)
    print("Servants Updated:", updated)    
    print("Total Servants:", len(servants) )
    print()

def displayServant( servant ):
    print()
    print("-------------------------")
    print("Name: " + servant.name)
    print("ID: " + str(servant.servant_id))
    print("Class: " + servant.servant_class)
    print("Rarity: " + str(servant.rarity))
    print()
    print("Ascension Materials:")
    num = 1
    for asc in servant.asc_mats:
        print("Ascension " + str(num) + ": ")
        for mat in asc:
            if ( mat[0] == 923 ):
                print ("- ( " + str( mat[1] ) + " ) Welfare Ascension Mat" )
            else:
                print ("- ( " + str( mat[1] ) + " ) " + loc.MATS_ALL[ mat[0] ] )
        num += 1
    num = 2

    print()

    print("Skill Names:")
    print( servant.skill_names[0] + " | " + servant.skill_names[1] + " | " +servant.skill_names[2] )

    print()

    print("Skill Materials")
    for sk in servant.skill_mats:
        print("Skill Level " + str(num) + ": ")
        for mat in sk:
            print ("- ( " + str( mat[1] ) + " ) " + loc.MATS_ALL[ mat[0] ] )
        num += 1
    
    print("Skill Level " + str( num ) + " : ")
    print("- ( 1 ) Crystalized Lore")
    
    print()

    num = 1
    for costume in servant.costumes:
        print(servant.costume_names[num-1] + ":")
        for mat in costume:
            print ("- ( " + str( mat[1] ) + " ) " + loc.MATS_ALL[ mat[0] ] )
        num += 1
    print()
    print("-------------------------")
    print()

def viewServant( servants ):

    user_input = ""

    while(True):
        user_input = input("Enter Servant ID: ")
        if(user_input == "q"):
            break
        else:
            try:
                displayServant( servants[int(user_input)] )
            except:
                print("\n\tNO SERVANT WITH THAT ID\n")

def updateCostumeNames( servants ):
    user_input = ""

    while(True):
        user_input = input("\nEnter Servant ID: ")
        if(user_input == "q"):
            break
        else:
            try:   
                servant = servants[int(user_input)] 
            except:
                print("\n\tFailed to Add Costume")
                continue

            if ( len(servant.costumes) == 0):
                print("No Costumes for that Servant")
                return
            
            num = 1
            for costume in servant.costumes:
                print(servant.costume_names[num-1] + ":")
                for mat in costume:
                    print ("- ( " + str( mat[1] ) + " ) " + loc.MATS_ALL[ mat[0] ] )

                new_name = input("New name for this costume: ")
                if (new_name != "n"):
                    servant.costume_names[num-1] = new_name[:]

                num += 1
            
            saveServants(servants)
                

def deleteServant( servants ):
    
    user_input = ""

    while(True):
        user_input = input("\nEnter Servant ID: ")
        if(user_input == "q"):
            break
        else:
            try:   
                servant = servants[int(user_input)] 
                print("\nDeleting <", servant.name,">")        
                servants.pop( int(user_input) )
            except:
                print("\n\tNO SERVANT WITH THAT ID")
                continue

def saveServants( servants ):
    try: 
        pickle.dump ( servants, open( "servantLibrary.fgoc", "wb" ) )    

    except:
        print("\n\tFAILED TO SAVE!")


if __name__ == '__main__':

    try:
        servants = pickle.load( open( "servantLibrary.fgoc", "rb" ) )
    except:
        servants = {}
        print("\n\tFAILED TO LOAD SERVANT LIBRARY")

    user_input = ""

    while(user_input != "q"):
        print()
        print("----------------------")
        print("-Servant Library Tool-")
        print("----------------------")
        print(" [u] - Update All Servants")
        print(" [s] - Save Servants")
        print(" [v] - View Servants")
        print(" [c] - Update Servant Costume Name")
        print(" [d] - Delete Servant")
        print(" [q] - Quit")

        user_input = input("- ")

        if   (user_input == "u"):
            updateAllServants( servants )    
        elif (user_input == "s"):
            print("Saving Servants...")
            saveServants(servants)
            print("...Servants Saved!")
        elif (user_input == "v"):
            viewServant(servants)            
        elif (user_input == "c"):
            updateCostumeNames(servants)  
        elif (user_input == "d"):
            deleteServant(servants)        
        elif (user_input != "q"):
            print("Input Not Recognized")
    
    user_input = input("Save Before Quitting? (y/n)- ")
    if( user_input == "y"):
        print("Saving Servants...")
        saveServants(servants)
        print("...Servants Saved!")



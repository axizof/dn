# dungeon's nightmare [ethan]
# Un roguelike avec pygame avec :
#  - une map qui change à chaque partie mais qui garde une hiérarchie et une compréhension des niveaux
#  - Un jeu simple et rapide à prendre en main
#  - Un leaderboard et un system de sauvegarde
# Les sauvegardes et peuvent être réutilisé pour un leaderboard global
#
# Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
# You are free to: copy and redistribute if you credit the author but you can not sell the game

"""
dungeon's nightmare case
"""

import pygame
import os

#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
#                       case joueur
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-

TUILEP_TYPE_xxx = 0

TUILEP_xxx = 0

TUILEP_TYPE_CORPS = 1

TUILEP_CORPS_HUMAN_F = 0
TUILEP_CORPS_HUMAN_M = 1
TUILEP_CORPS_ELF_F = 2
TUILEP_CORPS_ELF_M = 3
TUILEP_CORPS_DEEP_ELF_F = 4
TUILEP_CORPS_DEEP_ELF_M = 5
TUILEP_CORPS_DWARF_F = 6
TUILEP_CORPS_DWARF_M = 7
TUILEP_CORPS_HALFLING_F = 8
TUILEP_CORPS_HALFLING_M = 9
TUILEP_CORPS_ORC_F = 10
TUILEP_CORPS_ORC_M = 11
TUILEP_CORPS_KOBOLD_F = 12
TUILEP_CORPS_KOBOLD_M = 13
TUILEP_CORPS_MUMMY_F = 14
TUILEP_CORPS_MUMMY_M = 15
TUILEP_CORPS_NAGA_F = 16
TUILEP_CORPS_NAGA_M = 17
TUILEP_CORPS_GNOME_F = 18
TUILEP_CORPS_GNOME_M = 19
TUILEP_CORPS_OGRE_F = 20
TUILEP_CORPS_OGRE_M = 21
TUILEP_CORPS_TROLL_F = 22
TUILEP_CORPS_TROLL_M = 23
TUILEP_CORPS_OGRE_MAGE_F = 24
TUILEP_CORPS_OGRE_MAGE_M = 25
TUILEP_CORPS_DRACONIAN_F = 26
TUILEP_CORPS_DRACONIAN_M = 27
TUILEP_CORPS_CENTAUR_F = 28
TUILEP_CORPS_CENTAUR_M = 29
TUILEP_CORPS_DEMIGOD_F = 30
TUILEP_CORPS_DEMIGOD_M = 31
TUILEP_CORPS_SPRIGGAN_F = 32
TUILEP_CORPS_SPRIGGAN_M = 33
TUILEP_CORPS_MINOTAUR_F = 34
TUILEP_CORPS_MINOTAUR_M = 35
TUILEP_CORPS_DEMONSPAWN_F = 36
TUILEP_CORPS_DEMONSPAWN_M = 37
TUILEP_CORPS_GHOUL_F = 38
TUILEP_CORPS_GHOUL_M = 39
TUILEP_CORPS_KENKU_F = 40
TUILEP_CORPS_KENKU_M = 41
TUILEP_CORPS_MERFOLK_F = 42
TUILEP_CORPS_MERFOLK_M = 43
TUILEP_CORPS_SHADOW = 44

TUILEP_TYPE_CAPE = 2

TUILEP_CAPE_RED = 0
TUILEP_CAPE_BLUE = 1
TUILEP_CAPE_MAGENTA = 2
TUILEP_CAPE_YELLOW = 3
TUILEP_CAPE_BLACK = 4
TUILEP_CAPE_GRAY = 5
TUILEP_CAPE_BROWN = 6
TUILEP_CAPE_GREEN = 7
TUILEP_CAPE_CYAN = 8
TUILEP_CAPE_WHITE = 9

TUILEP_TYPE_PIEDS = 3

TUILEP_PIEDS_SHORT_RED = 0
TUILEP_PIEDS_SHORT_PURPLE = 1
TUILEP_PIEDS_SHORT_BROWN = 2
TUILEP_PIEDS_SHORT_BROWN2 = 3
TUILEP_PIEDS_PJ = 4
TUILEP_PIEDS_MIDDLE_BROWN = 5
TUILEP_PIEDS_MIDDLE_GRAY = 6
TUILEP_PIEDS_MIDDLE_GREEN = 7
TUILEP_PIEDS_MIDDLE_YBROWN = 8
TUILEP_PIEDS_MIDDLE_PURPLE = 9
TUILEP_PIEDS_MIDDLE_BROWN2 = 10
TUILEP_PIEDS_MESH_RED = 11
TUILEP_PIEDS_MESH_BLACK = 12
TUILEP_PIEDS_MESH_WHITE = 13
TUILEP_PIEDS_MESH_BLUE = 14
TUILEP_PIEDS_MIDDLE_GOLD = 15
TUILEP_PIEDS_LONG_RED = 16

TUILEP_TYPE_JAMBES = 4

TUILEP_JAMBES_BIKINI_RED = 0
TUILEP_JAMBES_LOINCLOTH_RED = 1
TUILEP_JAMBES_BELT_REDBROWN = 2
TUILEP_JAMBES_BELT_GRAY = 3
TUILEP_JAMBES_PANTS_BLACK = 4
TUILEP_JAMBES_PANTS_ORANGE = 5
TUILEP_JAMBES_PANTS_BLUE = 6
TUILEP_JAMBES_PANTS_DARKGREEN = 7
TUILEP_JAMBES_PANTS_BROWN = 8
TUILEP_JAMBES_PANTS_SHORT_DARKBROWN = 9
TUILEP_JAMBES_PANTS_SHORT_BROWN = 10
TUILEP_JAMBES_PANTS_SHORT_BROWN3 = 11
TUILEP_JAMBES_PANTS_SHORT_GRAY = 12
TUILEP_JAMBES_PJ = 13
TUILEP_JAMBES_SKIRT_BLUE = 14
TUILEP_JAMBES_SKIRT_GREEN = 15
TUILEP_JAMBES_SKIRT_WHITE = 16
TUILEP_JAMBES_METAL_GRAY = 17
TUILEP_JAMBES_METAL_GREEN = 18
TUILEP_JAMBES_PANTS16 = 19
TUILEP_JAMBES_LEG_ARMOR00 = 20
TUILEP_JAMBES_LEG_ARMOR01 = 21
TUILEP_JAMBES_LEG_ARMOR02 = 22
TUILEP_JAMBES_LEG_ARMOR03 = 23
TUILEP_JAMBES_LEG_ARMOR04 = 24
TUILEP_JAMBES_LEG_ARMOR05 = 25

TUILEP_TYPE_TORSE = 5

TUILEP_TORSE_ROBE_BLUE = 0
TUILEP_TORSE_ROBE_BLACK = 1
TUILEP_TORSE_ROBE_WHITE = 2
TUILEP_TORSE_ROBE_RED = 3
TUILEP_TORSE_ROBE_MAGENTA = 4
TUILEP_TORSE_ROBE_GREEN = 5
TUILEP_TORSE_ROBE_YELLOW = 6
TUILEP_TORSE_ROBE_BROWN = 7
TUILEP_TORSE_ROBE_CYAN = 8
TUILEP_TORSE_ROBE_RAINBOW = 9
TUILEP_TORSE_GANDALF_G = 10
TUILEP_TORSE_SARUMAN = 11
TUILEP_TORSE_ROBE_BLACK_HOOD = 12
TUILEP_TORSE_MONK_BLUE = 13
TUILEP_TORSE_MONK_BLACK = 14
TUILEP_TORSE_DRESS_GREEN = 15
TUILEP_TORSE_ROBE_BLACK_GOLD = 16
TUILEP_TORSE_ROBE_WHITE2 = 17
TUILEP_TORSE_ROBE_RED2 = 18
TUILEP_TORSE_ROBE_WHITE_RED = 19
TUILEP_TORSE_ROBE_WHITE_GREEN = 20
TUILEP_TORSE_ROBE_BLUE_WHITE = 21
TUILEP_TORSE_ROBE_PURPLE = 22
TUILEP_TORSE_ROBE_RED_GOLD = 23
TUILEP_TORSE_ROBE_BLACK_RED = 24
TUILEP_TORSE_ROBE_BLUE_GREEN = 25
TUILEP_TORSE_ROBE_RED3 = 26
TUILEP_TORSE_ROBE_BROWN2 = 27
TUILEP_TORSE_ROBE_GREEN_GOLD = 28
TUILEP_TORSE_ROBE_BROWN3 = 29
TUILEP_TORSE_ROBE_GRAY2 = 30
TUILEP_TORSE_DRESS_WHITE = 31
TUILEP_TORSE_ARWEN = 32
TUILEP_TORSE_SKIRT_ONEP_GREY = 33
TUILEP_TORSE_BLOODY = 34
TUILEP_TORSE_LEATHER_SHORT = 35
TUILEP_TORSE_CHINA_RED2 = 36
TUILEP_TORSE_ANIMAL_SKIN = 37
TUILEP_TORSE_NECK = 38
TUILEP_TORSE_BELT1 = 39
TUILEP_TORSE_BELT2 = 40
TUILEP_TORSE_SUSP_BLACK = 41
TUILEP_TORSE_SHOULDER_PAD = 42
TUILEP_TORSE_MESH_BLACK = 43
TUILEP_TORSE_MESH_RED = 44
TUILEP_TORSE_LEATHER_JACKET = 45
TUILEP_TORSE_SHIRT_WHITE1 = 46
TUILEP_TORSE_SHIRT_WHITE2 = 47
TUILEP_TORSE_SHIRT_WHITE3 = 48
TUILEP_TORSE_SHIRT_BLUE = 49
TUILEP_TORSE_BIKINI_RED = 50
TUILEP_TORSE_SHIRT_HAWAII = 51
TUILEP_TORSE_CHINA_RED = 52
TUILEP_TORSE_LEATHER_RED = 53
TUILEP_TORSE_CHUNLI = 54
TUILEP_TORSE_SHIRT_WHITE_YELLOW = 55
TUILEP_TORSE_SHIRT_CHECK = 56
TUILEP_TORSE_SLIT_BLACK = 57
TUILEP_TORSE_LEATHER_ARMOUR = 58
TUILEP_TORSE_LEATHER_GREEN = 59
TUILEP_TORSE_SHIRT_BLACK = 60
TUILEP_TORSE_SHIRT_BLACK_AND_CLOTH = 61
TUILEP_TORSE_SHIRT_BLACK3 = 62
TUILEP_TORSE_LEATHER2 = 63
TUILEP_TORSE_CHAINMAIL3 = 64
TUILEP_TORSE_SHIRT_VEST = 65
TUILEP_TORSE_KARATE = 66
TUILEP_TORSE_KARATE2 = 67
TUILEP_TORSE_LEATHER_HEAVY = 68
TUILEP_TORSE_TROLL_HIDE = 69
TUILEP_TORSE_GREEN_CHAIN = 70
TUILEP_TORSE_METAL_BLUE = 71
TUILEP_TORSE_GREEN_SUSP = 72
TUILEP_TORSE_JACKET2 = 73
TUILEP_TORSE_JACKET3 = 74
TUILEP_TORSE_LEATHER_STUD = 75
TUILEP_TORSE_JACKET_STUD = 76
TUILEP_TORSE_CHAINMAIL = 77
TUILEP_TORSE_CHAINMAIL2 = 78
TUILEP_TORSE_HALF_PLATE = 79
TUILEP_TORSE_HALF_PLATE2 = 80
TUILEP_TORSE_HALF_PLATE3 = 81
TUILEP_TORSE_BREAST_BLACK = 82
TUILEP_TORSE_VEST_RED = 83
TUILEP_TORSE_BPLATE_GREEN = 84
TUILEP_TORSE_BPLATE_METAL1 = 85
TUILEP_TORSE_BANDED = 86
TUILEP_TORSE_PLATE_AND_CLOTH = 87
TUILEP_TORSE_PLATE_AND_CLOTH2 = 88
TUILEP_TORSE_SCALEMAIL = 89
TUILEP_TORSE_LEATHER_METAL = 90
TUILEP_TORSE_PLATE = 91
TUILEP_TORSE_PLATE_BLACK = 92
TUILEP_TORSE_CRYSTAL_PLATE = 93
TUILEP_TORSE_ARMOR_MUMMY = 94
TUILEP_TORSE_DRAGONSC_GREEN = 95
TUILEP_TORSE_DRAGONSC_WHITE = 96
TUILEP_TORSE_DRAGONSC_MAGENTA = 97
TUILEP_TORSE_DRAGONSC_CYAN = 98
TUILEP_TORSE_DRAGONSC_BROWN = 99
TUILEP_TORSE_DRAGONSC_BLUE = 100
TUILEP_TORSE_DRAGONSC_GOLD = 101
TUILEP_TORSE_DRAGONARM_GREEN = 102
TUILEP_TORSE_DRAGONARM_WHITE = 103
TUILEP_TORSE_DRAGONARM_MAGENTA = 104
TUILEP_TORSE_DRAGONARM_CYAN = 105
TUILEP_TORSE_DRAGONARM_BROWN = 106
TUILEP_TORSE_DRAGONARM_BLUE = 107
TUILEP_TORSE_DRAGONARM_GOLD = 108
TUILEP_TORSE_ARAGORN = 109
TUILEP_TORSE_BOROMIR = 110
TUILEP_TORSE_FRODO = 111
TUILEP_TORSE_GIMLI = 112
TUILEP_TORSE_LEGOLAS = 113
TUILEP_TORSE_MERRY = 114
TUILEP_TORSE_PIPIN = 115
TUILEP_TORSE_PJ = 116
TUILEP_TORSE_SAM = 117
TUILEP_TORSE_EDISON = 118
TUILEP_TORSE_LEARS_CHAIN_MAIL = 119
TUILEP_TORSE_ROBE_OF_NIGHT = 120

TUILEP_TYPE_BRAS = 6

TUILEP_BRAS_GLOVE_RED = 0
TUILEP_BRAS_GLOVE_GRAY = 1
TUILEP_BRAS_GLOVE_WHITE = 2
TUILEP_BRAS_GLOVE_BLUE = 3
TUILEP_BRAS_GLOVE_BLACK = 4
TUILEP_BRAS_GLOVE_ORANGE = 5
TUILEP_BRAS_GLOVE_BROWN = 6
TUILEP_BRAS_GLOVE_BLACK2 = 7
TUILEP_BRAS_GLOVE_GRAYFIST = 8
TUILEP_BRAS_GLOVE_PURPLE = 9
TUILEP_BRAS_GLOVE_WRIST_PURPLE = 10
TUILEP_BRAS_GLOVE_CHUNLI = 11
TUILEP_BRAS_GLOVE_GOLD = 12
TUILEP_BRAS_GLOVE_SHORT_YELLOW = 13
TUILEP_BRAS_GLOVE_SHORT_RED = 14
TUILEP_BRAS_GLOVE_SHORT_WHITE = 15
TUILEP_BRAS_GLOVE_SHORT_GREEN = 16
TUILEP_BRAS_GLOVE_SHORT_BLUE = 17
TUILEP_BRAS_GLOVE_SHORT_GRAY = 18

TUILEP_TYPE_MAIN_D = 7

TUILEP_MAIN_D_DAGGER = 0
TUILEP_MAIN_D_DAGGER_SLANT = 1
TUILEP_MAIN_D_SHORT_SWORD = 2
TUILEP_MAIN_D_SHORT_SWORD2 = 3
TUILEP_MAIN_D_SWORD_THIEF = 4
TUILEP_MAIN_D_LONG_SWORD = 5
TUILEP_MAIN_D_LONG_SWORD_SLANT = 6
TUILEP_MAIN_D_GREAT_SWORD = 7
TUILEP_MAIN_D_GREAT_SWORD_SLANT = 8
TUILEP_MAIN_D_KATANA = 9
TUILEP_MAIN_D_SCIMITAR = 10
TUILEP_MAIN_D_SCIMITAR2 = 11
TUILEP_MAIN_D_SWORD2 = 12
TUILEP_MAIN_D_SWORD_TRI = 13
TUILEP_MAIN_D_BROADSWORD = 14
TUILEP_MAIN_D_BLACK_SWORD = 15
TUILEP_MAIN_D_SWORD_BLACK = 16
TUILEP_MAIN_D_SWORD_TWIST = 17
TUILEP_MAIN_D_KNIFE = 18
TUILEP_MAIN_D_SWORD_SEVEN = 19
TUILEP_MAIN_D_HEAVY_SWORD = 20
TUILEP_MAIN_D_SABRE = 21
TUILEP_MAIN_D_SWORD3 = 22
TUILEP_MAIN_D_SWORD_BREAKER = 23
TUILEP_MAIN_D_SWORD_JAG = 24
TUILEP_MAIN_D_BLOODBANE = 25
TUILEP_MAIN_D_CHILLY_DEATH = 26
TUILEP_MAIN_D_DOOM_KNIGHT = 27
TUILEP_MAIN_D_FLAMING_DEATH = 28
TUILEP_MAIN_D_LEECH = 29
TUILEP_MAIN_D_MORG = 30
TUILEP_MAIN_D_PLUTONIUM_SWORD = 31
TUILEP_MAIN_D_JIHAD = 32
TUILEP_MAIN_D_SINGING_SWORD = 33
TUILEP_MAIN_D_ZONGULDROK = 34
TUILEP_MAIN_D_CLUB = 35
TUILEP_MAIN_D_CLUB2 = 36
TUILEP_MAIN_D_CLUB3 = 37
TUILEP_MAIN_D_STICK = 38
TUILEP_MAIN_D_GIANT_CLUB = 39
TUILEP_MAIN_D_GIANT_CLUB_SPIKE = 40
TUILEP_MAIN_D_WHIP = 41
TUILEP_MAIN_D_SCEPTRE = 42
TUILEP_MAIN_D_MACE = 43
TUILEP_MAIN_D_MACE_RUBY = 44
TUILEP_MAIN_D_MORNINGSTAR = 45
TUILEP_MAIN_D_MORNINGSTAR2 = 46
TUILEP_MAIN_D_LARGE_MACE = 47
TUILEP_MAIN_D_BLACK_WHIP = 48
TUILEP_MAIN_D_HAMMER = 49
TUILEP_MAIN_D_HAMMER2 = 50
TUILEP_MAIN_D_FRAIL_STICK = 51
TUILEP_MAIN_D_FRAIL_BALL = 52
TUILEP_MAIN_D_FRAIL_SPIKE = 53
TUILEP_MAIN_D_FRAIL_BALL2 = 54
TUILEP_MAIN_D_FRAIL_BALLS = 55
TUILEP_MAIN_D_FRAIL_BALL3 = 56
TUILEP_MAIN_D_FRAIL_BALL4 = 57
TUILEP_MAIN_D_NUNCHAKU = 58
TUILEP_MAIN_D_MACE_OF_VARIABILITY = 59
TUILEP_MAIN_D_SPEAR1 = 60
TUILEP_MAIN_D_SPEAR2 = 61
TUILEP_MAIN_D_SPEAR3 = 62
TUILEP_MAIN_D_SPEAR4 = 63
TUILEP_MAIN_D_SPEAR5 = 64
TUILEP_MAIN_D_HOOK = 65
TUILEP_MAIN_D_HALBERD = 66
TUILEP_MAIN_D_PICK_AXE = 67
TUILEP_MAIN_D_TRIDENT = 68
TUILEP_MAIN_D_TRIDENT_ELEC = 69
TUILEP_MAIN_D_TRIDENT2 = 70
TUILEP_MAIN_D_TRIDENT3 = 71
TUILEP_MAIN_D_LANCE = 72
TUILEP_MAIN_D_LANCE2 = 73
TUILEP_MAIN_D_SCYTHE = 74
TUILEP_MAIN_D_PIKE = 75
TUILEP_MAIN_D_QUARTERSTAFF1 = 76
TUILEP_MAIN_D_QUARTERSTAFF2 = 77
TUILEP_MAIN_D_QUARTERSTAFF3 = 78
TUILEP_MAIN_D_QUARTERSTAFF4 = 79
TUILEP_MAIN_D_SICKLE = 80
TUILEP_MAIN_D_GLAIVE = 81
TUILEP_MAIN_D_GLAIVE2 = 82
TUILEP_MAIN_D_GLAIVE3 = 83
TUILEP_MAIN_D_D_GLAIVE = 84
TUILEP_MAIN_D_POLE_FORKED = 85
TUILEP_MAIN_D_FORK2 = 86
TUILEP_MAIN_D_GLAIVE_OF_PRUNE = 87
TUILEP_MAIN_D_VOODOO = 88
TUILEP_MAIN_D_FINISHER = 89
TUILEP_MAIN_D_STAFF_SKULL = 90
TUILEP_MAIN_D_STAFF_MAGE = 91
TUILEP_MAIN_D_STAFF_MAGE2 = 92
TUILEP_MAIN_D_GREAT_STAFF = 93
TUILEP_MAIN_D_STAFF_EVIL = 94
TUILEP_MAIN_D_STAFF_RING_BLUE = 95
TUILEP_MAIN_D_STAFF_MUMMY = 96
TUILEP_MAIN_D_STAFF_FORK = 97
TUILEP_MAIN_D_STAFF_RUBY = 98
TUILEP_MAIN_D_STAFF_LARGE = 99
TUILEP_MAIN_D_ELEMENTAL_STAFF = 100
TUILEP_MAIN_D_ASMODEUS = 101
TUILEP_MAIN_D_DISPATER = 102
TUILEP_MAIN_D_OLGREB = 103
TUILEP_MAIN_D_AXE = 104
TUILEP_MAIN_D_AXE_SMALL = 105
TUILEP_MAIN_D_HAND_AXE = 106
TUILEP_MAIN_D_WAR_AXE = 107
TUILEP_MAIN_D_GREAT_AXE = 108
TUILEP_MAIN_D_AXE_DOUBLE = 109
TUILEP_MAIN_D_AXE_BLOOD = 110
TUILEP_MAIN_D_AXE_SHORT = 111
TUILEP_MAIN_D_ARGA = 112
TUILEP_MAIN_D_SLING = 113
TUILEP_MAIN_D_BOW = 114
TUILEP_MAIN_D_BOW2 = 115
TUILEP_MAIN_D_BOW3 = 116
TUILEP_MAIN_D_GREAT_BOW = 117
TUILEP_MAIN_D_BOW_BLUE = 118
TUILEP_MAIN_D_CROSSBOW = 119
TUILEP_MAIN_D_CROSSBOW2 = 120
TUILEP_MAIN_D_CROSSBOW3 = 121
TUILEP_MAIN_D_CROSSBOW4 = 122
TUILEP_MAIN_D_PUNK = 123
TUILEP_MAIN_D_SNIPER = 124
TUILEP_MAIN_D_KRISHNA = 125
TUILEP_MAIN_D_DIRT = 126
TUILEP_MAIN_D_BONE_LANTERN = 127
TUILEP_MAIN_D_FAN = 128
TUILEP_MAIN_D_BOTTLE = 129
TUILEP_MAIN_D_BOX = 130
TUILEP_MAIN_D_CRYSTAL = 131
TUILEP_MAIN_D_DECK = 132
TUILEP_MAIN_D_DISC = 133
TUILEP_MAIN_D_HORN = 134
TUILEP_MAIN_D_LANTERN = 135
TUILEP_MAIN_D_ORB = 136
TUILEP_MAIN_D_STONE = 137
TUILEP_MAIN_D_FIRE_RED = 138
TUILEP_MAIN_D_FIRE_BLUE = 139
TUILEP_MAIN_D_SKULL = 140
TUILEP_MAIN_D_HEAD = 141
TUILEP_MAIN_D_FIRE_GREEN = 142
TUILEP_MAIN_D_FIRE_CYAN = 143
TUILEP_MAIN_D_FIRE_WHITE = 144
TUILEP_MAIN_D_LIGHT_BLUE = 145
TUILEP_MAIN_D_LIGHT_RED = 146
TUILEP_MAIN_D_LIGHT_YELLOW = 147
TUILEP_MAIN_D_SPARK = 148
TUILEP_MAIN_D_FIRE_DARK = 149
TUILEP_MAIN_D_FIRE_WHITE2 = 150
TUILEP_MAIN_D_ARAGORN = 151
TUILEP_MAIN_D_ARWEN = 152
TUILEP_MAIN_D_BOROMIR = 153
TUILEP_MAIN_D_FRODO = 154
TUILEP_MAIN_D_GANDALF = 155
TUILEP_MAIN_D_GIMLI = 156
TUILEP_MAIN_D_LEGOLAS = 157
TUILEP_MAIN_D_SARUMAN = 158

TUILEP_TYPE_MAIN_G = 8

TUILEP_MAIN_G_SHIELD_ROUND_SMALL = 0
TUILEP_MAIN_G_SHIELD_ROUND_SMALL2 = 1
TUILEP_MAIN_G_BULLSEYE = 2
TUILEP_MAIN_G_SHIELD_MIDDLE_ROUND = 3
TUILEP_MAIN_G_SHIELD_SKULL = 4
TUILEP_MAIN_G_SHIELD_ROUND_WHITE = 5
TUILEP_MAIN_G_BOROMIR = 6
TUILEP_MAIN_G_SHIELD_ROUND1 = 7
TUILEP_MAIN_G_SHIELD_ROUND2 = 8
TUILEP_MAIN_G_SHIELD_ROUND3 = 9
TUILEP_MAIN_G_SHIELD_ROUND4 = 10
TUILEP_MAIN_G_SHIELD_ROUND5 = 11
TUILEP_MAIN_G_SHIELD_ROUND6 = 12
TUILEP_MAIN_G_SHIELD_ROUND7 = 13
TUILEP_MAIN_G_SHIELD_KNIGHT_BLUE = 14
TUILEP_MAIN_G_SHIELD_KNIGHT_GRAY = 15
TUILEP_MAIN_G_SHIELD_KNIGHT_RW = 16
TUILEP_MAIN_G_SHIELD_MIDDLE_UNICORN = 17
TUILEP_MAIN_G_SHIELD_KITE1 = 18
TUILEP_MAIN_G_SHIELD_KITE2 = 19
TUILEP_MAIN_G_SHIELD_KITE3 = 20
TUILEP_MAIN_G_SHIELD_KITE4 = 21
TUILEP_MAIN_G_SHIELD_LONG_RED = 22
TUILEP_MAIN_G_SHIELD_MIDDLE_GRAY = 23
TUILEP_MAIN_G_SHIELD_DIAMOND_YELLOW = 24
TUILEP_MAIN_G_SHIELD_MIDDLE_BROWN = 25
TUILEP_MAIN_G_SHIELD_MIDDLE_BLACK = 26
TUILEP_MAIN_G_SHIELD_MIDDLE_CYAN = 27
TUILEP_MAIN_G_SHIELD_MIDDLE_ETHN = 28
TUILEP_MAIN_G_SHIELD_LONG_CROSS = 29
TUILEP_MAIN_G_SHIELD_SHAMAN = 30
TUILEP_MAIN_G_SHIELD_OF_RESISTANCE = 31
TUILEP_MAIN_G_BOOK_BLACK = 32
TUILEP_MAIN_G_BOOK_BLUE = 33
TUILEP_MAIN_G_BOOK_RED = 34
TUILEP_MAIN_G_BOOK_MAGENTA = 35
TUILEP_MAIN_G_BOOK_GREEN = 36
TUILEP_MAIN_G_BOOK_CYAN = 37
TUILEP_MAIN_G_BOOK_YELLOW = 38
TUILEP_MAIN_G_BOOK_WHITE = 39
TUILEP_MAIN_G_BOOK_SKY = 40
TUILEP_MAIN_G_BOOK_BLUE_DIM = 41
TUILEP_MAIN_G_BOOK_CYAN_DIM = 42
TUILEP_MAIN_G_BOOK_GREEN_DIM = 43
TUILEP_MAIN_G_BOOK_MAGENTA_DIM = 44
TUILEP_MAIN_G_BOOK_RED_DIM = 45
TUILEP_MAIN_G_BOOK_YELLOW_DIM = 46
TUILEP_MAIN_G_FIRE_GREEN = 47
TUILEP_MAIN_G_FIRE_CYAN = 48
TUILEP_MAIN_G_FIRE_WHITE = 49
TUILEP_MAIN_G_LIGHT_BLUE = 50
TUILEP_MAIN_G_LIGHT_RED = 51
TUILEP_MAIN_G_LIGHT_YELLOW = 52
TUILEP_MAIN_G_SPARK = 53
TUILEP_MAIN_G_FIRE_DARK = 54
TUILEP_MAIN_G_FIRE_WHITE2 = 55
TUILEP_MAIN_G_LANTERN = 56
TUILEP_MAIN_G_TORCH = 57
TUILEP_MAIN_G_PJ = 58
TUILEP_MAIN_G_TORSH2 = 59

TUILEP_TYPE_CHEVEUX = 9

TUILEP_CHEVEUX_SHORT_BLACK = 0
TUILEP_CHEVEUX_SHORT_RED = 1
TUILEP_CHEVEUX_SHORT_YELLOW = 2
TUILEP_CHEVEUX_SHORT_WHITE = 3
TUILEP_CHEVEUX_LONG_BLACK = 4
TUILEP_CHEVEUX_LONG_RED = 5
TUILEP_CHEVEUX_LONG_YELLOW = 6
TUILEP_CHEVEUX_LONG_WHITE = 7
TUILEP_CHEVEUX_FEM_BLACK = 8
TUILEP_CHEVEUX_FEM_RED = 9
TUILEP_CHEVEUX_FEM_YELLOW = 10
TUILEP_CHEVEUX_FEM_WHITE = 11
TUILEP_CHEVEUX_ELF_BLACK = 12
TUILEP_CHEVEUX_ELF_RED = 13
TUILEP_CHEVEUX_ELF_YELLOW = 14
TUILEP_CHEVEUX_ELF_WHITE = 15
TUILEP_CHEVEUX_ARAGORN = 16
TUILEP_CHEVEUX_ARWEN = 17
TUILEP_CHEVEUX_BOROMIR = 18
TUILEP_CHEVEUX_FRODO = 19
TUILEP_CHEVEUX_LEGOLAS = 20
TUILEP_CHEVEUX_MERRY = 21
TUILEP_CHEVEUX_PJ = 22
TUILEP_CHEVEUX_SAM = 23

TUILEP_TYPE_BARBE = 10

TUILEP_BARBE_SHORT_BLACK = 0
TUILEP_BARBE_SHORT_RED = 1
TUILEP_BARBE_SHORT_YELLOW = 2
TUILEP_BARBE_SHORT_WHITE = 3
TUILEP_BARBE_LONG_BLACK = 4
TUILEP_BARBE_LONG_RED = 5
TUILEP_BARBE_LONG_YELLOW = 6
TUILEP_BARBE_LONG_WHITE = 7
TUILEP_BARBE_PJ = 8

TUILEP_TYPE_TETE = 11

TUILEP_TETE_CONE_BLUE = 0
TUILEP_TETE_CONE_RED = 1
TUILEP_TETE_STRAW = 2
TUILEP_TETE_WIZARD_BLUE = 3
TUILEP_TETE_CAP_BLUE = 4
TUILEP_TETE_BANDANA_YBROWN = 5
TUILEP_TETE_HAT_BLACK = 6
TUILEP_TETE_GANDALF = 7
TUILEP_TETE_CROWN_GOLD = 8
TUILEP_TETE_CAP_BLACK1 = 9
TUILEP_TETE_CLOWN1 = 10
TUILEP_TETE_FEATHER_GREEN = 11
TUILEP_TETE_FEATHER_RED = 12
TUILEP_TETE_FEATHER_BLUE = 13
TUILEP_TETE_FEATHER_YELLOW = 14
TUILEP_TETE_FEATHER_WHITE = 15
TUILEP_TETE_BAND_WHITE = 16
TUILEP_TETE_BAND_RED = 17
TUILEP_TETE_BAND_YELLOW = 18
TUILEP_TETE_BAND_BLUE = 19
TUILEP_TETE_BAND_MAGENTA = 20
TUILEP_TETE_TAISO_BLUE = 21
TUILEP_TETE_TAISO_MAGENTA = 22
TUILEP_TETE_TAISO_YELLOW = 23
TUILEP_TETE_TAISO_RED = 24
TUILEP_TETE_TAISO_WHITE = 25
TUILEP_TETE_DYROVEPREVA = 26
TUILEP_TETE_WIZARD_PURPLE = 27
TUILEP_TETE_WIZARD_BLUEGREEN = 28
TUILEP_TETE_WIZARD_DARKGREEN = 29
TUILEP_TETE_WIZARD_BROWN = 30
TUILEP_TETE_WIZARD_BLACKGOLD = 31
TUILEP_TETE_WIZARD_BLACKRED = 32
TUILEP_TETE_WIZARD_RED = 33
TUILEP_TETE_WIZARD_WHITE = 34
TUILEP_TETE_TURBAN_WHITE = 35
TUILEP_TETE_TURBAN_BROWN = 36
TUILEP_TETE_IRON1 = 37
TUILEP_TETE_HELM_RED = 38
TUILEP_TETE_HORNED = 39
TUILEP_TETE_HELM_GREEN = 40
TUILEP_TETE_CHEEK_RED = 41
TUILEP_TETE_IRON_RED = 42
TUILEP_TETE_BLUE_HORN_GOLD = 43
TUILEP_TETE_HOOD_WHITE = 44
TUILEP_TETE_YELLOW_WING = 45
TUILEP_TETE_BROWN_GOLD = 46
TUILEP_TETE_BLACK_HORN = 47
TUILEP_TETE_FULL_GOLD = 48
TUILEP_TETE_CHAIN = 49
TUILEP_TETE_BLACK_HORN2 = 50
TUILEP_TETE_FULL_BLACK = 51
TUILEP_TETE_HORN_GRAY = 52
TUILEP_TETE_IRON2 = 53
TUILEP_TETE_IRON3 = 54
TUILEP_TETE_FHELM_GRAY3 = 55
TUILEP_TETE_FHELM_HORN_YELLOW = 56
TUILEP_TETE_FHELM_HORN2 = 57
TUILEP_TETE_HORN_EVIL = 58
TUILEP_TETE_HELM_PLUME = 59
TUILEP_TETE_MUMMY = 60
TUILEP_TETE_ART_DRAGONHELM = 61
TUILEP_TETE_HEALER = 62
TUILEP_TETE_HOOD_GRAY = 63
TUILEP_TETE_HOOD_RED = 64
TUILEP_TETE_HOOD_GREEN2 = 65
TUILEP_TETE_HOOD_CYAN = 66
TUILEP_TETE_HOOD_ORANGE = 67
TUILEP_TETE_HOOD_RED2 = 68
TUILEP_TETE_HOOD_BLACK2 = 69
TUILEP_TETE_HOOD_WHITE2 = 70
TUILEP_TETE_HOOD_YBROWN = 71
TUILEP_TETE_HOOD_GREEN = 72
TUILEP_TETE_NINJA_BLACK = 73

#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
#                         cases
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-

class RLTiles:
    def __init__(self):
        self.corps = (\
            (0,0,31,31,"corps","human_f"),
            (32,0,63,31,"corps","human_m"),
            (64,0,95,31,"corps","elf_f"),
            (96,0,127,31,"corps","elf_m"),
            (128,0,159,31,"corps","deep_elf_f"),
            (160,0,191,31,"corps","deep_elf_m"),
            (192,0,223,31,"corps","dwarf_f"),
            (224,0,255,31,"corps","dwarf_m"),
            (256,0,287,31,"corps","halfling_f"),
            (288,0,319,31,"corps","halfling_m"),
            (320,0,351,31,"corps","orc_f"),
            (352,0,383,31,"corps","orc_m"),
            (384,0,415,31,"corps","kobold_f"),
            (416,0,447,31,"corps","kobold_m"),
            (448,0,479,31,"corps","mummy_f"),
            (480,0,511,31,"corps","mummy_m"),
            (512,0,543,31,"corps","naga_f"),
            (544,0,575,31,"corps","naga_m"),
            (576,0,607,31,"corps","gnome_f"),
            (608,0,639,31,"corps","gnome_m"),
            (0,32,31,63,"corps","ogre_f"),
            (32,32,63,63,"corps","ogre_m"),
            (64,32,95,63,"corps","troll_f"),
            (96,32,127,63,"corps","troll_m"),
            (128,32,159,63,"corps","ogre_mage_f"),
            (160,32,191,63,"corps","ogre_mage_m"),
            (192,32,223,63,"corps","draconian_f"),
            (224,32,255,63,"corps","draconian_m"),
            (256,32,287,63,"corps","centaur_f"),
            (288,32,319,63,"corps","centaur_m"),
            (320,32,351,63,"corps","demigod_f"),
            (352,32,383,63,"corps","demigod_m"),
            (384,32,415,63,"corps","spriggan_f"),
            (416,32,447,63,"corps","spriggan_m"),
            (448,32,479,63,"corps","minotaur_f"),
            (480,32,511,63,"corps","minotaur_m"),
            (512,32,543,63,"corps","demonspawn_f"),
            (544,32,575,63,"corps","demonspawn_m"),
            (576,32,607,63,"corps","ghoul_f"),
            (608,32,639,63,"corps","ghoul_m"),
            (0,64,31,95,"corps","kenku_f"),
            (32,64,63,95,"corps","kenku_m"),
            (64,64,95,95,"corps","merfolk_f"),
            (96,64,127,95,"corps","merfolk_m"),
            (128,64,159,95,"corps","shadow"))
        
        self.cape = (\
            (160,64,191,95,"cape","red"),
            (192,64,223,95,"cape","blue"),
            (224,64,255,95,"cape","magenta"),
            (256,64,287,95,"cape","yellow"),
            (288,64,319,95,"cape","black"),
            (320,64,351,95,"cape","gray"),
            (352,64,383,95,"cape","brown"),
            (384,64,415,95,"cape","green"),
            (416,64,447,95,"cape","cyan"),
            (448,64,479,95,"cape","white"))
        
        self.pieds = (\
            (480,64,511,79,"pieds","short_red"),
            (480,80,511,95,"pieds","short_purple"),
            (512,64,543,79,"pieds","short_brown"),
            (512,80,543,95,"pieds","short_brown2"),
            (544,64,575,79,"pieds","pj"),
            (544,80,575,95,"pieds","middle_brown"),
            (576,64,607,79,"pieds","middle_gray"),
            (576,80,607,95,"pieds","middle_green"),
            (608,64,639,79,"pieds","middle_ybrown"),
            (608,80,639,95,"pieds","middle_purple"),
            (0,96,31,111,"pieds","middle_brown2"),
            (0,112,31,127,"pieds","mesh_red"),
            (32,96,63,111,"pieds","mesh_black"),
            (32,112,63,127,"pieds","mesh_white"),
            (64,96,95,111,"pieds","mesh_blue"),
            (64,112,95,127,"pieds","middle_gold"),
            (96,96,127,111,"pieds","long_red"))
        
        self.jambes = (\
            (128,96,159,111,"jambes","bikini_red"),
            (128,112,159,127,"jambes","loincloth_red"),
            (160,96,191,111,"jambes","belt_redbrown"),
            (160,112,191,127,"jambes","belt_gray"),
            (192,96,223,111,"jambes","pants_black"),
            (192,112,223,127,"jambes","pants_orange"),
            (224,96,255,111,"jambes","pants_blue"),
            (224,112,255,127,"jambes","pants_darkgreen"),
            (256,96,287,111,"jambes","pants_brown"),
            (256,112,287,127,"jambes","pants_short_darkbrown"),
            (288,96,319,111,"jambes","pants_short_brown"),
            (288,112,319,127,"jambes","pants_short_brown3"),
            (320,96,351,111,"jambes","pants_short_gray"),
            (320,112,351,127,"jambes","pj"),
            (352,96,383,111,"jambes","skirt_blue"),
            (352,112,383,127,"jambes","skirt_green"),
            (384,96,415,111,"jambes","skirt_white"),
            (384,112,415,127,"jambes","metal_gray"),
            (416,96,447,111,"jambes","metal_green"),
            (416,112,447,127,"jambes","pants16"),
            (448,96,479,111,"jambes","leg_armor00"),
            (448,112,479,127,"jambes","leg_armor01"),
            (480,96,511,111,"jambes","leg_armor02"),
            (480,112,511,127,"jambes","leg_armor03"),
            (512,96,543,111,"jambes","leg_armor04"),
            (512,112,543,127,"jambes","leg_armor05"))
        
        self.torse = (\
            (544,96,559,127,"torse","robe_blue"),
            (560,96,575,127,"torse","robe_black"),
            (576,96,591,127,"torse","robe_white"),
            (592,96,607,127,"torse","robe_red"),
            (608,96,623,127,"torse","robe_magenta"),
            (624,96,639,127,"torse","robe_green"),
            (0,128,15,159,"torse","robe_yellow"),
            (16,128,31,159,"torse","robe_brown"),
            (32,128,47,159,"torse","robe_cyan"),
            (48,128,63,159,"torse","robe_rainbow"),
            (64,128,79,159,"torse","gandalf_g"),
            (80,128,95,159,"torse","saruman"),
            (96,128,111,159,"torse","robe_black_hood"),
            (112,128,127,159,"torse","monk_blue"),
            (128,128,143,159,"torse","monk_black"),
            (144,128,159,159,"torse","dress_green"),
            (160,128,175,159,"torse","robe_black_gold"),
            (176,128,191,159,"torse","robe_white2"),
            (192,128,207,159,"torse","robe_red2"),
            (208,128,223,159,"torse","robe_white_red"),
            (224,128,239,159,"torse","robe_white_green"),
            (240,128,255,159,"torse","robe_blue_white"),
            (256,128,271,159,"torse","robe_purple"),
            (272,128,287,159,"torse","robe_red_gold"),
            (288,128,303,159,"torse","robe_black_red"),
            (304,128,319,159,"torse","robe_blue_green"),
            (320,128,335,159,"torse","robe_red3"),
            (336,128,351,159,"torse","robe_brown2"),
            (352,128,367,159,"torse","robe_green_gold"),
            (368,128,383,159,"torse","robe_brown3"),
            (384,128,399,159,"torse","robe_gray2"),
            (400,128,415,159,"torse","dress_white"),
            (416,128,431,159,"torse","arwen"),
            (432,128,447,159,"torse","skirt_onep_grey"),
            (448,128,463,159,"torse","bloody"),
            (464,128,479,159,"torse","leather_short"),
            (480,128,495,159,"torse","china_red2"),
            (496,128,511,159,"torse","animal_skin"),
            (512,128,527,159,"torse","neck"),
            (528,128,543,159,"torse","belt1"),
            (544,128,559,159,"torse","belt2"),
            (560,128,575,159,"torse","susp_black"),
            (576,128,591,159,"torse","shoulder_pad"),
            (592,128,607,159,"torse","mesh_black"),
            (608,128,623,159,"torse","mesh_red"),
            (624,128,639,159,"torse","leather_jacket"),
            (0,160,15,191,"torse","shirt_white1"),
            (16,160,31,191,"torse","shirt_white2"),
            (32,160,47,191,"torse","shirt_white3"),
            (48,160,63,191,"torse","shirt_blue"),
            (64,160,79,191,"torse","bikini_red"),
            (80,160,95,191,"torse","shirt_hawaii"),
            (96,160,111,191,"torse","china_red"),
            (112,160,127,191,"torse","leather_red"),
            (128,160,143,191,"torse","chunli"),
            (144,160,159,191,"torse","shirt_white_yellow"),
            (160,160,175,191,"torse","shirt_check"),
            (176,160,191,191,"torse","slit_black"),
            (192,160,207,191,"torse","leather_armour"),
            (208,160,223,191,"torse","leather_green"),
            (224,160,239,191,"torse","shirt_black"),
            (240,160,255,191,"torse","shirt_black_and_cloth"),
            (256,160,271,191,"torse","shirt_black3"),
            (272,160,287,191,"torse","leather2"),
            (288,160,303,191,"torse","chainmail3"),
            (304,160,319,191,"torse","shirt_vest"),
            (320,160,335,191,"torse","karate"),
            (336,160,351,191,"torse","karate2"),
            (352,160,367,191,"torse","leather_heavy"),
            (368,160,383,191,"torse","troll_hide"),
            (384,160,399,191,"torse","green_chain"),
            (400,160,415,191,"torse","metal_blue"),
            (416,160,431,191,"torse","green_susp"),
            (432,160,447,191,"torse","jacket2"),
            (448,160,463,191,"torse","jacket3"),
            (464,160,479,191,"torse","leather_stud"),
            (480,160,495,191,"torse","jacket_stud"),
            (496,160,511,191,"torse","chainmail"),
            (512,160,527,191,"torse","chainmail2"),
            (528,160,543,191,"torse","half_plate"),
            (544,160,559,191,"torse","half_plate2"),
            (560,160,575,191,"torse","half_plate3"),
            (576,160,591,191,"torse","breast_black"),
            (592,160,607,191,"torse","vest_red"),
            (608,160,623,191,"torse","bplate_green"),
            (624,160,639,191,"torse","bplate_metal1"),
            (0,192,15,223,"torse","banded"),
            (16,192,31,223,"torse","plate_and_cloth"),
            (32,192,47,223,"torse","plate_and_cloth2"),
            (48,192,63,223,"torse","scalemail"),
            (64,192,79,223,"torse","leather_metal"),
            (80,192,95,223,"torse","plate"),
            (96,192,111,223,"torse","plate_black"),
            (112,192,127,223,"torse","crystal_plate"),
            (128,192,143,223,"torse","armor_mummy"),
            (144,192,159,223,"torse","dragonsc_green"),
            (160,192,175,223,"torse","dragonsc_white"),
            (176,192,191,223,"torse","dragonsc_magenta"),
            (192,192,207,223,"torse","dragonsc_cyan"),
            (208,192,223,223,"torse","dragonsc_brown"),
            (224,192,239,223,"torse","dragonsc_blue"),
            (240,192,255,223,"torse","dragonsc_gold"),
            (256,192,271,223,"torse","dragonarm_green"),
            (272,192,287,223,"torse","dragonarm_white"),
            (288,192,303,223,"torse","dragonarm_magenta"),
            (304,192,319,223,"torse","dragonarm_cyan"),
            (320,192,335,223,"torse","dragonarm_brown"),
            (336,192,351,223,"torse","dragonarm_blue"),
            (352,192,367,223,"torse","dragonarm_gold"),
            (368,192,383,223,"torse","aragorn"),
            (384,192,399,223,"torse","boromir"),
            (400,192,415,223,"torse","frodo"),
            (416,192,431,223,"torse","gimli"),
            (432,192,447,223,"torse","legolas"),
            (448,192,463,223,"torse","merry"),
            (464,192,479,223,"torse","pipin"),
            (480,192,495,223,"torse","pj"),
            (496,192,511,223,"torse","sam"),
            (512,192,527,223,"torse","edison"),
            (528,192,543,223,"torse","lears_chain_mail"),
            (544,192,559,223,"torse","robe_of_night"))
        
        self.bras = (\
            (576,192,607,207,"bras","glove_red"),
            (576,208,607,223,"bras","glove_gray"),
            (608,192,639,207,"bras","glove_white"),
            (608,208,639,223,"bras","glove_blue"),
            (0,224,31,239,"bras","glove_black"),
            (0,240,31,255,"bras","glove_orange"),
            (32,224,63,239,"bras","glove_brown"),
            (32,240,63,255,"bras","glove_black2"),
            (64,224,95,239,"bras","glove_grayfist"),
            (64,240,95,255,"bras","glove_purple"),
            (96,224,127,239,"bras","glove_wrist_purple"),
            (96,240,127,255,"bras","glove_chunli"),
            (128,224,159,239,"bras","glove_gold"),
            (128,240,159,255,"bras","glove_short_yellow"),
            (160,224,191,239,"bras","glove_short_red"),
            (160,240,191,255,"bras","glove_short_white"),
            (192,224,223,239,"bras","glove_short_green"),
            (192,240,223,255,"bras","glove_short_blue"),
            (224,224,255,239,"bras","glove_short_gray"))
        
        self.main_d =(\
            (256,224,271,255,"main_d","dagger"),
            (272,224,287,255,"main_d","dagger_slant"),
            (288,224,303,255,"main_d","short_sword"),
            (304,224,319,255,"main_d","short_sword2"),
            (320,224,335,255,"main_d","sword_thief"),
            (336,224,351,255,"main_d","long_sword"),
            (352,224,367,255,"main_d","long_sword_slant"),
            (368,224,383,255,"main_d","great_sword"),
            (384,224,399,255,"main_d","great_sword_slant"),
            (400,224,415,255,"main_d","katana"),
            (416,224,431,255,"main_d","scimitar"),
            (432,224,447,255,"main_d","scimitar2"),
            (448,224,463,255,"main_d","sword2"),
            (464,224,479,255,"main_d","sword_tri"),
            (480,224,495,255,"main_d","broadsword"),
            (496,224,511,255,"main_d","black_sword"),
            (512,224,527,255,"main_d","sword_black"),
            (528,224,543,255,"main_d","sword_twist"),
            (544,224,559,255,"main_d","knife"),
            (560,224,575,255,"main_d","sword_seven"),
            (576,224,591,255,"main_d","heavy_sword"),
            (592,224,607,255,"main_d","sabre"),
            (608,224,623,255,"main_d","sword3"),
            (624,224,639,255,"main_d","sword_breaker"),
            (0,256,15,287,"main_d","sword_jag"),
            (16,256,31,287,"main_d","bloodbane"),
            (32,256,47,287,"main_d","chilly_death"),
            (48,256,63,287,"main_d","doom_knight"),
            (64,256,79,287,"main_d","flaming_death"),
            (80,256,95,287,"main_d","leech"),
            (96,256,111,287,"main_d","morg"),
            (112,256,127,287,"main_d","plutonium_sword"),
            (128,256,143,287,"main_d","jihad"),
            (144,256,159,287,"main_d","singing_sword"),
            (160,256,175,287,"main_d","zonguldrok"),
            (176,256,191,287,"main_d","club"),
            (192,256,207,287,"main_d","club2"),
            (208,256,223,287,"main_d","club3"),
            (224,256,239,287,"main_d","stick"),
            (240,256,255,287,"main_d","giant_club"),
            (256,256,271,287,"main_d","giant_club_spike"),
            (272,256,287,287,"main_d","whip"),
            (288,256,303,287,"main_d","sceptre"),
            (304,256,319,287,"main_d","mace"),
            (320,256,335,287,"main_d","mace_ruby"),
            (336,256,351,287,"main_d","morningstar"),
            (352,256,367,287,"main_d","morningstar2"),
            (368,256,383,287,"main_d","large_mace"),
            (384,256,399,287,"main_d","black_whip"),
            (400,256,415,287,"main_d","hammer"),
            (416,256,431,287,"main_d","hammer2"),
            (432,256,447,287,"main_d","frail_stick"),
            (448,256,463,287,"main_d","frail_ball"),
            (464,256,479,287,"main_d","frail_spike"),
            (480,256,495,287,"main_d","frail_ball2"),
            (496,256,511,287,"main_d","frail_balls"),
            (512,256,527,287,"main_d","frail_ball3"),
            (528,256,543,287,"main_d","frail_ball4"),
            (544,256,559,287,"main_d","nunchaku"),
            (560,256,575,287,"main_d","mace_of_variability"),
            (576,256,591,287,"main_d","spear1"),
            (592,256,607,287,"main_d","spear2"),
            (608,256,623,287,"main_d","spear3"),
            (624,256,639,287,"main_d","spear4"),
            (0,288,15,319,"main_d","spear5"),
            (16,288,31,319,"main_d","hook"),
            (32,288,47,319,"main_d","halberd"),
            (48,288,63,319,"main_d","pick_axe"),
            (64,288,79,319,"main_d","trident"),
            (80,288,95,319,"main_d","trident_elec"),
            (96,288,111,319,"main_d","trident2"),
            (112,288,127,319,"main_d","trident3"),
            (128,288,143,319,"main_d","lance"),
            (144,288,159,319,"main_d","lance2"),
            (160,288,175,319,"main_d","scythe"),
            (176,288,191,319,"main_d","pike"),
            (192,288,207,319,"main_d","quarterstaff1"),
            (208,288,223,319,"main_d","quarterstaff2"),
            (224,288,239,319,"main_d","quarterstaff3"),
            (240,288,255,319,"main_d","quarterstaff4"),
            (256,288,271,319,"main_d","sickle"),
            (272,288,287,319,"main_d","glaive"),
            (288,288,303,319,"main_d","glaive2"),
            (304,288,319,319,"main_d","glaive3"),
            (320,288,335,319,"main_d","d_glaive"),
            (336,288,351,319,"main_d","pole_forked"),
            (352,288,367,319,"main_d","fork2"),
            (368,288,383,319,"main_d","glaive_of_prune"),
            (384,288,399,319,"main_d","voodoo"),
            (400,288,415,319,"main_d","finisher"),
            (416,288,431,319,"main_d","staff_skull"),
            (432,288,447,319,"main_d","staff_mage"),
            (448,288,463,319,"main_d","staff_mage2"),
            (464,288,479,319,"main_d","great_staff"),
            (480,288,495,319,"main_d","staff_evil"),
            (496,288,511,319,"main_d","staff_ring_blue"),
            (512,288,527,319,"main_d","staff_mummy"),
            (528,288,543,319,"main_d","staff_fork"),
            (544,288,559,319,"main_d","staff_ruby"),
            (560,288,575,319,"main_d","staff_large"),
            (576,288,591,319,"main_d","elemental_staff"),
            (592,288,607,319,"main_d","asmodeus"),
            (608,288,623,319,"main_d","dispater"),
            (624,288,639,319,"main_d","olgreb"),
            (0,320,15,351,"main_d","axe"),
            (16,320,31,351,"main_d","axe_small"),
            (32,320,47,351,"main_d","hand_axe"),
            (48,320,63,351,"main_d","war_axe"),
            (64,320,79,351,"main_d","great_axe"),
            (80,320,95,351,"main_d","axe_double"),
            (96,320,111,351,"main_d","axe_blood"),
            (112,320,127,351,"main_d","axe_short"),
            (128,320,143,351,"main_d","arga"),
            (144,320,159,351,"main_d","sling"),
            (160,320,175,351,"main_d","bow"),
            (176,320,191,351,"main_d","bow2"),
            (192,320,207,351,"main_d","bow3"),
            (208,320,223,351,"main_d","great_bow"),
            (224,320,239,351,"main_d","bow_blue"),
            (240,320,255,351,"main_d","crossbow"),
            (256,320,271,351,"main_d","crossbow2"),
            (272,320,287,351,"main_d","crossbow3"),
            (288,320,303,351,"main_d","crossbow4"),
            (304,320,319,351,"main_d","punk"),
            (320,320,335,351,"main_d","sniper"),
            (336,320,351,351,"main_d","krishna"),
            (352,320,367,351,"main_d","dirt"),
            (368,320,383,351,"main_d","bone_lantern"),
            (384,320,399,351,"main_d","fan"),
            (400,320,415,351,"main_d","bottle"),
            (416,320,431,351,"main_d","box"),
            (432,320,447,351,"main_d","crystal"),
            (448,320,463,351,"main_d","deck"),
            (464,320,479,351,"main_d","disc"),
            (480,320,495,351,"main_d","horn"),
            (496,320,511,351,"main_d","lantern"),
            (512,320,527,351,"main_d","orb"),
            (528,320,543,351,"main_d","stone"),
            (544,320,559,351,"main_d","fire_red"),
            (560,320,575,351,"main_d","fire_blue"),
            (576,320,591,351,"main_d","skull"),
            (592,320,607,351,"main_d","head"),
            (608,320,623,351,"main_d","fire_green"),
            (624,320,639,351,"main_d","fire_cyan"),
            (0,352,15,383,"main_d","fire_white"),
            (16,352,31,383,"main_d","light_blue"),
            (32,352,47,383,"main_d","light_red"),
            (48,352,63,383,"main_d","light_yellow"),
            (64,352,79,383,"main_d","spark"),
            (80,352,95,383,"main_d","fire_dark"),
            (96,352,111,383,"main_d","fire_white2"),
            (112,352,127,383,"main_d","aragorn"),
            (128,352,143,383,"main_d","arwen"),
            (144,352,159,383,"main_d","boromir"),
            (160,352,175,383,"main_d","frodo"),
            (176,352,191,383,"main_d","gandalf"),
            (192,352,207,383,"main_d","gimli"),
            (208,352,223,383,"main_d","legolas"),
            (224,352,239,383,"main_d","saruman"))
        
        self.main_g = (\
            (256,352,271,383,"main_g","shield_round_small"),
            (272,352,287,383,"main_g","shield_round_small2"),
            (288,352,303,383,"main_g","bullseye"),
            (304,352,319,383,"main_g","shield_middle_round"),
            (320,352,335,383,"main_g","shield_skull"),
            (336,352,351,383,"main_g","shield_round_white"),
            (352,352,367,383,"main_g","boromir"),
            (368,352,383,383,"main_g","shield_round1"),
            (384,352,399,383,"main_g","shield_round2"),
            (400,352,415,383,"main_g","shield_round3"),
            (416,352,431,383,"main_g","shield_round4"),
            (432,352,447,383,"main_g","shield_round5"),
            (448,352,463,383,"main_g","shield_round6"),
            (464,352,479,383,"main_g","shield_round7"),
            (480,352,495,383,"main_g","shield_knight_blue"),
            (496,352,511,383,"main_g","shield_knight_gray"),
            (512,352,527,383,"main_g","shield_knight_rw"),
            (528,352,543,383,"main_g","shield_middle_unicorn"),
            (544,352,559,383,"main_g","shield_kite1"),
            (560,352,575,383,"main_g","shield_kite2"),
            (576,352,591,383,"main_g","shield_kite3"),
            (592,352,607,383,"main_g","shield_kite4"),
            (608,352,623,383,"main_g","shield_long_red"),
            (624,352,639,383,"main_g","shield_middle_gray"),
            (0,384,15,415,"main_g","shield_diamond_yellow"),
            (16,384,31,415,"main_g","shield_middle_brown"),
            (32,384,47,415,"main_g","shield_middle_black"),
            (48,384,63,415,"main_g","shield_middle_cyan"),
            (64,384,79,415,"main_g","shield_middle_ethn"),
            (80,384,95,415,"main_g","shield_long_cross"),
            (96,384,111,415,"main_g","shield_shaman"),
            (112,384,127,415,"main_g","shield_of_resistance"),
            (128,384,143,415,"main_g","book_black"),
            (144,384,159,415,"main_g","book_blue"),
            (160,384,175,415,"main_g","book_red"),
            (176,384,191,415,"main_g","book_magenta"),
            (192,384,207,415,"main_g","book_green"),
            (208,384,223,415,"main_g","book_cyan"),
            (224,384,239,415,"main_g","book_yellow"),
            (240,384,255,415,"main_g","book_white"),
            (256,384,271,415,"main_g","book_sky"),
            (272,384,287,415,"main_g","book_blue_dim"),
            (288,384,303,415,"main_g","book_cyan_dim"),
            (304,384,319,415,"main_g","book_green_dim"),
            (320,384,335,415,"main_g","book_magenta_dim"),
            (336,384,351,415,"main_g","book_red_dim"),
            (352,384,367,415,"main_g","book_yellow_dim"),
            (368,384,383,415,"main_g","fire_green"),
            (384,384,399,415,"main_g","fire_cyan"),
            (400,384,415,415,"main_g","fire_white"),
            (416,384,431,415,"main_g","light_blue"),
            (432,384,447,415,"main_g","light_red"),
            (448,384,463,415,"main_g","light_yellow"),
            (464,384,479,415,"main_g","spark"),
            (480,384,495,415,"main_g","fire_dark"),
            (496,384,511,415,"main_g","fire_white2"),
            (512,384,527,415,"main_g","lantern"),
            (528,384,543,415,"main_g","torch"),
            (544,384,559,415,"main_g","pj"),
            (560,384,575,415,"main_g","torsh2"))
        
        self.cheveux = (\
            (576,384,591,399,"cheveux","short_black"),
            (592,384,607,399,"cheveux","short_red"),
            (576,400,591,415,"cheveux","short_yellow"),
            (592,400,607,415,"cheveux","short_white"),
            (608,384,623,399,"cheveux","long_black"),
            (624,384,639,399,"cheveux","long_red"),
            (608,400,623,415,"cheveux","long_yellow"),
            (624,400,639,415,"cheveux","long_white"),
            (0,416,15,431,"cheveux","fem_black"),
            (16,416,31,431,"cheveux","fem_red"),
            (0,432,15,447,"cheveux","fem_yellow"),
            (16,432,31,447,"cheveux","fem_white"),
            (32,416,47,431,"cheveux","elf_black"),
            (48,416,63,431,"cheveux","elf_red"),
            (32,432,47,447,"cheveux","elf_yellow"),
            (48,432,63,447,"cheveux","elf_white"),
            (64,416,79,431,"cheveux","aragorn"),
            (80,416,95,431,"cheveux","arwen"),
            (64,432,79,447,"cheveux","boromir"),
            (80,432,95,447,"cheveux","frodo"),
            (96,416,111,431,"cheveux","legolas"),
            (112,416,127,431,"cheveux","merry"),
            (96,432,111,447,"cheveux","pj"),
            (112,432,127,447,"cheveux","sam"))
        
        self.barbe = (\
            (128,416,143,431,"barbe","short_black"),
            (144,416,159,431,"barbe","short_red"),
            (128,432,143,447,"barbe","short_yellow"),
            (144,432,159,447,"barbe","short_white"),
            (160,416,175,431,"barbe","long_black"),
            (176,416,191,431,"barbe","long_red"),
            (160,432,175,447,"barbe","long_yellow"),
            (176,432,191,447,"barbe","long_white"),
            (192,416,207,431,"barbe","pj"))
        
        self.tete = (\
            (224,416,239,431,"tete","cone_blue"),
            (240,416,255,431,"tete","cone_red"),
            (224,432,239,447,"tete","straw"),
            (240,432,255,447,"tete","wizard_blue"),
            (256,416,271,431,"tete","cap_blue"),
            (272,416,287,431,"tete","bandana_ybrown"),
            (256,432,271,447,"tete","hat_black"),
            (272,432,287,447,"tete","gandalf"),
            (288,416,303,431,"tete","crown_gold"),
            (304,416,319,431,"tete","cap_black1"),
            (288,432,303,447,"tete","clown1"),
            (304,432,319,447,"tete","feather_green"),
            (320,416,335,431,"tete","feather_red"),
            (336,416,351,431,"tete","feather_blue"),
            (320,432,335,447,"tete","feather_yellow"),
            (336,432,351,447,"tete","feather_white"),
            (352,416,367,431,"tete","band_white"),
            (368,416,383,431,"tete","band_red"),
            (352,432,367,447,"tete","band_yellow"),
            (368,432,383,447,"tete","band_blue"),
            (384,416,399,431,"tete","band_magenta"),
            (400,416,415,431,"tete","taiso_blue"),
            (384,432,399,447,"tete","taiso_magenta"),
            (400,432,415,447,"tete","taiso_yellow"),
            (416,416,431,431,"tete","taiso_red"),
            (432,416,447,431,"tete","taiso_white"),
            (416,432,431,447,"tete","dyrovepreva"),
            (432,432,447,447,"tete","wizard_purple"),
            (448,416,463,431,"tete","wizard_bluegreen"),
            (464,416,479,431,"tete","wizard_darkgreen"),
            (448,432,463,447,"tete","wizard_brown"),
            (464,432,479,447,"tete","wizard_blackgold"),
            (480,416,495,431,"tete","wizard_blackred"),
            (496,416,511,431,"tete","wizard_red"),
            (480,432,495,447,"tete","wizard_white"),
            (496,432,511,447,"tete","turban_white"),
            (512,416,527,431,"tete","turban_brown"),
            (528,416,543,431,"tete","iron1"),
            (512,432,527,447,"tete","helm_red"),
            (528,432,543,447,"tete","horned"),
            (544,416,559,431,"tete","helm_green"),
            (560,416,575,431,"tete","cheek_red"),
            (544,432,559,447,"tete","iron_red"),
            (560,432,575,447,"tete","blue_horn_gold"),
            (576,416,591,431,"tete","hood_white"),
            (592,416,607,431,"tete","yellow_wing"),
            (576,432,591,447,"tete","brown_gold"),
            (592,432,607,447,"tete","black_horn"),
            (608,416,623,431,"tete","full_gold"),
            (624,416,639,431,"tete","chain"),
            (608,432,623,447,"tete","black_horn2"),
            (624,432,639,447,"tete","full_black"),
            (0,448,15,463,"tete","horn_gray"),
            (16,448,31,463,"tete","iron2"),
            (0,464,15,479,"tete","iron3"),
            (16,464,31,479,"tete","fhelm_gray3"),
            (32,448,47,463,"tete","fhelm_horn_yellow"),
            (48,448,63,463,"tete","fhelm_horn2"),
            (32,464,47,479,"tete","horn_evil"),
            (48,464,63,479,"tete","helm_plume"),
            (64,448,79,463,"tete","mummy"),
            (80,448,95,463,"tete","art_dragonhelm"),
            (64,464,79,479,"tete","healer"),
            (80,464,95,479,"tete","hood_gray"),
            (96,448,111,463,"tete","hood_red"),
            (112,448,127,463,"tete","hood_green2"),
            (96,464,111,479,"tete","hood_cyan"),
            (112,464,127,479,"tete","hood_orange"),
            (128,448,143,463,"tete","hood_red2"),
            (144,448,159,463,"tete","hood_black2"),
            (128,464,143,479,"tete","hood_white2"),
            (144,464,159,479,"tete","hood_ybrown"),
            (160,448,175,463,"tete","hood_green"),
            (176,448,191,463,"tete","ninja_black"))
        
class Tuile_Perso:
    def __init__(self):
        """Chargement en memoire des differentes parties"""
        # Tuile representant le joueur à l'ecran
        tuiles = pygame.image.load(os.path.join('data', 'tiles', 'player.png'))
        
        rltiles = RLTiles()
        
        self.corps = []
        for liste in rltiles.corps:
            tuile = pygame.Surface((liste[2] - liste[0], liste[3] - liste[1]), pygame.SRCALPHA, 32)
            tuile.blit(tuiles, (0,0), (liste[0], liste[1], liste[2]-liste[0], liste[3]-liste[1]))
            self.corps.append(tuile.convert_alpha())
            
        self.cape = []
        for liste in rltiles.cape:
            tuile = pygame.Surface((liste[2]-liste[0], liste[3]-liste[1]),pygame.SRCALPHA,32)
            tuile.blit(tuiles, (0,0), (liste[0], liste[1], liste[2]-liste[0], liste[3]-liste[1]))
            self.cape.append(tuile.convert_alpha())        
    
        self.pieds = []
        for liste in rltiles.pieds:
            tuile = pygame.Surface((liste[2]-liste[0], liste[3]-liste[1]),pygame.SRCALPHA,32)
            tuile.blit(tuiles, (0,0), (liste[0], liste[1], liste[2]-liste[0], liste[3]-liste[1]))
            self.pieds.append(tuile.convert_alpha())        
    
        self.jambes = []
        for liste in rltiles.jambes:
            tuile = pygame.Surface((liste[2]-liste[0], liste[3]-liste[1]),pygame.SRCALPHA,32)
            tuile.blit(tuiles, (0,0), (liste[0], liste[1], liste[2]-liste[0], liste[3]-liste[1]))
            self.jambes.append(tuile.convert_alpha())        
    
        self.torse = []
        for liste in rltiles.torse:
            tuile = pygame.Surface((liste[2]-liste[0], liste[3]-liste[1]),pygame.SRCALPHA,32)
            tuile.blit(tuiles, (0,0), (liste[0], liste[1], liste[2]-liste[0], liste[3]-liste[1]))
            self.torse.append(tuile.convert_alpha())        
    
        self.bras = []
        for liste in rltiles.bras:
            tuile = pygame.Surface((liste[2]-liste[0], liste[3]-liste[1]),pygame.SRCALPHA,32)
            tuile.blit(tuiles, (0,0), (liste[0], liste[1], liste[2]-liste[0], liste[3]-liste[1]))
            self.bras.append(tuile.convert_alpha())        
    
        self.main_d = []
        for liste in rltiles.main_d:
            tuile = pygame.Surface((liste[2]-liste[0], liste[3]-liste[1]),pygame.SRCALPHA,32)
            tuile.blit(tuiles, (0,0), (liste[0], liste[1], liste[2]-liste[0], liste[3]-liste[1]))
            self.main_d.append(tuile.convert_alpha()) 
                
        self.main_g = []
        for liste in rltiles.main_g:
            tuile = pygame.Surface((liste[2]-liste[0], liste[3]-liste[1]),pygame.SRCALPHA,32)
            tuile.blit(tuiles, (0,0), (liste[0], liste[1], liste[2]-liste[0], liste[3]-liste[1]))
            self.main_g.append(tuile.convert_alpha())        
        
        self.cheveux = []
        for liste in rltiles.cheveux:
            tuile = pygame.Surface((liste[2]-liste[0], liste[3]-liste[1]),pygame.SRCALPHA,32)
            tuile.blit(tuiles, (0,0), (liste[0], liste[1], liste[2]-liste[0], liste[3]-liste[1]))
            self.cheveux.append(tuile.convert_alpha())        
    
        self.barbe = []
        for liste in rltiles.barbe:
            tuile = pygame.Surface((liste[2]-liste[0], liste[3]-liste[1]),pygame.SRCALPHA,32)
            tuile.blit(tuiles, (0,0), (liste[0], liste[1], liste[2]-liste[0], liste[3]-liste[1]))
            self.barbe.append(tuile.convert_alpha())        
    
        self.tete = []
        for liste in rltiles.tete:
            tuile = pygame.Surface((liste[2]-liste[0], liste[3]-liste[1]),pygame.SRCALPHA,32)
            tuile.blit(tuiles, (0,0), (liste[0], liste[1], liste[2]-liste[0], liste[3]-liste[1]))
            self.tete.append(tuile.convert_alpha()) 
            
def bodytile(tp, num_corps=0, num_jambes=-1, num_cheveux=-1, num_barbe=-1, 
                ombre = False):
    """
    La tuile representant le corps de base
    """
    tuile = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
    # ombre
    if ombre:
        tuile.blit(tp.corps[TUILEP_CORPS_SHADOW], (0,0))
    # Corps
    tuile.blit(tp.corps[num_corps], (0,0))
    # Jambes
    if num_jambes >= 0:
        tuile.blit(tp.jambes[num_jambes], (0,16))
    # Cheveux
    if num_cheveux >= 0:
        tuile.blit(tp.cheveux[num_cheveux], (8,0))
    # Barbe
    if num_barbe >= 0:
        tuile.blit(tp.barbe[num_barbe], (8,0))
    return tuile
    
    
def playertile(tp, body_tile, cloack = None, boots = None, helmet = None,
              gauntlets = None, armor = None, weapon = None, shield = None):
    """
    La tuile du PNJ
    """
    tile = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
    tile.blit(tp.corps[TUILEP_CORPS_SHADOW], (0, 0))
    if cloack is not None:
        tile.blit(tp.cape[cloack], (0, 0))
    tile.blit(body_tile, (0,0))
    if boots is not None:
        tile.blit(tp.pieds[boots], (0, 16))
    if helmet is not None:
        tile.blit(tp.tete[helmet], (8, 0))
    if gauntlets is not None:
        tile.blit(tp.bras[gauntlets], (0, 8))
    if armor is not None:
        tile.blit(tp.torse[armor], (8, 0))
    if weapon is not None:
        tile.blit(tp.main_d[weapon], (0, 0))
    if shield is not None:
        tile.blit(tp.main_g[weapon], (16, 0))
    return tile
 
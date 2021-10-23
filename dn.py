# dungeon's nightmare [ethan]
# Un jeu dungeon de combat avec pygame avec :
#  - une map qui change à chaque partie mais qui garde une hiérarchie et une compréhension des niveaux
#  - Un jeu simple et rapide à prendre en main
#  - Un leaderboard et un system de sauvegarde
# Les sauvegardes et peuvent être réutilisé pour un leaderboard global
#
# Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
# You are free to: copy and redistribute if you credit the author but you can not sell the game

"""
dungeon's nightmare
"""

import random
import time
import numpy as N
import configparser
import pickle
import os
import sys
import locale
import gettext

gettext.install('dn')

#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
#                        Constants
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
# la plupart des nom sont generer avec des generateur de noms en ligne
PLACES = ['Rosland', 'Dry', 'Ororey', 'Lumnear', 'Scarswe', 'Kirlet', 'Prickly',
           'Abterre', 'Desolate', 'Lonrial', 'Churchmar', 'Nokoree', 'Votfolk', 
           'Musthon', 'Mighty', 'Lucent', 'Nipanach', 'Maldon', 'Brodes', 
           'Hastmis', 'Beverdown', 'Drumberg', 'Monknear', 'Harpnia', 'Ellisly', 
           'Hingden', 'Beholding', 'Kingsroy', 'Arborchill', 'Caswater', 'Terrestrial', 
           'Plymcana', 'Delorcola', 'Irririch', 'Twisting', 'Hollow', 'Draysack', 'Lourden',
           'Beauway', 'Feared', 'Lookecarres', 'Yelling', 'Feared', 'Lourden', 'Nipaset', 
           'Causaline', 'Rocky', 'Bordboro', 'Asgough', 'Galway', 'Smithspar', 
           'Beddingna', 'Shebury', 'Osocroft', 'Dalcola', 'Charmed', 'Malevolent', 'Musborg',
           'Unresting', 'Twilford', 'Congue', 'Attlede', 'Picronto', 'Naiberry', 
           'Torringcona', 'Hepboro', 'Durstone', 'Picronto', 'Shadowy', 'Jagged', 'Teal', 
           'Farmlam']


# Multiplicateurs pour transformer les coordonnées en d'autres octants :
MULT = [[1,  0,  0, -1, -1,  0,  0,  1],
        [0,  1, -1,  0,  0, -1,  1,  0],
        [0,  1,  1,  0,  0, -1, -1,  0],
        [1,  0,  0,  1, -1,  0,  0, -1]]

# Directions
DIRS8 = [(-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1)]
DIRS = [(-1,0), (0,-1), (1,0), (0,1)]

# Couleurs
COLOR_BLACK = 0
COLOR_BLUE = 1
COLOR_CYAN = 2
COLOR_GREEN = 3
COLOR_MAGENTA = 4
COLOR_RED = 5
COLOR_WHITE = 6
COLOR_YELLOW = 7

COLOR_BOLD = 8

# Articles spéciaux sur le sol
SPECIAL_NONE        = 0
SPECIAL_DOOR        = 1
SPECIAL_UPSTAIRS    = 2
SPECIAL_DOWNSTAIRS1 = 3
SPECIAL_DOWNSTAIRS2 = 4
SPECIAL_MUSHROOM    = 5
SPECIAL_POTION      = 6
SPECIAL_SWORD       = 10
SPECIAL_AXE         = 20
SPECIAL_SPEAR       = 30
SPECIAL_WARHAMMER   = 40

DUNGEON_FLOOR       = 0
DUNGEON_WALL        = 1

# Constantes des armes
WEAPON_SWORD        = 0
WEAPON_AXE          = 1
WEAPON_SPEAR        = 2
WEAPON_WARHAMMER    = 3

WEAPON_NONE         = -1
WEAPON_FLAVOR0      = 0
WEAPON_FLAVOR1      = 1
WEAPON_FLAVOR2      = 2
WEAPON_FLAVOR3      = 3
WEAPON_FLAVOR4      = 4
WEAPON_FLAVOR5      = 5

WEAPON_NAME = (_("sword"), _("axe"), _("spear"), _("warhammer"))
WEAPON_TILE = ("/", "P", "|", "T")
WEAPON_FLAVOR = (_("training"), _("iron"), _("steel"), _("mithril"), 
                 _("adamantite"), _("vorpal"))

# Constantes d'ambiance
MOOD_QUIET          = 0
MOOD_FRENZY         = 1
MOOD_BERZERK        = 2

# Mood triggers
TRIGGER_SUFFER      = 0
TRIGGER_KILL        = 1
TRIGGER_REST        = 2
TRIGGER_HEAL        = 3
TRIGGERS = (5, 10, -2, -40)

# Noms des monstres
MONSTER = (_("Homunculus"), 
           _("Imp"),
           _("Lesser Demon"),
           _("Demon"),
           _("Greater Demon"),
           _("Lesser Balrog"),
           _("Balrog"),
           _("Greater Balrog"),
           _("Balrog captain"),
           _("Gothmog, lord of balrogs"))

# Canaux sonores
CHANNEL_SOUNDS = 0

# Sons
SOUND_PLAYER_ATTACK = 11
SOUND_PLAYER_KILL = 12
SOUND_MONSTER_ATTACK = 13
SOUND_MONSTER_KILL = 14
SOUND_OPEN_DOOR = 15
SOUND_GRAB_STUFF = 16
SOUND_DRINK = 17
SOUND_REST = 18
SOUND_PLAYER_LEVELUP = 19
SOUND_MONSTER_LEVELUP = 20
SOUND_MONSTER_SUMMON = 21

# Événements
EVENT_NONE = 0
EVENT_LEVELUP = 1
EVENT_STAIRSDOWN = 2
EVENT_STAIRSUP = 3
EVENT_BERZERK = 4
EVENT_DEATH = 5
EVENT_START = 6


#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
#                   générateur de nom 
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
class Mdict:
    def __init__(self):
        self.d = {}
    def __getitem__(self, key):
        if key in self.d:
            return self.d[key]
        else:
            raise KeyError(key)
    def add_key(self, prefix, suffix):
        if prefix in self.d:
            self.d[prefix].append(suffix)
        else:
            self.d[prefix] = [suffix]
    def get_suffix(self,prefix):
        l = self[prefix]
        return random.choice(l)

class MName:
    """
    gen nom
    """
    def __init__(self, chainlen = 2):
        """
        Construction du dictionnaire
        """
        if chainlen > 10 or chainlen < 1:
            print("La longueur de la chaine doit etre comprise entre 1 et 10, inclus.")
            sys.exit(0)
    
        self.mcd = Mdict()
        oldnames = []
        self.chainlen = chainlen
    
        for l in PLACES:
            l = l.strip()
            oldnames.append(l)
            s = " " * chainlen + l
            for n in range(0,len(l)):
                self.mcd.add_key(s[n:n+chainlen], s[n+chainlen])
            self.mcd.add_key(s[len(l):len(l)+chainlen], "\n")
    
    def New(self):
        """
        Nouveau nom de la chaine de Markov
        """
        prefix = " " * self.chainlen
        name = ""
        suffix = ""
        while True:
            suffix = self.mcd.get_suffix(prefix)
            if suffix == "\n" or len(name) > 9:
                break
            else:
                name = name + suffix
                prefix = prefix[1:] + suffix
        return name.capitalize()
    
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
#                    Classe monstres
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-

class Monster:
    ASLEEP = 0
    AWAKEN = 1
    def __init__(self, pos, level):
        self.pos = pos
        self.level_start = level
        self.level = level
            
        if self.level < 10:
            self.levelmax = min(level + level-1, 9)
            while random.randint(1, 5) == 1 and self.level < self.levelmax:
                self.level +=1
            #self.level = min(self.level, 9)
            self.hp = 1 + self.level * (self.level + 1)
            self.state = Monster.ASLEEP
        else:
            self.levelmax = 10
            self.hp = 150
            self.state = Monster.AWAKEN
            
        self.hpmax = self.hp
            
        
    def name(self):
        """
        le vrai nom du monstre
        """
        if self.level_start < 10:
            return "%s le %s" % (self.tile(), MONSTER[self.level-1])
        else:
            return MONSTER[self.level-1]
         
    def is_awake(self):
        return self.state == Monster.AWAKEN
    
    def awake(self):
        """
        Changer d'etat pour devenir agressif
        """
        self.state = min(self.state + 1, Monster.AWAKEN)
        
    def tile(self):
        """
        case de monstre sur deux personnages
        """
        if self.is_awake():
            if self.level < 10:
                return "M%s" % self.level
            else:
                return "ME"
        else:
            return "M~"
    
    def move(self, pos):
        """
        se deplace vers une nouvelle position
        """
        self.pos = pos
        
    def heal(self):
        """
        Le monstre est gueri de ses blessures.
        """
        self.hp = self.hpmax
        
    def upgrade(self):
        """
        Le monstre gagne un niveau
        """
        if self.level < self.levelmax:
            self.level += 1
            self.hpmax = 1 + self.level * (self.level + 1)
            self.hp = self.hpmax
        
    def damage(self):
        """
        Combien de degats le monstre inflige-t-il ?
        """
        l2 = self.level
        l1 = max(0, l2 - 3)
        return 1 + random.randint(l1, l2) + random.randint(l1, l2) + random.randint(l1, l2)
    
    def stun(self, n):
        """
        Assommer le monstre
        """
        self.state = -n
        

#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
#                      Classe dongeon
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-

class Dungeon:
    def __init__(self, size = (32, 32), ratio = 60, name = None, level = 1):
        """
        Initialisation d'un plancher de donjon
        size : (largeur, hauteur)
        ratio : ratio des pièces par rapport à la surface totale (en %)
                 de 10 à 60
        nom   : graine aleatoire dans une chaine de caracteres
        """
        self.size = size
        self.name = name
        self.level = level
        # Posez la seed
        state = random.getstate()
        random.seed(name)
            
        # Création du array d'étage
        # 0: le sol
        # 1: les murs
        self.floor = N.ones(size) * DUNGEON_WALL
        # array des salles
        self.rooms = N.ones(size)
        # nombre de cellules occupées par les pièces
        self.surf_rooms = 0
        # portes, escaliers, ... array
        self.special = N.ones(size) * SPECIAL_NONE
        # Liste des impasses
        self.list_de = []
        # Dictionnaire des monstres
        self.monster = {}
        # flag pour savoir si ME a ajouté
        self.me_added = False
        
        self.corridor_v(False)
        
        r = self.size[0] * self.size[1] * ratio / 100
        n = 0
        nmax = r * 10
        
        while n < r:
            n += 1
            self.corridor_h()
            self.corridor_v()
            if self.surf_rooms < r:
                self.room()
        # Ajout de portes aux pièces
        self.special *= (1 - self.floor) * SPECIAL_DOOR
        # Ajout d'escaliers et de trésors aux impasses
        self.dead_end()
        # Restaurer l'état du générateur aléatoire
        random.setstate(state)
        
    
    def corridor_h(self, test = True):
        """
        Un couloir horizontal
        """
        l = random.randint(2, 6) * 2 + 1
        x = (random.randint(2, self.size[0] - l - 2) // 2) * 2 + 1
        y = (random.randint(6, self.size[1] - 6) // 2) * 2 + 1
        if l // 5 > N.sum(N.sum(1 - self.floor[x:x+l, y])) > 0 or not test:
            self.floor[x:x+l, y] = DUNGEON_FLOOR
            self.list_de.append((x, y))
            self.list_de.append((x+l-1, y))
            return True
        return False
        
        
    def corridor_v(self, test = True):
        """
        Un couloir vertical
        """
        l = random.randint(2, 6) * 2 + 1
        x = (random.randint(6, self.size[0] - 6) // 2) * 2 + 1
        y = (random.randint(2, self.size[1] - l - 2) // 2) * 2 + 1
        if l // 5 > N.sum(N.sum(1 - self.floor[x, y:y+l])) > 0 or not test:
            self.floor[x, y:y+l] = DUNGEON_FLOOR
            self.list_de.append((x, y))
            self.list_de.append((x, y+l-1))
            return True
        return False
        
    def room(self, pos = None, test = True):
        """
        Une pièce
        """
        lx = random.randint(2, 5) * 2 + 1
        ly = random.randint(2, 5) * 2 + 1
        if pos is None:
            x = (random.randint(0, self.size[0] - lx - 2) // 2) * 2 + 1
            y = (random.randint(0, self.size[1] - ly - 2) // 2) * 2 + 1
        else:
            x, y = pos
        if (N.sum(N.sum(1 - self.floor[x:x+lx, y:y+ly])) > 0 \
            and N.sum(N.sum(1 - self.rooms[x:x+lx, y:y+ly])) == 0) \
            or not test:  
            # La chambre se trouve au-dessus d'un couloir ou plus
            # mais pas au-dessus d'une autre pièce
            self.surf_rooms += lx * ly
            self.floor[x:x+lx, y:y+ly] = DUNGEON_FLOOR
            self.rooms[x:x+lx, y:y+ly] = 0
            self.special[x-1:x+lx+1, y-1:y+ly+1] = SPECIAL_DOOR
            self.special[x:x+lx, y:y+ly] = SPECIAL_NONE
            n = random.randint(1, 5 + self.level)
            posn = (x+random.randint(1, lx-1), y+random.randint(1, ly-1))
            if n == 1:
                self.add_special(posn, SPECIAL_POTION)
            elif n < 4:
                self.add_special(posn, SPECIAL_MUSHROOM)
            else:
                self.add_monster(posn, self.level)
            return True
        return False
    
    
    def weapon_params(self, pos):
        """
        Retourne la saveur et le numéro d'une arme en position dans le donjon.
        """
        weap_flav = int(self.special[pos] % 10)
        weap_type = int((self.special[pos] - weap_flav) / 10 - 1)
        return weap_flav, weap_type
    
    
    def add_mushroom(self, pos, nb):
        """
        ajouter des champignons autour de la position après avoir tué un monstre
        """
        l = list(DIRS8)
        random.shuffle(l)
        n = 0
        for i in range(len(l)):
            p = (pos[0] + l[i][0], pos[1] + l[i][1])
            if self.is_reachable(p) and self.special[p] == SPECIAL_NONE:
                n += 1
                self.add_special(p, SPECIAL_MUSHROOM)
                if n == nb:
                    break
        return n
                
    
    def add_special(self, pos, type):
        """
        Ajouter quelque chose de spécial à la pose
        """
        if self.special[pos] == SPECIAL_NONE:
            self.special[pos] = type
            
    def has_special(self, pos, type):
        """
        Vrai s'il y a un type spécial à la pos, Faux sinon
        """
        return self.special[pos] == type
    
    def grab_special(self, pos, type):
        """
        Obtient le type spécial a la position
        """
        if self.has_special(pos, type):
            self.special[pos] = SPECIAL_NONE
            return 1
        return 0

    def add_monster(self, pos, level):
        """
        Ajouter un monstre au poste
        """
        if self.is_reachable(pos):
            if level == 10:
                if self.me_added:
                    self.monster[pos] = Monster(pos, 9)
                else:
                    self.me_added = True
                    self.monster[pos] = Monster(pos, 10)
            else:
                self.monster[pos] = Monster(pos, level)
                
    
    def has_monster(self, pos):
        """
        Vrai s'il y a un monstre a la pos, Faux sinon
        """
        return pos in self.monster
    
    def bash_monster(self, pos, n):
        """
        Enlever n points aux points de vie du monstre
        """
        if self.has_monster(pos):
            if self.monster[pos].hp <= n:
                xp = self.monster[pos].hpmax
                self.monster.pop(pos)
                return xp
            else:
                self.monster[pos].hp -= n
                return 0
        
    def dead_end(self):
        """
        Traitement les impasses
        """
        nb_sp = 1
        for i in range(len(self.list_de)):
            x, y = self.list_de[i]
            if N.sum(N.sum(self.floor[x-1:x+2, y-1:y+2])) != 7:
                # Add one potion every 3 monster
                if i % 3 == 0:
                    self.add_special((x, y), SPECIAL_POTION)
                else:
                    self.add_monster((x, y), self.level)
            else:
                # C'est une véritable impasse
                nb_sp += 1
                if nb_sp < 5:
                    if nb_sp not in (SPECIAL_DOWNSTAIRS1, SPECIAL_DOWNSTAIRS2) or self.level < 9:
                        # Escalier descendant seulement avant le niveau 9
                        self.special[x, y] = nb_sp
                    # Enregistrement de la position de départ
                    if nb_sp == 2:
                        self.pos_start = self.list_de[i]
                else:
                    # Ajouter une arme
                    if self.level == 9:
                        weap_type = SPECIAL_SWORD
                        weap_flav = WEAPON_FLAVOR5
                    else:
                        weap_type = random.choice((SPECIAL_SWORD, SPECIAL_AXE, SPECIAL_SPEAR, SPECIAL_WARHAMMER))
                        weap_flav = random.randint(max(0, self.level // 2 - 2), self.level // 2)
                    self.special[x, y] = weap_type + weap_flav
                    if self.level == 1:
                        l = 1
                    else:
                        l = self.level + 1
                    self.add_monster((x-1, y), l)
                    self.add_monster((x+1, y), l)
                    self.add_monster((x, y-1), l)
                    self.add_monster((x, y+1), l)
                        
        if nb_sp == 1:
            # Aucune impasse trouvée
            # Nous ajoutons les escaliers manuellement
            self.special[self.list_de[0]] = SPECIAL_UPSTAIRS
            # Enregistrement de la position de départ
            self.pos_start = self.list_de[0]
            if self.level < 9:
                self.special[self.list_de[1]] = SPECIAL_DOWNSTAIRS1
        elif nb_sp == 2:
            #print "Le bas a été atteint !"
            pass

        
    def is_reachable(self, pos):
        """
        Retourne True si le poste est accessible
        Faux sinon
        """
        if self.has_special(pos, SPECIAL_DOOR):
            return False
        else:
            return self.floor[pos[0], pos[1]] == DUNGEON_FLOOR and \
                   pos not in self.monster
 
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
#                      Classe joueur
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-

class Player:
    def __init__(self, size, seed, dungeon_name = "nightmare", cols = 30,
                 scores = {}, known_dungeon = {}, record = True):
        
        self.dsize = size
        
        #-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
        #                       Santé du joueur
        #-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
        self.xp = 0
        self.level = 1
        self.levels = self.levels()
        """
        self.hp, self.hpmax = 10, 10
        self.deepness = 1
        self.deepness_max = 1
        """
        self.hp, self.hpmax = 10, 10
        self.deepness = 1
        self.deepness_max = 1
        self.mushroom = 0
        # Liste des poses de champignons vues par le joueur
        self.mush_seen = {}
        self.potion = 1 # initial 1 potion au démarage 999 -= si on veut des potions en illimité
        # L'humeur pour avoir un mode gore(enragé)
        self.mood = 0
        self.mood_state = MOOD_QUIET
        self.mood_level = self.moods()
        # Flag pour décider si on retire 1 point d'humeur à la fin du tour.
        # le faire que si l'humeur n'a pas été mise à jour pendant le cycle.
        self.mood_updated = False
        
        #-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
        #                       Armes joueurs
        #-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
        # Liste des armes détenues
        self.weapon_flavor = [WEAPON_FLAVOR0, WEAPON_NONE, WEAPON_NONE, WEAPON_NONE]
        self.active_weapon = 0
        # Direction le joueur fait face (utilisé l'épées (chargés))
        self.dir = [0, 0]
        # Puissance de la charge de l'épée
        self.charge = 0
        # flag pour la hache
        self.hit_by_monster = False
        
        #-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
        #                      Mémoire du joueur
        #-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
        self.fov = max(size[0], size[1])        
        # seed aléatoire et état aléatoire
        self.seed = []
        self.update_seed(seed)        
        self.record = record        
        # Key history
        self.history = []
        
        if dungeon_name == "random" or dungeon_name == "Random":
            self.dname = MName().New()
        else:
            self.dname = dungeon_name
        self.dname_full = "%s (%s, %s)" % (self.dname, self.dsize[0], self.dsize[1])
        self.cols = cols        
        # Dictionnaire des sols visités
        self.dict_dungeon = {}
        # Dictionnaire des sols connus des ancêtres
        self.known_dungeon = known_dungeon.copy()
        # Liste des pose de départ dans le niveaux
        self.start_pos = [(0, 0)]
        # Chargement du premier étage
        self.load_dungeon_floor(self.start_pos[-1], False)
        self.pos = self.dungeon.pos_start
        self.known[self.pos] = 1
        # Messages de (texte, couleur)
        self.message = []
        # Flag pour tester la fin du programme
        # 0 : en jeu
        # 1 : tué
        # 2 : sortie des mines
        self.exit = 0
        
        # Un dictionnaire où la clé est le nom du dungeon, et la valeur est un tuple.
        # Chaque tuple contient tous les scores d'un dungeon.
        self.scores = scores        
        # Nombre de tours (pour le cas du GAGNANT)
        self.round = 0
        self.winner = False
        # Events
        self.init_event(EVENT_START)
        
        
    def init_event(self, event=EVENT_NONE):
        """
        Evénements pour la musique
        """
        self.event = event
        
        
    def update_seed(self, seed):
        """
        Met à jour la valeur de la graine aléatoire
        """
        self.seed.append(seed)
        random.seed(seed)
        
        
    def record_history(self, key):
        """
        Enregistre les touches pressées pour le replay
        """
        self.history.append(key)
        
        
    def clean_history(self):
        """
        Suppression de la touche Esc à la fin de l'historique lorsque l'on continue à jouer
        """
        if self.history[-1] == 27:
            self.history.pop(-1)
            
        
    def moods(self):
        """
        Calculer des seuils d'humeur pour améliorer l'humeur des joueurs
        """
        n = self.dsize[0] + self.dsize[1]
        return 0, n/2, 3*n/2
    
    
    def update_mood(self, trigger):
        """
        Actualise l'humeur du joueur grâce à des déclencheurs d'humeur
        plus le joueur est blessé, plus elle est augmentée
        """
        mult = 1
        if trigger > 0 and self.hp < self.hpmax/3:
            mult = 4
        elif trigger > 0 and self.hp < 2*self.hpmax/3:
            mult = 2
        self.mood = max(0, self.mood + TRIGGERS[trigger] * mult)
        self.mood_updated = True
        
        
    def analyse_mood(self):
        """
        Analyser l'humeur à la fin du tour
        """
        # Le joueur se calme à chaque tour
        if not self.mood_updated:
            self.mood = max(self.mood - 1, 0)
        self.mood_updated = False
        if self.mood >= self.mood_level[MOOD_BERZERK]:
            new_mood_state =  MOOD_BERZERK
            self.event = EVENT_BERZERK
        elif self.mood >= self.mood_level[MOOD_FRENZY]:
            new_mood_state =  MOOD_FRENZY
        else:
            new_mood_state =  MOOD_QUIET
        
        if new_mood_state < self.mood_state:
            # vous vous calmez
            if self.mood_state == MOOD_BERZERK:
                self.add_message(_("Vous n'êtes plus berzerk."), COLOR_YELLOW)
            elif self.mood_state == MOOD_FRENZY:
                self.add_message(_("Vous vous calmez."), COLOR_YELLOW)
        elif new_mood_state > self.mood_state:
            # vous êtes frenzier
            if self.mood_state == MOOD_FRENZY:
                self.add_message(_("Vous devenez berzerk!!!"), COLOR_YELLOW)
            elif self.mood_state == MOOD_QUIET:
                self.add_message(_("Vous devenez frénétique!"), COLOR_YELLOW)
                
        self.mood_state = new_mood_state
                
             
    def levels(self):
        """
        Calculer les montants d'xp pour augmenter le niveau du joueur
        pour le niveau 2 : le joueur doit tuer 10(changer) monstres du niveau 1 quand 40 x 40
        pour le niveau 3 : le joueur doit tuer 12(changer) monstres de niveau 2 quand 40 x 40
        pour le niveau 4 : le joueur doit tuer 14(changer) monstres de niveau 3 quand 40 x 40
        ...
        """
        l = [0,]
        # n est le nombre de monstres à tuer au niveau du dungeon pour atteindre le niveau suivant du joueur.
        n = int((self.dsize[0] + self.dsize[1]) / 15) - 1 # 10 (changement de difficulter -4 pour facile changement du /15 plus haut plus facile)
        for level in range(1, 21):
            l.append(l[-1] + (n + 2 * level) * (1 +  level * (level + 1)))
        return l
    
    def increase_round(self):
        """
        Encore un tour
        """
        self.round += 1
        self.analyse_mood()
        
        
    def change_active_weapon(self, type):
        """
        changer l'arme active du joueur
        """
        n = type // 10 - 1
        if self.weapon_flavor[n] != WEAPON_NONE:
            if self.active_weapon == n:
                self.add_message(_("Vous tenez déjà votre %s %s.") % (WEAPON_FLAVOR[self.weapon_flavor[n]], WEAPON_NAME[n]),
                                 COLOR_BLUE)
                return False
            else:
                self.active_weapon = n
                self.add_message(_("Vous prenez votre %s %s.") % (WEAPON_FLAVOR[self.weapon_flavor[n]], WEAPON_NAME[n]),
                                 COLOR_BLUE)
                return True
        else:
            self.add_message(_("Vous n'avez pas de %s dans votre équipement.") % WEAPON_NAME[n],
                             COLOR_BLUE)
            return False
            
            
    def weapon_name(self, weap_num, weap_flav):
        """
        Renvoie le nom de l'arme
        """
        return _("un %s %s") % (WEAPON_FLAVOR[weap_flav], WEAPON_NAME[weap_num])
        
        
    def help(self):
        """
        Aide en jeu
        """
        help = (_("Aide générale :"),
                _("--------------"),
                _("Vous êtes un jeune héros et pour prouver votre force, vous décidez d'explorer les mines à proximité de votre village natal."),
                _("Mais attention ! On dit que ces mines sont hantées par de dangereux monstres."),
                _("Armé uniquement de votre épée d'entraînement et d'une potion de santé, vous entrez dans un dédale de pièces et de couloirs."),
                "",
                _("- 'F2' : comment jouer"),
                _("- 'F3' : les cases à l'écran"),
                _("- 'F4' : les touches"),
                _("--------"),
                _("(Plus à lire dans le fichier readme.txt)"))
        for mess in help:
            self.add_message(mess, COLOR_CYAN)
        
    def help_f2(self):
        """
        Aide en jeu f2
        """
        help = (_("Comment jouer ?"),
                _("-------------"),
                _("Ce jeu est un roguelike. Il est basé sur le tour par tour, et une fois que votre personnage meurt, il n'y a pas de retour en arrière."),
                _("En vous déplaçant dans les quatre directions, vous attaquez des monstres, ouvrez des portes, collectez des équipements ou utilisez des escaliers."),
                _("Votre but est de survivre assez longtemps dans les mines, en progressant en tuant des monstres et en descendant le plus profondément possible."),
                _("On dit que votre véritable némésis vous attend au fond..."))
        for mess in help:
            self.add_message(mess, COLOR_CYAN)
            
    
    def help_f3(self):
        """
        Aide en jeu : f3
        """
        help = (_("Les cases du jeu"),
                _("---------------------"),
                _("arbes/mur : mur"),
                _("++ : a door; bump into it to open it"),
                _("porte escalier : descente escaliers"),
                _("porte escaleir : montée escaliers"),
                _("fiol jeune: une potion que vous pouvez boire pour récupérer des points de vie"),
                _("champignon  : un champignon magique que l'on peut manger en se reposant(hors des monstres)"),
                _("arbre mort/porte  : passage vers d'autre salle"))
        for mess in help:
            self.add_message(mess, COLOR_CYAN)
        
    def help_f4(self):
        """
        Aide en jeu : f4
        """
        help = (_("Les touches du jeu"),
                _("--------------------"),
                _("- h, F2, F3, F4 : Aide en jeu"),
                _("- keyboard arrows: to move and attack North, South, East and West"),
                _("- espace : attendre un tour"),
                _("- d : boire une potion de santé"),
                _("- r : se reposer pour récupérer des HP en mangeant des champignons"),
                _("- e : se reposer et manger un champignon"),
                _("- 1, 2, 3, 4 : équipez votre meilleure épée, hache, lance, marteau de guerre"),
                _("- i : les armes dans votre inventaire"),
                _("- esc : sauvegarder et fermer le jeu"))
        for mess in help:
            self.add_message(mess, COLOR_CYAN)
                    
    def inventory(self):
        """
        Liste de tous les effets personnels du joueur
        """
        mess = _("Vous avez")
        for n in range(len(self.weapon_flavor)):
            if self.weapon_flavor[n] != WEAPON_NONE:
                if n == self.active_weapon:
                    mess = "%s %s (%s-%s)," % (mess, 
                                               self.weapon_name(n, self.weapon_flavor[n]),
                                               self.damage_min(n),
                                               self.damage_max(n))
                else:
                    mess = "%s %s," % (mess, self.weapon_name(n, self.weapon_flavor[n]))
        self.add_message("%s." % mess[:-1], COLOR_BLUE)
        
    
    def dist(self, pos1, pos2, dir4 = True):
        """
        calculer la distance entre la position 1 et la position 2
        """
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        if dir4:
            return dx + dy
        else:
            return max(dx, dy)
    
    
    def blocked(self, pos):
        """
        Vrai si (x, y) ne peut pas être accédé, Faux sinon
        """
        if self.dsize[0] >= pos[0] >= 0 and self.dsize[1] >= pos[1] >= 0:
            return self.dungeon.floor[pos] == DUNGEON_WALL \
                or self.dungeon.has_special(pos, SPECIAL_DOOR)
        return False
                
                
    def lit(self, pos):
        """
        Vrai si la cellule à la position est allumée, Faux dans les autres cas.
        """
        return self.seen[pos] == 1
        
        
    def set_lit(self, pos):
        """
        Allumez la cellule à pos
        """
        if 0 <= pos[0] <= self.dsize[0] and 0 <= pos[1] <= self.dsize[1]:
            self.seen[pos] = 1
            self.known[pos] = 1
    
    
    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        """
        Fonction récursive de projection de lumière
        """
        if start < end:
            return
        radius_squared = radius*radius
        for j in range(row, radius+1):
            dx, dy = -j-1, -j
            blocked = False
            while dx <= 0:
                dx += 1
                    # Traduisez les coordonnées dx, dy en coordonnées cartographiques :
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope et r_slope stockent les pistes de la gauche et de la droite.
                # les extrémités du carré que nous considérons :
                l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # faisceau lumineux touche ce carré ; allume-le :
                    if dx*dx + dy*dy < radius_squared:
                        self.set_lit((X, Y))
                    if blocked:
                        # on scanne une rangée de carrés bloqués :
                        if self.blocked((X, Y)):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked((X, Y)) and j < radius:
                            # C'est un carré block, commencez un scan du child:
                            blocked = True
                            self._cast_light(cx, cy, j+1, start, l_slope,
                                             radius, xx, xy, yx, yy, id+1)
                            new_start = r_slope
            # Le rang est balayé ; faites le rang suivant sauf si le dernier carré est bloqué :
            if blocked:
                break
    
    
    def do_fov(self, radius):
        """
        Calculer les carrés éclairés à partir de l'emplacement et du rayon donnés
        """
        self.seen = N.zeros(self.dsize)
        self.seen[self.pos] = 1
        x, y = self.pos
        for oct in range(8):
            self._cast_light(x, y, 1, 1.0, 0.0, radius,
                             MULT[0][oct], MULT[1][oct],
                             MULT[2][oct], MULT[3][oct], 0)
        
                
    def last_word(self):
        """
        phrases de fin
        """
        l = (_("Il a fait combien de dégâts ? !"),
             _("Encore un tour avant d'utiliser cette potion de santé."),
             _("Je suis sûr que je vais obtenir beaucoup d'XP si je pouvais battre ce gars-là ..."),
             _("Soit il va me tuer, soit je vais le tuer."),
             _("Hé, je suis stupéfait, qu'est-ce que c'est ?"),
             _("Je crois que j'ai enfin compris le principe."),
             _("Je me demande ce que c'est ?"),
             _("Je serai en sécurité dans ces escaliers. ....arrrgh !"),
             _("Argh ! Descends du clavier, espèce de chat... Oh Non !"),
             _("Encore un tour..."),
             _("Qu'est-ce qu'il fait si haut dans le dungeon ?"),
             _("Aaargh!"))
        return random.choice(l)
    
    
    def deal_damage(self, tile, n, sound = None):
        """
        Le joueur subit n HP de dégâts
        """
        self.hp -= n # damage p
        hit = random.choice((_("morsures"), _("griffes"), _("coupures"), _("éraflures"), _("ronger"), \
                             _("aracher"), _("coups de pied"), _("coup de poing"), _("déchirures"), _("piqûres")))
        self.add_message(_("%s %s vous pour %s point(s) de dégâts !") % (tile, hit, n),
                         COLOR_MAGENTA)
        if self.hp > 0:
            if sound is not None:
                sound[CHANNEL_SOUNDS].queue(sound[SOUND_MONSTER_ATTACK])
            self.update_mood(TRIGGER_SUFFER)
        else:
            if sound is not None:
                sound[CHANNEL_SOUNDS].queue(sound[SOUND_MONSTER_KILL])
            self.exit = 1  
            self.event = EVENT_DEATH
            
    
    def add_mushroom_seen(self, pos):
        """
        Se souvient d'un champignon vu par le joueur
        """
        self.mush_seen[pos] = 1
        
            
    def remove_mushroom_seen(self, pos):
        """
        Supprime un champignon de la liste self.mush_seen
        """
        if pos in self.mush_seen:
            del self.mush_seen[pos]
    
    def closest_mushroom(self, pos, dir4 = True):
        """
        Trouve le champignon le plus proche de la position d'un monstre.
        """
        if len(self.mush_seen) == 0:
            # No mushroom seen
            return (1000, 1000), 1000
        else:
            d_mush = 1000
            for pos_found in self.mush_seen:
                d = self.dist(pos_found, pos, dir4)
                if d < d_mush:
                    d_mush = d
                    pos_mush = pos_found
            return pos_mush, d_mush
        
    
    def move_monsters(self, sound = None):
        """
        Parcourir tous les monstres et déplacer ceux qui sont éveillés
        """
        # Dictionnaire temporaire
        monsters = {}
        # flag pour combat de hache
        flag_hit = False
        # Nouveaux monstres à ajouter
        add_monster = []
        
        for pos, monster in list(self.dungeon.monster.items()):
            move = False
            if monster.is_awake():
                # Choisir le plus proche entre le champignon le plus proche et le joueur le monstre level up si il mange un champignon
                pos_mush, d_mush = self.closest_mushroom(pos, monster.level < 6)
                d_player = self.dist(pos, self.pos, monster.level < 6)
                if d_player < d_mush:
                    spos, d = self.pos, d_player
                else:
                    spos, d = pos_mush, d_mush
                
                if d == 1 and d_player < d_mush:
                    flag_hit = True
                    self.deal_damage(monster.name(), monster.damage(), sound)
                    
                elif d == 0 and not d_player < d_mush:
                    self.dungeon.grab_special(pos_mush, SPECIAL_MUSHROOM)
                    self.remove_mushroom_seen(pos_mush)
                    monster_name = monster.name()
                    if monster.hp == monster.hpmax:
                        if monster.level < monster.levelmax:
                            if sound is not None:
                                sound[CHANNEL_SOUNDS].queue(sound[SOUND_MONSTER_LEVELUP])
                            monster.upgrade()
                            self.add_message(_("%s mange un champignon et se transforme en %s!") % (monster_name, monster.name()),
                                     COLOR_MAGENTA)
                        elif monster.level < 4:
                            self.add_message(_("%s mange un champignon.") % monster_name,
                                         COLOR_MAGENTA)
                        else:
                            # Appeler un nouveau monstre en l'ajoutant à la liste 'add_monster'.
                            dirs = DIRS8
                            random.shuffle(dirs)
                            for j in range(len(dirs)):
                                pos_test = (pos[0] + dirs[j][0], pos[1] + dirs[j][1])
                                if self.dungeon.is_reachable(pos_test) and \
                                (pos_test[0] != self.pos[0] or pos_test[1] != self.pos[1]):
                                    if sound is not None:
                                        sound[CHANNEL_SOUNDS].queue(sound[SOUND_MONSTER_SUMMON])
                                    l = random.randint(1, monster.level)
                                    add_monster.append((pos_test, l))
                                    self.add_message(_("%s invoque un ami!") % monster_name, COLOR_MAGENTA)
                                    if monster.level < 10:
                                        break
                    else:
                        if sound is not None:
                            sound[CHANNEL_SOUNDS].queue(sound[SOUND_REST])
                        monster.heal()
                        self.add_message(_("%s mange un champignon et récupère la totalité de ses forces!") % monster_name,
                                         COLOR_MAGENTA)
                else:
                    # Le monstre se déplace vers la cible
                    d_new = d
                    pos_alt = pos
                    if monster.level < 6:
                        dirs = DIRS
                    else:
                        dirs = DIRS8
                    random.shuffle(dirs)
                    for dir in dirs:
                        pos_temp = (pos[0] + dir[0], pos[1] + dir[1])
                        if self.dungeon.is_reachable(pos_temp) and \
                        (pos_temp[0] != self.pos[0] or pos_temp[1] != self.pos[1]) and \
                        pos_temp not in monsters:
                            pos_alt = pos_temp
                            d_temp = self.dist(pos_temp, spos, monster.level < 6)
                            if d_temp <= d_new:
                                d_new, pos_new = d_temp, pos_temp
                    move = d_new < d or pos_alt != pos
                    if pos_alt != pos and d_new == d:
                        # Il vaut mieux avancer que ne pas avancer.
                        pos_new = pos_alt
            if move:
                monsters[pos_new] = monster
            else:
                monsters[pos] = monster
        # Hack (Impossible de changer le dictionnaire en le parcourant)
        self.dungeon.monster = monsters
        
        # Ajout de nouveaux monstres
        for pos_test, l in add_monster:
            self.dungeon.add_monster(pos_test, l)
        
        if flag_hit:
            self.hit_by_monster = True
        else:
            self.hit_by_monster = False
            
    
    def tile(self):
        """
        case de joueur à l'écran
        """
        return "&%s" % WEAPON_TILE[self.active_weapon]
        
    
    def load_dungeon_floor(self, pos, save = True):
        """
        Charge un dungeon à partir de son nom, de son niveau et d'une position.
        """
        self.mush_seen = {}
        
        if save:
            # Nous sauvegardons les informations du donjon
            self.dict_dungeon[self.dungeon.name] = self.dungeon #(self.dungeon, self.known)
            self.known_dungeon[self.dungeon.name] = self.known
            
        name = "%s-%s (%s, %s)" % (self.dname, self.deepness, pos[0], pos[1])
        
        if name in self.dict_dungeon:
            # Cet étage a déjà été visité
            self.dungeon = self.dict_dungeon[name]
        else:
            self.dungeon = Dungeon(self.dsize, 45, name, self.deepness)
            
        if name in self.known_dungeon:
            # Le joueur connaît déjà cet étage par la mémoire de ses ancêtres.
            self.known = self.known_dungeon[name]
            """ * (self.dungeon.special <> SPECIAL_POTION) \
                * (self.dungeon.special <> SPECIAL_MUSHROOM)"""
        else:
            self.known = N.zeros(self.dsize)
            
        
    def add_message(self, message, color = None):
        """
        Ajouter un message
        """
        if color is None:
            color = COLOR_WHITE
        list = []
        elt = ""
        for word in message.split(' '):
            if len(elt) + len(word) < self.cols:
                elt += " " + word
            else:
                list.append(elt[1:])
                elt = " " + word
        list.append(elt[1:])
        for mess in list:
            self.message.insert(0, (mess, color))
            if len(self.message) > 100:
                self.message.pop()
        
    
    def progress(self, xp, sound = None):
        """
        Le joueur reçoit des points d'expérience
        """
        self.xp += xp
        if self.xp >= self.levels[self.level]:
            self.event = EVENT_LEVELUP
            if sound is not None:
                sound[CHANNEL_SOUNDS].queue(sound[SOUND_PLAYER_LEVELUP])
            self.level += 1
            self.hpmax += self.hpmax / 2
            self.hp = self.hpmax
            self.add_message(_("Vous gagnez %s d'XP et progressez au niveau %s !") % (xp, self.level),
                             COLOR_YELLOW | COLOR_BOLD)
        else:
            self.add_message(_("Vous gagnez %s XP.") % xp)
            
        if xp == 150:
            self.winner = True
            self.add_message(_("Félicitations ! !! Tu m'as vaincu. Tu es un **GAGNANT** !"),
                             COLOR_YELLOW | COLOR_BOLD)
            self.add_message(_("Tu peux partager le replay et montrée à quel point tu es fort."),
                             COLOR_YELLOW)
            self.exit = 2

        
    def drink(self, sound = None):
        """
        boit une potion
        """
        if self.potion > 0:
            if self.mood_state < MOOD_BERZERK:
                if sound is not None:
                    sound[CHANNEL_SOUNDS].queue(sound[SOUND_DRINK])
                self.potion -= 1
                self.add_message(_("Vous buvez une potion de santé et récupérez tous vos points de vie. !"),
                                 COLOR_GREEN)
                self.hp = self.hpmax
                self.update_mood(TRIGGER_HEAL)
                return True
            else:
                mess = (_("Votre humeur berzerk vous empêche de vous soigner.."),
                        _("Du sang ! Sang ! Sang !"),
                        _("Tu ne veux pas prendre soin de toi."),
                        _("mort ! mort ! Tuez !"))
                self.add_message(random.choice(mess))
                return False
        else:
            self.add_message(_("Vous n'avez pas de potion de santé à boire."))
            return False
            
    
    def rest(self, n = 1000, sound = None):
        """
        se reposer pour récupérer des HP en mangeant des champignons
        """
        for pos, monster in list(self.dungeon.monster.items()):
            if monster.is_awake():
                self.add_message(_("Vous ne pouvez pas vous reposer et manger tant qu'il y a des monstres éveillés autour de vous."))
                return False
            
        if self.hp == self.hpmax: 
            self.add_message(_("Vous êtes déjà au maximum de vos points de vie."))
            return False
        
        hp_rest = int(min(n, self.mushroom, self.hpmax - self.hp))
        if hp_rest == 0:
            self.add_message(_("Vous ne récupérez aucun point de vie. Vous avez besoin de champignons!"))
            return False
        
        if sound is not None:
            sound[CHANNEL_SOUNDS].queue(sound[SOUND_REST])
                
        self.hp += hp_rest
        self.round += hp_rest
        self.mushroom -= hp_rest
        for i in range(hp_rest):
            self.update_mood(TRIGGER_REST)
                
        if self.hp == self.hpmax: 
            self.add_message(_("Vous vous reposez pendant un moment et mangez suffisamment de champignons pour récupérer tous vos points de vie.."),
                             COLOR_GREEN)
        else:
            self.add_message(_("Vous vous reposez et mangez %s, en récupérant %s.") \
                             % (self._plural(hp_rest, _("mushroom")), self._plural(hp_rest, _("health point"))), \
                             COLOR_GREEN)
        return True

    
    def damage(self):
        """
        Combien de dégâts le joueur inflige-t-il
        """
        l1 = self.weapon_flavor[self.active_weapon] + (self.charge + self.mood_state) * self.level
        if l1 == WEAPON_FLAVOR5:
            l1 += self.level
        if self.hit_by_monster and \
            (self.active_weapon == WEAPON_AXE or self.active_weapon == WEAPON_WARHAMMER) \
            and self.mood_state == MOOD_QUIET:
            l2 = l1 + self.level / 2
        else:
            l2 = l1 + self.level
        return int(1 + random.randint(int(l1), int(l2)) + random.randint(int(l1), int(l2)))
    
    
    def damage_min(self, n):
        """
        Combien de dommages le joueur inflige au minimum avec l'arme n.
        """
        l1 = self.weapon_flavor[n] + (self.charge + self.mood_state) * self.level
        if l1 == WEAPON_FLAVOR5:
            l1 += self.level
        return 1 + l1 + l1
    
    
    def damage_max(self, n):
        """
        Combien de dommages le joueur inflige au maximum avec l'arme n
        """
        l1 = self.weapon_flavor[n] + (self.charge + self.mood_state) * self.level
        if l1 == WEAPON_FLAVOR5:
            l1 += self.level
        if self.hit_by_monster and \
            (self.active_weapon == WEAPON_AXE or self.active_weapon == WEAPON_WARHAMMER) \
            and self.mood_state == MOOD_QUIET:
            l2 = l1 + self.level / 2
        else:
            l2 = l1 + self.level
        return 1 + l2 + l2
    
    
    def save(self):
        """
        enregistrer dans un fichier
        """
        self.known_dungeon[self.dungeon.name] = self.known
        output = open('dn.sav', 'wb')
        # Décrocher du joueur
        pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        output.close()
    
    
    def save_movie(self, score, desc):
        """
        Après die ou exit, sauvegarde les actions dans un fichier
        """
        if not os.path.isdir('movies'):
            os.mkdir('movies')
        i = 0
        while True:
            name = '%s-%sx%s-%03d.dn' % (self.dname, self.dsize[0], self.dsize[1], i)
            if os.path.isfile(os.path.join('movies', name)):
                i += 1
            else:
                break
        output = open(os.path.join('movies', name), 'wb')
        # Pickle the data
        pickle.dump(desc, output, pickle.HIGHEST_PROTOCOL)        
        pickle.dump(self.dsize, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.dname, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.history, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.seed, output, pickle.HIGHEST_PROTOCOL)        
        pickle.dump(self.known_dungeon, output, pickle.HIGHEST_PROTOCOL)        
        output.close()
    def save_score(self):
        """
        Enregistrer le score dans le dictionnaire
        """
        if self.winner:
            print(_("Vous êtes un gagnant !"))
            #  : en cas de victoire, le moins de rounds possible (pour le tri des rangs)
            score = 1000000 - self.round
            new_entry = _("** WINNER ** au %s rounds - Profondeur max %s - Char. lvl %s (%s)") \
            % (self.round, self.deepness_max, self.level, time.strftime("%c"))
        else:
            print(_("Vous avez obtenu un score de %s.") % self.xp)
            score = self.xp
            new_entry = _("Score %04d - Profondeur max %s - Char. lvl %s (%s)") \
            % (score, self.deepness_max, self.level, time.strftime("%c"))
        print("------------------")
        
        if not os.path.isdir('morgue'):
            os.mkdir('morgue')
        morguefile = "%s-%sx%s.txt" % (self.dname, self.dsize[0], self.dsize[1])
        file = open(os.path.join('morgue', morguefile), "a")
        file.write(new_entry + "\n")
        file.close()
        
        if self.dname_full not in self.scores:
            # This is the first score in this dungeon
            self.scores[self.dname_full] = []
            
        self.scores[self.dname_full].append((score, new_entry))
        #self.scores[self.dname_full].sort(lambda x,y: cmp(y[0],x[0]))
        
        print(_("%s rangs :") % self.dname_full)
        print("-" * (len(self.dname_full) + 8))
        for i in range(len(self.scores[self.dname_full])):
            print("%03d : %s" % (i+1, self.scores[self.dname_full][i][1]))
        
        if self.record:
            self.save_movie(score, new_entry)
            
            
    def grab_mushroom(self, pos, sound = None):
        """
        Prenez un champignon quand vous en avez besoin
        """ 
        if sound is not None:
            sound[CHANNEL_SOUNDS].queue(sound[SOUND_GRAB_STUFF])
        self.add_message(_("Vous prenez un champignon."))
        self.mushroom += self.dungeon.grab_special(pos, SPECIAL_MUSHROOM)
        self.remove_mushroom_seen(pos)
        
                    
    def update_dir(self, pos):
        """
        Met à jour la direction à laquelle le joueur regarde
        """
        dir = (self.pos[0] - pos[0], self.pos[1] - pos[1])
        if self.dir == dir and self.dir != (0, 0) and self.active_weapon == WEAPON_SWORD:
            self.charge += 1
        else:
            self.charge = 0
        self.dir = (self.pos[0] - pos[0], self.pos[1] - pos[1])        
    
    
    def _plural(self, n, text):
        if n > 1:
            return "%s %ss" %(n, text)
        else:
            return "%s %s" %(n, text)
        
    
    def move(self, pos, coef = 1, sound = None):
        """
        Tente de déplacer le joueur vers la nouvelle position.
        coef est un multiplicateur d'XP lorsque vous combinez des monstres (1, 2, 4, 8, ...)
        """
        
        if pos[0] == self.pos[0] and pos[1] == self.pos[1]:
            if self.dungeon.has_special(pos, SPECIAL_MUSHROOM):
                # mushroom
                self.grab_mushroom(pos, sound)
            else:
                self.add_message(_("Vous attendez..."))
            
        elif self.dungeon.has_monster(pos):
            
            monster_name = self.dungeon.monster[pos].name()
            
            if self.hit_by_monster and \
            (self.active_weapon == WEAPON_AXE or self.active_weapon == WEAPON_WARHAMMER) \
            and self.mood_state == MOOD_QUIET:
                self.add_message(_("Vous vous sentez confus lorsque vous utilisez votre arme...."))
            
            if self.active_weapon == WEAPON_SWORD \
            and self.charge > 0:
                if self.dir == (pos[0] - self.pos[0], pos[1] - self.pos[1]):
                    self.add_message(_("Chargement d'épée #%d !") % self.charge,
                                     COLOR_YELLOW | COLOR_BOLD)
                else:
                    self.charge = 0
                
            n = self.damage() * coef
            l = self.dungeon.monster[pos].level
            xp = self.dungeon.bash_monster(pos, n) * coef
            
            if xp > 0:
                
                if sound is not None:
                    sound[CHANNEL_SOUNDS].queue(sound[SOUND_PLAYER_KILL])
            
                if self.active_weapon == WEAPON_AXE:
                    if coef > 1:
                        self.add_message(_("Tourbillon de la hache #%d !") % coef, COLOR_YELLOW | COLOR_BOLD)
                    self.add_message(_("Vous frappez %s pour %s de dégâts, le tuant.") % (monster_name, self._plural(n, _("point"))),
                                     COLOR_YELLOW)
                    if coef == 1:
                        random.shuffle(DIRS8)
                        for dir in DIRS8:
                            pos_next = (self.pos[0] + dir[0], self.pos[1] + dir[1])
                            if pos_next != pos and self.dungeon.has_monster(pos_next):
                                time.sleep(.1)
                                #self.display(s)
                                self.move(pos_next, coef * 2, sound)
                    
                elif self.active_weapon == WEAPON_SPEAR:
                    # Spear
                    self.add_message(_("Charge de la lance #%d !") % coef, COLOR_YELLOW | COLOR_BOLD)
                    self.add_message(_("Vous chargez %s pour %s de dommages, le tuant.") % (monster_name, self._plural(n, _("point"))),
                                 COLOR_YELLOW)
                    pos_next = (2 * (pos[0] - self.pos[0]) + self.pos[0],
                                2 * (pos[1] - self.pos[1]) + self.pos[1])
                    self.pos = (pos[0], pos[1])
                    #self.display(s)
                    time.sleep(.1)
                    self.move(pos_next, coef * 2, sound)
                
                elif self.active_weapon == WEAPON_WARHAMMER:
                    self.add_message(_("Vous frappez %s pour %s de dégâts, le tuant.") % (monster_name, self._plural(n, _("point"))),
                                 COLOR_YELLOW)
                    
                else:
                    self.add_message(_("Vous avez touché %s pour %s de dégâts, le tuant.") % (monster_name, self._plural(n, _("point"))),
                                 COLOR_YELLOW)
                    
                self.progress(xp, sound)
                n = self.dungeon.add_mushroom(pos, l + 1)
                self.add_message(_("%s dépose %s sur le sol.") % (monster_name, self._plural(n, _("mushroom"))))
                if self.dungeon.has_special(self.pos, SPECIAL_MUSHROOM):
                    # mushroom
                    self.grab_mushroom(self.pos, sound)
                self.update_mood(TRIGGER_KILL)
                
            else:
                if sound is not None:
                    sound[CHANNEL_SOUNDS].queue(sound[SOUND_PLAYER_ATTACK])
            
                if self.active_weapon == WEAPON_WARHAMMER:
                    m = self.weapon_flavor[self.active_weapon] + 1
                    if random.randint(0, m + self.dungeon.monster[pos].level) <= m:
                        # Pousser ou frapper ?
                        knock = False
                        self.add_message(_("Charge Warhammer #%d !") % m,
                                         COLOR_YELLOW | COLOR_BOLD)
                        pos_monster = pos
                        for i in range(m+1):
                            pos_next = ((2 + i) * (pos[0] - self.pos[0]) + self.pos[0],
                                        (2 + i) * (pos[1] - self.pos[1]) + self.pos[1])
                            if self.dungeon.is_reachable(pos_next):
                                # Monstre à pousser
                                self.dungeon.monster[pos_next] = self.dungeon.monster.pop(pos_monster)
                                pos_monster = pos_next
                                time.sleep(.1)
                                #self.display(s)
                            else:
                                # Monstre Knock
                                knock = True
                                self.dungeon.monster[pos_monster].stun(m)
                                # Casse la porte derrière
                                if self.dungeon.has_special(pos_next, SPECIAL_DOOR):
                                    self.dungeon.grab_special(pos_next, SPECIAL_DOOR)
                                # Monstre étourdissant derrière
                                elif self.dungeon.has_monster(pos_next):
                                    self.dungeon.monster[pos_next].stun(m)
                                time.sleep(.1)
                                #self.display(s)
                                self.add_message(_("Vous frappez %s pour %s et l'étourdissez pour %s.") % \
                                                 (monster_name, self._plural(n, _("point")), self._plural(m, _("round"))),
                                                 COLOR_YELLOW)
                                break
                        if not knock:
                            # Monstre pousser
                            self.add_message(_("Vous frappez %s pour %s de dégâts.") % (monster_name, self._plural(n, _("point"))),
                                      COLOR_YELLOW)
                        # Déplacement du joueur
                        if self.dungeon.is_reachable(pos):
                            self.pos = (pos[0], pos[1])                                
                            
                    else:
                        self.add_message(_("Vous frappez %s pour %s de dégâts.") % (monster_name, self._plural(n, _("point"))),
                                      COLOR_YELLOW)
                        
                else:
                    self.add_message(_("Vous touchez %s pour %s de dégâts.") % (monster_name, self._plural(n, _("point"))),
                                      COLOR_YELLOW)
                         
        elif self.dungeon.has_special(pos, SPECIAL_DOOR):
            if sound is not None:
                    sound[CHANNEL_SOUNDS].queue(sound[SOUND_OPEN_DOOR])
            self.add_message(_("Vous ouvrez la porte."))
            self.dungeon.grab_special(pos, SPECIAL_DOOR)
            
        elif self.dungeon.is_reachable(pos):
            
            self.pos = (pos[0], pos[1])
            
            if self.dungeon.special[pos] >= SPECIAL_SWORD:
                weap_flav, weap_num = self.dungeon.weapon_params(pos)
                if weap_flav > self.weapon_flavor[weap_num]:
                    if sound is not None:
                        sound[CHANNEL_SOUNDS].queue(sound[SOUND_GRAB_STUFF])
                    self.add_message(_("Vous attrapez %s.") % self.weapon_name(weap_num, weap_flav),
                                     COLOR_BLUE)
                    self.weapon_flavor[weap_num] = weap_flav
                    self.dungeon.special[pos] = 0
                elif weap_flav < self.weapon_flavor[weap_num]:
                    self.add_message(_("Vous en avez déjà une meilleure %s.") % WEAPON_NAME[weap_num])
                else:                    
                    self.add_message(_("Vous avez déjà %s.") % self.weapon_name(weap_num, weap_flav))
            
            elif self.dungeon.has_special(pos, SPECIAL_MUSHROOM):
                # champignon
                self.grab_mushroom(pos, sound)
            
            elif self.dungeon.has_special(pos, SPECIAL_POTION):
                # potion
                if sound is not None:
                    sound[CHANNEL_SOUNDS].queue(sound[SOUND_GRAB_STUFF])
                self.add_message(_("Vous prenez une potion de santé."))
                self.potion += self.dungeon.grab_special(pos, SPECIAL_POTION)

            elif self.dungeon.has_special(pos, SPECIAL_DOWNSTAIRS1) or \
                 self.dungeon.has_special(pos, SPECIAL_DOWNSTAIRS2):
                # Escalier vers le bas
                self.add_message(_("Vous descendez les escaliers."))
                self.deepness += 1
                self.deepness_max = max(self.deepness_max, self.deepness)
                self.load_dungeon_floor(pos, True)
                self.pos = self.dungeon.pos_start
                self.start_pos.append(pos)
                self.known[self.pos] = 1
                self.event = EVENT_STAIRSDOWN
                
            elif self.dungeon.has_special(pos, SPECIAL_UPSTAIRS):
                # Escalier vers le haut
                if self.deepness == 1:
                    self.add_message(_("Tu sais qu'il n'y a pas de retour en arrière, n'est-ce pas ?"))
                    #self.exit = 2
                else:
                    self.add_message(_("Vous montez les escaliers."))
                    self.deepness -= 1
                    self.pos = self.start_pos[-1]
                    self.start_pos.pop()
                    self.load_dungeon_floor(self.start_pos[-1], True)
                    self.known[self.pos] = 1               
                    self.event = EVENT_STAIRSUP
        else:
            self.add_message(_("Vous ne pouvez pas y aller."))
            return False
    
        return True

            
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
#                            Main
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-
def load_config():
    """
    Charge le fichier dn.ini
    """
    CURSES_DIRS = "{32: (0, 0), 258: (0, 1), 259: (0, -1), 260: (-1, 0), 261: (1, 0), 350: (0, 0)}"
    PYG_DIRS = "{105: (0, 0), 1073741905: (0, 1), 1073741906: (0, -1), 1073741904: (-1, 0), 1073741903: (1, 0), 109: (0, 0)}"
    
    if not os.path.isfile('dn.ini'):
        conf_new = configparser.ConfigParser()
        
        conf_new.add_section('Game')
        conf_new.set('Game', 'Name', 'Random')
        conf_new.set('Game', 'Width', "40")
        conf_new.set('Game', 'Height', "40")
        conf_new.set('Game', 'difficulty', "15")
        conf_new.set('Game', 'cf', "False")
        
        conf_new.add_section('Movie')
        conf_new.set("Movie", 'Record', "True")
        conf_new.set("Movie", 'Speed', "500")
        

        
        conf_new.add_section("Pygame")
        conf_new.set('Pygame', 'TileSize', "12")
        conf_new.set('Pygame', 'Dirs', PYG_DIRS)

        conf_new.set('Pygame', 'ScreenWidth', "1024")
        conf_new.set('Pygame', 'ScreenHeight', "600")
        conf_new.set('Pygame', 'Fullscreen', "False")
        conf_new.set('Pygame', 'Music', "True")

        # sauvegarde du fichier ini
        conf_new.write(open('dn.ini', 'w'))
        
    conf = configparser.ConfigParser()
    conf.read('dn.ini')
    
    name = conf.get("Game", "Name")
    width = conf.getint("Game", "Width")
    height = conf.getint("Game", "Height")
    conf_difficulty = conf.getint("Game", "difficulty")
    conf_chcod = conf.get("Game", "cf")
    conf_game = (name, width, height)
    
    record = conf.getboolean("Movie", "Record")
    replay_speed = conf.getint("Movie", "Speed")
    conf_movie = (record, replay_speed)
    

    
    #return name, eval(dirs), width, height, cols, record, replay_speed
    tilesize = conf.getint("Pygame", "TileSize")
    dirs = conf.get("Pygame", "Dirs")
    screenwidth = conf.getint("Pygame", "ScreenWidth")
    screenheight = conf.getint("Pygame", "ScreenHeight")
    fullscreen = conf.getboolean("Pygame", "Fullscreen")
    music = conf.getboolean("Pygame", "Music")
    conf_pygame = (tilesize, eval(dirs), screenwidth, screenheight, fullscreen, music)
    
    #return conf_game, conf_movie, conf_pygame,conf chcod
    return conf_game, conf_movie, conf_pygame, conf_chcod , conf_difficulty


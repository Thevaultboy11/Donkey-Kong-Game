add_library('minim')

import random        # random utilities (unused currently)
import time          # timing for delta time
import os

###
"""
Notes from the Developers:
    
    ...
"""
###

#Board Global Variables and AudioPlayer

audio_player = Minim(this)

BOARD_W = int(224*2.5)
BOARD_H = int(256*2.5)
BACKGROUND_COLOR = 000

PATH = os.getcwd() + "/data/"

#GLOBAL VARIABLES
SCORE = 0 
NUM_LIVES = 2
#Game State: (0:initial screen),(1:playing screen),(2:pause screen),(3:end screen)
GAME_STATE = 0
DID_WIN = False
DID_LOSE_LIFE = False
LEVEL = 1

PLAYER_DEATH_TIMER = 0
STATE_DEATH = 4


# SFX

GLOBAL_SOUNDS = { # Dictionary with all the SFX loaded to the audio_player
    "LOADING_SCREEN": audio_player.loadFile(PATH + "/sfx/loading_screen.wav"),
    "BACKGROUND_LEVEL_1": audio_player.loadFile(PATH + "/sfx/background_noise_level_1.wav"),
    "BACKGROUND_LEVEL_2": audio_player.loadFile(PATH + "/sfx/background_noise_level_2.wav"),
    "HAMMER_TIME": audio_player.loadFile(PATH + "/sfx/hammer_time.wav"),
    "JUMP_SFX": audio_player.loadFile(PATH + "/sfx/jump_small.wav"),
    "ITEM_COLLECT": audio_player.loadFile(PATH + "/sfx/pickup_item.wav"),
    "SCORE_GIVE": audio_player.loadFile(PATH + "/sfx/getting_points.wav"),
    "LEVEL_2_END": audio_player.loadFile(PATH + "/sfx/ending_level_2.wav")
}

# SPRITES

# MARIO
mario_running = loadImage(PATH + "mario_running.png")
mario_jumping = loadImage(PATH + "mario_jump.png")
mario_idle = loadImage(PATH + "mario_idle.png")
mario_climbing_ladder = loadImage(PATH + "mario_ladder_climb.png")
mario_dying_right = loadImage(PATH + "mario_death_right.png")
mario_dying_left = loadImage(PATH + "mario_death_left.png")
mario_hammer_idle = loadImage(PATH + "mario_hammer_idle.png")
mario_hammer_running = loadImage(PATH + "mario_hammer_running.png")


# DONKEY KONG
donkey_idle = loadImage(PATH + "donkey_kong_idle.png")
kong_pounding = loadImage(PATH + "kong_pounding.png")

donkey_barrel_throw = loadImage(PATH + "donkey_barrel_drop.png")
donkey_brown_barrel_drop = loadImage(PATH + "donkey_brown_barrel_drop.png")
donkey_blue_barrel_drop = loadImage(PATH + "donkey_blue_barrel_drop.png")

donkey_climbing_ladder = loadImage(PATH + "donkey_climbing_ladder.png")
donkey_dying = loadImage(PATH + "donkey_kong_screaming_falling.png")

# INFRASTRUCTURE
platform_red = loadImage(PATH + "platform_red.png")
platform_blue = loadImage(PATH + "platform_blue.png")
ladder_image = loadImage(PATH + "ladder_white.png")
ladder_yellow = loadImage(PATH + "yellow_ladder.png")
screw = loadImage(PATH + "screw.png")


# BARRELS
barrel_brown_roll_side = loadImage(PATH + "brown_barrel_roll_side.png")
barrel_brown_roll_front = loadImage(PATH + "brown_barrel_roll_front.png")

barrel_blue_roll_side = loadImage(PATH + "blue_barrel_roll_side.png")
barrel_blue_roll_front = loadImage(PATH + "blue_barrel_roll_front.png")

# ENTITIES
fire_sprit_orange = loadImage(PATH + "fire_spirit_orange.png")
fire_sprit_blue = loadImage(PATH + "fire_spirit_blue.png")

princess_scared = loadImage(PATH + "princess_worried.png")
princess_idle = loadImage(PATH + "princess_idle.png")

# STATIC ITEMS
oil_barrel = loadImage(PATH + "oil_barrel.png")
hammer_item = loadImage(PATH + "hammer_item.png")
static_barrel = loadImage(PATH + "barrel_static.png")

# PARTICLES
fire_small = loadImage(PATH + "fire_small.png")
fire_big = loadImage(PATH + "fire_big.png")
score_100 = loadImage(PATH + "score_100.png")
score_500 = loadImage(PATH + "score_500.png")
score_800 = loadImage(PATH + "score_800.png")

barrel_destroy = loadImage(PATH + "hammer_destroy_barrel_particle.png")

heart_rescaled = loadImage(PATH + "heart_32x.png")
broken_heart = loadImage(PATH + "broken_heart_32x.png")

#2 LEVEL PICKUP ITEMS
first_princess_pickup_item = loadImage(PATH + "princess_pickup2.png")
second_princess_pickup_item = loadImage(PATH + "princess_pickup3.png")
third_princess_pickup_item = loadImage(PATH + "princess_pickup4.png")

#GUI INFRASTRUCTURE

gui_mario_angel_icon = loadImage(PATH + "gui_mario_angel.png")
gui_princess_icon = loadImage(PATH + "gui_princess.png")
gui_kong_idle = loadImage(PATH + "gui_kong_idle.png")
gui_kong_pounding = loadImage(PATH + "gui_kong_pounding.png")
#The Fonts For The Game Screen
title_font = None
menu_font  = None
hud_font = None

def setup():
    # Placeholder for Processing setup; currently unused
    global GAME_STATE
    
    frameRate(50)
    size(BOARD_W, BOARD_H)
    background(BACKGROUND_COLOR)
    global title_font, menu_font, hud_font
    title_font = createFont("kong_arcade_font.TTF", 72)
    menu_font  = createFont("kong_arcade_font.TTF", 32)
    hud_font  = createFont("kong_arcade_font.TTF", 24)
    
    textAlign(CENTER, BASELINE)

    #print(gui_mario_hammer_icon, gui_mario_angel_icon, gui_princess_icon, gui_kong_idle, gui_kong_pounding)
    pass

Enum = {} #Enumerated constants that correspond to INTEGER values for comparisons during runtime.

# 0 - 100
Enum["COLLIDER_TYPE"] = {
    "CIRCLE": 0,
    "LINE": 1
}

# 101 - 200
Enum["ENUM_TYPE"] = {
    "PLAYER": 101,
    "PLATFORM": 102,
    "BARREL": 103,
    "LADDER": 104,
    "FIRE_SPIRIT": 105,
    "ITEM": 106,
    "HALF_LADDER": 107,
    "SCREW": 108,
    "PRINCESS_PICKUP": 109
}


class Vector:
    # An abstract class for Vectors
    
    def __init__(self):
        pass
    
class Vector2(Vector):
    # A vector with two components, x and y
    
    def __init__(self, x=0, y=0):
        # instantiates the Vector
        
        Vector.__init__(self)
        
        self.x = x
        self.y = y
        
    def __str__(self):
        # used for debugging, converts vector into a string of format '(x, y)'
        
        return "(" + str(self.x) + "," + str(self.y) + ")"
        
    def __sub__(self, VectorB):
        # performs vector subtraction, self - VectorB
        
        if isinstance(VectorB, Vector2):
            return Vector2(self.x - VectorB.x, self.y - VectorB.y)
        
    def rmul(self, r):
        # Scale both components by a scalar
        return Vector2(self.x * r, self.y * r)
    
    def rdiv(self, r):
        # Scale both components by a scalar
        
        return self.rmul(1/r)
    
    def vadd(self, VectorB):
        # Vector addition returning a new Vector2
        if isinstance(VectorB, Vector2):
            return Vector2(self.x + VectorB.x, self.y + VectorB.y)
        
    def vsub(self, VectorB):
        # same functionality as self.__sub__() but in a different method
        
        if isinstance(VectorB, Vector2):
            return Vector2(VectorB.x - self.x, VectorB.y - self.y)
        
    def dotp(self, VectorB):
        # Dot product of two vectors
        return self.x * VectorB.x + self.y * VectorB.y
    
    def perp(self):
        # Returns a perpendicular vector (rotated 90 degrees) to self
        return Vector2(-self.y, self.x)
        
    def magnitude(self):
        # Euclidean length of the vector, yields distance or size of the vector
        return (self.x**2 + self.y**2)**0.5
    
    def unit(self):
        # Normalized vector (length 1) in direction of original vector
        return self.rdiv(self.magnitude())
    
class Ray2:
    
    def __init__(self, origin=Vector2(0, 0), direction=Vector2(1, 1), magnitude=5):
        # Ray in 2D defined by origin, direction, and max travel distance
        self.origin = origin
        self.direction = direction
        
        self.magnitude = magnitude
    
class Collider:
    
    def __init__(self, collider_type = Enum["COLLIDER_TYPE"]["CIRCLE"], position = Vector2(0, 0), l = 0):
        # Collider primitive with type, position, and size (l = radius for circle)
        self.collider_type = collider_type
        self.position = position
        self.l = l #dimension / size / radius, etc.
        
        self.collider_aura = 0 # an additional region/offset around the collider
        
    @staticmethod
    def circle_collision(c1, c2):
        # Checks for the collision between two cirular colliders
        dx = c1.position.x - c2.position.x
        dy = c1.position.y - c2.position.y

        dist_sq = dx*dx + dy*dy
        r = (c1.l + c1.collider_aura/2) + (c2.l + c2.collider_aura/2)

        return dist_sq <= r*r
    
    # DEPRECATED
    def ray2_intersected(self, ray):
        # Computes ray-circle intersection; returns closest hit within ray.magnitude or None
        if self.collider_type == Enum["COLLIDER_TYPE"]["CIRCLE"]:
            
            r = self.l + self.collider_aura / 2
            
            # Ray-Circle Intersection
            A_x = ray.origin.x
            A_y = ray.origin.y
            
            C_x = self.position.x
            C_y = self.position.y
            
            m = 0
            
            try:
                m = ray.direction.y / ray.direction.x
            except:
                m = (ray.direction.y) / (ray.direction.x+0.01)

            a = 1 + m**2
            b = 2 * m * A_x - 2 * C_y * m - 2 * C_x - 2 * m**2 * A_x
            c = C_x**2 + C_y**2 + m**2 * A_x**2 + A_y**2 - 2 * m * A_x + 2 * m * A_x * C_y - 2 * A_y * C_y - r**2
            
            det = b**2 - 4*a*c
            
            
            #print("DET:", det)
            if det > 0:
                
                
                x1 = (-b + (det)**0.5) / (2 * a)
                x2 = (-b - (det)**0.5) / (2 * a)
                
                y1 = m * x1 - m*A_x + A_y
                y2 = m * x2 - m*A_x + A_y
                
                P1 = Vector2(x1, y1)
                P2 = Vector2(x2, y2)
                
                P1_mag = (P1 - ray.origin).magnitude()
                P2_mag = (P2 - ray.origin).magnitude()
                
                if P1_mag <= ray.magnitude:
                    
                    if P2_mag <= ray.magnitude:
                        
                        if P1_mag < P2_mag:
                            return (P1, P2)
                        
                        else:
                            return (P2, P1)
                        
                    else:
                        
                        return (P1)
                    
                else:
                    
                    if P2_mag <= ray.magnitude:
                        return (P2)
                    
                    else:
                        return ()
                    
            else:
                
                if det == 0:
                    
                    x1 = (-b + (det)**0.5) / (2 * a)
                    y1 = m * x1 - m*A_x + A_y
                    
                    P1 = Vector2(x1, y1)
                    
                    if P1.magnitude() <= ray.magnitude:
                        
                        return (P1)
                    
                    else:
                        return ()
                    
                    
                else:
                    
                    return ()
                
    # DEPRECATED
    def retrace_ray2_collision(self, ray2, v):
        # Retraces the ray from its collision point.
        
        if self.collider_type == Enum["COLLIDER_TYPE"]["CIRCLE"]:
            
            A_x = ray2.origin.x
            A_y = ray2.origin.y
            
            C = self.position
            C_x = self.position.x
            C_y = self.position.y
            
            v_x = v.x
            v_y = v.y
            
            d_x = ray2.direction.x
            d_y = ray2.direction.y
            
            #theta = math.acos(v.dotp(ray2.direction) / (v.magnitude() * ray2.direction.magnitude()))
            #a = theta % math.pi
            
            lambda1 = (C_y*d_y + C_x*d_x - A_y*d_y - A_x*d_x) / (d_x**2 + d_y**2)
            P = Vector2(A_x + lambda1*d_x, A_y + lambda1*d_y)
            
            if d_y*v_x - d_x*v_y == 0:
                return Vector2(C_x, C_y)
            
            lambda2 = (v_x*C_y + A_x*v_y - C_x*v_y - A_y*v_x) / (d_y*v_x - d_x*v_y)
            B = Vector2(A_x + lambda2*d_x, A_y + lambda2*d_y)
            
            delta = (C-P).magnitude()
            
            P_r = (P-B).rmul(self.l / delta).vadd(B)
            
            #return Vector2(C_x, C_y - 100)
            
            return Vector2(C_x + (P_r.x - (P-B).x), C_y + self.l - delta)
                   
class Service:
    # The base class for Services that handle important parts of the game's functionality.
    def __init__(self, name):
        # Base service type (e.g., Workspace)
        self.name = name
              
class Instance:
    # the base class for Instances, basically almost every object you see rendered in the game. 
    
    def __init__(self, name, EnumType, anchored = False, canCollide = True):
        self.name = name
        self.enum_type = EnumType
        self.objectId = -1
        
        self.active = True
        
        self.anchored = anchored # IF anchored is True, the Instance will not be affected by physics
        self.canCollide = canCollide # If canCollide is True, the Instance can be collided with
        
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        
        if EnumType == Enum["ENUM_TYPE"]["PLAYER"] or EnumType == Enum["ENUM_TYPE"]["BARREL"] or EnumType == Enum["ENUM_TYPE"]["FIRE_SPIRIT"] or EnumType == Enum["ENUM_TYPE"]["ITEM"]:
            self.collider = Collider(Enum["COLLIDER_TYPE"]["CIRCLE"], self.position)
            
        elif EnumType == Enum["ENUM_TYPE"]["PLATFORM"] or EnumType == Enum["ENUM_TYPE"]["LADDER"]:
            self.collider = Collider(Enum["COLLIDER_TYPE"]["LINE"], Ray2(self.position))
            
class Sound:
    # A sound that loads files to audio player every time it is instantiated to avoid 
    # unintended conflicts and functionality during runtime.
    
    def __init__(self, sound_name="", looped=False):
        
        self.sound_name = sound_name
        self.looped = looped
        
        self.sounds = GLOBAL_SOUNDS
        
        self.__sound = self.sounds[self.sound_name]
            
        self.IsPlaying = False # True if the sound is currently playing, False otherwise
        
    def Resume(self):
        # continues playing the sound from current pointer if it is not already playing
        if not self.IsPlaying:
            self.IsPlaying = True
            
            if self.looped:
                self.__sound.loop()
            else:
                self.__sound.play()
            
    def Rewind(self):
        # changes the internal pointer of the sound to 0 (start)
        self.__sound.rewind()
            
    def Play(self):
        # continues playing the sound from start if it is not already playing
        if not self.IsPlaying:
            self.Rewind()
            self.Resume()
        
    def Stop(self):
        # Stops the sound if it is playing at the current pointer.
        if self.IsPlaying:
            self.IsPlaying = False
            
            self.__sound.pause()
    
    # DEPRECATED
    def Halt(self):
        if self.IsPlaying:
            
            self.Stop()

class Animation:
    # used to display sprites in a much more efficient manner than
    # creating unfathomable amounts of variables for each animation
    # in their required classes.
     
    def __init__(self, sprite=None, imageW=32, imageH=32, direction=RIGHT, total_slices=0):
        # Instantiates the Animation with parameters for its display, facing direction and total slices
        # that make up the sprite. Sprites can also be made of a single slice
        
        self.sprite = sprite
        self.img_w = imageW
        self.img_h = imageH
        self.slice = 0
        self.direction = direction
        self.animation_speed = 0.2   # seconds per frame (adjust)
        self.animation_timer = 0     # accumulates dt
        self.total_slices = total_slices

    def update(self, dt):
        # Updates the current slice displayed if a preset amount of time has elapsed
        
        #if there is only one slice then do not update anything.
        if self.total_slices <= 1:
            return
        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if GAME_STATE == 4:   # death animation mode
                if self.slice < self.total_slices - 1:
                    self.slice += 1
                # else: remain on last frame (do NOT loop)
                return
            self.slice = (self.slice + 1) % self.total_slices

    def play(self, xPosition, yPositon):
        # Displays the animation's current slice with directionality
        # taken into account.
        
        if self.direction == RIGHT:
            image(self.sprite, xPosition - self.img_w // 2, yPositon - self.img_h // 2, self.img_w, self.img_h, self.slice * (self.img_w+4), 0, (self.slice) * (self.img_w+4) + self.img_w, self.img_h)
        elif self.direction == LEFT:
            image(self.sprite, xPosition - self.img_w // 2, yPositon - self.img_h // 2, self.img_w, self.img_h, (self.slice) * (self.img_w+4) + self.img_w, 0, self.slice * (self.img_w+4), self.img_h)
        else:
            image(self.sprite, xPosition - self.img_w // 2, yPositon - self.img_h // 2, self.img_w, self.img_h, self.slice * (self.img_w+4), 0, (self.slice) * (self.img_w+4) + self.img_w, self.img_h)
            
class Workspace(Service):
    # A service responsible for maintaining Instances in a safe,
    # ordered manner and provides methods for fetching, adding,
    # getting all child Instances and removing children.
    
    def __init__(self, gravity=10):
        # Instantiates a new Workspace with preset gravity that
        # can be changed on runtime.
        
        Service.__init__(self, "Workspace")
        
        self.gravity = gravity
        self.__index = 0 # The INTEGER referening the internal pointer of the Workspace
                         # to keep track of which ObjectId is the next free one.
        self.__objects = {} # The dictionary containing all key-value pairs of 
                            # objectId's as Keys and Instances as Values
        
    # DANGER: USE CAREFULLY!
    def ResetCounter(self):
        # Resets the internal counter of the Workspace
        self.__index = 0
        
    def AddChild(self, object):
        # Registers a child instance and returns its object id
        
        self.__objects[self.__index] = object
        object.objectId = self.__index
        self.__index += 1
        
        return object.objectId
    
    def RemoveChild(self, object):
        # Removes a child by instance reference
        del self.__objects[object.objectId]
        
    def GetChild(self, objectId):
        # Retrieves a child by object id
        return self.__objects.get(objectId, None)
    
    def GetChildren(self):
        # Returns a list of all children in the Workspace
        return self.__objects.values()
    
    def Raycast(self, ray2):
        # Casts a ray and returns the Vector2 point of Intersection and the 
        # Instance intersected with, if any
        
        intersection = None # Vector2
        target = None # Instance
        
        C = ray2.origin
        C_x = C.x
        C_y = C.y
        
        v = ray2.direction
        v_x = ray2.direction.x
        v_y = ray2.direction.y
        
        for i in self.GetChildren():
                
            if i.canCollide:
                if i.collider.collider_type == Enum["COLLIDER_TYPE"]["LINE"]:
                    
                    A = i.P1
                    B = i.P2
                    
                    A_x = A.x
                    A_y = A.y
                    
                    d = (B-A).unit()
                    d_x = d.x
                    d_y = d.y
                    
                    if d_y*v_x - d_x*v_y != 0:
                        lambda1 = (v_x*C_y + A_x*v_y - C_x*v_y - A_y*v_x) / (d_y*v_x - d_x*v_y)
                        
                        temp_pos = Vector2(A_x + lambda1*d_x, A_y + lambda1*d_y)
                        
                        t_mag = (temp_pos - C).magnitude()
                        
                        if t_mag <= ray2.magnitude:
                            
                            if intersection == None:
                                if (A-temp_pos).magnitude() + (B-temp_pos).magnitude() <= (A-B).magnitude() and (temp_pos - C).dotp(v) > 0:
                                    intersection = temp_pos
                                    target = i
                                
                            else:
                                if (A-temp_pos).magnitude() + (B-temp_pos).magnitude() <= (A-B).magnitude() and (temp_pos - C).dotp(v) > 0 and t_mag < (C-intersection).magnitude():
                                    intersection = temp_pos
                                    target = i
                                                    
        return (intersection, target)

class Debris(Service):
    # A service that guarantees removal of instances from Workspace
    # after a preset amount of time.
    
    def __init__(self, Workspace):
        # instantiates a new Debris service
        
        Service.__init__(self, "Debris")
        
        self.__Workspace = Workspace

        self.__index = 0 # Internal counter for the Debris service used in its internal dictionary mappings
        self.__objects = {} # Internal dictionary mappings for key-Instance pairs processed by Debris Service
        self.__threads = {} # NOUSE: MultiThreading not implemented
        
    def AddItem(self, item, timeout=1):
        # Adds a new Instance to DebrisService for processing its guaranteed removal from the game
        
        if not self.__objects.get(item.objectId, None):
            self.__objects[item.objectId] = [item, 0, timeout]
            
    def update(self, dt):
        # Updates the state of all objects in DebrisService
        
        for d in self.__objects.values():
            d[1] += dt
            if d[1] >= d[2]:
                d[0].active = False
                
                try:
                    if Workspace.GetChild(d[0].objectId):
                        Workspace.RemoveChild(d[0])
                    
                    else:
                        del self.__objects[d[0].objectId]
                except:
                    del self.__objects[d[0].objectId]
                    

class Screw(Instance):
    # An Instance that appears in Level 2 and disappears when the player steps on it
    # Yeah thats literally its entire existance. What did you expect?
    
    def __init__(self, P=Vector2(0,0), radius=10):
        # Instantiates the screw
        Instance.__init__(self, "Screw", Enum["ENUM_TYPE"]["SCREW"], True, False)
        
        self.position = P
        self.isShowing = True
        self.collider = Collider(Enum["COLLIDER_TYPE"]["CIRCLE"], self.position)
        self.collider.l = radius  
        self.radius = radius

    def update(self ,dt=0):
        # Update the collider's position to match screw
        self.collider.position = self.position

        # Check collision with player — but only if showing
        if self.isShowing:
            player = game.localPlayer
            if self.collider.circle_collision(self.collider, player.collider):
                # Check if player is touching TOP of the screw
                self.isShowing = False
                self.active = False   # remove from game workspace
                game.Workspace.RemoveChild(self)

    def display(self, dt=0):
        # Display the screw...
        if self.isShowing:
            image(screw, self.position.x, self.position.y+20, 24, 24, 0, 0, 30, 32)
            
class PrincessPickup(Instance):
    # Items that spawn in Level 2 and yield score points when collected
    
    def __init__(self, P=Vector2(0,0), radius=32, type=0):
        Instance.__init__(self, "Item", Enum["ENUM_TYPE"]["PRINCESS_PICKUP"], True, False)
        
        self.position = P
        self.isShowing = True
        self.collider = Collider(Enum["COLLIDER_TYPE"]["CIRCLE"], self.position)
        self.collider.l = radius  
        self.radius = radius
        self.type = type

    def update(self ,dt=0):
        # Handle player collections here and sound aswell, since its more streamlined.
        global SCORE
        
        self.collider.position = self.position

        # Check collision with player — but only if showing
        if self.isShowing:
            player = game.localPlayer
            if self.collider.circle_collision(self.collider, player.collider):
                # Check if player is touching TOP of the screw

                # Player must be slightly ABOVE the screw
                if abs(player.position.x - self.position.x) < 40 and abs(player.position.y - self.position.y) < 40:
                    self.isShowing = False
                    self.active = False  
                    score_particle = Item(Vector2(self.position.x, self.position.y), "SCORE_500", 30)
                    SCORE += 500
                    game.Workspace.AddChild(score_particle)
                    game.Debris.AddItem(score_particle, 1)
                    game.Workspace.RemoveChild(self)
                    
                    game.item_collect.Stop()
                    game.item_collect.Play()


    def display(self, dt=0):
        if self.isShowing:
            if self.type == 0:
                image(first_princess_pickup_item, self.position.x, self.position.y, 32, 32, 0, 0, 30, 32)
            elif self.type == 1:
                image(second_princess_pickup_item, self.position.x, self.position.y, 32, 32, 0, 0, 30, 32)
            elif self.type == 2:
                image(third_princess_pickup_item, self.position.x, self.position.y, 32, 32, 0, 0, 30, 32)


class HalfLadder(Instance):
  
    def __init__(self, P=Vector2(0,0), raycast_function=None):
        Instance.__init__(self, "Halfladder", Enum["ENUM_TYPE"]["HALF_LADDER"], True, False)
        self.position = P
        self.raycast_function = raycast_function
        self.width = 20
        self.top_pos = None
        self.bottom_pos = None
        self.height = 0
        self.rect_pos = None
        def compute_ladder_bounds():
            if self.raycast_function is None:
                return
            #The main jist of this algo is that we take the initial position that can be whenever between the two platforms, then it used the vectorray function to calculate the top edge of the ladder and the bottom part of the ladder so that later we can create a white rectangle.
            up_origin = Vector2(self.position.x, self.position.y)
            up_direction = Vector2(0, -1)
            up_intersection, up_target = self.raycast_function(Ray2(up_origin, up_direction, 10000))
            
            #if we can find the up intersection then we set the top position to a up_intersection.
            if up_intersection:
                self.top_pos = up_intersection
            
            down_origin = Vector2(self.position.x, self.position.y)
            down_dir = Vector2(0, 1)
            down_intersection, down_target = self.raycast_function(Ray2(down_origin, down_dir, 10000))
            
            #if we can find the down intersection then we set the top position to a up_intersection.
            if down_intersection:
                self.bottom_pos = down_intersection
            
            #if we can find both of the positions then we calculate the height and change the rectangle_position 
            if self.top_pos and self.bottom_pos:
                self.height = abs(self.top_pos.y - self.bottom_pos.y)
                self.rect_pos = Vector2(self.position.x - self.width/2, self.top_pos.y)
        compute_ladder_bounds()
        
    def update(self, dt):
        pass
    
    
    def display(self, dt=0):
        if self.rect_pos and self.height > 0:
            number_of_ladders = int(self.height // 32)
            if self.height % 32 > 0:
                number_of_ladders += 1
            #middle_start = number_of_ladders // 3            
            #middle_end = (number_of_ladders * 2) // 3
            
            for num in range(0, number_of_ladders):
                if num == number_of_ladders // 2:
                    pass
                else:
                    image(ladder_image, self.rect_pos.x-8, self.rect_pos.y + (num *32),32, 32, 0, 0, 32, 32)
    
class Ladder(Instance):
    
    def __init__(self, P=Vector2(0,0), raycast_function=None):
        Instance.__init__(self, "Ladder", Enum["ENUM_TYPE"]["LADDER"], True, False)
        self.position = P
        self.raycast_function = raycast_function
        self.width = 20
        self.top_pos = None
        self.bottom_pos = None
        self.height = 0
        self.rect_pos = None
        def compute_ladder_bounds():
            if self.raycast_function is None:
                return
            #The main jist of this algo is that we take the initial position that can be whenever between the two platforms, then it used the vectorray function to calculate the top edge of the ladder and the bottom part of the ladder so that later we can create a white rectangle.
            up_origin = Vector2(self.position.x, self.position.y)
            up_direction = Vector2(0, -1)
            up_intersection, up_target = self.raycast_function(Ray2(up_origin, up_direction, 10000))
            
            #if we can find the up intersection then we set the top position to a up_intersection.
            if up_intersection:
                self.top_pos = up_intersection
            
            down_origin = Vector2(self.position.x, self.position.y)
            down_dir = Vector2(0, 1)
            down_intersection, down_target = self.raycast_function(Ray2(down_origin, down_dir, 10000))
            
            #if we can find the down intersection then we set the top position to a up_intersection.
            if down_intersection:
                self.bottom_pos = down_intersection
            
            #if we can find both of the positions then we calculate the height and change the rectangle_position 
            if self.top_pos and self.bottom_pos:
                self.height = abs(self.top_pos.y - self.bottom_pos.y)
                self.rect_pos = Vector2(self.position.x - self.width/2, self.top_pos.y)
        compute_ladder_bounds()
        
    def update(self, dt):
        pass
    
    
    def display(self, dt=0):
        if self.rect_pos and self.height > 0:
            number_of_ladders = int(self.height // 32)
            if self.height % 32 > 0:
                number_of_ladders += 1
                
            for num in range(0, number_of_ladders):
                
                if game.level == 2:
                    image(ladder_yellow, self.rect_pos.x-8, self.rect_pos.y + (num *32),32, 32, 0, 0, 32, 32)
                    
                else:
                    image(ladder_image, self.rect_pos.x-8, self.rect_pos.y + (num *32),32, 32, 0, 0, 32, 32)
            
class Item(Instance):
    # A stationary object whose entire purpose is to be rendered and
    # cease to exist when collected
    
    def __init__(self, P=Vector2(0,0), type="HAMMER", radius=30):
        Instance.__init__(self, "Item", Enum["ENUM_TYPE"]["ITEM"], True, False)
        self.position =  P
        self.collider = Collider(Enum["COLLIDER_TYPE"]["CIRCLE"], self.position)
        self.radius = radius
        self.collider.l = radius  
        self.type = type
        self.state = 0
        
        self.animations = { # dictionary of Animations
            "HAMMER": Animation(hammer_item, 32, 32, RIGHT, 1),
            "OIL_BARREL": Animation(oil_barrel, 32, 32, RIGHT, 1),
            "FIRE_SMALL": Animation(fire_small, 32, 32, RIGHT, 2),
            "FIRE_BIG": Animation(fire_big, 32, 32, RIGHT, 2),
            "BARREL_STATIC": Animation(static_barrel, 32, 32, RIGHT, 1),
            "BARREL_DESTROY": Animation(barrel_destroy, 32, 32, RIGHT, 4),
            "SCORE_100": Animation(score_100, 32, 32, RIGHT, 1),
            "SCORE_500": Animation(score_500, 32, 32, RIGHT, 1),
            "SCORE_800": Animation(score_800, 32, 32, RIGHT, 1),
            "PRINCESS_SCARED": Animation(princess_scared, 32, 64, RIGHT, 2),
            "PRINCESS_IDLE": Animation(princess_idle, 32, 64, RIGHT, 1),
        }
        
        # Adjusting speed of some animations to look right
        self.animations["BARREL_DESTROY"].animation_speed = 0.25
        self.animations["PRINCESS_SCARED"].animation_speed = 0.5
    
    def display(self, dt=0):
        # Displays the animation with some custom functionality for some of these cases
        
        if self.type == "HAMMER":
            self.animations["HAMMER"].play(self.position.x, self.position.y)
            
        elif self.type == "OIL_BARREL":
            if self.state == 0:
                self.animations["FIRE_SMALL"].update(dt + 1/frameRate)
                self.animations["FIRE_SMALL"].play(self.position.x, self.position.y - 32)
                self.animations["OIL_BARREL"].play(self.position.x, self.position.y)
            else:
                self.animations["FIRE_BIG"].update(dt + 1/frameRate)
                self.animations["FIRE_BIG"].play(self.position.x, self.position.y - 32)
                self.animations["OIL_BARREL"].play(self.position.x, self.position.y)
                
        elif self.type == "BARREL_STATIC":
            self.animations["BARREL_STATIC"].play(self.position.x, self.position.y)
            
        elif self.type == "SMALL_FIRE_PARTICLE":
            self.animations["FIRE_SMALL"].update(dt + 1/frameRate)
            self.animations["FIRE_SMALL"].play(self.position.x, self.position.y)
            
        elif self.type == "BARREL_DESTROY_PARTICLE":
            self.animations["BARREL_DESTROY"].update(dt + 1/frameRate)
            self.animations["BARREL_DESTROY"].play(self.position.x, self.position.y)
            
        elif self.type == "SCORE_100" or self.type == "SCORE_500" or self.type == "SCORE_800":
            self.animations[self.type].play(self.position.x, self.position.y-16)
            
        elif self.type == "PRINCESS":
            if self.state == 1:
                if self.animations["PRINCESS_SCARED"].animation_timer > 0.45:
                    self.state = 0
                    self.animations["PRINCESS_SCARED"].animation_timer = 0
                    
                self.animations["PRINCESS_SCARED"].update(dt + 1/frameRate)
                self.animations["PRINCESS_SCARED"].play(self.position.x, self.position.y)
            else:
                self.animations["PRINCESS_IDLE"].play(self.position.x, self.position.y)
            
            
    
    def update(self, dt):
        pass
    
class Barrel(Instance): 
    # The barrels rolling around the map that destroy the player on contact,
    # and can be destroyed by a hammer for points.
    
    def __init__(self, P=Vector2(0,0)):
        # instantiates instance including initial... position
        
        Instance.__init__(self, "Barrel", Enum["ENUM_TYPE"]["BARREL"], False, True)
        
        self.position = P
        
        self.width = 20
        self.height = 20
        
        self.collider.l = 10 # diameter / 2
        
        #Temporary Variable that we use to check if the player is on the ground.
        self.on_ground = False
        self.isClimbing = False
        self.climbDirection = None
        #Consants that represent the speed of the player moving right and left, gravity forces in numbers..
        self.speed = 120
        self.jump_force  = -180
        self.climb_velocity = 40
        
        self.move_direction = LEFT
        
        self.BASE_POINT = BOARD_H

        self.animations = {
            "SIDE": Animation(barrel_brown_roll_side, 32, 32, RIGHT, 4),
            "FRONT": Animation(barrel_brown_roll_front, 32, 32, RIGHT, 2)
        }
        #self.gravity = 0.5 NO NEED, WORKSPACE HANDLES GRAVITY
        
        self.current_animation = self.animations["FRONT"]

    def update(self, dt):
        # handles physis and stuff for the barrel, aswell as destruction on reaching end with flame
        # animation
        
        if random.randint(0, 1000) > 998:
            self.climbDirection = DOWN
        
        # if reached start point, do something, like blue barrel becomes fire spirit
        if (self.position - game.startpoint).magnitude() < 50:
            fire_particle = Item(Vector2(self.position.x, self.position.y - 5), "SMALL_FIRE_PARTICLE", 30)
            game.Workspace.AddChild(fire_particle)
            game.Debris.AddItem(fire_particle, 1)
            
            self.active = False
            self.move_direction = None
        
        if self.move_direction == LEFT:
            self.velocity.x = -self.speed
        elif self.move_direction == RIGHT:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0
        
        #applying the gravity
        self.velocity.y += game.Workspace.gravity * dt * (1-self.anchored)
        #update position
        self.position.y += self.velocity.y * dt * (1-self.anchored)
        
        if self.position.x + self.velocity.x * dt < self.collider.l:
            self.position.x = self.collider.l
            self.border_reached()
            
        elif self.position.x + self.velocity.x * dt > BOARD_W - self.collider.l:
            self.position.x = BOARD_W - self.collider.l
            self.border_reached()
        else:
            self.position.x += self.velocity.x * dt * (1-self.anchored)

        # ground collision (temporary)
        if self.position.y + self.height/2 > self.BASE_POINT and not self.anchored and self.canCollide:
            self.position.y = self.BASE_POINT - self.height/2
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        self.collider.position = self.position
        
        for child in game.Workspace.GetChildren():
            # randomly decides which ladders to descend, if any and then does that
            
            if child.enum_type == Enum["ENUM_TYPE"]["LADDER"] or child.enum_type == Enum["ENUM_TYPE"]["HALF_LADDER"]:
                ladder = child
                
                top = ladder.top_pos
                bottom = ladder.bottom_pos
                
                if abs(self.position.x - top.x) <= self.collider.l:
                    
                    if bottom.y - 20 >= self.position.y >= top.y - self.collider.l-5:
                        if self.climbDirection == DOWN and not self.isClimbing:
                            self.isClimbing = True
                            self.anchored = True
                            
                        elif self.climbDirection:
                            self.position.y += self.climb_velocity * dt
                            self.velocity.y = 0

                    elif self.isClimbing and self.climbDirection == DOWN:

                        if bottom.y - 10 >= self.position.y >= bottom.y - self.collider.l-20:
                            self.isClimbing = False
                            self.anchored = False
                            self.climbDirection = None
                            
                            if self.move_direction == RIGHT:
                                self.move_direction = LEFT
                            elif self.move_direction == LEFT:
                                self.move_direction = RIGHT
                        else:
                            self.isClimbing = True
                            self.anchored = True    
                            
        self.collider.position = self.position 
        
    #helper functions that we use to change  the velocity speed of the player
    def move_left(self):
        self.velocity.x = -self.speed
    
    def move_right(self):
        self.velocity.x = self.speed
    
    def stop(self):
        self.velocity.x = 0
    
    # DEPRECATED
    def jump(self):
        #temporary jump mechanics
        if self.on_ground:
            self.velocity.y += self.jump_force
            self.on_ground = False
            
    def border_reached(self):
        # switch directions if the barrel reaches the side of the screen
        if self.move_direction == LEFT:
            self.move_direction = RIGHT
        
        else:
            if self.move_direction == RIGHT:
                self.move_direction = LEFT

    def choose_animation_state(self, dt):
        # chooses animation to display based on conditions like whether it is climbing down a ladder
        # or not
        if not self.isClimbing:
            self.current_animation = self.animations["SIDE"]
            
            if self.move_direction == LEFT:
                self.current_animation.direction = RIGHT
            else:
                self.current_animation.direction = LEFT

            return
        
        if self.isClimbing:
            self.current_animation = self.animations["FRONT"]
            self.current_animation.direction = self.move_direction

            return
    
    def display(self, dt=0):
        # display the barrel
        if GAME_STATE != 4:
            self.choose_animation_state(dt + (1/frameRate))
            self.current_animation.update(dt + (1/frameRate))
            self.current_animation.play(self.position.x, self.position.y)

        #fill(150, 75, 0)
        #circle(self.position.x, self.position.y, self.height)
        
class BlueBarrel(Instance): 
    #Same as the barrel class except it moves faster and
    # spawns in a FireSpirit if it reaches the burning oil at the start
    
    def __init__(self, P=Vector2(0,0)):
        
        Instance.__init__(self, "Barrel", Enum["ENUM_TYPE"]["BARREL"], False, True)
        
        self.position = P
        
        self.width = 20
        self.height = 20
        
        self.collider.l = 10 # diameter / 2
        
        #Temporary Variable that we use to check if the player is on the ground.
        self.on_ground = False
        self.isClimbing = False
        self.climbDirection = None
        #Consants that represent the speed of the player moving right and left, gravity forces in numbers..
        self.speed = 200
        self.jump_force  = -180
        self.climb_velocity = 60
        
        self.move_direction = LEFT
        
        self.BASE_POINT = BOARD_H

        self.animations = {
            "SIDE": Animation(barrel_blue_roll_side, 32, 32, RIGHT, 4),
            "FRONT": Animation(barrel_blue_roll_front, 32, 32, RIGHT, 2)
        }
        #self.gravity = 0.5 NO NEED, WORKSPACE HANDLES GRAVITY
        self.current_animation = self.animations["FRONT"]
        
        self.isStart = False # If the barrel is the first barrel dropped

    def update(self, dt):
        
        if self.isStart:
            if self.position.y >= BOARD_H - 32:
                self.isStart = False
                self.speed = 200
                self.anchored = False
                self.move_direction = LEFT
                
                
            elif self.position.y >= BOARD_H:
                fs = FireSpirit(Vector2(100, BOARD_H - 32))
                game.Workspace.AddChild(fs)
            else:
                self.current_animation = self.animations["FRONT"]
                self.anchored = True
                self.BASE_POINT = BOARD_H
                self.position.y += 150 * dt
                return
        
        if random.randint(0, 1000) > 998:
            self.climbDirection = DOWN
        
        # if reached start point, do something, like blue barrel becomes fire spirit
        if (self.position - game.startpoint).magnitude() < 50:
            self.active = False
            self.move_direction = None
        
        if self.move_direction == LEFT:
            self.velocity.x = -self.speed
        elif self.move_direction == RIGHT:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0
        
        #applying the gravity
        self.velocity.y += game.Workspace.gravity * dt * (1-self.anchored)
        #update position
        self.position.y += self.velocity.y * dt * (1-self.anchored)
        
        if self.position.x + self.velocity.x * dt < self.collider.l:
            self.position.x = self.collider.l
            self.border_reached()
            
        elif self.position.x + self.velocity.x * dt > BOARD_W - self.collider.l:
            self.position.x = BOARD_W - self.collider.l
            self.border_reached()
        else:
            self.position.x += self.velocity.x * dt * (1-self.anchored)

        # ground collision (temporary)
        if self.position.y + self.height/2 > self.BASE_POINT and not self.anchored:
            self.position.y = self.BASE_POINT - self.height/2
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        self.collider.position = self.position
        
        for child in game.Workspace.GetChildren():
            
            if child.enum_type == Enum["ENUM_TYPE"]["LADDER"] or child.enum_type == Enum["ENUM_TYPE"]["HALF_LADDER"]:
                ladder = child
                
                top = ladder.top_pos
                bottom = ladder.bottom_pos
                
                if abs(self.position.x - top.x) <= self.collider.l:
                    
                    if bottom.y - 20 >= self.position.y >= top.y - self.collider.l-5:
                        if self.climbDirection == DOWN and not self.isClimbing:
                            self.isClimbing = True
                            self.anchored = True
                            
                        elif self.climbDirection == DOWN:
                            self.position.y += self.climb_velocity * dt
                            self.velocity.y = 0

                    elif self.isClimbing and self.climbDirection == DOWN:
                        
                        if bottom.y - 10 >= self.position.y >= bottom.y - self.collider.l-20:
                            self.isClimbing = False
                            self.anchored = False
                            self.climbDirection = None
                            
                            if self.move_direction == RIGHT:
                                self.move_direction = LEFT
                            elif self.move_direction == LEFT:
                                self.move_direction = RIGHT
                        else:
                            self.isClimbing = True
                            self.anchored = True    
                            
        self.collider.position = self.position 
        
    #helper functions that we use to change  the velocity speed of the player
    def move_left(self):
        self.velocity.x = -self.speed
    
    def move_right(self):
        self.velocity.x = self.speed
    
    def stop(self):
        self.velocity.x = 0
    
    def jump(self):
        #temporary jump mechanics
        if self.on_ground:
            self.velocity.y += self.jump_force
            self.on_ground = False
            
    def border_reached(self):
        if self.move_direction == LEFT:
            self.move_direction = RIGHT
        
        else:
            if self.move_direction == RIGHT:
                self.move_direction = LEFT

    def choose_animation_state(self, dt):
        
        if not self.isClimbing and not self.isStart:
            self.current_animation = self.animations["SIDE"]
            
            if self.move_direction == LEFT:
                self.current_animation.direction = RIGHT
            else:
                self.current_animation.direction = LEFT

            return
        
        if self.isClimbing:
            self.current_animation = self.animations["FRONT"]
            self.current_animation.direction = self.move_direction

            return
    
    def display(self, dt=0):

        self.choose_animation_state(dt + (1/frameRate))
        self.current_animation.update(dt + (1/frameRate))
        self.current_animation.play(self.position.x, self.position.y)

        #fill(150, 75, 0)
        #circle(self.position.x, self.position.y, self.height)
        
class FireSpirit(Instance): 

    # an entity that moves erraticaly and can climb up ladders to
    # defeat the player on contact
    
    def __init__(self, P=None):
        
        Instance.__init__(self, "FireSpirit", Enum["ENUM_TYPE"]["BARREL"], False, True)
        
        self.position = P
        
        self.width = 20
        self.height = 20
        
        self.collider.l = 10 # diameter / 2
        
        #Temporary Variable that we use to check if the player is on the ground.
        self.on_ground = False
        self.climbDirection = None
        self.isClimbing = False
        #Consants that represent the speed of the player moving right and left, gravity forces in numbers..
        self.speed = 120
        self.jump_force  = -180
        self.climb_velocity = 30
        
        self.BASE_POINT = BOARD_H
        
        self.move_direction = RIGHT

        #sprite=None, imageW=32, imageH=32, direction=None, total_slices=0
        self.animations = {
            "ORANGE": Animation(fire_sprit_orange, 32, 32, RIGHT, 2)
        }

        self.current_animation = self.animations["ORANGE"]
        self.direction = RIGHT
        self.move_right()

    def choose_animation_state(self, dt):

        self.current_animation.direction = self.direction


    def update(self, dt):
        
        # randomly choose move directio and whether to climb a ladder or not

        if random.randint(0, 1000) >= 999:
            self.climbDirection = UP

        if random.randint(0, 1000) >= 997:
            if self.move_direction == LEFT:
                self.move_direction = RIGHT
                self.move_right()

            elif self.move_direction == RIGHT:
                self.move_direction = LEFT
                self.move_left()
                
        if self.move_direction == RIGHT:
            self.velocity.x = self.speed
            
        elif self.move_direction == LEFT:
            self.velocity.x = -self.speed
            
        else:
            self.velocity.x = 0
        
        #applying the gravity
        self.velocity.y += game.Workspace.gravity * dt * (1-self.anchored)
        #update position
        self.position.y += self.velocity.y * dt * (1-self.anchored)
        
        if self.position.x + self.velocity.x * dt <= self.collider.l:
            self.position.x = self.collider.l * (1-self.anchored)
            self.move_direction = RIGHT
            self.move_right()

        elif self.position.x + self.velocity.x * dt >= BOARD_W - self.collider.l:
            self.position.x = BOARD_W - self.collider.l
            self.move_direction = LEFT
            self.move_left()
        else:
            self.position.x += self.velocity.x * dt * (1-self.anchored)
        

        # ground collision (temporary)
        if self.position.y + self.height/2 > self.BASE_POINT and self.anchored == False:
            self.position.y = self.BASE_POINT - self.height/2
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        self.collider.position = self.position
        
        for child in game.Workspace.GetChildren():
            
            if child.enum_type == Enum["ENUM_TYPE"]["LADDER"] or child.enum_type == Enum["ENUM_TYPE"]["HALF_LADDER"]:
                ladder = child
                
                top = ladder.top_pos
                bottom = ladder.bottom_pos
                
                if abs(self.position.x - top.x) <= self.collider.l:

                    if bottom.y >= self.position.y >= top.y - self.collider.l - 5:

                        if self.climbDirection == UP and not self.isClimbing and abs(bottom.y - self.position.y) < self.collider.l + 5:
                            self.isClimbing = True
                            self.anchored = True
                            
                        elif self.isClimbing and self.climbDirection:
                            self.position.y -= self.climb_velocity * dt
                            self.velocity.y = 0

                    elif self.isClimbing and self.climbDirection == None:
                        
                        if top.y - self.collider.l - 5 >= self.position.y >= top.y - self.collider.l-5:
                            self.isClimbing = False
                            self.anchored = False
                            self.climbDirection = None
                            
                        else:
                            self.isClimbing = True
                            self.anchored = True
                    
                    elif self.isClimbing and not(bottom.y >= self.position.y >= top.y - self.collider.l - 5) and bottom.y >= self.position.y >= top.y - self.collider.l - 10:
                        self.isClimbing = False
                        self.anchored = False
                        self.climbDirection = None
                        
                    if bottom.y - 20 >= self.position.y >= top.y - self.collider.l-5:
                        if self.climbDirection == DOWN and not self.isClimbing:
                            self.isClimbing = True
                            self.anchored = True
                            
                        elif self.climbDirection == DOWN:
                            self.position.y += self.climb_velocity * dt
                            self.velocity.y = 0

                    elif self.isClimbing and self.climbDirection == DOWN:
                        
                        if bottom.y - 10 >= self.position.y >= bottom.y - self.collider.l-20:
                            self.isClimbing = False
                            self.anchored = False
                            self.climbDirection = None
                        else:
                            self.isClimbing = True
                            self.anchored = True

                            
        self.collider.position = self.position  

                                
        
    #helper functions that we use to change  the velocity speed of the player
    def move_left(self):
        self.velocity.x = -self.speed
        self.direction = LEFT
        self.move_direction = LEFT
    
    def move_right(self):
        self.velocity.x = self.speed
        self.direction = RIGHT
        self.move_direction = RIGHT

    def stop(self):
        self.velocity.x = 0
    
    def jump(self):
        #temporary jump mechanics
        if self.on_ground and not self.has_hammer:
            self.velocity.y += self.jump_force
            self.on_ground = False
    
    def display(self, dt=0):
        #updating the dt
        
        self.choose_animation_state(dt + (1/frameRate))
        self.current_animation.update(dt + (1/frameRate))
        self.current_animation.play(self.position.x, self.position.y)
        
class BlueSpirit(FireSpirit):
    
    def __init__(p=Vector2(0, 0)):
        
        FireSpirit.__init__(self, p)
        self.current_animation = Animation(fire_sprit_blue, 32, 32, RIGHT, 2)
        self.speed = 180
        self.climb_velocity = 50
        
#Class For The Player
class Player(Instance): 
    def __init__(self, P=None):
        
        Instance.__init__(self, "Player", Enum["ENUM_TYPE"]["PLAYER"], False, True)
        
        self.position = P
        
        self.width = 20
        self.height = 20
        
        self.collider.l = 10 # diameter / 2
        
        #Temporary Variable that we use to check if the player is on the ground.
        self.on_ground = False
        self.climbDirection = None
        self.isClimbing = False
        #Consants that represent the speed of the player moving right and left, gravity forces in numbers..
        self.speed = 240 #120
        self.jump_force  = -130
        self.climb_velocity = 60 #30
        
        self.BASE_POINT = BOARD_H # the point where the player's foot is, used in collision detection
                                  # to stop player from constantly falling down
        
        self.move_direction = LEFT
        #self.gravity = 0.5 NO NEED, WORKSPACE HANDLES GRAVITY
        
        self.has_hammer = False
        self.hammer_time = 0
        self.hammer_radius = 50

        #sprite=None, imageW=32, imageH=32, direction=None, total_slices=0
        self.animations = {
            "WALK": Animation(mario_running, 32, 32, RIGHT, 3),
            "CLIMB": Animation(mario_climbing_ladder, 32, 32, None, 2),
            "IDLE": Animation(mario_idle, 32, 32, None, 1),
            "JUMP": Animation(mario_jumping, 32, 32, RIGHT, 1),
            "HAMMER_IDLE": Animation(mario_hammer_idle, 64, 64, RIGHT, 2),
            "HAMMER_WALK": Animation(mario_hammer_running, 64, 64, RIGHT, 4),
            "DIE_RIGHT": Animation(mario_dying_right, 32, 32, None, 5),
            "DIE_LEFT": Animation(mario_dying_left, 32, 32, None, 5)
        }

        self.current_animation = self.animations["IDLE"]
        self.direction = RIGHT
        
        self.barrel_score_debounce = 0 # used to give player a score for jumping over a
                                       # barrel with a 0.5 second debounce. this tracks
                                       # elapsed time
        
        # SFX
        
        self.jump_sfx = Sound("JUMP_SFX", False) # jump sound effect

    def choose_animation_state(self, dt):
        
        if GAME_STATE == 4:
            return

        if self.has_hammer:
            if self.velocity.x == 0:
                self.current_animation = self.animations["HAMMER_IDLE"]
                self.current_animation.direction = self.direction
                
            else:
                self.current_animation = self.animations["HAMMER_WALK"]
                self.current_animation.direction = self.direction
                
            return
       
        if self.isClimbing and self.climbDirection:
            self.animations["CLIMB"].total_slices = 2
            self.current_animation = self.animations["CLIMB"]
            self.current_animation.direction = None
            return
        
        if self.isClimbing and not self.climbDirection:
            self.animations["CLIMB"].total_slices = 1
            return
       
        if not self.on_ground and abs(self.position.y - self.BASE_POINT) > (self.collider.l + 5):
            self.current_animation = self.animations["JUMP"]
            self.current_animation.direction = self.direction
            return
        
        if self.on_ground and self.velocity.x != 0 and abs(self.position.y - self.BASE_POINT) < (self.collider.l + 2):
            self.current_animation = self.animations["WALK"]
            self.current_animation.direction = self.direction
            return
        
        if self.velocity.magnitude() == 0:
            self.current_animation = self.animations["IDLE"]
            self.current_animation.direction = self.direction
            return

    def update(self, dt):
        # responsibel for calculating physics, collisions, and movement, etc.
        
        global SCORE
        
        self.barrel_score_debounce -= dt
        
        #applying the gravity
        self.velocity.y += game.Workspace.gravity * dt * (1-self.anchored)
        #update position
        self.position.y += self.velocity.y * dt * (1-self.anchored)
                    
        # if player has hammer, update hammer duration and collider accordingly
        if self.has_hammer:
            self.hammer_time -= dt
            if self.hammer_time <= 0:
                self.has_hammer = False
                self.collider.l = 10
        
        # prevents player from walking off the sides of the screen
        if self.position.x + self.velocity.x * dt < self.collider.l:
            self.position.x = self.collider.l * (1-self.anchored)
            
        elif self.position.x + self.velocity.x * dt > BOARD_W - self.collider.l:
            self.position.x = BOARD_W - self.collider.l
            
        else:
            self.position.x += self.velocity.x * dt * (1-self.anchored)
        

        # ground collision
        if self.position.y + self.height/2 > self.BASE_POINT and self.anchored == False:
            self.position.y = self.BASE_POINT - self.height/2
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        self.collider.position = self.position
        
        for child in game.Workspace.GetChildren():   
            # handles player ladder up and down mechanics.     
            
            if child.enum_type == Enum["ENUM_TYPE"]["LADDER"] and not self.has_hammer:
                ladder = child
                
                top = ladder.top_pos
                bottom = ladder.bottom_pos
                
                if abs(self.position.x - top.x) <= self.collider.l:
                    
                    moved_up = False

                    if bottom.y >= self.position.y >= top.y - self.collider.l:

                        if self.climbDirection == UP and not self.isClimbing:
                            self.isClimbing = True
                            self.anchored = True
                            
                        elif self.climbDirection == UP:
                            self.position.y -= self.climb_velocity * dt
                            moved_up = True
                            self.velocity.y = 0

                    elif self.isClimbing and self.climbDirection == None:
                        
                        if top.y - self.collider.l >= self.position.y >= top.y - self.collider.l-5:
                            self.isClimbing = False
                            self.anchored = False
                            
                        else:
                            self.isClimbing = True
                            self.anchored = True
                            
                    if bottom.y - 20 >= self.position.y >= top.y - self.collider.l-10 and not moved_up:
                        if self.climbDirection == DOWN and not self.isClimbing:
                            self.isClimbing = True
                            self.anchored = True
                            
                        elif self.climbDirection == DOWN and not moved_up:
                            self.position.y += self.climb_velocity * dt
                            self.velocity.y = 0

                    elif self.isClimbing and self.climbDirection == DOWN:
                        
                        if bottom.y - 10 >= self.position.y >= bottom.y - self.collider.l-20:
                            self.isClimbing = False
                            self.anchored = False
                            self.climbDirection = None
                            
                        else:
                            self.isClimbing = True
                            self.anchored = True
                            
            elif child.enum_type == Enum["ENUM_TYPE"]["BARREL"]:
                if (self.position - child.position).magnitude() <= self.collider.l + child.collider.l:
                    global NUM_LIVES, DID_LOSE_LIFE, GAME_STATE, PLAYER_DEATH_TIMER

                    if not DID_LOSE_LIFE:
                        #print("LIVES:",NUM_LIVES)
                        NUM_LIVES -= 1
                        DID_LOSE_LIFE = True

                        # Freeze player completely
                        self.velocity = Vector2(0, 0)
                        self.anchored = True
                        self.isClimbing = False
                        self.climbDirection = None

                        #print(self.current_animation == self.animations["DIE_RIGHT"], self.current_animation == self.animations["DIE_LEFT"])

                        if self.direction == RIGHT:
                            self.current_animation = self.animations["DIE_RIGHT"]
                            #print("Fired! r")
                        else:
                            self.current_animation = self.animations["DIE_LEFT"]
                            #print("Fired! l")

                        PLAYER_DEATH_TIMER = 1.5 
                        GAME_STATE = 4
             
                elif abs(self.position.x - child.position.x) <= 10:

                    if child.position.y - 8 >= self.position.y >= child.position.y - 64:
                        
                        if isinstance(child, FireSpirit):
                            pass

                        elif isinstance(child, Barrel) or isinstance(child, BlueBarrel):
                            
                            if self.barrel_score_debounce > 0.5:
                                pass
                            elif not self.isClimbing:
                                self.barrel_score_debounce = 1
                                SCORE += 100
                            
                                score_particle = Item(Vector2(child.position.x, child.position.y), "SCORE_100", 30)
                                game.Workspace.AddChild(score_particle)
                        
                                game.Debris.AddItem(score_particle, 1)
                                
                                game.score_give.Stop()
                                game.score_give.Play()
                            
        self.collider.position = self.position  

                                
        
    #helper functions that we use to change  the velocity speed of the player
    def move_left(self):
        self.velocity.x = -self.speed
        
        #if self.direction == RIGHT and self.has_hammer:
            #self.position.x -= 32
            #self.collider.position = self.position
        
        self.direction = LEFT
    
    def move_right(self):
        self.velocity.x = self.speed
        
        #if self.direction == LEFT and self.has_hammer:
            #self.position.x += 32
            #self.collider.position = self.position
        
        self.direction = RIGHT

    def stop(self):
        self.velocity.x = 0
    
    def jump(self):
        #temporary jump mechanics
        if self.on_ground and not self.has_hammer:
            self.jump_sfx.Halt()
            self.velocity.y += self.jump_force
            self.on_ground = False
            self.jump_sfx.Play()
    
    def display(self, dt=0):
        # displays the player with correct animation to display
        
        if self.velocity.x != 0:
            if self.velocity.x > 0:
                self.animations["WALK"].direction = RIGHT
            elif self.velocity.x < 0:
                self.animations["WALK"].direction = LEFT
                
        elif self.velocity.x == 0 and self.velocity.y == 0:
            self.animations["IDLE"].direction = self.direction
        
        self.choose_animation_state(dt + (1/frameRate))
        self.current_animation.update(dt + (1/frameRate))
            
        if self.current_animation == self.animations["HAMMER_IDLE"] or self.current_animation == self.animations["HAMMER_WALK"]:
            self.current_animation.play(self.position.x, self.position.y-17)
        else:
            self.current_animation.play(self.position.x, self.position.y)
        

#Class Platform
class Platform(Instance):
    #a platform drawn between two points.
    
    def __init__(self, P1=Vector2(0,100), P2=Vector2(BOARD_W,200), isBlue=False):
        # This class is special, as it is the only Instance handled as a Ray2
        # which means we can make platforms with finite length (modulo 16) 
        # and in nearly any direction we want.
        
        Instance.__init__(self, "Platform", Enum["ENUM_TYPE"]["PLATFORM"], True, True)
        
        self.P1 = P1
        self.P2 = P2
        
        d = P2 - P1
        
        if d.magnitude() % 16 == 0:
            self.P2 = d.unit().rmul((d.magnitude() // 16) * 16 + 16).vadd(P1)
        else:
            self.P2 = d.unit().rmul((d.magnitude() // 16) * 16 + 16).vadd(P1)
        
        self.isBlue = isBlue
        
    def update(self, dt):
        pass
    
    #The draw funtions of the platform, where from the 2 points we create 16 pixels blocks. (this funciton can be used for vertical horizotnal and diagonal platforms.)
    def display(self, dt=0):
        direction = self.P2 - self.P1;
        distance = direction.magnitude()
        unit_direction = direction.unit()

        num_tiles = int(distance // 16)

        for i in range(num_tiles):
            tile_position = unit_direction.rmul(16 * i).vadd(self.P1)
            stroke(255)         
            fill(255, 0, 0) 
            if not self.isBlue:
                image(platform_red, tile_position.x, tile_position.y, 32, 32, 0, 0, 32, 32)
            else:
                image(platform_blue, tile_position.x, tile_position.y, 32, 32, 0, 0, 32, 32)
                
class HiddenPlatform(Instance):
    # sometimes, due to lag spikes, deltaTime (dt) can be large and cause glitches.
    # HiddenPlatform is a second layer of glitch prevention placed under some platforms
    # that prevents players from falling through platforms. They function similarly to
    # regular platforms except that they are not rendered in physically, but have
    # collision detection.
    
    def __init__(self, P1=Vector2(0,100), P2=Vector2(BOARD_W,200), isBlue=False):
        
        Instance.__init__(self, "Platform", Enum["ENUM_TYPE"]["PLATFORM"], True, True)
        
        self.P1 = P1
        self.P2 = P2
        
        self.isBlue = isBlue
        
    def update(self, dt):
        pass
    
    #The draw funtions of the platform, where from the 2 points we create 15 pixels blocks. (this funciton can be used for vertical horizotnal and diagonal platforms.)
    def display(self, dt=0):
        pass

            
class GUI:
    def __init__(self):
        self.selected = 0
        self.start_menu = ["START GAME", "EXIT"]
        self.pause_menu = ["CONTINUE", "EXIT"]
        self.end_menu   = ["RETRY", "EXIT"]
        
        self.menu_sound = Sound("LOADING_SCREEN", True)

    def apply_menu_choice(self):
        global GAME_STATE
        current_menu = None

        if GAME_STATE == 0:
            current_menu = self.start_menu
        elif GAME_STATE == 2:
            current_menu = self.pause_menu
        elif GAME_STATE == 3:
            current_menu = self.end_menu

        if current_menu is None:
            return  # No menu active, do nothing

        choice = current_menu[self.selected]  # Get selected option

        # Change game state based on choice
        if choice in ("START GAME", "CONTINUE", "RETRY"):
            GAME_STATE = 1  # Enter gameplay
        elif choice == "EXIT":
            self.quit_game()

        #print("Menu choice:", choice, "| GAME_STATE now:", GAME_STATE)


    def draw_donkey_kong_animation(self):
        # Alternate every 2 seconds (~120 frames)
        if (frameCount // 120) % 2 == 0:
            image(gui_kong_idle,
                BOARD_W/2 - 96,
                BOARD_H * 0.28 - 32,
                192, 128, 0,0,192,128)
        else:
            # Show pounding animation (2 frames, each 200x128)
            frame_width = 200
            frame_height = 128
            current_frame = (frameCount // 15) % 2  # Slow toggle between 2 frames

            sx = current_frame * frame_width
            sy = 0

            image(gui_kong_pounding,
                BOARD_W/2 - 100,
                BOARD_H * 0.28 - 32,
                200, 128,
                sx, sy,
                sx + frame_width-8, sy + frame_height)



    # Menu Drawer
    def draw_menu(self, items, base_y):
        spacing = 55
        textFont(menu_font)

        for i, option in enumerate(items):
            x = BOARD_W/2
            y = base_y + i*spacing

            if i == self.selected:
                fill(255,0,0)
            else:
                fill(255)

            text(option, x +1, y)

            # if i == self.selected:
            #     tw = textWidth(option)
            #     image(gui_mario_hammer_icon,
            #         x - tw/2 - 60,
            #         y - 64,
            #         64, 64)

    # --- START SCREEN ---
    def draw_start(self):
        background(0)
        textFont(title_font)
        fill(0,150,255)

        title = "DONKEY KONG"
        text(title, BOARD_W/2 +1, BOARD_H * 0.15)

        self.draw_donkey_kong_animation()
        self.draw_menu(self.start_menu, BOARD_H * 0.60)

    # --- PAUSE SCREEN ---
    def draw_pause(self):
        background(0)
        textFont(title_font)
        fill(255)

        pause_text = "PAUSED"
        text(pause_text, BOARD_W/2 +1, BOARD_H * 0.25)

        self.draw_menu(self.pause_menu, BOARD_H*0.55)


    # --- END SCREEN ---
    def draw_end(self):
        background(0)
        
        gameover = "GAME OVER"

        if DID_WIN:
            image(gui_princess_icon,
                BOARD_W/2 - 36,
                BOARD_H*0.18 - 64,
                72, 128, 0, 0, 72-8, 128)
            
            gameover = "VICTORY"
            self.end_menu = ["EXIT"]
        else:
            image(gui_mario_angel_icon,
                BOARD_W/2 - 64,
                BOARD_H*0.18 - 64,
                128, 128)

        textFont(title_font)
        fill(255)

        
        text(gameover, BOARD_W/2 +1, BOARD_H*0.45)

        textFont(menu_font)

        score_text = "FINAL SCORE " + str(SCORE)
        text(score_text, BOARD_W/2 +1, BOARD_H*0.58)

        self.draw_menu(self.end_menu, BOARD_H*0.75)

    def handle_selection(self):
        global GAME_STATE, NUM_LIVES
        
        current_menu = None      
        if GAME_STATE == 0:
            current_menu = self.start_menu
        elif GAME_STATE == 2:
            current_menu = self.pause_menu
        elif GAME_STATE == 3:
            current_menu = self.end_menu
      
        if current_menu is not None:
            choice = current_menu[self.selected]
            
            #print(choice)
            if choice == "START GAME" or choice == "CONTINUE":
                GAME_STATE = 1
            elif choice == "RETRY":
                #DID_LOSE_LIFE = False
                NUM_LIVES = 2
                
                GAME_STATE = 1
                game.level = 1
                reset_level()
                
            elif choice == "EXIT":
                self.quit_game()
        else:
            #print("  WARNING: current_menu is None for GAME_STATE:", GAME_STATE)
            pass

    def draw_hud(self, score, lives):
        textFont(hud_font)
        fill(255)
        textAlign(RIGHT, TOP)

        text("SCORE ", BOARD_W - 10, 20)
        text(str(score).zfill(6), BOARD_W, 40)
        text("LIVES ", BOARD_W - 10, 60)
        text(str(lives).zfill(2), BOARD_W, 80)
        
        textAlign(CENTER, BASELINE)

    def menu_length(self):
        if GAME_STATE == 0:
            return len(self.start_menu)
        if GAME_STATE == 2:
            return len(self.pause_menu)
        if GAME_STATE == 3:
            return len(self.end_menu)
        return 0

    def quit_game(self):
        try:
            for instance in game.Workspace.GetChildren():
                game.Workspace.RemoveChild(instance)
        except:
            pass
            
        try:
            del game
        except:
            pass
            
        try:
            for i in GLOBAL_SOUNDS.values():
                del i
        except:
            pass
            
        finally:
            try:
                del GLOBAL_SOUNDS
                del audio_player
                
            except:
                pass
            
        exit()

    def display(self):

        if GAME_STATE == 0:
            self.draw_start()
        elif GAME_STATE == 2:
            self.draw_pause()
        elif GAME_STATE == 3:
            self.draw_end()
                            
class Game:
    # The class that pipelines processes and handles the entire game's functionality.
    
    def __init__(self):
        
        self.Workspace = Workspace(200) # new Workspace
        self.Debris = Debris(self.Workspace) # new DebrisService
        
        self.__idle_threads = {} # NOUSE
        self.__running_threads = {} # NOUSE
        
        self._PhysicsPipelineRunning = False # Protected flag for whether physics pipeline is running or not
        self._RenderPipelineRunning = False # Protected flag for whether render pipeline is running or not
        
        self.localPlayer = Player(Vector2(100, 550)) # the player.
        self.localPlayer.collider.collider_aura = 10
        
        self.Workspace.AddChild(self.localPlayer) # adds player to workspace manually
        
        self.startpoint = Vector2(10, BOARD_H-50) # also used to destroy barrels when they reach the start
        
        self.barrel_spawn_interval = 4
        self.barrel_spawn_time = 0
        
        self.blue_barrel_chance = 0.2 # Probability of KONG in spawning a blue barrel instead of regular barrel
        
        self.level = 1 # The current level of the game
        
        self.animations = {
            "DONKEY_KONG_IDLE": Animation(donkey_idle, 96, 64, RIGHT, 1),
            "DONKEY_KONG_BARREL_DROP": Animation(donkey_barrel_throw, 96, 64, RIGHT, 3),
            "DONKEY_KONG_BROWN_BARREL_DROP": Animation(donkey_brown_barrel_drop, 96, 64, RIGHT, 3),
            "DONKEY_KONG_BLUE_BARREL_DROP": Animation(donkey_blue_barrel_drop, 96, 64, RIGHT, 3),
            "DONKEY_KONG_POUNDING": Animation(kong_pounding, 96, 64, RIGHT, 2),
            
            "DONKEY_KONG_CLIMBING": Animation(donkey_climbing_ladder, 96, 80, RIGHT, 4),
            "DONKEY_KONG_DYING": Animation(donkey_dying, 96, 64, RIGHT, 3),
            
            "HEART": Animation(heart_rescaled, 32, 32, RIGHT, 1),
            "BROKEN_HEART": Animation(broken_heart, 32, 32, RIGHT, 1)
        }
        
        # Adjust speeds of the animations so they dont look weird
        self.animations["DONKEY_KONG_BARREL_DROP"].animation_speed = 1.5
        self.animations["DONKEY_KONG_BROWN_BARREL_DROP"].animation_speed = 1.5
        self.animations["DONKEY_KONG_BLUE_BARREL_DROP"].animation_speed = 1.5
        self.animations["DONKEY_KONG_POUNDING"].animation_speed = 1
        
        self.current_donkey_animation = self.animations["DONKEY_KONG_IDLE"]
        
        self.new_barrel_type = None
        self.new_barrel_obj = None
        self.barrel_threshold_medium = 5
        self.barrel_threshold_insane = 10
        
        self.burnt_barrels = 0
        
        self.princess = Item(Vector2(240, 43), "PRINCESS", 30) # princess handled as an item as she has
                                                               # limited in-game functionality.
        self.Workspace.AddChild(self.princess)
        
        self.kong_position = Vector2(100, 100)
        self.kong_animation_timer = 0
        
        self.timekeeper = 0 # keeps time for transitions like kong leaving a level and the final death animation of kong
        self.transition_occuring = False
        
        self.last_spirit_spawn = 0
        self.fire_spirit_count = 0
        
        # SFX
        self.menu_sound = Sound("LOADING_SCREEN", True)
        self.lvl1 = Sound("BACKGROUND_LEVEL_1", True)
        self.lvl2 = Sound("BACKGROUND_LEVEL_2", True)
        
        self.item_collect = Sound("ITEM_COLLECT", False)
        self.score_give = Sound("SCORE_GIVE", False)
        
        self.lvl2_end = Sound("LEVEL_2_END", False)
        
    def Level1ExitAnim(self, dt):
        global LEVEL
        # the animation of Kong grabbing Princess
        # and moving to level 2
        
        self.transition_occuring = True
        
        self.timekeeper += dt
        
        self.lvl1.Stop()
        
        self.current_donkey_animation = self.animations["DONKEY_KONG_IDLE"]
        
        if self.timekeeper < 3:
            self.animations["HEART"].play(300, 30)
        elif self.timekeeper < 6:
        
            self.current_donkey_animation = self.animations["DONKEY_KONG_CLIMBING"]
            
            self.animations["BROKEN_HEART"].play(300, 30)
            
            self.princess.position = Vector2(1000, 1000)
            self.kong_position = Vector2(197, self.kong_position.y - 50*dt)
            
        else:
            
            LEVEL = 2
            game.localPlayer.position = Vector2(1000, 1000)
            reset_level()
            self.timekeeper = 0
            self.transition_occuring = False
        
            
    def Level2ExitAnim(self, dt):
        # the animation of kong falling to his death
        global GAME_STATE, DID_WIN
        
        self.transition_occuring = True
        
        self.timekeeper += dt
        
        if self.lvl2.IsPlaying:
            self.lvl2.Halt()
        
        if self.timekeeper < 3:
            self.current_donkey_animation = self.animations["DONKEY_KONG_POUNDING"]
        elif self.timekeeper < 5:
        
            self.current_donkey_animation = self.animations["DONKEY_KONG_IDLE"]
            
            self.Workspace.GetChild(5).P1.y = BOARD_H - 32
            self.Workspace.GetChild(5).P2.y = BOARD_H - 32
            
            self.Workspace.GetChild(11).P1.y = BOARD_H - 16*3
            self.Workspace.GetChild(11).P2.y = BOARD_H - 16*3
            
            self.Workspace.GetChild(17).P1.y = BOARD_H - 16*4
            self.Workspace.GetChild(17).P2.y = BOARD_H - 16*4
            
            self.Workspace.GetChild(23).P1.y = BOARD_H - 16*5
            self.Workspace.GetChild(23).P2.y = BOARD_H - 16*5
            
            if self.Workspace.GetChild(36):
                self.Workspace.RemoveChild(self.Workspace.GetChild(36))
                self.Workspace.RemoveChild(self.Workspace.GetChild(39))
                self.Workspace.RemoveChild(self.Workspace.GetChild(40))
                
                self.Workspace.RemoveChild(self.Workspace.GetChild(43))
                self.Workspace.RemoveChild(self.Workspace.GetChild(46))
                self.Workspace.RemoveChild(self.Workspace.GetChild(47))
                
            for child in game.Workspace.GetChildren():
                
                if child.enum_type == Enum["ENUM_TYPE"]["BARREL"] or child.enum_type == Enum["ENUM_TYPE"]["ITEM"] and child.type != "PRINCESS":
                    game.Workspace.RemoveChild(child)
        
        elif self.kong_position.y < BOARD_H - 112:
            
            if not self.lvl2_end.IsPlaying:
                self.lvl2_end.Play()
            
            self.current_donkey_animation = self.animations["DONKEY_KONG_DYING"]
            self.princess.position = Vector2(300, 118)
            
            if self.kong_position.y >= BOARD_H - 112:
                self.kong_position = Vector2(self.kong_position.x, BOARD_H - 112)
                
            else:
                self.kong_position = Vector2(self.kong_position.x, self.kong_position.y + 100*dt)
                
        elif self.timekeeper < 11:
            self.Workspace.GetChild(27).P1.y = BOARD_H - 16 - 96*4
            self.Workspace.GetChild(27).P2.y = BOARD_H - 16 - 96*4
            
            #print(BOARD_H - 16 - 96*4 - 28)
            self.princess.position = Vector2(300, BOARD_H - 16 - 96*4 - 28)
            
            self.localPlayer.position.x = 380
            self.localPlayer.position.y = BOARD_H - 16 - 96*4 - 16
            
            self.localPlayer.direction = LEFT
            
            self.animations["HEART"].play(340, 200)
            
        else:
            GAME_STATE = 3
            DID_WIN = True
    
    def handle_player_death(self, dt):
        global GAME_STATE, PLAYER_DEATH_TIMER, DID_LOSE_LIFE, NUM_LIVES, SCORE

        SCORE = 0
        fixed_dt = 1.0 / 60.0
        
        #ANIMATION PART
        anim = self.localPlayer.current_animation
        anim.update(fixed_dt)
        anim.play(self.localPlayer.position.x, self.localPlayer.position.y)
        

        # Count down timer with real dt
        PLAYER_DEATH_TIMER -= dt
        #print("Is this even called", PLAYER_DEATH_TIMER)
        if PLAYER_DEATH_TIMER <= 0:
            DID_LOSE_LIFE = False
            #print("calling broo")
           
            if NUM_LIVES <= 0:
                GAME_STATE = 3
                return
            
            GAME_STATE = 1
            reset_level()
            
    def getScrewCount(self):
        # for level 2, returns the number of screws that are
        # currently in Workspace
        
        count = 0
        
        for child in game.Workspace.GetChildren():
                
            if child.enum_type == Enum["ENUM_TYPE"]["SCREW"]:
                count += 1
        
        return count  
    
    # DEPRECATED
    def getFireSpiritCount(self):
        # for level 2, returns the number of FireSpirits 
        # that are currently in Workspace
        
        count = 0
        
        for child in game.Workspace.GetChildren():
                
            if child.name == "FireSpirit":
                count += 1
        
        return count  

    # WARNING: HERE BE PIPELINES!
    def PreSimulation(self, dt):
        # Preproccesing for physics simulation
        
        if self.burnt_barrels >= self.barrel_threshold_medium:
            self.barrel_spawn_interval = 3
            
            game.oil_barrel_item.state = 1
            
            if self.burnt_barrels >= self.barrel_threshold_insane:
                self.barrel_spawn_interval = 2.2
                self.blue_barrel_chance = 0.35
                
                game.oil_barrel_item.animations["FIRE_BIG"].animation_speed = 0.15
        
        
        if self.level == 2 and self.fire_spirit_count < 5 and not game.transition_occuring:
            self.last_spirit_spawn -= (dt)
            if self.last_spirit_spawn <= 0:
                self.fire_spirit_count += 1
                self.last_spirit_spawn = 3
                fs = FireSpirit(self.kong_position)
                game.Workspace.AddChild(fs)
        pass
        
    def Simulation(self, dt):
        # the actual physics and core mechanics processing
        
        global SCORE
        
        if GAME_STATE != 1 and GAME_STATE != 4:
            return
        
        # Iterate through objects in Game.Workspace and do the honors
        collision_detected = True
        updated_instances = {}
        
        self.Debris.update(dt)       
        
        if GAME_STATE == 4:
            game.handle_player_death(time.time() - Timestamp)
            return
        
        if self.transition_occuring:
            return
        
        for i in self.Workspace.GetChildren():
            if True:
                if i.enum_type == Enum["ENUM_TYPE"]["PLAYER"] or i.enum_type == Enum["ENUM_TYPE"]["BARREL"]:
                    # update the BASE_POINT for every object affected by platforms
                    origin = Vector2(i.position.x, i.position.y + i.collider.l/2)
                    direction = Vector2(0, 1)

                    intersection, target = self.Workspace.Raycast(Ray2(origin, direction, 10000))

                    if intersection:
                        i.BASE_POINT = intersection.y  - i.collider.collider_aura/2
                    
                i.update(dt) # call local update method for instance 'i'
                
                if i.enum_type == Enum["ENUM_TYPE"]["ITEM"]:
                    # player collected an item that is a hammer.
                    if i.collider.circle_collision(game.localPlayer.collider, i.collider):
                        #print("PLAYER PICKED", i.type)

                        if i.type == "HAMMER" and not game.localPlayer.has_hammer:
                            game.localPlayer.has_hammer = True
                            game.localPlayer.hammer_time = 9
                            
                            self.item_collect.Stop()
                            self.item_collect.Play()
                            #game.localPlayer.collider.l = game.localPlayer.hammer_radius
                            
                            
                        
                            self.Workspace.RemoveChild(i)
                if game.localPlayer.has_hammer and i.enum_type == Enum["ENUM_TYPE"]["BARREL"]:
                    if i.collider.circle_collision(Collider(Enum["COLLIDER_TYPE"]["CIRCLE"], game.localPlayer.position, game.localPlayer.hammer_radius), i.collider):
                        # give points when player defeats Barrel or BlueBarrel with hammer
                        
                        if isinstance(i, Barrel) or isinstance(i, BlueBarrel):
                            SCORE += 500
                        
                            destroy_particle = Item(i.position, "BARREL_DESTROY_PARTICLE", 30)
                            self.Workspace.AddChild(destroy_particle)
                        
                            self.Debris.AddItem(destroy_particle, 0.42)
                        
                            score_particle = Item(i.position, "SCORE_500", 30)
                            self.Workspace.AddChild(score_particle)
                        
                            self.Debris.AddItem(score_particle, 1)
                        
                            self.Workspace.RemoveChild(i)
                            
                            self.score_give.Stop()
                            self.score_give.Play()
                        
                        elif isinstance(i, FireSpirit):
                            # give points when player defeats FireSpirit with hammer
                            
                            SCORE += 800
                        
                            destroy_particle = Item(i.position, "BARREL_DESTROY_PARTICLE", 30)
                            self.Workspace.AddChild(destroy_particle)
                        
                            self.Debris.AddItem(destroy_particle, 0.42)
                        
                            score_particle = Item(i.position, "SCORE_800", 30)
                            self.Workspace.AddChild(score_particle)
                        
                            self.Debris.AddItem(score_particle, 1)
                        
                            self.Workspace.RemoveChild(i)
                            
                            self.fire_spirit_count -= 1
                            
                            self.score_give.Stop()
                            self.score_give.Play()
                            
        if game.localPlayer.position.x <=225 and game.localPlayer.position.y <= 130:
            game.localPlayer.position.x = 225
                                                        
        
    def PostSimulation(self, dt):
        # PostProcessing for physics, garbage collection and debris clearing (via Debris service)
        
        for i in self.Workspace.GetChildren():
            if i.active == False:
                
                if isinstance(i, BlueBarrel):
                    new_spirit = FireSpirit(i.position)
                    new_spirit.direction = RIGHT
                    new_spirit.move_direction = RIGHT
                    
                    self.burnt_barrels += 1
                    self.Workspace.AddChild(new_spirit)
                    
                elif isinstance(i, Barrel):
                    self.burnt_barrels += 1
                    
                self.Workspace.RemoveChild(i)
        pass
        
    def PreRender(self, dt):
        # Preprocessing for the frame to render, like updating animaton states, etc..
        
        background(0)
        
        if self.transition_occuring:
            return
       
        if random.randint(0, 1000) <= 2:
            self.princess.state = 1
        
        self.barrel_spawn_time += dt
        if self.barrel_spawn_time >= self.barrel_spawn_interval and self.level == 1:
            
            
            if not self.new_barrel_type:
                if random.randint(1, 100) <= 100*self.blue_barrel_chance:
                    self.new_barrel_type = "BLUE"
                    self.new_barrel_obj = BlueBarrel(Vector2(160, 116))
                else:
                    self.new_barrel_type = "BROWN"
                    self.new_barrel_obj = Barrel(Vector2(160, 116))
                    
            
            if self.new_barrel_type == "BLUE":
                self.current_donkey_animation = self.animations["DONKEY_KONG_BLUE_BARREL_DROP"]
                
            else:
                self.current_donkey_animation = self.animations["DONKEY_KONG_BROWN_BARREL_DROP"]
                
            if self.current_donkey_animation.slice == 2 and self.new_barrel_obj:
                self.new_barrel_obj.move_direction = RIGHT
                game.Workspace.AddChild(self.new_barrel_obj)
                self.new_barrel_obj = None
                
            
            
            if self.current_donkey_animation.slice == 2 and self.current_donkey_animation.animation_timer >= self.current_donkey_animation.animation_speed - 0.05:
                self.barrel_spawn_time = 0
                self.current_donkey_animation.slice = 0
                self.current_donkey_animation.animation_timer = 0
                self.current_donkey_animation = self.animations["DONKEY_KONG_IDLE"]
                
                self.new_barrel_type = None
                
                
        else:
            self.current_donkey_animation = self.animations["DONKEY_KONG_IDLE"]
            
        # PRINCESS & KONG DISPLAYS
        
        if self.level == 2:
            self.princess.position = Vector2(300, 118)
            
            self.kong_position = Vector2(280, 208)
            
            if (frameCount // 120) % 2 == 0:
                self.current_donkey_animation = self.animations["DONKEY_KONG_IDLE"]
                self.animations["DONKEY_KONG_POUNDING"].slice = 0
                self.animations["DONKEY_KONG_POUNDING"].animation_timer = 0
            else:
                # Show pounding animation (2 frames, each 200x128)
                self.current_donkey_animation = self.animations["DONKEY_KONG_POUNDING"]
                
        
    def Render(self, dt):
        # Iterate through objects in Game.Workspace and do the honors
            
        if GAME_STATE == 0 or GAME_STATE == 2 or GAME_STATE == 3:
            if not self.menu_sound.IsPlaying:
                self.menu_sound.Play()
                
        else:
            self.menu_sound.Halt()
            
        if GAME_STATE == 1 or GAME_STATE == 4 and not game.localPlayer.has_hammer:
            
            if game.level == 1:
                if not self.lvl1.IsPlaying:
                    self.lvl2.Halt()
                    self.lvl1.Play()
                
            else:
                if not self.lvl2.IsPlaying and not self.transition_occuring:
                    self.lvl1.Halt()
                    self.lvl2.Play()
                
        else:
            self.lvl1.Halt()
            self.lvl2.Halt()
        
        if GAME_STATE != 1 and GAME_STATE != 4:
            gui.display()
            return
            pass
       
        if GAME_STATE == 1 or GAME_STATE == 4:
            gui.draw_hud(SCORE, NUM_LIVES)
            
            
            pass
        
        for i in self.Workspace.GetChildren():
            if not i.enum_type == Enum["ENUM_TYPE"]["PLAYER"]:
                i.display(dt)
                #self.__running_threads[i.objectId] = threading.Thread(target = i.display, args = (dt))
                #self.__running_threads[i.objectId].start()
            
        self.current_donkey_animation.update(dt + 1/frameRate)
        self.current_donkey_animation.play(self.kong_position.x, self.kong_position.y)
        
        self.localPlayer.display(dt)
        
        if game.level == 1 and 346 >= game.localPlayer.position.x >= 230 and game.localPlayer.position.y <= 70:
            self.Level1ExitAnim(dt)
            return
        
        if game.level == 2 and game.getScrewCount() <= 0:
            self.Level2ExitAnim(dt)
            return
        
        #self.__running_threads[self.localPlayer.objectId] = threading.Thread(target = self.localPlayer.display, args = (dt))
        #self.__running_threads[self.localPlayer.objectId].start()
        
    def PostRender(self, dt):
        # Post processing after frame has been drawn. remove all garbage, etc.
        
        #for i in self.Workspace.GetChildren():
            #if self.__running_threads.get(i.objectId, False):
                #try:
                    #self.__running_threads[i.objectId].join()
                    #del self.__running_threads[i.objectId]
                #except:
                    #print("CRITICAL ERROR")
            
        self._RenderPipelineRunning = False

#Creating the classes for the game and interfaces.
game = Game()
gui = GUI()

# build the level and its objects on demand with these methods
def assemble_level_1():
    
    game.level = 1
    
    platforms = [
        Platform(Vector2(0-16, BOARD_H-16), Vector2(200, BOARD_H-16)),
        Platform(Vector2(208, BOARD_H - 16), Vector2(BOARD_W+32, BOARD_H - 16*2)),
        
        Platform(Vector2(0-16, BOARD_H - 16*6-32), Vector2(BOARD_W - 16*2-32, BOARD_H - 16*5-32)),    
        
        Platform(Vector2(16*2+32, BOARD_H - 16*8.7 - 32*2), Vector2(BOARD_W+32, BOARD_H - 16*10 -32*2)),
        
        Platform(Vector2(0-16, BOARD_H - 16*14.2 - 32*3), Vector2(BOARD_W-16*2-32, BOARD_H - 16*13 -32*3)),
        
        Platform(Vector2(16*2+32, BOARD_H - 16*16.9 - 32*4), Vector2(BOARD_W+32, BOARD_H - 16*18.3 -32*4)),
        
        Platform(Vector2(208, 132), Vector2(BOARD_W-16*2-32, BOARD_H - 16*21.5 -32*5)),
        Platform(Vector2(0-16, 132), Vector2(200, 132)),
        
        Platform(Vector2(230, 70), Vector2(346, 70)),
        
        Platform(Vector2(-16, -320), Vector2(BOARD_W+16, -320))
    ]
    start_barrel = BlueBarrel(Vector2(100, 100))
    start_barrel.speed = 0
    start_barrel.canCollide = False
    start_barrel.isStart = True

    Obstacles = [
        #Barrel(Vector2(100, 0)),
        start_barrel,
        #FireSpirit(Vector2(100, 0))
    ]

    for p in platforms:
        game.Workspace.AddChild(p)
        
        p.collider.position.origin = p.P1
        p.collider.position.direction = (p.P2 - p.P1).unit()
        p.collider.position.magnitude = (p.P2 - p.P1).magnitude()
        
    for b in Obstacles:
        game.Workspace.AddChild(b)
        

    Ladders = [
        HalfLadder(Vector2(180, BOARD_H - 100), game.Workspace.Raycast),
        Ladder(Vector2(400, BOARD_H - 100), game.Workspace.Raycast),
        
        Ladder(Vector2(250, BOARD_H - 200), game.Workspace.Raycast),
        Ladder(Vector2(100, BOARD_H - 200), game.Workspace.Raycast),
        
        HalfLadder(Vector2(175, BOARD_H - 300), game.Workspace.Raycast),
        Ladder(Vector2(300, BOARD_H - 300), game.Workspace.Raycast),
        Ladder(Vector2(475, BOARD_H - 300), game.Workspace.Raycast),
        
        HalfLadder(Vector2(400, BOARD_H - 400), game.Workspace.Raycast),
        Ladder(Vector2(225, BOARD_H - 400), game.Workspace.Raycast),
        Ladder(Vector2(100, BOARD_H - 350), game.Workspace.Raycast),
        
        HalfLadder(Vector2(270, BOARD_H - 500), game.Workspace.Raycast),
        Ladder(Vector2(450, BOARD_H - 500), game.Workspace.Raycast),
        
        Ladder(Vector2(325, BOARD_H - 510), game.Workspace.Raycast),
        HalfLadder(Vector2(214, 0), game.Workspace.Raycast),
        HalfLadder(Vector2(180, 0), game.Workspace.Raycast),
    ]

    for l in Ladders:
        game.Workspace.AddChild(l)
        

    hammer1 = Item(Vector2(50, 190), "HAMMER", 10)
    game.Workspace.AddChild(hammer1)

    hammer2 = Item(Vector2(400, BOARD_H-180), "HAMMER", 10)
    game.Workspace.AddChild(hammer2)

    start_p = platforms[0]    
    game.oil_barrel_item = Item(Vector2((start_p.P1.x + 40), start_p.P1.y - 16), "OIL_BARREL", 30)
    game.Workspace.AddChild(game.oil_barrel_item)

    static_barrels = [
        Item(Vector2(16, 116), "BARREL_STATIC", 30),
        Item(Vector2(16, 84), "BARREL_STATIC", 30),
        Item(Vector2(42, 116), "BARREL_STATIC", 30),
        Item(Vector2(42, 84), "BARREL_STATIC", 30) 
    ]

    for sb in static_barrels:
        game.Workspace.AddChild(sb)
        
def assemble_level_2():
    
    game.level = 2
    
    platforms = [
        Platform(Vector2(0-16, BOARD_H-16), Vector2(BOARD_W+16, BOARD_H-16), True),

        Platform(Vector2(8, BOARD_H - 16-96), Vector2(120, BOARD_H - 16-96), True),
        HiddenPlatform(Vector2(16, BOARD_H - 16-96+1), Vector2(128+32, BOARD_H - 16-96+1)),
        Platform(Vector2(120 + 48, BOARD_H - 16-96), Vector2(384 - 24, BOARD_H - 16-96), True),
        HiddenPlatform(Vector2(128 + 48, BOARD_H - 16-96+1), Vector2(384+8, BOARD_H - 16-96+1)),
        Platform(Vector2(408, BOARD_H - 16-96), Vector2(496+24, BOARD_H - 16-96), True),
        HiddenPlatform(Vector2(408, BOARD_H - 16-96+1), Vector2(504+48, BOARD_H - 16-96+1)),
        
        Platform(Vector2(8+32, BOARD_H - 16-96*2), Vector2(120, BOARD_H - 16-96*2), True),
        HiddenPlatform(Vector2(16+32, BOARD_H - 16-96*2+1), Vector2(128+32, BOARD_H - 16-96*2+1)),
        Platform(Vector2(120 + 48, BOARD_H - 16-96*2), Vector2(384 - 24, BOARD_H - 16-96*2), True),
        HiddenPlatform(Vector2(128 + 48, BOARD_H - 16-96*2+1), Vector2(384+8, BOARD_H - 16-96*2+1)),
        Platform(Vector2(408, BOARD_H - 16-96*2), Vector2(496-8, BOARD_H - 16-96*2), True),
        HiddenPlatform(Vector2(408, BOARD_H - 16-96*2+1), Vector2(504+16, BOARD_H - 16-96*2+1)),
        
        Platform(Vector2(8+64, BOARD_H - 16-96*3), Vector2(120, BOARD_H - 16-96*3), True),
        HiddenPlatform(Vector2(16+64, BOARD_H - 16-96*3+1), Vector2(128+32, BOARD_H - 16-96*3+1)),
        Platform(Vector2(120 + 48, BOARD_H - 16-96*3), Vector2(384 - 24, BOARD_H - 16-96*3), True),
        HiddenPlatform(Vector2(128 + 48, BOARD_H - 16-96*3+1), Vector2(384+8, BOARD_H - 16-96*3+1)),
        Platform(Vector2(408, BOARD_H - 16-96*3), Vector2(496-40, BOARD_H - 16-96*3), True),
        HiddenPlatform(Vector2(408, BOARD_H - 16-96*3+1), Vector2(504-16, BOARD_H - 16-96*3+1)),
        
        Platform(Vector2(8+96, BOARD_H - 16-96*4), Vector2(120, BOARD_H - 16-96*4), True),
        HiddenPlatform(Vector2(16+96, BOARD_H - 16-96*4+1), Vector2(128+32, BOARD_H - 16-96*4+1)),
        Platform(Vector2(120 + 48, BOARD_H - 16-96*4), Vector2(384 - 24, BOARD_H - 16-96*4), True),
        HiddenPlatform(Vector2(128 + 48, BOARD_H - 16-96*4+1), Vector2(384+8, BOARD_H - 16-96*4+1)),
        Platform(Vector2(408, BOARD_H - 16-96*4), Vector2(496-72, BOARD_H - 16-96*4), True),
        HiddenPlatform(Vector2(408, BOARD_H - 16-96*4+1), Vector2(504-48, BOARD_H - 16-96*4+1)),
        
        Platform(Vector2(120 + 32, BOARD_H - 16-96*5), Vector2(384 - 8, BOARD_H - 16-96*5), True),
        HiddenPlatform(Vector2(128 + 48, BOARD_H - 16-96*4+1), Vector2(384+8, BOARD_H - 16-96*4+1)),
        
        Platform(Vector2(-16, -320), Vector2(BOARD_W+16, -320), True)
    ]

    Obstacles = [
        FireSpirit(Vector2(100, 350)),
        FireSpirit(Vector2(150, 350)),
        FireSpirit(Vector2(200, 350)),
        FireSpirit(Vector2(250, 350)),
        FireSpirit(Vector2(300, 350))
    ]

    for p in platforms:
        game.Workspace.AddChild(p)
        
        p.collider.position.origin = p.P1
        p.collider.position.direction = (p.P2 - p.P1).unit()
        p.collider.position.magnitude = (p.P2 - p.P1).magnitude()
        
        
    for b in Obstacles:
        game.Workspace.AddChild(b)
        
    game.fire_spirit_count = 5
        

    Ladders = [
        Ladder(Vector2(32-8, BOARD_H - 100), game.Workspace.Raycast),
        Ladder(Vector2(300, BOARD_H - 100), game.Workspace.Raycast),
        Ladder(Vector2(BOARD_W-36+16, BOARD_H - 100), game.Workspace.Raycast),
        
        Ladder(Vector2(32*2-8, BOARD_H - 200), game.Workspace.Raycast),
        Ladder(Vector2(200, BOARD_H - 200), game.Workspace.Raycast),
        Ladder(Vector2(364, BOARD_H - 200), game.Workspace.Raycast),
        Ladder(Vector2(BOARD_W-32*2+4+8, BOARD_H - 200), game.Workspace.Raycast),
        
        Ladder(Vector2(88, BOARD_H - 300), game.Workspace.Raycast),
        Ladder(Vector2(300, BOARD_H - 300), game.Workspace.Raycast),
        Ladder(Vector2(BOARD_W-32*3+12, BOARD_H - 300), game.Workspace.Raycast),
        
        Ladder(Vector2(32*4-8, BOARD_H - 380), game.Workspace.Raycast),
        Ladder(Vector2(200, BOARD_H - 380), game.Workspace.Raycast),
        Ladder(Vector2(364, BOARD_H - 380), game.Workspace.Raycast),
        Ladder(Vector2(BOARD_W-32*4+4+8, BOARD_H - 380), game.Workspace.Raycast),
    ]

    for l in Ladders:
        game.Workspace.AddChild(l)
        
    #adding testing screws
    screws = [
        Screw(Vector2(148, BOARD_H-36-96)),
        Screw(Vector2(400-12, BOARD_H-36-96)),
        
        Screw(Vector2(148, BOARD_H-36-96*2)),
        Screw(Vector2(400-12, BOARD_H-36-96*2)),
        
        Screw(Vector2(148, BOARD_H-36-96*3)),
        Screw(Vector2(400-12, BOARD_H-36-96*3)),
        
        Screw(Vector2(148, BOARD_H-36-96*4)),
        Screw(Vector2(400-12, BOARD_H-36-96*4))
    ]
    
    for new_screw in screws:
        game.Workspace.AddChild(new_screw)

    hammer1 = Item(Vector2(280, 470), "HAMMER", 10)
    game.Workspace.AddChild(hammer1)

    hammer2 = Item(Vector2(280, 275), "HAMMER", 10)
    game.Workspace.AddChild(hammer2)
    
    princes_pickup_1 = PrincessPickup(Vector2(460, BOARD_H-96-46), 32, 0)
    game.Workspace.AddChild(princes_pickup_1)

    princes_pickup_2 = PrincessPickup(Vector2(400, BOARD_H - 47), 32, 1)
    game.Workspace.AddChild(princes_pickup_2)

    princes_pickup_3 = PrincessPickup(Vector2(100, 210), 32, 2)
    game.Workspace.AddChild(princes_pickup_3)

    start_p = platforms[0]    
    game.oil_barrel_item = Item(Vector2((start_p.P1.x + 40), start_p.P1.y + 160), "OIL_BARREL", 30)
    game.Workspace.AddChild(game.oil_barrel_item)

    static_barrels = [
    ]

    for sb in static_barrels:
        game.Workspace.AddChild(sb)

# build level
assemble_level_1()

# used to calculate deltaTime (dt) to handle physics and renders
Timestamp = time.time()

# reset the level and other player attributes entirely
def reset_level():
    global game, SCORE

    del game
    game = Game()
    
    game.level = LEVEL
    
    if game.level == 1:
        assemble_level_1()
    else:
        assemble_level_2()
        game.princess.position = Vector2(300, 118)


#game input for player
def keyPressed():
    global GAME_STATE

    if keyCode == 32:
        gui.handle_selection()
    
    # Menu Navigation (Start, Pause, End screens)
    if GAME_STATE != 1 and GAME_STATE != 4:
        if keyCode == DOWN:
            gui.selected = (gui.selected + 1) % gui.menu_length()
        elif keyCode == UP:
            gui.selected = (gui.selected - 1) % gui.menu_length()
    elif GAME_STATE == 1:
        
        if game.transition_occuring:
            return

        if keyCode == LEFT:
            game.localPlayer.move_left()
        if keyCode == RIGHT:
            game.localPlayer.move_right()
        if keyCode == 32:
            game.localPlayer.jump()
        if keyCode == UP:
            game.localPlayer.climbDirection = UP
        if keyCode == DOWN:
            game.localPlayer.climbDirection = DOWN
        if keyCode == 80:  
            GAME_STATE = 2
        
def keyReleased():
    if keyCode == LEFT or keyCode == RIGHT:
        game.localPlayer.stop()
    if keyCode == UP:
        game.localPlayer.climbDirection = None
    if keyCode == DOWN:
        game.localPlayer.climbDirection = None
        
def draw():
    # Physics pipeline first (no multi-threading)
     
    global Timestamp
       

    if not game._PhysicsPipelineRunning:
        game._PhysicsPipelineRunning = True
        # NO MULTITHREADING HERE!!!!
        
        game.PreSimulation(time.time() - Timestamp)
        game.Simulation(time.time() - Timestamp)
        game.PostSimulation(time.time() - Timestamp)
        
        game._PhysicsPipelineRunning = False
        
        if not game._RenderPipelineRunning:
            game._RenderPipelineRunning = True
            
            # CAN MULTITHREAD, UPDATE RenderPipelineRunning in PostRender after all threads have finished
            
            game.PreRender(time.time() - Timestamp)
            game.Render(time.time() - Timestamp)
            game.PostRender(time.time() - Timestamp)
            
        Timestamp = time.time()

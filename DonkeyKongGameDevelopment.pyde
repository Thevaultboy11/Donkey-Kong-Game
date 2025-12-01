import math          # math helpers (unused currently)
import random        # random utilities (unused currently)
import threading     # threading hooks for render pipeline (not yet used)
import time          # timing for delta time
import os

#Board Global Variables

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

#GLOBAL IMAGES

# MARIO
mario_running = loadImage(PATH + "mario_running.png")
mario_jumping = loadImage(PATH + "mario_jump.png")
mario_idle = loadImage(PATH + "mario_idle.png")
mario_climbing_ladder = loadImage(PATH + "mario_ladder_climb.png")
mario_dying_right = loadImage(PATH + "mario_dying_right.png")
mario_dying_left = loadImage(PATH + "mario_dying_left.png")
mario_hammer_idle = loadImage(PATH + "mario_hammer_idle.png")
mario_hammer_running = loadImage(PATH + "mario_hammer_running.png")

# DONKEY KONG
donkey_idle = loadImage(PATH + "donkey_kong_idle.png")
donkey_barrel_throw = loadImage(PATH + "donkey_barrel_drop.png")
donkey_brown_barrel_drop = loadImage(PATH + "donkey_brown_barrel_drop.png")
donkey_blue_barrel_drop = loadImage(PATH + "donkey_blue_barrel_drop.png")

# INFRASTRUCTURE
platform_red = loadImage(PATH + "platform_red.png")
ladder_image = loadImage(PATH + "ladder_white.png")
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
    size(BOARD_W, BOARD_H)
    background(BACKGROUND_COLOR)
    global title_font, menu_font, hud_font
    title_font = createFont("kong_arcade_font.TTF", 72)
    menu_font  = createFont("kong_arcade_font.TTF", 32)
    hud_font  = createFont("kong_arcade_font.TTF", 24)

    #print(gui_mario_hammer_icon, gui_mario_angel_icon, gui_princess_icon, gui_kong_idle, gui_kong_pounding)
    pass

Enum = {}

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
    "SCREW": 108
}


class Vector:
    # An abstract class for Vectors
    
    def __init__(self):
        # Base class carries no state; defined for type hierarchy
        pass
    
class Vector2(Vector):
    # A vector with two components, x and y
    
    def __init__(self, x=0, y=0):
        
        Vector.__init__(self)
        
        self.x = x
        self.y = y
        
    def __str__(self):
        
        return "(" + str(self.x) + "," + str(self.y) + ")"
        
    def __sub__(self, VectorB):
        # A -> self
        
        if isinstance(VectorB, Vector2):
            return Vector2(self.x - VectorB.x, self.y - VectorB.y)
        
    def rmul(self, r):
        # Scale both components by a scalar
        return Vector2(self.x * r, self.y * r)
    
    def rdiv(self, r):
        
        return self.rmul(1/r)
    
    def vadd(self, VectorB):
        # Vector addition returning a new Vector2
        if isinstance(VectorB, Vector2):
            return Vector2(self.x + VectorB.x, self.y + VectorB.y)
        
    def vsub(self, VectorB):
        # self -> B
        
        if isinstance(VectorB, Vector2):
            return Vector2(VectorB.x - self.x, VectorB.y - self.y)
        
    def dotp(self, VectorB):
        # Dot product of two vectors
        return self.x * VectorB.x + self.y * VectorB.y
    
    def perp(self):
        # Returns a perpendicular vector (rotated 90 degrees)
        return Vector2(-self.y, self.x)
        
    def magnitude(self):
        # Euclidean length
        return (self.x**2 + self.y**2)**0.5
    
    def unit(self):
        # Normalized vector (length 1)
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
        dx = c1.position.x - c2.position.x
        dy = c1.position.y - c2.position.y

        dist_sq = dx*dx + dy*dy
        r = (c1.l + c1.collider_aura/2) + (c2.l + c2.collider_aura/2)

        return dist_sq <= r*r
        
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
                
                
    def retrace_ray2_collision(self, ray2, v):
        
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
    
    def __init__(self, name):
        # Base service type (e.g., Workspace)
        self.name = name
              
class Instance:
    
    def __init__(self, name, EnumType, anchored = False, canCollide = True):
        # Base instance type with name, enum classification, and object id
        self.name = name
        self.enum_type = EnumType
        self.objectId = -1
        
        self.active = True
        
        self.anchored = anchored
        self.canCollide = canCollide
        
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        
        if EnumType == Enum["ENUM_TYPE"]["PLAYER"] or EnumType == Enum["ENUM_TYPE"]["BARREL"] or EnumType == Enum["ENUM_TYPE"]["FIRE_SPIRIT"] or EnumType == Enum["ENUM_TYPE"]["ITEM"]:
            self.collider = Collider(Enum["COLLIDER_TYPE"]["CIRCLE"], self.position)
            
        elif EnumType == Enum["ENUM_TYPE"]["PLATFORM"] or EnumType == Enum["ENUM_TYPE"]["LADDER"]:
            self.collider = Collider(Enum["COLLIDER_TYPE"]["LINE"], Ray2(self.position))

class Animation:    
    def __init__(self, sprite=None, imageW=32, imageH=32, direction=RIGHT, total_slices=0):
        self.sprite = sprite
        self.img_w = imageW
        self.img_h = imageH
        self.slice = 0
        self.direction = direction
        self.animation_speed = 0.2   # seconds per frame (adjust)
        self.animation_timer = 0     # accumulates dt
        self.total_slices = total_slices

    def update(self, dt):
        #if there is only one slice then do not update anything.
        if self.total_slices <= 1:
            return
        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.slice = (self.slice + 1) % self.total_slices

    def play(self, xPosition, yPositon):
        if self.direction == RIGHT:
            image(self.sprite, xPosition - self.img_w // 2, yPositon - self.img_h // 2, self.img_w, self.img_h, self.slice * (self.img_w+4), 0, (self.slice) * (self.img_w+4) + self.img_w, self.img_h)
        elif self.direction == LEFT:
            image(self.sprite, xPosition - self.img_w // 2, yPositon - self.img_h // 2, self.img_w, self.img_h, (self.slice) * (self.img_w+4) + self.img_w, 0, self.slice * (self.img_w+4), self.img_h)
        else:
            image(self.sprite, xPosition - self.img_w // 2, yPositon - self.img_h // 2, self.img_w, self.img_h, self.slice * (self.img_w+4), 0, (self.slice) * (self.img_w+4) + self.img_w, self.img_h)
class Workspace(Service):
    
    def __init__(self, gravity=10):
        
        Service.__init__(self, "Workspace")
        
        self.gravity = gravity
        self.__index = 0
        self.__objects = {}
        
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
        # Returns a list of all childrent in the Workspace
        return self.__objects.values()
    
    def Raycast(self, ray2):
        # casts ray and does stuff
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
    
    def __init__(self, Workspace):
        
        Service.__init__(self, "Debris")
        
        self.__Workspace = Workspace

        self.__index = 0
        self.__objects = {}
        self.__threads = {}
        
    def AddItem(self, item, timeout=1):
        
        if not self.__objects.get(item.objectId, None):
            self.__objects[item.objectId] = [item, 0, timeout]
            
    def update(self, dt):
        
        for d in self.__objects.values():
            d[1] += dt
            if d[1] >= d[2]:
                d[0].active = False
                del self.__objects[d[0].objectId]

class Screw(Instance):
    def __init__(self, P=Vector2(0,0), radius=32):
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

                # Player must be slightly ABOVE the screw
                if player.position.y <= self.position.y - 10:
                    self.isShowing = False
                    self.active = False   # remove from game workspace
                    game.Workspace.RemoveChild(self)

    def display(self, dt=0):
        if self.isShowing:
            image(screw, self.position.x, self.position.y+20, 24, 24, 0, 0, 30, 32)


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
                image(ladder_image, self.rect_pos.x-8, self.rect_pos.y + (num *32),32, 32, 0, 0, 32, 32)
            
class Item(Instance):
    def __init__(self, P=Vector2(0,0), type="HAMMER", radius=30):
        Instance.__init__(self, "Item", Enum["ENUM_TYPE"]["ITEM"], True, False)
        self.position =  P
        self.collider = Collider(Enum["COLLIDER_TYPE"]["CIRCLE"], self.position)
        self.radius = radius
        self.collider.l = radius  
        self.type = type
        self.state = 0
        
        self.animations = {
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
        
        self.animations["BARREL_DESTROY"].animation_speed = 0.25
        self.animations["PRINCESS_SCARED"].animation_speed = 0.5
    
    def display(self, dt=0):
        
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
    #The class only takes the initial position as a vector as arguments.
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

    def update(self, dt):
        
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

        self.choose_animation_state(dt + (1/frameRate))
        self.current_animation.update(dt + (1/frameRate))
        self.current_animation.play(self.position.x, self.position.y)

        #fill(150, 75, 0)
        #circle(self.position.x, self.position.y, self.height)
        
class BlueBarrel(Instance): 
    #The class only takes the initial position as a vector as arguments.
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

    def update(self, dt):
        
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

        self.choose_animation_state(dt + (1/frameRate))
        self.current_animation.update(dt + (1/frameRate))
        self.current_animation.play(self.position.x, self.position.y)

        #fill(150, 75, 0)
        #circle(self.position.x, self.position.y, self.height)
        
class FireSpirit(Instance): 

    #The class only takes the initial position as a vector as arguments.
    def __init__(self, P=None):
        
        Instance.__init__(self, "Player", Enum["ENUM_TYPE"]["BARREL"], False, True)
        
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
        
#Class For The Player
class Player(Instance): 
    #The class only takes the initial position as a vector as arguments.
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
        self.speed = 120
        self.jump_force  = -130
        self.climb_velocity = 30
        
        self.BASE_POINT = BOARD_H
        
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
        
        self.barrel_score_debounce = 0

    def choose_animation_state(self, dt):
        
        #print(self.on_ground, self.position.y, self.BASE_POINT)
        
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
        
        global SCORE
        
        self.barrel_score_debounce -= dt
        
        #applying the gravity
        self.velocity.y += game.Workspace.gravity * dt * (1-self.anchored)
        #update position
        self.position.y += self.velocity.y * dt * (1-self.anchored)

        if self.has_hammer:
            self.hammer_time -= dt
            if self.hammer_time <= 0:
                self.has_hammer = False
                self.collider.l = 10
        
        if self.position.x + self.velocity.x * dt < self.collider.l:
            self.position.x = self.collider.l * (1-self.anchored)
            
        elif self.position.x + self.velocity.x * dt > BOARD_W - self.collider.l:
            self.position.x = BOARD_W - self.collider.l
            
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
            
            if child.enum_type == Enum["ENUM_TYPE"]["LADDER"] and not self.has_hammer:
                ladder = child
                
                top = ladder.top_pos
                bottom = ladder.bottom_pos
                
                if abs(self.position.x - top.x) <= self.collider.l:

                    if bottom.y >= self.position.y >= top.y - self.collider.l:

                        if self.climbDirection == UP and not self.isClimbing:
                            self.isClimbing = True
                            self.anchored = True
                            
                        elif self.climbDirection:
                            self.position.y -= self.climb_velocity * dt
                            self.velocity.y = 0

                    elif self.isClimbing and self.climbDirection == None:
                        
                        if top.y - self.collider.l >= self.position.y >= top.y - self.collider.l-5:
                            self.isClimbing = False
                            self.anchored = False
                            
                        else:
                            self.isClimbing = True
                            self.anchored = True
                            
            elif child.enum_type == Enum["ENUM_TYPE"]["BARREL"]:
                
                if abs(self.position.x - child.position.x) <= 10:
                    
                    if child.position.y - 8 >= self.position.y >= child.position.y - 64:
                        
                        if isinstance(child, FireSpirit):
                            pass
                            # LIFE LOST
                        elif isinstance(child, Barrel) or isinstance(child, BlueBarrel):
                            
                            if self.barrel_score_debounce > 0.5:
                                pass
                            elif not self.isClimbing:
                                self.barrel_score_debounce = 1
                                SCORE += 100
                            
                                score_particle = Item(Vector2(child.position.x, child.position.y), "SCORE_100", 30)
                                game.Workspace.AddChild(score_particle)
                        
                                game.Debris.AddItem(score_particle, 1)
                            
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
            self.velocity.y += self.jump_force
            self.on_ground = False
    
    def display(self, dt=0):
        #updating the dt
        
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
    
    #Intial variables that have 2 points as the initial points
    def __init__(self, P1=Vector2(0,100), P2=Vector2(BOARD_W,200)):
        
        Instance.__init__(self, "Platform", Enum["ENUM_TYPE"]["PLATFORM"], True, True)
        
        self.P1 = P1
        self.P2 = P2
        
        d = P2 - P1
        
        self.P2 = d.unit().rmul((d.magnitude() // 16) * 16).vadd(P1)
        
    def update(self, dt):
        pass
    
    #The draw funtions of the platform, where from the 2 points we create 15 pixels blocks. (this funciton can be used for vertical horizotnal and diagonal platforms.)
    def display(self, dt=0):
        direction = self.P2 - self.P1;
        distance = direction.magnitude()
        unit_direction = direction.unit()

        num_tiles = int(distance // 16)

        for i in range(num_tiles):
            tile_position = unit_direction.rmul(16 * i).vadd(self.P1)
            stroke(255)         
            fill(255, 0, 0) 
            image(platform_red, tile_position.x, tile_position.y, 32, 32, 0, 0, 32, 32)
            
class GUI:
    def __init__(self):
        self.selected = 0
        self.start_menu = ["START GAME", "EXIT"]
        self.pause_menu = ["CONTINUE", "EXIT"]
        self.end_menu   = ["RETRY", "EXIT"]

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
                BOARD_W/2 - 100,
                BOARD_H * 0.28 - 32,
                200, 128)
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
                sx + frame_width, sy + frame_height)



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

            text(option, x - textWidth(option)/2, y)

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
        text(title, BOARD_W/2 - textWidth(title)/2, BOARD_H * 0.15)

        self.draw_donkey_kong_animation()
        self.draw_menu(self.start_menu, BOARD_H * 0.60)

    # --- PAUSE SCREEN ---
    def draw_pause(self):
        background(0)
        textFont(title_font)
        fill(255)

        pause_text = "PAUSED"
        text(pause_text, BOARD_W/2 - textWidth(pause_text)/2, BOARD_H*0.25)

        self.draw_menu(self.pause_menu, BOARD_H*0.55)

    # --- END SCREEN ---
    def draw_end(self):
        background(0)

        if DID_WIN:
            image(gui_princess_icon,
                BOARD_W/2 - 36,
                BOARD_H*0.18 - 64,
                72, 128)
        else:
            image(gui_mario_angel_icon,
                BOARD_W/2 - 64,
                BOARD_H*0.18 - 64,
                128, 128)

        textFont(title_font)
        fill(255)

        gameover = "GAME OVER"
        text(gameover, BOARD_W/2 - textWidth(gameover)/2, BOARD_H*0.45)

        textFont(menu_font)

        score_text = "FINAL SCORE: " + str(SCORE)
        text(score_text, BOARD_W/2 - textWidth(score_text)/2, BOARD_H*0.58)

        self.draw_menu(self.end_menu, BOARD_H*0.75)

    def handle_selection(self):
        global GAME_STATE
        current_menu = None      
        if GAME_STATE == 0:
            current_menu = self.start_menu
        elif GAME_STATE == 2:
            current_menu = self.pause_menu
        elif GAME_STATE == 3:
            current_menu = self.end_menu
      
        if current_menu is not None:
            choice = current_menu[self.selected]
      
            if choice != "EXIT":
                GAME_STATE = 1
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

    def menu_length(self):
        if GAME_STATE == 0:
            return len(self.start_menu)
        if GAME_STATE == 2:
            return len(self.pause_menu)
        if GAME_STATE == 3:
            return len(self.end_menu)
        return 0

    def quit_game(self):
        exit()

    def display(self):

        if GAME_STATE == 0:
            self.draw_start()
        elif GAME_STATE == 2:
            self.draw_pause()
        elif GAME_STATE == 3:
            self.draw_end()
                            
class Game:
    
    def __init__(self):
        
        self.Workspace = Workspace(200)
        self.Debris = Debris(self.Workspace)
        
        self.__idle_threads = {}
        self.__running_threads = {}
        
        self._PhysicsPipelineRunning = False
        self._RenderPipelineRunning = False
        
        self.localPlayer = Player(Vector2(100, 550))
        self.localPlayer.collider.collider_aura = 10
        
        self.Workspace.AddChild(self.localPlayer)
        
        self.startpoint = Vector2(10, BOARD_H-50)
        
        self.barrel_spawn_interval = 4
        self.barrel_spawn_time = 0
        
        self.blue_barrel_chance = 0.2 # Percent
        
        self.animations = {
            "DONKEY_KONG_IDLE": Animation(donkey_idle, 96, 64, RIGHT, 1),
            "DONKEY_KONG_BARREL_DROP": Animation(donkey_barrel_throw, 96, 64, RIGHT, 3),
            "DONKEY_KONG_BROWN_BARREL_DROP": Animation(donkey_brown_barrel_drop, 96, 64, RIGHT, 3),
            "DONKEY_KONG_BLUE_BARREL_DROP": Animation(donkey_blue_barrel_drop, 96, 64, RIGHT, 3)
        }
        
        self.animations["DONKEY_KONG_BARREL_DROP"].animation_speed = 1.5
        self.animations["DONKEY_KONG_BROWN_BARREL_DROP"].animation_speed = 1.5
        self.animations["DONKEY_KONG_BLUE_BARREL_DROP"].animation_speed = 1.5
        
        self.current_donkey_animation = self.animations["DONKEY_KONG_IDLE"]
        
        self.new_barrel_type = None
        self.new_barrel_obj = None
        self.barrel_threshold_medium = 5
        self.barrel_threshold_insane = 10
        
        self.burnt_barrels = 0
        
        self.princess = Item(Vector2(240, 43), "PRINCESS", 30)
        self.Workspace.AddChild(self.princess)
        
    def PreSimulation(self, dt):
        # Preproccesing for physics simulation
        
        if self.burnt_barrels >= self.barrel_threshold_medium:
            self.barrel_spawn_interval = 3
            
            game.oil_barrel_item.state = 1
            
            if self.burnt_barrels >= self.barrel_threshold_insane:
                self.barrel_spawn_interval = 2.2
                self.blue_barrel_chance = 0.35
                
                game.oil_barrel_item.animations["FIRE_BIG"].animation_speed = 0.15
        pass
        
    def Simulation(self, dt):
        
        global SCORE
        
        if GAME_STATE != 1:
            return
        
        # Iterate through objects in Game.Workspace and do the honors
        collision_detected = True
        updated_instances = {}
        
        self.Debris.update(dt)       
        
            
        for i in self.Workspace.GetChildren():
            if True:
                if i.enum_type == Enum["ENUM_TYPE"]["PLAYER"] or i.enum_type == Enum["ENUM_TYPE"]["BARREL"]:
                    origin = Vector2(i.position.x, i.position.y + i.collider.l/2)
                    direction = Vector2(0, 1)

                    intersection, target = self.Workspace.Raycast(Ray2(origin, direction, 10000))

                    if intersection:
                        i.BASE_POINT = intersection.y  - i.collider.collider_aura/2
                    
                i.update(dt)
                
                if i.enum_type == Enum["ENUM_TYPE"]["ITEM"]:
                    if i.collider.circle_collision(game.localPlayer.collider, i.collider):
                        #print("PLAYER PICKED", i.type)

                        if i.type == "HAMMER" and not game.localPlayer.has_hammer:
                            game.localPlayer.has_hammer = True
                            game.localPlayer.hammer_time = 12
                            #game.localPlayer.collider.l = game.localPlayer.hammer_radius
                            
                            
                        
                            self.Workspace.RemoveChild(i)
                if game.localPlayer.has_hammer and i.enum_type == Enum["ENUM_TYPE"]["BARREL"]:
                    if i.collider.circle_collision(Collider(Enum["COLLIDER_TYPE"]["CIRCLE"], game.localPlayer.position, game.localPlayer.hammer_radius), i.collider):
                        
                        if isinstance(i, Barrel) or isinstance(i, BlueBarrel):
                            SCORE += 500
                        
                            destroy_particle = Item(i.position, "BARREL_DESTROY_PARTICLE", 30)
                            self.Workspace.AddChild(destroy_particle)
                        
                            self.Debris.AddItem(destroy_particle, 0.42)
                        
                            score_particle = Item(i.position, "SCORE_500", 30)
                            self.Workspace.AddChild(score_particle)
                        
                            self.Debris.AddItem(score_particle, 1)
                        
                            self.Workspace.RemoveChild(i)
                        
                        elif isinstance(i, FireSpirit):
                            SCORE += 800
                        
                            destroy_particle = Item(i.position, "BARREL_DESTROY_PARTICLE", 30)
                            self.Workspace.AddChild(destroy_particle)
                        
                            self.Debris.AddItem(destroy_particle, 0.42)
                        
                            score_particle = Item(i.position, "SCORE_800", 30)
                            self.Workspace.AddChild(score_particle)
                        
                            self.Debris.AddItem(score_particle, 1)
                        
                            self.Workspace.RemoveChild(i)
                            
        if game.localPlayer.position.x <=225 and game.localPlayer.position.y <= 130:
            print("OUT_OF_BOUNDS")
                    
        
        if True:
            return
        
        while collision_detected:
            collision_detected = False
            for i in self.Workspace.GetChildren():
                
                if not i.anchored and not updated_instances.get(i.objectId, False):
                    i.update(dt)
                    updated_instances[i.objectId] = True
                
                for v in self.Workspace.GetChildren():
                    
                    
                    if i.objectId != v.objectId:
                        
                        if not v.anchored and not updated_instances.get(v.objectId, False):
                            v.update(dt)
                            updated_instances.set(v.objectId, True)
                            
                        if i.collider.collider_type == Enum["COLLIDER_TYPE"]["LINE"] and v.collider.collider_type == Enum["COLLIDER_TYPE"]["CIRCLE"]:
                            
                            ret = v.collider.ray2_intersected(i.collider.position)
                            
                            if ret:
                                if len(ret) >= 2:
                                    collision_detected = True
                                
                                    #v.position = v.collider.retrace_ray2_collision(i.collider.position, v.velocity)
                                    #v.collider.position = v.position
                                    
                                    # Raycast to determine v.BASE_POS
                                    
                                    origin = self.localPlayer.position
                                    direction = Vector2(0, 1)
                                    
                                    intersection, target = self.Workspace.Raycast(Ray2(origin, direction, 10000))
                                    #print(intersection)
                                    
                                    if intersection:
                                        self.localPlayer.BASE_POINT = intersection.y  - self.localPlayer.collider.collider_aura/2
                                                        
        
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
        # Preprocessing for the frame to render, such as setting up the threads, etc.
        background(0)
        
        if random.randint(0, 1000) <= 2:
            self.princess.state = 1
        
        self.barrel_spawn_time += dt
        if self.barrel_spawn_time >= self.barrel_spawn_interval:
            
            
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
        
    def Render(self, dt):
        # Iterate through objects in Game.Workspace and do the honors, run every thread here
        
        if GAME_STATE != 1:
            gui.display()
            return
            pass
       
        if GAME_STATE == 1:
            gui.draw_hud(SCORE, NUM_LIVES)
            pass
        
        for i in self.Workspace.GetChildren():
            if not i.enum_type == Enum["ENUM_TYPE"]["PLAYER"]:
                i.display(dt)
                #self.__running_threads[i.objectId] = threading.Thread(target = i.display, args = (dt))
                #self.__running_threads[i.objectId].start()
            
        self.current_donkey_animation.update(dt + 1/frameRate)
        self.current_donkey_animation.play(100, 100)
        
        self.localPlayer.display(dt)
        
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

#Creating the testing class Player and platforms.
game = Game()
gui = GUI()

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

Obstacles = [
    #Barrel(Vector2(100, 0)),
    #BlueBarrel(Vector2(100, 0)),
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
    HalfLadder(Vector2(215, BOARD_H - 550), game.Workspace.Raycast),
    HalfLadder(Vector2(180, BOARD_H - 550), game.Workspace.Raycast),
]

for l in Ladders:
    game.Workspace.AddChild(l)
    
#adding testing screws
new_screw = Screw(Vector2(250, 300))
game.Workspace.AddChild(new_screw)

first = platforms[1]    
#hammer1 = Item(Vector2((first.P1.x + first.P2.x)/2, first.P1.y - 40), "HAMMER", 10)
#game.Workspace.AddChild(hammer1)

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

Timestamp = time.time()

#temporary game input for player
def keyPressed():
    global GAME_STATE

    if keyCode == 32:
        gui.handle_selection()
    
    # Menu Navigation (Start, Pause, End screens)
    if GAME_STATE != 1:
        if keyCode == DOWN:
            gui.selected = (gui.selected + 1) % gui.menu_length()
        elif keyCode == UP:
            gui.selected = (gui.selected - 1) % gui.menu_length()
    elif GAME_STATE == 1:

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

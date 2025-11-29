import math          # math helpers (unused currently)
import random        # random utilities (unused currently)
import threading     # threading hooks for render pipeline (not yet used)
import time          # timing for delta time

#Board Global Variables

BOARD_W = int(224*2.5)
BOARD_H = int(256*2.5)
BACKGROUND_COLOR = 000

def setup():
    # Placeholder for Processing setup; currently unused
    size(BOARD_W, BOARD_H)
    background(BACKGROUND_COLOR)
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
    "FIRE_SPIRIT": 105
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
        
    def ray2_intersected(self, ray):
        # Computes ray-circle intersection; returns closest hit within ray.magnitude or None
        if self.collider_type == Enum["COLLIDER_TYPE"]["CIRCLE"]:
            
            r = self.l + self.collider_aura / 2
            
            # Ray-Circle Intersection
            A_x = ray.origin.x
            A_y = ray.origin.y
            
            C_x = self.position.x
            C_y = self.position.y
            
            m = ray.direction.y / ray.direction.x

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
        
        self.anchored = anchored
        self.canCollide = canCollide
        
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        
        if EnumType == Enum["ENUM_TYPE"]["PLAYER"] or EnumType == Enum["ENUM_TYPE"]["BARREL"] or EnumType == Enum["ENUM_TYPE"]["FIRE_SPIRIT"]:
            self.collider = Collider(Enum["COLLIDER_TYPE"]["CIRCLE"], self.position)
            
        elif EnumType == Enum["ENUM_TYPE"]["PLATFORM"] or EnumType == Enum["ENUM_TYPE"]["LADDER"]:
            self.collider = Collider(Enum["COLLIDER_TYPE"]["LINE"], Ray2(self.position))

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
    
    
    def display(self):
        if self.rect_pos and self.height > 0:
            stroke(255)
            fill(255)
            rect(self.rect_pos.x, self.rect_pos.y, self.width, self.height)
    
class Barrel(Instance): 
    #The class only takes the initial position as a vector as arguments.
    def __init__(self, P=Vector2(0,0)):
        
        Instance.__init__(self, "Barrel", Enum["ENUM_TYPE"]["BARREL"], False, True)
        
        self.position = P
        
        self.width = 40
        self.height = 40
        
        self.collider.l = 20 # diameter / 2
        
        #Temporary Variable that we use to check if the player is on the ground.
        self.on_ground = False
        #Consants that represent the speed of the player moving right and left, gravity forces in numbers..
        self.speed = 120
        self.jump_force  = -180
        
        self.move_direction = LEFT
        
        self.BASE_POINT = BOARD_H
        #self.gravity = 0.5 NO NEED, WORKSPACE HANDLES GRAVITY

    def update(self, dt):
        
        # if reached start point, do something, like blue barrel becomes fire spirit
        if (self.position - game.startpoint).magnitude() < self.collider.l*2:
            self.move_direction = None
        
        if self.move_direction == LEFT:
            self.velocity.x = -self.speed
        elif self.move_direction == RIGHT:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0
        
        #applying the gravity
        self.velocity.y += game.Workspace.gravity * dt
        #update position
        self.position.y += self.velocity.y * dt
        
        if self.position.x + self.velocity.x * dt < self.collider.l:
            self.position.x = self.collider.l
            self.border_reached()
            
        elif self.position.x + self.velocity.x * dt > BOARD_W - self.collider.l:
            self.position.x = BOARD_W - self.collider.l
            self.border_reached()
        else:
            self.position.x += self.velocity.x * dt

        # ground collision (temporary)
        if self.position.y + self.height/2 > self.BASE_POINT:
            self.position.y = self.BASE_POINT - self.height/2
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
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
    
    def display(self):
        fill(150, 75, 0)
        circle(self.position.x, self.position.y, self.height)
        
class BlueBarrel(Instance): 
    #The class only takes the initial position as a vector as arguments.
    def __init__(self, P=Vector2(0,0)):
        
        Instance.__init__(self, "Barrel", Enum["ENUM_TYPE"]["BARREL"], False, True)
        
        self.position = P
        
        self.width = 30
        self.height = 30
        
        self.collider.l = 15 # diameter / 2
        
        #Temporary Variable that we use to check if the player is on the ground.
        self.on_ground = False
        #Consants that represent the speed of the player moving right and left, gravity forces in numbers..
        self.speed = 200
        self.jump_force  = -180
        
        self.move_direction = LEFT
        
        self.BASE_POINT = BOARD_H
        #self.gravity = 0.5 NO NEED, WORKSPACE HANDLES GRAVITY

    def update(self, dt):
        
        # if reached start point, do something, like blue barrel becomes fire spirit
        if (self.position - game.startpoint).magnitude() < self.collider.l*2:
            self.move_direction = None
        
        if self.move_direction == LEFT:
            self.velocity.x = -self.speed
        elif self.move_direction == RIGHT:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0
        
        #applying the gravity
        self.velocity.y += game.Workspace.gravity * dt
        #update position
        self.position.y += self.velocity.y * dt
        
        if self.position.x + self.velocity.x * dt < self.collider.l:
            self.position.x = self.collider.l
            self.border_reached()
            
        elif self.position.x + self.velocity.x * dt > BOARD_W - self.collider.l:
            self.position.x = BOARD_W - self.collider.l
            self.border_reached()
        else:
            self.position.x += self.velocity.x * dt

        # ground collision (temporary)
        if self.position.y + self.height/2 > self.BASE_POINT:
            self.position.y = self.BASE_POINT - self.height/2
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
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
    
    def display(self):
        fill(0, 75, 255)
        circle(self.position.x, self.position.y, self.height)
        
class FireSpirit(Instance): 
    #The class only takes the initial position as a vector as arguments.
    def __init__(self, P=Vector2(0,0)):
        
        Instance.__init__(self, "FireSpirit", Enum["ENUM_TYPE"]["BARREL"], False, True)
        
        self.position = P
        
        self.width = 20
        self.height = 20
        
        self.collider.l = 10 # diameter / 2
        
        #Temporary Variable that we use to check if the player is on the ground.
        self.on_ground = False
        #Consants that represent the speed of the player moving right and left, gravity forces in numbers..
        self.speed = 120
        self.jump_force  = -180
        
        self.move_direction = LEFT
        
        self.BASE_POINT = BOARD_H
        #self.gravity = 0.5 NO NEED, WORKSPACE HANDLES GRAVITY

    def update(self, dt):
        
        # if reached start point, do something, like blue barrel becomes fire spirit
        if (self.position - game.startpoint).magnitude() < self.collider.l*2:
            self.move_direction = None
        
        if self.move_direction == LEFT:
            self.velocity.x = -self.speed
        elif self.move_direction == RIGHT:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0
        
        #applying the gravity
        self.velocity.y += game.Workspace.gravity * dt
        #update position
        self.position.y += self.velocity.y * dt
        
        if self.position.x + self.velocity.x * dt < self.collider.l:
            self.position.x = self.collider.l
            self.border_reached()
            
        elif self.position.x + self.velocity.x * dt > BOARD_W - self.collider.l:
            self.position.x = BOARD_W - self.collider.l
            self.border_reached()
        else:
            self.position.x += self.velocity.x * dt

        # ground collision (temporary)
        if self.position.y + self.height/2 > self.BASE_POINT:
            self.position.y = self.BASE_POINT - self.height/2
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
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
    
    def display(self):
        fill(255, 165, 0)
        circle(self.position.x, self.position.y, self.height)
        
#Class For The Player
class Player(Instance): 
    #The class only takes the initial position as a vector as arguments.
    def __init__(self, P=Vector2(0,0)):
        
        Instance.__init__(self, "Player", Enum["ENUM_TYPE"]["PLAYER"], False, True)
        
        self.position = P
        
        self.width = 20
        self.height = 20
        
        self.collider.l = 10 # diameter / 2
        
        #Temporary Variable that we use to check if the player is on the ground.
        self.on_ground = False
        #Consants that represent the speed of the player moving right and left, gravity forces in numbers..
        self.speed = 120
        self.jump_force  = -180
        
        self.BASE_POINT = BOARD_H
        
        self.move_direction = LEFT
        #self.gravity = 0.5 NO NEED, WORKSPACE HANDLES GRAVITY

    def update(self, dt):
        #applying the gravity
        self.velocity.y += game.Workspace.gravity * dt
        #update position
        self.position.y += self.velocity.y * dt
        
        if self.position.x + self.velocity.x * dt < self.collider.l:
            self.position.x = self.collider.l
            
        elif self.position.x + self.velocity.x * dt > BOARD_W - self.collider.l:
            self.position.x = BOARD_W - self.collider.l
            
        else:
            self.position.x += self.velocity.x * dt
        

        # ground collision (temporary)
        if self.position.y + self.height/2 > self.BASE_POINT:
            self.position.y = self.BASE_POINT - self.height/2
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
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
    
    def display(self):
        fill(255,255,255)
        circle(self.position.x, self.position.y, self.height)



#Class Platform
class Platform(Instance):
    
    #Intial variables that have 2 points as the initial points
    def __init__(self, P1=Vector2(0,100), P2=Vector2(BOARD_W,200)):
        
        Instance.__init__(self, "Platform", Enum["ENUM_TYPE"]["PLATFORM"], True, True)
        
        self.P1 = P1
        self.P2 = P2
        
        d = P2 - P1
        
        self.P2 = d.unit().rmul((d.magnitude() // 16) * 16).vadd(P1)
        
    def update(dt):
        pass
    
    #The draw funtions of the platform, where from the 2 points we create 15 pixels blocks. (this funciton can be used for vertical horizotnal and diagonal platforms.)
    def display(self):
        direction = self.P2 - self.P1;
        distance = direction.magnitude()
        unit_direction = direction.unit()

        num_tiles = int(distance // 16)

        for i in range(num_tiles):
            tile_position = unit_direction.rmul(16 * i).vadd(self.P1)
            stroke(255)         
            fill(255, 0, 0) 
            rect(tile_position.x, tile_position.y, 16, 16)
                
                
class Game:
    
    def __init__(self):
        
        self.Workspace = Workspace(200)
        self.__idle_threads = {}
        self.__running_threads = {}
        
        self._PhysicsPipelineRunning = False
        self._RenderPipelineRunning = False
        
        self.localPlayer = Player(Vector2(100, 0))
        self.localPlayer.collider.collider_aura = 10
        
        self.Workspace.AddChild(self.localPlayer)
        
        self.startpoint = Vector2(0, BOARD_H)
        
    def PreSimulation(self, dt):
        # Preproccesing for physics simulation
        pass
        
    def Simulation(self, dt):
        # Iterate through objects in Game.Workspace and do the honors
        collision_detected = True
        updated_instances = {}
        
        
            
        for i in self.Workspace.GetChildren():
            if not i.anchored:
                if i.enum_type == Enum["ENUM_TYPE"]["PLAYER"] or i.enum_type == Enum["ENUM_TYPE"]["BARREL"]:
                    origin = Vector2(i.position.x, i.position.y + i.collider.l/2)
                    direction = Vector2(0, 1)

                    intersection, target = self.Workspace.Raycast(Ray2(origin, direction, 10000))
                    print(intersection)

                    if intersection:
                        i.BASE_POINT = intersection.y  - i.collider.collider_aura/2
                    
                i.update(dt)
        
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
        pass
        
    def PreRender(self, dt):
        # Preprocessing for the frame to render, such as setting up the threads, etc.
        pass
        background(0)
        
    def Render(self, dt):
        # Iterate through objects in Game.Workspace and do the honors, run every thread here
        
        for i in self.Workspace.GetChildren():
            i.display()
            #self.__running_threads[i.objectId] = threading.Thread(target = i.display, args = ())
            #self.__running_threads[i.objectId].start()
        
    def PostRender(self, dt):
        # Post processing after frame has been drawn. remove all garbage, etc.
        
        #for i in self.Workspace.GetChildren():
            #self.__running_threads[i.objectId].join()
            #del self.__running_threads[i.objectId]
            
        self._RenderPipelineRunning = False

#Creating the testing class Player and platforms.
game = Game()
platforms = [
    Platform(Vector2(0-16, BOARD_H - 16), Vector2(BOARD_W+32, BOARD_H - 16*2)),
    Platform(Vector2(0-16, BOARD_H - 16*6-32), Vector2(BOARD_W - 16*2-32, BOARD_H - 16*5-32)),    
    Platform(Vector2(16*2+32, BOARD_H - 16*8.7 - 32*2), Vector2(BOARD_W+32, BOARD_H - 16*10 -32*2)),
    Platform(Vector2(0-16, BOARD_H - 16*14.2 - 32*3), Vector2(BOARD_W-16*2-32, BOARD_H - 16*13 -32*3)),
    Platform(Vector2(16*2+32, BOARD_H - 16*16.9 - 32*4), Vector2(BOARD_W+32, BOARD_H - 16*18.3 -32*4)),
    Platform(Vector2(0-16, BOARD_H - 16*21.5 - 32*5), Vector2(BOARD_W-16*2-32, BOARD_H - 16*21 -32*5))
]

Obstacles = [
    Barrel(Vector2(100, 0)),
    BlueBarrel(Vector2(100, 0)),
    FireSpirit(Vector2(100, 0))
]

for p in platforms:
    game.Workspace.AddChild(p)
    
    p.collider.position.origin = p.P1
    p.collider.position.direction = (p.P2 - p.P1).unit()
    p.collider.position.magnitude = (p.P2 - p.P1).magnitude()
    
for b in Obstacles:
    game.Workspace.AddChild(b)
    
ladder_test = Ladder(Vector2(200, 500), game.Workspace.Raycast)
game.Workspace.AddChild(ladder_test)
    
    

Timestamp = time.time()

#temporary game input for player
def keyPressed():
    if key == 'a':
        game.localPlayer.move_left()
    if key == 'd':
        game.localPlayer.move_right()
    if key == 'w':
        game.localPlayer.jump()

def keyReleased():
    if key == 'a' or key == 'd':
        game.localPlayer.stop()

def draw():
    # Physics pipeline first (no multi-threading)
     
    global Timestamp
    
    if not game._PhysicsPipelineRunning:
        game._PhysicsPipelineRunning = True
        # NO MULTITHREADING HERE!!!!
        
        game.PreSimulation(time.time() - Timestamp)
        game.Simulation(time.time() - Timestamp)
        game.PostSimulation(time.time() - Timestamp)
        
        Timestamp = time.time()
        
        game._PhysicsPipelineRunning = False
        
        if not game._RenderPipelineRunning:
            game._RenderPipelineRunning = True
            
            # CAN MULTITHREAD, UPDATE RenderPipelineRunning in PostRender after all threads have finished
            
            game.PreRender(time.time() - Timestamp)
            game.Render(time.time() - Timestamp)
            game.PostRender(time.time() - Timestamp)

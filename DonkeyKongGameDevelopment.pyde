import math          # math helpers (unused currently)
import random        # random utilities (unused currently)
import threading     # threading hooks for render pipeline (not yet used)
import time          # timing for delta time

#Board Global Variables

BOARD_W = 400
BOARD_H = 600
BACKGROUND_COLOR = 000

def setup():
    # Placeholder for Processing setup; currently unused
    size(BOARD_W, BOARD_H)
    background(BACKGROUND_COLOR)
    pass

Enum = {}

# 0 - 100
Enum["COLLIDER_TYPE"] = {
    "CIRCLE": 0
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
        
    def ray2_intersected(self, ray):
        # Computes ray-circle intersection; returns closest hit within ray.magnitude or None
        if self.collider_type == Enum["COLLIDER_TYPE"]["CIRCLE"]:
            
            # Ray-Circle Intersection
            A_x = ray.origin.x
            A_y = ray.origin.y
            
            C_x = self.position.x
            C_y = self.position.y
            
            m = ray.origin.y / ray.origin.x

            a = 1 + m**2
            b = 2 * m * A_x - 2 * C_y * m - 2 * C_x - 2 * m**2 * A_x
            c = C_x**2 + C_y**2 + m**2 * A_x**2 + A_y**2 - 2 * m * A_x + 2 * m * A_x * C_y - 2 * A_y * C_y - r**2
            
            det = b**2 - 4*a*c
            
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
                            return P1
                        
                        else:
                            return P2
                        
                    else:
                        
                        return P1
                    
                else:
                    
                    if P2_magnitude <= ray.magnitude:
                        return P2
                    
                    else:
                        return None
                    
            else:
                
                if det == 0:
                    
                    x1 = (-b + (det)**0.5) / (2 * a)
                    y1 = m * x1 - m*A_x + A_y
                    
                    P1 = Vector2(x1, y1)
                    
                    if P1.magnitude() <= ray.magnitude:
                        
                        return P1
                    
                    else:
                        return None
                    
                    
                else:
                    
                    return None
                
                
class Service:
    
    def __init__(self, name):
        # Base service type (e.g., Workspace)
        self.name = name
        
        
class Instance:
    
    def __init__(self, name, EnumType):
        # Base instance type with name, enum classification, and object id
        self.name = name
        self.enum_type = EnumType
        self.objectId = -1

class Workspace(Service):
    
    def __init__(self, gravity=10):
        
        Service.__init__(self, "Workspace")
        
        self.gravity = 10
        self.__index = 0
        self.__objects = {}
        
    # def AddChild(object: Instance):
    #     # Registers a child instance and returns its object id
    #     self.__objects[self.__index] = object
    #     object.objectId = self.__index
    #     self.__index += 1
        
    #     return object.objectId
    
    # def RemoveChild(object: Instance):
    #     # Removes a child by instance reference
    #     del self.__objects[object.objectId]
        
    # def GetChild(objectId):
    #     # Retrieves a child by object id
    #     return self.__objects.get(objectId, None)
        
                
                
class Game:
    
    def __init__(self):
        
        self.Workspace = Workspace(10)
        self.__idle_threads = {}
        self.__running_threads = {}
        
        self._PhysicsPipelineRunning = False
        self._RenderPipelineRunning = False
        
    def PreSimulation(self, dt):
        # Preproccesing for physics simulation
        pass
        
    def Simulation(self, dt):
        # Iterate through objects in Game.Workspace and do the honors
        pass
        
    def PostSimulation(self, dt):
        # PostProcessing for physics, garbage collection and debris clearing (via Debris service)
        pass
        
    def PreRender(self, dt):
        # Preprocessing for the frame to render, such as setting up the threads, etc.
        pass
        
    def Render(self, dt):
        # Iterate through objects in Game.Workspace and do the honors, run every thread here
        pass
        
    def PostRender(self, dt):
        # Post processing after frame has been drawn. remove all garbage, etc.
        
        pass

#Class For The Player
class Player: 
    #The class only takes the initial position as a vector as arguments.
    def __init__(self, P=Vector2(0,0)):
        self.position = P
        #This is a vector with which we simulate velocity, and all of the movment is the byproduct of this velocity.
        self.velocity = Vector2(0,0)
        self.width = 20
        self.height = 20
        #Temporary Variable that we use to check if the player is on the ground.
        self.on_ground = False
        #Consants that represent the speed of the player moving right and left, gravity forces in numbers..
        self.speed = 3
        self.jump_force  = -10
        self.gravity = 0.5

    def update(self):
        #applying the gravity
        self.velocity.y += self.gravity
        #update position
        self.position = self.position.vadd(self.velocity)

        # ground collision (temporary)
        if self.position.y + self.height > BOARD_H:
            self.position.y = BOARD_H - self.height
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
        
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
            self.velocity.y = self.jump_force
            self.on_ground = False
    
    def draw(self):
        fill(255,255,255)
        circle(self.position.x, self.position.y, self.height)

    

#Class Platform
class Platform:
    
    #Intial variables that have 2 points as the initial points
    def __init__(self, P1=Vector2(0,100), P2=Vector2(BOARD_W,200)):
        self.P1 = P1
        self.P2 = P2
    
    #The draw funtions of the platform, where from the 2 points we create 15 pixels blocks. (this funciton can be used for vertical horizotnal and diagonal platforms.)
    def draw(self):
        direction = self.P2 - self.P1;
        distance = direction.magnitude()
        unit_direction = direction.unit()

        num_tiles = int(distance // 16)

        for i in range(num_tiles + 1):
            tile_position = unit_direction.rmul(16 * i).vadd(self.P1)
            stroke(255)         
            fill(255, 0, 0) 
            rect(tile_position.x, tile_position.y, 16, 16)




#Creating the testing class Player and platforms.
game = Game()
player = Player(Vector2(100, 0))
platforms = [
    Platform(Vector2(0, 540), Vector2(350, 540)),    
    Platform(Vector2(300, 480), Vector2(0, 450))
]
Timestamp = time.time()

#temporary game input for player
def keyPressed():
    if key == 'a':
        player.move_left()
    if key == 'd':
        player.move_right()
    if key == 'w':
        player.jump()

def keyReleased():
    if key == 'a' or key == 'd':
        player.stop()

def draw():
    #Creating the temporary rendering of the game (the background(0) resets the whole canvas 60 times a second)
    background(0)
    for p in platforms:
        p.draw()
    player.update()
    player.draw()
     # Physics pipeline first (no multi-threading)
    
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

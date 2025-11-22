import math
import random
import threading
import time

def setup():
    pass

Enum = {}

# 0 - 100
Enum["COLLIDER_TYPE"] = {
    "CIRCLE": 0
}
        

class Vector:
    # An abstract class for Vectors
    
    def __init__(self):
        
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
        
        return Vector2(self.x * r, self.y * r)
    
    def rdiv(self, r):
        
        return self.rmul(1/r)
    
    def vadd(self, VectorB):
        
        if isinstance(VectorB, Vector2):
            return Vector2(self.x + VectorB.x, self.y + VectorB.y)
        
    def vsub(self, VectorB):
        # self -> B
        
        if isinstance(VectorB, Vector2):
            return Vector2(VectorB.x - self.x, VectorB.y - self.y)
        
    def dotp(self, VectorB):
        
        return self.x * VectorB.x + self.y * VectorB.y
    
    def perp(self):
        
        return Vector2(-self.y, self.x)
        
    def magnitude(self):
        
        return (self.x**2 + self.y**2)**0.5
    
    def unit(self):
        
        return self.rdiv(self.magnitude())
    
class Ray2:
    
    def __init__(self, origin=Vector2(0, 0), direction=Vector2(1, 1), magnitude=5):
        
        self.origin = origin
        self.direction = direction
        
        self.magnitude = magnitude
    
    
class Collider:
    
    def __init__(self, collider_type = Enum["COLLIDER_TYPE"]["CIRCLE"], position = Vector2(0, 0), l = 0):
        
        self.collider_type = collider_type
        self.position = position
        self.l = l #dimension / size / radius, etc.
        
    def ray2_intersected(self, ray):
        
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
        
        self.name = name
        
        
class Instance:
    
    def __init__(self, name, EnumType):
        
        self.name = name
        self.enum_type = EnumType
        self.objectId = -1
        
        
class Workspace(Service):
    
    def __init__(self, gravity=10):
        
        Service.__init__(self, "Workspace")
        
        self.gravity = 10
        self.__index = 0
        self.__objects = {}
        
    def AddChild(object: Instance):
        
        self.__objects[self.__index] = object
        object.objectId = self.__index
        self.__index += 1
        
        return object.objectId
    
    def RemoveChild(object: Instance):
        
        del self.__objects[object.objectId]
        
    def GetChild(objectId):
        
        return self.__objects.get(objectId, None)
        
                
                
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
        

game = Game()

Timestamp = time.time()
def draw():
    
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
            
        
        
        
    
            

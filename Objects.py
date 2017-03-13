import math
from time import process_time as time
from time import sleep
SHIP_TYPES = [
  {
   "name" : "basic",
   "size" : 3,
   "maxvelocity" : 3,
   "maxrotationvelocity" : 10,
  },
]

Objects = []

class CollisionObject():
    def init(self, x, y, r):
        self.x = x
        self.y = y
        self.r = 0
        self.vx = 0
        self.vy = 0
        self.vr = 0
        self.sleepy = False
        self.radius = r
    def collided(self, target):
        pass
    def update(self, time):
        self.x += self.vx * time
        self.y += self.vy * time
        self.r += self.vr * time
        self.minCollisionTime -= time
        self.vy *= 0.999
        self.vx *= 0.999
        if self.vx < 0.01:
            self.vx = 0
        if self.vy < 0.01:
            self.vy = 0
        if (self.vx == 0) and (self.vy == 0):
            self.sleepy == True
        else:
            self.sleepy = False
        if not self.collisionTimeActive:
            self.collisionTimeActive = True
            self.minCollisionTime = 10 / (self.x + self.y)


    def isColliding(self, target):
        global Objects
        assert hasattr(target, "radius"), "No 'radius' attribute in class " + type(target)
        assert hasattr(target, "x"), "No 'x' attribute in class " + type(target)
        assert hasattr(target, "y"), "No 'y' attribute in class " + type(target)
        #TODO: add sectors
        x = (self.x - target.x)
        y = (self.y - target.y)
        dist = math.hypot(x, y)
        totalRadius = target.radius + self.radius
        return dist <= target.radius + self.radius, dist
    def resolveCollision(self, target, time):
        if self.collisionTimeActive:
            if self.minCollisionTime > 0:
                return
        else:
            self.collisionTimeActive = False
        if self.sleepy:
            return
        (isCollided, distance) = self.isColliding(target)
        if isCollided:
            delta = (target.x - self.x, target.y - self.y)
            self.vx += delta[0] * time
            self.vy += delta[1] * time
            target.vx -= delta[0] * time
            target.vy -= delta[1] * time
            self.collided(target)
            target.collided(self)
            self.minCollisionTime = 0
        else:
            self.minCollisionTime = min(self.minCollisionTime, distance)
        return True

class Ship(CollisionObject):
    def __init__(self, x, y, shiptype):
        global Objects
        self.type = shiptype
        self.ship = SHIP_TYPES[self.type]
        self.init(x, y, self.ship["size"])
        self.pos = len(Objects)
        self.minCollisionTime = 0
        self.collisionTimeActive = False
        Objects.append(self)


def Physics_Update(Objects, time):
    checked = [False] * len(Objects)
    for i, Object in enumerate(Objects):
        for itarget in range(i, len(Objects)):
            if not checked[itarget] and itarget != i:
                target = Objects[itarget]
                if Object.resolveCollision(target, time):
                    checked[i] = True
                #TODO: use 'sleepy' parameter
    for i, Object in enumerate(Objects):
        Object.update(time)
        #print(i, Object.x, Object.y)

import sys
sys.stdout = open('log.txt','w')

if __name__ == "__main__":
    #Ship(10, 10, 0)
    #Ship(12, 12, 0)
    #Ship(20, 20, 0)
    for i in range(5):
        Ship(10, i*20, 0)
    starttime = ctime = time()
    tick = 0
    while True:
        elapsed = time()-ctime
        ctime = time()
        print(time() - starttime)
        Physics_Update(Objects, min(elapsed, 0.1))
        tick += 1
        if time() - starttime>=60:
            stime = time() - starttime
            break

sys.stdout.close()
sys.stdout = sys.__stdout__
print('Complited in', stime)
print('Tick passed', tick)
print('Mean tick time', stime/tick)

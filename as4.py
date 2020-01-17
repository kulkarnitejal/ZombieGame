import random
import math

from gamelib import *

class ZombieCharacter(ICharacter):
    def __init__(self, obj_id, health, x, y, map_view):
        ICharacter.__init__(self, obj_id, health, x, y, map_view)

    def selectBehavior(self):
        prob = random.random()

        # If health is less than 50%, then heal with a 10% probability
        if prob < 0.1 and self.getHealth() < self.getInitHealth() * 0.5:
            return HealEvent(self)

        # Pick a random direction to walk 1 unit (Manhattan distance)
        x_off = random.randint(-1, 1)
        y_off = random.randint(-1, 1)

        # Check the bounds
        map_view = self.getMapView()
        size_x, size_y = map_view.getMapSize()
        x, y = self.getPos()
        if x + x_off < 0 or x + x_off >= size_x:
            x_off = 0
        if y + y_off < 0 or y + y_off >= size_y:
            y_off = 0

        return MoveEvent(self, x + x_off, y + y_off)

class PlayerCharacter(ICharacter):
    def __init__(self, obj_id, health, x, y, map_view):
        ICharacter.__init__(self, obj_id, health, x, y, map_view)
        # You may add any instance attributes you find useful to save information between frames
        self.alreadyAttacked = False
        self.shouldScan = 0
        self.heal_count = 5
    def selectBehavior(self):
        # Replace the body of this method with your character's behavior

        if self.getHealth() < self.getInitHealth() * 0.75:
            if self.heal_count > 0:
                self.shouldScan = (self.shouldScan+1)%3
                self.heal_count -= 1
                return HealEvent(self)

        if self.shouldScan == 0:
            self.shouldScan = (self.shouldScan+1)%3
            self.alreadyAttacked = False
            return ScanEvent(self)
        else :
            self.shouldScan = (self.shouldScan+1)%3
        x, y = self.getPos()

        if not self.getScanResults():
            # Pick a random direction to walk 1 unit (Manhattan distance)
            x_off = random.randint(-1, 1)
            y_off = random.randint(-1, 1)

            # Check the bounds
            map_view = self.getMapView()
            size_x, size_y = map_view.getMapSize()

            if x + x_off < 0 or x + x_off >= size_x:
                x_off = 0
            if y + y_off < 0 or y + y_off >= size_y:
                y_off = 0

            return MoveEvent(self, x + x_off, y + y_off)

        if not self.alreadyAttacked:
            for item in self.getScanResults():
                zombiex = item.getPos()[0]
                zombiey = item.getPos()[1]
                if abs(self.getPos()[0] - zombiex) + abs(self.getPos()[1] - zombiey) <= 2:
                    self.alreadyAttacked = True
                    return AttackEvent(self, item.getID())


        closestDistance = abs(self.getPos()[0] - self.getScanResults()[0].getPos()[0]) + abs(self.getPos()[1] - self.getScanResults()[0].getPos()[1])
        closestx = self.getScanResults()[0].getPos()[0]
        closesty = self.getScanResults()[0].getPos()[1]
        for item in self.getScanResults():
            zombiex = item.getPos()[0]
            zombiey = item.getPos()[1]
            if abs(self.getPos()[0] - zombiex) + abs(self.getPos()[1] - zombiey) < closestDistance :
                closestx = zombiex
                closesty = zombiey
                closestDistance = abs(self.getPos()[0] - zombiex) + abs(self.getPos()[1] - zombiey)

        map_view = self.getMapView()
        size_x, size_y = map_view.getMapSize()

        if (self.getPos()[0] - closestx) == 0 :
            if (self.getPos()[1] - closesty) > 0 :
                if  y - 3 >= 0 :
                    return MoveEvent(self, x , y - 3)
            else :
                if  y + 3 < size_y :
                    return MoveEvent(self, x , y + 3)

        if (self.getPos()[1] - closesty) == 0 :
            if (self.getPos()[1] - closestx) > 0 :
                if  x - 3 >= 0 :
                    return MoveEvent(self, x - 3, y)
            else :
                if  x + 3 < size_x :
                    return MoveEvent(self, x + 3 , y)

        moveX = 0
        moveY = 0
        if (self.getPos()[0] - closestx) > 0 :
            x_off = -1
        else :
            x_off = 1
        if (self.getPos()[0] - closesty) > 0 :
            y_off = -1
        else :
            y_off = 1




        if x + x_off < 0 or x + x_off >= size_x:
            x_off = 0
        if y + y_off < 0 or y + y_off >= size_y:
            y_off = 0

        return MoveEvent(self, x + x_off, y + y_off)

        pass

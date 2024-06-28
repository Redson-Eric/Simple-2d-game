import pygame as p
from vector import *

class Player:
    def __init__(self):
        self.image = p.image.load("resource/player.png")
        self.hitBox = self.image.get_rect()
        self.soundHurt = p.mixer.Sound("sound/playerHurt.mp3")
        
        self.hp = 50    # Player health
        self.speed = Vector(5, 5)
        self.isAlive = True
        self.looking_angle = 0.0

        self.forward = Vector.getforward(self.looking_angle)
        self._position = Vector(self.hitBox.x, self.hitBox.y)

    def draw(self, surface):
        rotated_image = p.transform.rotate(self.image, todegree(self.looking_angle) - 90) # Rotate the image from its center angle (current orientation-90)
        surface.blit(rotated_image, (self.position.x, self.position.y, self.hitBox.w, self.hitBox.h))

    def checkIfAlive(self):
        if self.hp <=0:
            self.isAlive = False

    def doDammage(self, ennemiList):
        self.checkIfAlive()
        for bot in ennemiList:
            if self.hitBox.colliderect(bot.hitBox):
                self.soundHurt.play()

    def move_forward(self, mousepos: Vector):
        tomouse = (mousepos - self.position).get_angle()
        self.position += self.speed * Vector.getforward(tomouse)

    def move_backward(self, mousepos: Vector):
        tomouse = (mousepos - self.position).get_angle()
        self.position += -1 * self.speed * Vector.getforward(tomouse)

    def move_right(self, mousepos: Vector):
        tomouse = (mousepos - self.position).get_angle()
        self.position += self.speed * Vector.getforward(tomouse - toradian(90))
    
    def move_left(self, mousepos: Vector):
        tomouse = (mousepos - self.position).get_angle()
        self.position += self.speed * Vector.getforward(tomouse + toradian(90))

    @property
    def position(self): return self._position

    @position.setter
    def position(self, p: Vector):
        """Auto update hitbox for collision detection"""
        self._position = p
        self.hitBox.x, self.hitBox.y = p.x, p.y
        

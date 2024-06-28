import pygame as p
from player import Player
from random import uniform
from vector import Vector, todegree

class Bot:
    def __init__(self):
        self.image = p.image.load("resource/ennemi.png")
        self.hitBox = self.image.get_rect()
        self.deathSound = p.mixer.Sound("sound/explosion.wav")
        self.isAlive = True

        self.speed = uniform(1.36, 2.3) # m/s
        self.hp = 10
        self.damage = 10

        self._orientation = 0.0 # Angle (in radian) in which this bot currently looking for
        self.forward = Vector.getforward(self.orientation)
        self._position = Vector(self.hitBox.x, self.hitBox.y)

    def draw(self, surface: p.Surface):
        surface.blit(
            p.transform.rotate(self.image, todegree(self.orientation) - 90),
            (self.position.x, self.position.y, self.hitBox.w, self.hitBox.h)
        )

    def chase(self, target: Player):
        """Control bot forward vector to face the target (Player)"""

        # Make bot face the target
        self.orientation = (target.position - self.position).get_angle()
        self.forward = Vector.getforward(self.orientation)

    def move(self):
        """Moves the bot dependents of its directinal vector"""
        self.position += self.speed * self.forward

    def checkCollisionToPlayer(self, target: Player):
        """
        Check collision between this bots and the player.
        Remove this bot, if that is the case, and hit player
        """
        if self.hitBox.colliderect(target.hitBox):
            self.deathSound.play()
            self.isAlive = False
            target.hp -= self.damage

    def checkCollision(self, ennemilist: list[p.Rect]):
        """
        Check collision between themself
        and control life state

        Paramter:
        listRect: list of Bot's hitBox
        """
        for bot in ennemilist:
            box = bot.hitBox
            if box != self.hitBox:
                if self.hitBox.colliderect(box):
                    self.deathSound.play()
                    self.isAlive = False
                    bot.isAlive = False

    @property
    def orientation(self): return self._orientation

    @orientation.setter
    def orientation(self, angle: float):
        """
        Change bots orientations

        Parameter:
        ----------
        angle: The angle in degree in wich bot faces
        """
        self._orientation = angle

    @property
    def position(self): return self._position

    @position.setter
    def position(self, p: Vector):
        self._position = p
        self.hitBox.x, self.hitBox.y = p.x, p.y
        


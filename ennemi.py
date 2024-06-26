import pygame as p
from player import Player

class Bot:
    def __init__(self):
        self.image = p.image.load("resource/ennemi.png")
        self.hitBox = self.image.get_rect() # Bot coordinate
        self.deathSound = p.mixer.Sound("sound/explosion.wav")
        self.isAlive = True

        # Directional Vector
        self.velocityX = 0
        self.velocityY = 0

        self.lastX = 0
        self.lastY = 0
        self.speed = 1
        self.hp = 10
        self.damage = 10
        self._orientation = 0.0 # Angle (in degree) in which this bot currently looking for


    def draw(self, surface):
        surface.blit(
            p.transform.rotate(self.image, self.orientation),
            self.hitBox
        )

    def chase(self, target):
        """Control bot directional vector to face the target (Player)"""

        #target.hitBox.centerX ------ target.hitBox.CenterY
        targetX = target.hitBox.centerx
        targetY = target.hitBox.centery

        #Y
        if self.hitBox.centery > targetY:
            self.velocityY = -1
        elif self.hitBox.centery < targetY:
            self.velocityY = 1
        else:
            self.velocityY = 0
        #X
        if self.hitBox.centerx > targetX:
            self.velocityX = -1
        elif self.hitBox.centerx < targetX:
            self.velocityX = 1
        else:
            self.velocityX = 0

        # Make bot face the target
        from main import Game
        self.orientation = Game.getRotateAngle(targetX-self.hitBox.centerx, targetY-self.hitBox.centery) - 90

    def move(self):
        """Moves the bot dependents of its directinal vector"""
        self.hitBox.move_ip(self.velocityX * self.speed, self.velocityY * self.speed)

    def checkCollisionToPlayer(self, target: Player):
        """
        Check collision between this bots and the player.
        Remove this bot, if that is the case, and hit player
        """
        if self.hitBox.colliderect(target.hitBox):
            self.deathSound.play()
            self.isAlive = False
            target.hp -= self.damage

    def checkCollision(self, listRect):
        """
        Check collision between themself
        and control life state

        Paramter:
        listRect: list of Bot's hitBox
        """
        for x in listRect:
            if x != self.hitBox:
                if self.hitBox.colliderect(x):
                    self.deathSound.play()
                    self.isAlive = False
                else:
                    pass
                    
            else:
                pass

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

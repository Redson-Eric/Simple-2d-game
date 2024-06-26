import pygame as p

class Bot:
    def __init__(self):
        self.image = p.image.load("resource/ennemi.png")
        self.hitBox = self.image.get_rect()
        self.deathSound = p.mixer.Sound("sound/explosion.wav")
        self.isAlive = True
        self.velocityX = 0
        self.velocityY = 0
        self.lastX = 0
        self.lastY = 0
        self.speed = 1
        self.hp = 10
        self.damage = 10


    def draw(self, surface):
        surface.blit(self.image, self.hitBox)

    def chase(self,target):
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
    def move(self):
        self.hitBox.move_ip(self.velocityX * self.speed, self.velocityY * self.speed)

    def checkCollisionToPlayer(self, target):
        if self.hitBox.colliderect(target.hitBox):
            self.deathSound.play()
            self.isAlive = False
            target.hp -= self.damage
    def checkCollision(self, listRect):

        for x in listRect:
            if x != self.hitBox:
                if self.hitBox.colliderect(x):
                    self.deathSound.play()
                    self.isAlive = False

                else:
                    pass
            else:
                pass



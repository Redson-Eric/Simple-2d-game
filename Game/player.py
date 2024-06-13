import pygame as p

class Player:
    def __init__(self):
        self.image = p.image.load("resource/player.png")
        self.hitBox = self.image.get_rect()
        self.soundHurt = p.mixer.Sound("sound/playerHurt.mp3")
        self.velocityX = 0
        self.velocityY = 0
        self.hp = 100
        self.speed = 3
        self.isAlive = True

    def draw(self, surface):
        surface.blit(self.image, self.hitBox)

    def checkIfAlive(self):
        if self.hp <=0:
            self.isAlive = False
        else:
            pass
    def doDammage(self, ennemiList):
        self.checkIfAlive()
        for x in ennemiList:
            if self.hitBox.colliderect(x):
                self.soundHurt.play()
                print(f"{self.hp}")
            else:
                pass

    def move(self):
        self.hitBox.move_ip(self.velocityX*self.speed, self.velocityY*self.speed)


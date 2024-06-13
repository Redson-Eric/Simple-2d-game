import pygame as p

class Player:
    def __init__(self):
        self.image = p.image.load("resource/player.png")
        self.hitBox = self.image.get_rect()
        self.velocityX = 0
        self.velocityY = 0
        self.hp = 100
        self.speed = 3

    def draw(self, surface):
        surface.blit(self.image, self.hitBox)

    def move(self):
        self.hitBox.move_ip(self.velocityX*self.speed, self.velocityY*self.speed)

import pygame as p

class Bot:
    def __init__(self):
        self.image = p.image.load("resource/ennemi.png")
        self.hitBox = self.image.get_rect()
        self.velocityX = 0
        self.velocityY = 0
        self.speed = 2
        self.hp = 10
        self.damage = 10

    def draw(self, surface):
        surface.blit(self.image, self.hitBox)
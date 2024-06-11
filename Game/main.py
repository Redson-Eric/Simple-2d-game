import pygame as p
from time import sleep
from random import randint
from player import Player

class Game:
    def __init__(self,titre):
        self.fps = p.time.Clock()

        self.state = 1
        p.display.set_caption(titre)
        self.screen = p.display.set_mode((720,480))
        self.player = Player("Me")

    def keyEvent(self):
        keys = p.key.get_pressed()
        #### Y
        if keys[p.K_z]:
            self.player.velocityY = -1
        elif keys[p.K_s]:
            self.player.velocityY = 1
        else:
            self.player.velocityY = 0
        #########X
        if keys[p.K_q]:
            self.player.velocityX = -1
        elif keys[p.K_d]:
            self.player.velocityX = 1
        else:
            self.player.velocityX = 0

    def drawScreen(self):
        self.screen.fill((0,0,0))
        self.player.draw(self.screen)
        self.player.move()



    def updateScreen(self):
        p.display.flip()

    def start(self):
        while self.state == 1:
            for ev in p.event.get():
                if ev.type == p.QUIT:
                    self.state = 0
                else:
                    continue
            self.fps.tick(60)
            self.keyEvent()
            self.drawScreen()
            self.updateScreen()


game = Game("My 2d game")
game.start()

p.quit()
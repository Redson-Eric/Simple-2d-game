import pygame as p
from time import sleep
from random import randint
from player import Player
from ennemi import Bot

class Game:
    def __init__(self):
        self.fps = p.time.Clock()
        p.display.set_caption("Simple 2d Game")
        self.state = 1
        self.manche = 1
        self.ennemiList = []
        self.screen = p.display.set_mode((720,480))
        self.player = Player()
    def keyEvent(self):
        limitWidth = self.screen.get_width()
        limitHeight = self.screen.get_height()
        keys = p.key.get_pressed()
        #### Y
        playerTop = self.player.hitBox.top
        playerLeft = self.player.hitBox.left
        playerRight = self.player.hitBox.right
        playerBottom = self.player.hitBox.bottom

        if keys[p.K_z] and playerTop>0:
            self.player.velocityY = -1
        elif keys[p.K_s] and playerBottom<limitHeight:
            self.player.velocityY = 1
        else:
            self.player.velocityY = 0
        #########X
        if keys[p.K_q] and playerLeft>0:
            self.player.velocityX = -1
        elif keys[p.K_d] and playerRight<limitWidth:
            self.player.velocityX = 1
        else:
            self.player.velocityX = 0

    def spawnBot(self,n):
        width = self.screen.get_width()
        height = self.screen.get_height()
        ### bot making
        nbrEnnemi = len(self.ennemiList);
        if nbrEnnemi <= 0:
            for x in range(n):
                randomX = randint(20, width - 20)
                randomY = randint(20, height - 20)
                n = Bot()
                n.hitBox.centerx = randomX
                n.hitBox.centery = randomY
                self.ennemiList.append(n)
        ### bot spawning
        else:
            for bot in self.ennemiList:
                bot.draw(self.screen)




    def drawScreen(self):
        self.screen.fill((0,0,0))
        self.player.draw(self.screen)
        self.player.move()
        self.spawnBot(5)



    def updateScreen(self):
        p.display.flip()
        self.fps.tick(60)

    def start(self):
        while self.state == 1:
            for ev in p.event.get():
                if ev.type == p.QUIT:
                    self.state = 0
                else:
                    continue

            self.keyEvent()
            self.drawScreen()
            self.updateScreen()


game = Game()
game.start()

p.quit()
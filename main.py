import pygame
import pygame as p
import keyboard as k
from time import sleep
from random import randint
from player import Player
from ennemi import Bot
import math
class Game:
    def __init__(self):
        self.fps = p.time.Clock()
        p.display.set_caption("Simple 2d Game")
        self.state = 1
        self.crosshair = p.image.load("resource/cr.png")
        self.crosshairBox = self.crosshair.get_rect()
        self.manche = 1
        self.ennemiList = []
        self.ennemiHitBox = []
        self.mouseX = 0
        self.mouseY = 0
        self.screen = p.display.set_mode((720,480))
        self.deadScreen = p.image.load("resource/dead.png")
        self.deadScreenRect = self.deadScreen.get_rect()
        self.player = Player()
        self.player.hitBox.centerx = 720/2
        self.player.hitBox.centery = 480/2
    def keyEvent(self):
        self.player.doDammage(self.ennemiHitBox)
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
        #############"
        if keys[p.K_r] and self.player.isAlive == False:
            print("restart")
            self.restart()
        elif keys[p.K_ESCAPE]:
            self.state = 0

    def spawnBot(self,n):
        width = self.screen.get_width()
        height = self.screen.get_height()
        ### bot making
        nbrEnnemi = len(self.ennemiList)

        if nbrEnnemi <= 0:
            for x in range(n):
                randomX = randint(0, width)
                randomY = randint(-20, 0) or randint(480, 500)
                n = Bot()
                n.hitBox.centerx = randomX
                n.hitBox.centery = randomY
                ### BotFamily
                self.ennemiHitBox.append(n.hitBox)
                self.ennemiList.append(n)
                self.manche += 1
        ### bot spawning + move
        else:
            for bot in self.ennemiList:
                if bot.isAlive and self.player.isAlive:
                    bot.draw(self.screen)
                    bot.chase(self.player)
                    bot.checkCollision(self.ennemiHitBox)
                    bot.checkCollisionToPlayer(self.player)
                    bot.move()

                else:
                    self.ennemiList.remove(bot)
                    self.ennemiHitBox.remove(bot.hitBox)
                    del bot

    def deleteAllBot(self):
        nbr = len(self.ennemiList)
        if nbr>0:
            for bot in self.ennemiList:
                self.ennemiList.remove(bot)
                self.ennemiHitBox.remove(bot.hitBox)
                del bot
        else:
            pass

    def restart(self):
        self.deleteAllBot()
        self.player.isAlive = True
        self.player.hp = 20
        self.player.hitBox.centerx = 720/2
        self.player.hitBox.centery = 480/2


    def drawScreen(self):
        self.screen.fill((0,0,0))
        self.player.draw(self.screen)
        self.player.move()
        self.spawnBot(8)
        self.screen.blit(self.crosshair, self.crosshairBox)
        if (self.player.isAlive == False):
            self.screen.blit(self.deadScreen, self.deadScreenRect)
            self.deleteAllBot()

    def getRotateAngle(self, x, y):
        angleRadian = math.atan2(y, x)
        angleDegree = angleRadian * (180/math.pi)
        angleDegree *= -1
        return angleDegree
    def updateScreen(self):

        p.display.flip()
        self.mouseX = p.mouse.get_pos()[0]
        self.mouseY = p.mouse.get_pos()[1]
        self.crosshairBox.centerx = self.mouseX
        self.crosshairBox.centery = self.mouseY
        self.player.angle = self.getRotateAngle(self.mouseX - self.player.hitBox.centerx, self.mouseY - self.player.hitBox.centery)
        print(f"L angle est : {self.player.angle}")

        p.mouse.set_visible(False)

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

pygame.init()
pygame.mixer.init()

game = Game()
game.start()
sleep(0.5)

p.quit()
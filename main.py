import pygame
import pygame as p
from time import sleep
from random import randint
from player import Player
from ennemi import Bot
import math

class Game:

    def __init__(self):
        """Setup Game Environments"""
        self.fps = p.time.Clock()
        p.display.set_caption("Simple 2d Game")

        # a boolean running state 
        self.state = 1

        # setup crosshair
        self.crosshair = p.image.load("resource/cr.png")
        self.crosshairBox = self.crosshair.get_rect()

        # setup enemi
        self.manche = 1
        self.ennemiList = []
        self.ennemiHitBox = []

        # mouse coordinates
        self.mouseX = 0
        self.mouseY = 0

        self.screen = p.display.set_mode((720,480))

        # setup dead's screen
        self.deadScreen = p.image.load("resource/dead.png")
        self.deadScreenRect = self.deadScreen.get_rect()

        # create player in the center of the screen
        self.player = Player()
        self.player.hitBox.centerx = self.screen.get_width()/2
        self.player.hitBox.centery = self.screen.get_height()/2

    def keyEvent(self):
        """
        Control player directions
        and Game options (quit and restart)
        """

        # Is player actually under attack or not
        # Play sound if that is the case
        self.player.doDammage(self.ennemiHitBox)
        
        # Get current screen size
        limitWidth = self.screen.get_width()
        limitHeight = self.screen.get_height()

        keys = p.key.get_pressed()
        playerTop = self.player.hitBox.top
        playerLeft = self.player.hitBox.left
        playerRight = self.player.hitBox.right
        playerBottom = self.player.hitBox.bottom

        #### Y
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

        # Game options
        if keys[p.K_r] and self.player.isAlive == False:
            # Restart
            self.restart()
        elif keys[p.K_ESCAPE]:
            # Leave Game
            self.state = 0

    def spawnBot(self, n: int) -> None:
        """
        Attempt to spawn or update and draw bots.

        Parameters
        ----------
        n: number of bots to generate

        Note
        ----
        Bots only spawn when there is no more bot actually
        """
        width = self.screen.get_width()
        height = self.screen.get_height()
        ### bot making
        nbrEnnemi = len(self.ennemiList)

        if nbrEnnemi <= 0:
            for x in range(n):
                # Random coordinate for the new bot
                randomX = randint(0, width)
                randomY = randint(-20, 0) or randint(480, 500)
                
                b = Bot()
                b.hitBox.centerx = randomX
                b.hitBox.centery = randomY

                # Insert new bot into the game
                self.ennemiHitBox.append(b.hitBox)
                self.ennemiList.append(b)
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
        """
        Draw game objects in the screen.
        And update player and bots
        """

        # Draw player
        self.screen.fill((0,0,0))
        self.player.draw(self.screen)
        self.screen.blit(self.crosshair, self.crosshairBox)

        # Update player and attempt to spawn or move bots
        self.player.move()
        self.spawnBot(8)

        # Draw dead screen when player deads
        if (self.player.isAlive == False):
            self.screen.blit(self.deadScreen, self.deadScreenRect)
            # Delete bots
            self.deleteAllBot()

    @staticmethod
    def getRotateAngle(x: float, y: float):
        """
        Get angle between two coordinates.
        
        Parameters:
        -----------
        x: Difference in x
        y: Difference in y

        Return:
        -------
        The angle in degree founded
        """
        angleRadian = math.atan2(y, x)
        angleDegree = angleRadian * (180/math.pi)
        angleDegree *= -1
        return angleDegree
    
    def updateScreen(self):
        """Update: screen and player angle"""
        p.display.flip()
        self.mouseX = p.mouse.get_pos()[0]
        self.mouseY = p.mouse.get_pos()[1]

        # update crosshair positions
        self.crosshairBox.centerx = self.mouseX
        self.crosshairBox.centery = self.mouseY

        self.player.angle = self.getRotateAngle(self.mouseX - self.player.hitBox.centerx, self.mouseY - self.player.hitBox.centery)

        p.mouse.set_visible(False)

        self.fps.tick(60)

    def start(self):
        """
        Starting point in this game.
        It is the main loop for which we listen for events and its response,
        and the main update.
        """
        while self.state == 1:
            for ev in p.event.get():
                if ev.type == p.QUIT:
                    self.state = 0
                else:
                    continue

            self.keyEvent()
            self.drawScreen()
            self.updateScreen()

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    game = Game()
    game.start()
    sleep(0.5)

    p.quit()
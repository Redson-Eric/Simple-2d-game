import pygame
import pygame as p
from random import randint, uniform
from player import Player
from ennemi import Bot
from vector import *

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

        # mouse coordinates
        self.mousepos = Vector(*p.mouse.get_pos())

        self.screen_width = Vector(1024,780)
        self.screen = p.display.set_mode((self.screen_width.x, self.screen_width.y))

        # setup dead's screen
        self.deadScreen = p.image.load("resource/dead.png")
        self.deadScreenRect = self.deadScreen.get_rect()
        self.deadScreenRect.x = (self.screen_width.x - self.deadScreenRect.w)/2
        self.deadScreenRect.y = (self.screen_width.y - self.deadScreenRect.h)/2

        # create player in the center of the screen
        self.player = Player()
        self.player.position = Vector(self.screen_width.x/2, self.screen_width.y/2)

    def keyEvent(self):
        """
        Control player directions
        and Game options (quit and restart)
        """

        # Is player actually under attack or not
        # Play sound if that is the case
        self.player.doDammage(self.ennemiList)

        keys = p.key.get_pressed()

        # Y
        if not self.player.hitBox.colliderect(self.crosshairBox):
            if (keys[p.K_z] or keys[p.K_UP]):
                self.player.move_forward(self.mousepos)
            elif (keys[p.K_s] or keys[p.K_DOWN]):
                self.player.move_backward(self.mousepos)

            # X
            if (keys[p.K_q] or keys[p.K_LEFT]):
                self.player.move_left(self.mousepos)
            elif (keys[p.K_d] or keys[p.K_RIGHT]):
                self.player.move_right(self.mousepos)

        # Game options
        if keys[p.K_r] and self.player.isAlive == False:
            # Restart
            self.restart()
        elif keys[p.K_ESCAPE]:
            # Leave Game
            self.state = 0

    def spawn_bots(self, n: int) -> None:
        """
        Spawn n bot

        Parameters
        ----------
        n: number of bots to generate
        """
        for i in range(n):
            # Random coordinate for the new bot
            randomX = uniform(0, self.screen_width.x)
            randomY = uniform(-200, 0) if randint(0, 1) else randint(self.screen_width.y, self.screen_width.y + 500)
            
            b = Bot()
            b.position = Vector(randomX, randomY)

            # Insert new bot into the game
            self.ennemiList.append(b)

    def deleteAllBot(self):
        for bot in self.ennemiList:
            self.delete_bot(bot)

    def delete_bot(self, bot: Bot):
        self.ennemiList.remove(bot)
        del bot

    def restart(self):
        self.deleteAllBot()
        self.player.isAlive = True
        self.player.hp = 20
        self.player.position = self.screen_width/2

    def drawScreen(self):
        """
        Draw game objects in the screen.
        And update player and bots
        """

        

        # attempt to spawn or move bots
        self.spawnBot(20)

        
        if (self.player.isAlive == False):
    
            # Delete bots
            self.deleteAllBot()

    def draw(self):
        # Draw player
        self.screen.fill((0,0,0))
        self.player.draw(self.screen)
        self.screen.blit(self.crosshair, self.crosshairBox)

        # Draw dead screen when player deads
        if not self.player.isAlive:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.deadScreen, self.deadScreenRect)
        else:
            for bot in self.ennemiList:
                if bot.isAlive: bot.draw(self.screen)

        p.display.flip()

    def update(self):
        self.mousepos = Vector(*p.mouse.get_pos())

        # crosshair positions
        self.crosshairBox.centerx = self.mousepos.x
        self.crosshairBox.centery = self.mousepos.y

        # Player and bots
        if self.player.isAlive:
            # set player angle
            if not self.player.hitBox.colliderect(self.crosshairBox): self.player.looking_angle = (self.mousepos - Vector(self.player.hitBox.centerx, self.player.hitBox.centery)).get_angle()

            for bot in self.ennemiList:
                if bot.isAlive:
                    bot.chase(self.player)
                    bot.move()
                    bot.checkCollisionToPlayer(self.player)
                    bot.checkCollision(self.ennemiList)
                else: self.delete_bot(bot)

        else: self.deleteAllBot()

        if len(self.ennemiList) == 0 and self.player.isAlive: self.spawn_bots(20)

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

            self.draw()
            self.keyEvent()
            self.update()
            p.mouse.set_visible(False)
            self.fps.tick(60)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    game = Game()
    game.start()

    p.quit()
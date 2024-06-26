import pygame as p

class Player:
    def __init__(self):
        self.image = p.image.load("resource/player.png")
        self.hitBox = self.image.get_rect() # Player position
        self.soundHurt = p.mixer.Sound("sound/playerHurt.mp3")

        # Direction vectors
        self.velocityX = 0
        self.velocityY = 0
        
        self.hp = 20    # Player health
        self.speed = 3
        self.isAlive = True
        self._angle = 0.0

    def draw(self, surface):
        #rotateImage = p.transform.rotate(self.image, 90)
        #self.image = rotateImage
        rotated_image = p.transform.rotate(self.image, self.angle)
        surface.blit(rotated_image, self.hitBox)

    def checkIfAlive(self):
        if self.hp <=0:
            self.isAlive = False
        else:
            pass

    def doDammage(self, ennemiList):
        # FIXME: The next code is currently useless
        self.checkIfAlive()

        for x in ennemiList:
            if self.hitBox.colliderect(x):
                self.soundHurt.play()
            else:
                pass

    def move(self):
        """Move player dependend on his directional vectors"""
        self.hitBox.move_ip(self.velocityX*self.speed, self.velocityY*self.speed)

    # Getter and setter for player angle
    @property
    def angle(self): return self._angle

    @angle.setter
    def angle(self, degree: float):
        """
        Changle player image angle
        by setting from the top center of 
        an imaginary circle in the image(90deg)
        """
        self._angle = degree - 90.0


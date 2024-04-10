import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Bullets to fire'''

    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #create a bullet at 0,0 and move later
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop

        self.y=float(self.rect.y)

    def update(self):
        '''Update the bullet position '''
        self.y -= self.settings.bullet_speed
        
        # Update the rect
        self.rect.y = self.y

    def draw_bullet(self):
        '''Draw the bullet'''
        pygame.draw.rect(self.screen,self.color,self.rect)
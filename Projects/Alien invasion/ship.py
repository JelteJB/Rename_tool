import pygame

class Ship:
    '''A class to handle the ship'''

    def __init__(self,ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings=ai_game.settings
        #Load image
        self.image=pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # start at the bottom
        self.rect.midbottom=self.screen_rect.midbottom

        # Location
        self.x = float(self.rect.x)

        # Moving
        self.moving_left = False
        self.moving_right = False

    def update(self):
        '''Update the ships position '''
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Update the rect
        self.rect.x = self.x
        
    def update_loc_after_screen_resize(self,ai_game):
        self.screen_rect = ai_game.screen.get_rect()
        self.rect.bottom = self.screen_rect.bottom


    def blitme(self):
        '''Draw ship'''
        self.screen.blit(self.image,self.rect)
        
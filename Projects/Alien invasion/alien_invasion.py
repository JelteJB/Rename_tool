import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    '''Overall class to manage game assets and behavior'''

    def __init__(self):
        '''Initialize the game and create game resources'''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings=Settings()
        
        if self.settings.screen_width and self.settings.screen_height:
            self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        else:
            self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
            self.settings.screen_width=self.screen.get_rect().width
            self.settings.screen_height=self.screen.get_rect().height

        pygame.display.set_caption("Alien invasion")
        self.ship=Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        
    def run_game(self):
        '''Start the main game loop'''
        while True:
            self._check_events()
            self.ship.update()
            self._check_aliens()
            self._check_bullets()
            self._update_screen()
            self.clock.tick(60)



    def _create_fleet(self):
        '''Make alien fleet'''
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        current_y=alien_height

        while current_y < (self.settings.screen_height - 3* alien_height):
            self._create_alien_row(current_y,alien_width)
            current_y +=2*alien_width
        

    def _create_alien_row(self,y_pos,alien_width):
        '''Create a row of aliens'''
        current_x=alien_width
        while current_x < (self.settings.screen_width - 2 * alien_width):
            self._create_alien(current_x,y_pos)
            current_x +=2*alien_width

    def _create_alien(self,x_pos,y_pos):
        '''Create single alien for fleet'''
        new_alien = Alien(self)
        new_alien.x=x_pos
        new_alien.rect.y=y_pos
        new_alien.rect.x=x_pos
        self.aliens.add(new_alien)

    def _check_alien_drop(self):
        '''Check if any alien is at the edge'''
        for alien in self.aliens:
            if (alien.rect.right > self.settings.screen_width - 0.1 * alien.rect.width) or (alien.rect.left < 0.1 * alien.rect.width):
                return True
        return False

    def _check_aliens(self):
        '''Check if the alien need to drop'''
        drop = self._check_alien_drop()
        if drop:
            # If drop, also change direction
            self.settings.alien_direction = - self.settings.alien_direction 
        self.aliens.update(drop)
        

    def _check_bullets(self):
        '''Check the location of all the bullets'''
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        
        # Collisions
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,not self.settings.bullet_high_power,True)

        

    def _check_events(self):
        '''Watch for I/O events'''
        for event in pygame.event.get():
            match (event.type): 
                case pygame.QUIT:
                    sys.exit()
 
                case pygame.KEYDOWN:
                    self._check_keyupdown_event(event,True)

                case pygame.KEYUP:
                    self._check_keyupdown_event(event,False)
                

    def _check_keyupdown_event(self,event,bool=False):
        '''Respond to key up down events'''
        match (event.key):
            case pygame.K_RIGHT:
                # Move ship to right
                self.ship.moving_right = bool
            case pygame.K_LEFT:
                # Move ship to left
                self.ship.moving_left = bool
            case pygame.K_q:
                # Quit game
                if bool:
                    sys.exit()
            
            case pygame.K_F11:
                if bool:
                    self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                    self.settings.screen_width=self.screen.get_rect().width
                    self.settings.screen_height=self.screen.get_rect().height
                    self.ship.update_loc_after_screen_resize(self)
            case pygame.K_F10:
                if bool:
                    self.settings.normal_setting()
                    self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
                    self.ship.x=self.settings.screen_width//2
                    self.ship.update_loc_after_screen_resize(self)
            case pygame.K_SPACE:
                if bool:
                    self._fire_bullet()


    def _fire_bullet(self):
        '''Adding a bullet to the list'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        ''' Draw screen and items '''
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    # Make game instance and run
    ai=AlienInvasion()
    ai.run_game()

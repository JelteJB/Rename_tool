class Settings:
    '''A Class to store all AlienInvasion settings'''

    def __init__(self) -> None:
        '''Init the settings'''

        # Demo settings
        self.demo_mode=False

        # Screen settings
        self.normal_setting()
        self.bg_color = (230,230,230)


        #ship Settings
        self.ship_speed = 1.5

        # Bullet Settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3
        self.bullet_high_power=False
        if self.demo_mode:
            self._set_normal_mode()
        else:
            self._set_demo_mode()
            

        # Alien Settings
        self.alien_speed = 1.0
        self.alien_drops = 10

        # Direction 1 -> Right and -1 -> Left
        self.alien_direction = 1 

       
        if self.demo_mode:
            self._set_demo_mode()

    def _set_demo_mode(self):
        self.bullet_high_power=True
        self.bullet_width=300
        self.bullets_allowed = 10000

    def _set_normal_mode(self):
        self.bullet_width = 3
        self.bullets_allowed = 3
        self.bullet_high_power=False

    def normal_setting(self):
        self.screen_width = 1200
        self.screen_height = 800
        
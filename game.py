import logging
import pygame
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Konstanter
FPS = 60
SCREEN_SIZE = (800, 600)
CAPTION = "Pygame Example"

COLOR = {'ship': pygame.Color('#FF0000'),
         'ship_fill': pygame.Color('#660000'),
         'bg': pygame.Color('#333333'),
         'bg_pause': pygame.Color('#DD3333'),
         'thruster': pygame.Color('#7799FF'),
         'fuel_green': pygame.Color('#33cc33'),
         'fuel_yellow': pygame.Color('#ffff00'),
         'fuel_red': pygame.Color('#ff0000'),
         'text_color': pygame.Color('#000000'),
}

# Game states
STATE_PREGAME = 1
STATE_RUNNING = 2
STATE_PAUS = 3
STATE_GAMEOVER = 4



class Controller():
    """Game controller."""

    def __init__(self):
        """Initialize game controller."""
        self.fps = FPS

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.player = Player(self.screen)

        # Initialize game state
        self.game_state = STATE_PREGAME
        self.next_state = None

        self.large_text = pygame.font.SysFont("comicsansms",110)

    def run(self):
        """Main game loop."""
        while True:
            if self.next_state:
                self.game_state = self.next_state
                self.next_state = None
                logger.info('Changning state to {}'.format(self.game_state))

            # Hantera event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # ALT + F4 or icon in upper right corner.
                    self.quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Escape key pressed.
                    self.quit()


                # -- Game state PREGAME --------------------------------------
                if self.game_state == STATE_PREGAME:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.next_state = STATE_RUNNING


                # -- Game state RUNNING --------------------------------------
                if self.game_state == STATE_RUNNING:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        self.next_state = STATE_PAUS
                        logger.debug('Pausing')

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                        self.player.engine_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_w:
                        self.player.engine_off()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                        self.player.right_thruster_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_a:
                        self.player.right_thruster_off()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                        self.player.left_thruster_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_d:
                        self.player.left_thruster_off()


                # -- Game state PAUS -----------------------------------------
                if self.game_state == STATE_PAUS:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        self.player.toggle_engine()

                        self.next_state = STATE_RUNNING
                        logger.debug('Unpausing')

                # -- Game state GAMEOVER -------------------------------------
                if self.game_state == STATE_GAMEOVER:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.next_state = STATE_RUNNING
                        self.player.reset()



            # Hantera speltillstånd
            if self.game_state == STATE_PREGAME:
                self.screen.fill(COLOR['bg_pause'])
                text = self.large_text.render("Press here to start", True, COLOR['text_color'] )
                pos = (SCREEN_SIZE[0] / 2 - text.get_width() / 2,
                        SCREEN_SIZE[1] / 2 - text.get_height() / 2)
                self.screen.blit(text, pos)



            if self.game_state == STATE_RUNNING:
                self.player.tick()

                if self.player.y > SCREEN_SIZE[1] - 10 or self.player.y < 10:
#                    logger.debug('OUT OF BOUNDS!')
                        self.game_state = STATE_GAMEOVER
                if self.player.x > SCREEN_SIZE[0] - 5 or self.player.x < 5:
#                    logger.debug('OUT OF BOUNDS!')
                    self.game_state = STATE_GAMEOVER
                self.screen.fill(COLOR['bg'])
                self.player.draw()


            if self.game_state == STATE_PAUS:

                self.screen.fill(COLOR['bg_pause'])
                text = self.large_text.render("Game paused", True, COLOR['text_color'] )
                pos = (SCREEN_SIZE[0] / 2 - text.get_width() / 2,
                        SCREEN_SIZE[1] / 2 - text.get_height() / 2)
                self.screen.blit(text, pos)


            if self.game_state == STATE_GAMEOVER:
                        self.screen.fill(COLOR['bg_pause'])
                        text = self.large_text.render("Game over|r to reset", True, COLOR['text_color'] )
                        pos = (SCREEN_SIZE[0] / 2 - text.get_width() / 2,
                                SCREEN_SIZE[1] / 2 - text.get_height() / 2)
                        self.screen.blit(text, pos)


                #self.quit()  # Gör något bättre.

            pygame.display.flip()

            self.clock.tick(self.fps)


    def quit(self):
        logging.info('Quitting... good bye!')
        pygame.quit()
        sys.exit()

    def paus(self):
        pass



class Player():
    def __init__(self, screen):
        self.x = SCREEN_SIZE[0] / 2
        self.y = SCREEN_SIZE[1] / 2
        self.screen = screen
        self.engine = False
        self.left_thruster = False
        self.right_thruster = False
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0.1
        self.fuel = 100

    def draw(self):
        surface = pygame.Surface((20, 20))
        screen = pygame.Surface((800, 600))
        surface.fill(COLOR['bg'])
        pygame.draw.polygon(surface, COLOR['ship_fill'], ((10, 0), (15, 15), (5, 15)), 0)
        pygame.draw.polygon(surface, COLOR['ship'], ((10, 0), (15, 15), (5, 15)), 1)

        if self.engine:
            pygame.draw.polygon(surface, COLOR['thruster'], ((13, 16), (10, 19), (7, 16)), 0)

        if self.left_thruster:
            pygame.draw.polygon(surface, COLOR['thruster'], ((6, 12), (5, 14), (2, 13), (6, 12), 0))

        if self.right_thruster:
            pygame.draw.polygon(surface, COLOR['thruster'], ((14, 12), (15, 14), (18, 13), (14, 12), 0))
        if self.fuel:
            pygame.draw.rect(self.screen, COLOR[self.fuel_color], (680, 30, self.fuel, 10))




        self.screen.blit(surface, (self.x - 10, self.y - 10))
    def toggle_engine(self):
        #--- turn the engines off when game_state = paused
        self.engine = False
        self.left_thruster = False
        self.right_thruster = False

    def reset(self):
        #--- resets the game when restarting
            self.x = SCREEN_SIZE[0] / 2
            self.y = SCREEN_SIZE[1] / 2
            self.engine = False
            self.left_thruster = False
            self.right_thruster = False
            self.x_speed = 0
            self.y_speed = 0
            self.fuel = 100

    def tick(self):
        # -- Y-axis control
        if self.engine:
            self.y_speed -= 0.01
        else:
            self.y_speed += 0.01

        self.y = self.y + self.y_speed + self.gravity

        # -- X-axis control
        if self.left_thruster:
            self.x_speed += 0.05

        if self.right_thruster:
            self.x_speed -= 0.05

        self.x_speed = self.x_speed * 0.99

        self.x = self.x + self.x_speed

        # -- fuel bar
        if self.fuel > 50:
            self.fuel_color = 'fuel_green'
        elif self.fuel > 25:
            self.fuel_color = 'fuel_yellow'
        else:
            self.fuel_color = 'fuel_red'

        # -- fuel usage
        if self.engine == True:
            self.fuel -= 0.05
        if self.left_thruster == True:
                self.fuel -= 0.008
        if self.right_thruster == True:
                self.fuel -= 0.008
        if self.fuel < 0:
            self.fuel = 0
            self.engine = False
            self.left_thruster = False
            self.right_thruster = False


    def engine_on(self):
        self.engine = True

    def engine_off(self):
        self.engine = False

    def left_thruster_on(self):
        self.left_thruster = True

    def left_thruster_off(self):
        self.left_thruster = False

    def right_thruster_on(self):
        self.right_thruster = True

    def right_thruster_off(self):
        self.right_thruster = False

if __name__ == "__main__":
    logger.info('Starting...')
    c = Controller()
    c.run()

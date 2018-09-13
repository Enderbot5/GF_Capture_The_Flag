from GameFrame import Bot, Globals
import random


class BlueBot(Bot):
    def __init__(self, room, x, y):
        Bot.__init__(self, room, x, y)
        blue_bot_image = self.load_image('bot_blue.png')
        self.set_image(blue_bot_image, 16, 16)

        self.rotate(-90)

        self.register_collision_object('Red1')
        self.register_collision_object('BlueFlag')

    def frame(self):
        if self.has_flag:
            Globals.blue_flag.x = self.x + 21
            Globals.blue_flag.y = self.y

            if Globals.blue_flag.x <= 0:
                Globals.blue_flag.x = 0
                self.x = self.prev_x
                self.y = self.prev_y
            elif Globals.blue_flag.rect.right >= Globals.SCREEN_WIDTH:
                Globals.blue_flag.x = Globals.SCREEN_WIDTH - Globals.blue_flag.rect.width
                self.x = self.prev_x
                self.y = self.prev_y

            if Globals.blue_flag.y <= 0:
                Globals.blue_flag.y = 0
                self.x = self.prev_x
                self.y = self.prev_y
            elif Globals.blue_flag.rect.bottom >= Globals.SCREEN_HEIGHT:
                Globals.blue_flag.y = Globals.SCREEN_HEIGHT - Globals.blue_flag.rect.height
                self.x = self.prev_x
                self.y = self.prev_y

        self.tick()

    def tick(self):
        pass

    def handle_collision(self, other):
        other_type = type(other).__name__
        if other_type == 'BlueFlag':
            self.has_flag = True
        elif other_type == 'RedFlag':
            pass
        else:
            if self.rect.right > Globals.SCREEN_WIDTH / 2:
                self.has_flag = False
                self.curr_rotation = 0
                self.rotate(-90)
                self.x = self.starting_x
                self.y = random.randint(50, 550)



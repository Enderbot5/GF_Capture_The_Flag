from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    RETURN_HOME = 3


class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)

        self.curr_state = STATE.WAIT

    def tick(self):

        if self.curr_state == STATE.WAIT:
            self.wait()
        elif self.curr_state == STATE.ATTACK:
            self.attack()
        elif self.curr_state == STATE.RETURN_HOME:
            self.return_home()
        else:
            self.curr_state = STATE.RETURN_HOME

    def wait(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
            self.curr_state = STATE.ATTACK

    def attack(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
            self.turn_towards(bot.x, bot.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.curr_state = STATE.RETURN_HOME

    def return_home(self):
        self.turn_towards(self.starting_x, self.starting_y, Globals.FAST)
        self.drive_forward(Globals.FAST)
        if abs(self.x - self.starting_x) < 20 and abs(self.y - self.starting_y) < 20:
            self.curr_state = STATE.WAIT
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
            self.curr_state = STATE.ATTACK

    def closest_enemy_to_flag(self):
        closest_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         Globals.blue_flag.x, Globals.blue_flag.y)
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         Globals.blue_flag.x, Globals.blue_flag.y)
            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance

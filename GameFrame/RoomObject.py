import math
import os
import pygame
import math


class RoomObject:

    def __init__(self, room, x, y):
        self.room = room
        self.depth = 0
        self.x = x
        self.y = y
        self.rect = 0
        self.prev_x = x
        self.prev_y = y
        self.width = 0
        self.height = 0
        self.image = 0
        self.image_orig = 0
        self.curr_rotation = 0
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0
        self.handle_key_events = False
        self.handle_mouse_events = False
        self.angle = 0

        self.collision_object_types = set()
        self.collision_objects = []

    def load_image(self, file_name):
        '''
        Loads an image to be used as a sprite\n
        Takes 1 argument: file_name\n
        the file is searched for in the Images folder
        '''
        return os.path.join('Images', file_name)

    def set_image(self, image, width, height):
        '''
        Sets a sprite's image\n
        takes 3 arguments: image, width, and height\n
        image has to be loaded using the self.load_image() function\n
        width and height define the dimensions of the sprite
        '''
        self.image_orig = pygame.image.load(image).convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (width, height))
        self.width = width
        self.height = height
        self.image = self.image_orig.copy()
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def register_collision_object(self, collision_object):
        '''
        Registers a collision object\n
        Takes 1 argument: collision_object\n
        This is the class name of the object 
        '''
        self.collision_object_types.add(collision_object)

    def update(self):
        self.y_speed = self.y_speed + self.gravity
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def delete_object(self, obj):
        '''
        deletes an object\n
        takes 1 argument: obj\n
        This is the class name of the object
        '''
        self.room.delete_object(obj)

    def remove_object(self, obj):
        for index, list_obj in enumerate(self.collision_objects):
            if list_obj is obj:
                self.collision_objects.pop(index)

    def step(self):
        pass

    def check_collisions(self):
        '''
        Checks if the ovject is colliding with another object\n
        Takes no arguments
        '''
        for item in self.collision_objects:
            if self.rect.colliderect(item.rect):
                self.handle_collision(item)

    def collides_at(self, obj, x, y, collision_type):

        check_rect = obj.rect.move(x, y)
        collision_found = False
        for item in self.collision_objects:
            if check_rect.colliderect(item.rect):
                if type(item).__name__ == collision_type:
                    collision_found = True
                    break
        return collision_found

    def handle_collision(self, other):
        pass

    def key_pressed(self, key):
        pass

    def clicked(self, button_number):
        pass

    def mouse_event(self, mouse_x, mouse_y, button_left, button_middle, button_right):
        pass

    def bounce(self, other):

        # self is to the side of other
        if other.rect.top < self.rect.centery < other.rect.bottom:
            self.x_speed *= -1
            self.x = self.prev_x

        # self is above or below other
        if other.rect.left < self.rect.centerx < other.rect.right:
            self.y_speed *= -1
            self.y = self.prev_y

    def blocked(self):

        self.x = self.prev_x
        self.y = self.prev_y
        self.x_speed = 0
        self.y_speed = 0

    def set_timer(self, ticks, function_call):
        '''
        Waits a set number of ticks before running a function\n
        Takes 2 arguments: ticks, function_call\n
        After the set number of ticks, the function defined with "function_call" will be run
        '''
        self.room.set_timer(ticks, function_call)

    def set_direction(self, angle, speed):
        if angle < 0:
            pass
        elif angle == 0:
            self.x_speed = speed
            self.y_speed = 0
        elif angle < 90:
            self.x_speed, self.y_speed = self.get_direction(angle, speed)
        elif angle == 90:
            self.x_speed = 0
            self.y_speed = speed
        elif angle < 180:
            self.x_speed, self.y_speed = self.get_direction(angle - 90, speed)
            self.x_speed, self.y_speed = -self.y_speed, self.x_speed
        elif angle == 180:
            self.x_speed = -speed
            self.y_speed = 0
        elif angle < 270:
            self.x_speed, self.y_speed = self.get_direction(angle - 180, speed)
            self.x_speed, self.y_speed = -self.x_speed, -self.y_speed
        elif angle == 270:
            self.x_speed = 0
            self.y_speed = -speed
        elif angle < 360:
            self.x_speed, self.y_speed = self.get_direction(angle - 270, speed)
            self.x_speed, self.y_speed = self.y_speed, -self.x_speed

    def get_direction(self, angle, speed):
        # Use Trigonometry to calculate x_speed and y_speed values
        new_x_speed = math.cos(math.radians(angle)) * speed
        new_y_speed = math.sin(math.radians(angle)) * speed

        return round(new_x_speed), round(new_y_speed)

    def get_direction_coordinates(self, angle, speed):

        angle += 90
        if angle >= 360:
            angle = angle - 360

        if angle < 0:
            angle = 360 + angle

        if angle == 0:
            x = speed
            y = 0
        elif angle < 90:
            x, y = self.get_direction(angle + 90, speed)
            x, y = y, x
        elif angle == 90:
            x = 0
            y = -speed
        elif angle < 180:
            x, y = self.get_direction(angle, speed)
            y *= -1
        elif angle == 180:
            x = -speed
            y = 0
        elif angle < 270:
            x, y = self.get_direction(angle - 90, speed)
            y, x = -x, -y
        elif angle == 270:
            x = 0
            y = speed
        elif angle < 360:
            x, y = self.get_direction(angle - 180, speed)
            y, x = y, -x

        return x, y

    def rotate(self, angle):

        if self.curr_rotation > 360:
            self.curr_rotation = self.curr_rotation - 360
        elif self.curr_rotation < 0:
            self.curr_rotation = 350 - self.curr_rotation

        self.curr_rotation = self.angle = angle + self.curr_rotation

        self.image = pygame.transform.rotate(self.image_orig, self.angle)

        x, y = self.rect.center

        self.rect = self.image.get_rect()

        self.x = x - int((self.rect.width / 2))
        self.y = y - int((self.rect.height / 2))

        self.rect.x = self.x
        self.rect.y = self.y

    def get_rotation_to_coordinate(self, target_x, target_y):
        '''
        returns the rotation to a set of coordinates\n
        takes 2 arguments: target_x and target_y
        '''
        distance_x = self.x + (self.width / 2) - target_x
        distance_y = self.y + (self.height / 2) - target_y

        return math.degrees(math.atan2(distance_x, distance_y))

    def rotate_to_coordinate(self, target_x, target_y):
        '''
        rotates the bot towards a set of given coordinates\n
        takes 2 arguments: target_x and target_y
        '''
        self.curr_rotation = 0
        self.rotate(self.get_rotation_to_coordinate(target_x, target_y))

    def get_position(self):
        '''
        Returns the position of the bot\n
        Takes no arguments\n
        '''
        return self.x, self.y

    def move_in_direction(self, angle, distance):
        x, y = self.get_direction_coordinates(angle, distance)
        self.x += x
        self.y += y

    def point_to_point_distance(self, x1, y1, x2, y2):
        '''
        returns the distance between 2 points\n
        takes 4 arguments: x1, y1, x2, y2\n
        x1 and y1 refer to the first set of coordinates\n
        x2 and y2 refer to the second set of coordinates        
        '''
        x_dist = abs(x1 - x2)
        y_dist = abs(y1 - y2)
        return math.sqrt(x_dist * x_dist + y_dist * y_dist)


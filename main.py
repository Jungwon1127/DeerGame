"""
Deer Game

"""
#CITE: https://arcade.academy/examples/platform_tutorial/index.html
#DESC: Simple platformer guide on arcade website
#CITE: https://arcade.academy/tutorials/views/02_views.html#views
#DESC: Guide to creating different screens in python


import arcade
import random

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
PLAYER_MOVEMENT_SPEED = 5

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 64
TOP_VIEWPORT_MARGIN = 64

SCREEN_TITLE = "Deer Game"

# class ReplayButton(arcade.TextButton):
#
#
#     def __init__(self):
#
#     def check_mouse_release(self, _x, _y):
#


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        self.wall_list = None
        self.apple_list = None
        self.player_list = None
        self.enemy_list = None
        self.end_game = False
        self.lose = False

        self.player_sprite = None
        self.enemy = None

        # If you have sprite lists, you should create them here,
        # and set them to None

        self.view_bottom = 0
        self.view_left = 0

        self.apples_eaten = 0

        self.collect_apple_sound = arcade.load_sound("sounds/Minecraft-eat1.mp3")

    def setup(self):

        self.apples_eaten = 0

        # Create your sprites and sprite lists here
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.apple_list = arcade.SpriteList(use_spatial_hash=True)
        self.goal_list = arcade.SpriteList(use_spatial_hash=True)

        # Setup Deer player
        player_image = "images/deer.png"
        self.player_sprite = arcade.Sprite(player_image, 0.1)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 750
        self.player_list.append(self.player_sprite)

        #setting up the walls
        wall_coordinates = []
        wall_image = ":resources:images/tiles/boxCrate.png"
        for walls in range(-32, 833, 864):
            for x in range(0, 1400, 64):
                wall = arcade.Sprite(wall_image, .5)
                wall.center_x = x
                wall.center_y = walls
                self.wall_list.append(wall)
        for walls in range(-32, 1433, 1464):
            for y in range(0, 800, 64):
                wall = arcade.Sprite(wall_image, .5)
                wall.center_x = walls
                wall.center_y = y
                self.wall_list.append(wall)

        for coordinate in wall_coordinates:
            wall = arcade.Sprite(wall_image, .1)
            wall.center_x = coordinate[0]
            wall.center_y = coordinate[1]
            self.wall_list.append(wall)

        #setting up apples
        apple_image = "images/apple.png"

        apple_coordinates = []
        for apple in range(10):
            x = random.randint(100, 1200)
            y = random.randint(100,700)
            location = (x,y)
            apple_coordinates.append(location)

        for coordinate in apple_coordinates:
            apple = arcade.Sprite(apple_image, 0.05)
            apple.center_x = coordinate[0]
            apple.center_y = coordinate[1]
            self.apple_list.append(apple)

        #setting up goal
        goal_image = "images/dorm.png"
        goal = arcade.Sprite(goal_image, 0.2)
        goal.center_x = 1300
        goal.center_y = 100
        self.goal_list.append(goal)

        #setting up enemy
        enemy_image = "images/student.png"
        self.enemy = arcade.Sprite(enemy_image, 0.1)
        self.enemy.center_x = 600
        self.enemy.center_y = 600
        self.enemy_list.append(self.enemy)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        self.physics_engine2 = arcade.PhysicsEngineSimple(self.enemy, self.wall_list)



    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.wall_list.draw()
        self.apple_list.draw()
        self.player_list.draw()
        self.goal_list.draw()
        self.enemy_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.apples_eaten}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)

    def on_update(self, delta_time):
        """

        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.physics_engine.update()
        self.physics_engine2.update()

        # See if we hit any apples
        apple_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.apple_list)

        # Loop through each apple we hit (if any) and remove it
        for apple in apple_hit_list:
            # Remove the apple
            apple.remove_from_sprite_lists()
            self.apples_eaten += 1
            arcade.play_sound(self.collect_apple_sound)

        #see if we hit any enemies
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.enemy_list)

        if enemy_hit_list != []:
            self.end_game = True
            self.lose = True

        if self.end_game == True:
            GameView.end_game(self)


        #enemy movement
        if self.enemy.center_x < self.player_sprite.center_x:
            self.enemy.change_x = PLAYER_MOVEMENT_SPEED // 1.5
        elif self.enemy.center_x > self.player_sprite.center_x:
            self.enemy.change_x = -PLAYER_MOVEMENT_SPEED // 1.5

        if self.enemy.center_y < self.player_sprite.center_y:
            self.enemy.change_y = PLAYER_MOVEMENT_SPEED // 1.5
        elif self.enemy.center_y > self.player_sprite.center_y:
            self.enemy.change_y = -PLAYER_MOVEMENT_SPEED // 1.5

        # # --- Manage Scrolling ---
        #
        # # Track if we need to change the viewport
        #
        # changed = False
        #
        # # Scroll left
        # left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        # if self.player_sprite.left < left_boundary:
        #     self.view_left -= left_boundary - self.player_sprite.left
        #     changed = True
        #
        # # Scroll right
        # right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        # if self.player_sprite.right > right_boundary:
        #     self.view_left += self.player_sprite.right - right_boundary
        #     changed = True
        #
        # # Scroll up
        # top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        # if self.player_sprite.top > top_boundary:
        #     self.view_bottom += self.player_sprite.top - top_boundary
        #     changed = True
        #
        # # Scroll down
        # bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        # if self.player_sprite.bottom < bottom_boundary:
        #     self.view_bottom -= bottom_boundary - self.player_sprite.bottom
        #     changed = True
        #
        # if changed:
        #     # Only scroll to integers. Otherwise we end up with pixels that
        #     # don't line up on the screen
        #     self.view_bottom = int(self.view_bottom)
        #     self.view_left = int(self.view_left)
        #
        #     # Do the scrolling
        #     arcade.set_viewport(self.view_left,
        #                         SCREEN_WIDTH + self.view_left,
        #                         self.view_bottom,
        #                         SCREEN_HEIGHT + self.view_bottom)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def end_game(self):
        view = GameOverScreen()
        self.window.show_view(view)

class GameOverScreen(arcade.View):


    def __init__(self):
        super().__init__()
        self.gameover_image = arcade.load_texture("images/gameover.png")

    def on_draw(self):
        arcade.start_render()
        self.gameover_image.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self,_x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = GameView()
    window.show_view(game_view)
    game_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()

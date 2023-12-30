import pygame
import time
import random

class SnakeGame:
    def __init__(self):
        pygame.init()

        # Set up the game window
        self.width, self.height = 800, 600
        self.game_window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")

        # Define colors
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.black = (0, 0, 0)

        # Snake properties
        self.snake_block = 10
        self.snake_speed = 15

    def display_message(self, msg, color, y_displace=0, size="small"):
        font_size = {"small": 25, "medium": 40, "large": 60}
        font = pygame.font.SysFont(None, font_size[size])
        text_surface = font.render(msg, True, color)
        return text_surface, text_surface.get_rect(center=(self.width / 2, self.height / 2 + y_displace))

    def is_mouse_over_button(self, button_rect):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return button_rect.collidepoint(mouse_x, mouse_y)

    def main_menu(self):
        menu = True

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_mouse_over_button(self.play_button_rect):
                        menu = False
                    elif self.is_mouse_over_button(self.quit_button_rect):
                        pygame.quit()
                        quit()

            self.game_window.fill(self.black)

            welcome_text, welcome_text_rect = self.display_message("Welcome to Snake Game", self.white, -50, "large")
            self.game_window.blit(welcome_text, welcome_text_rect)

            # Draw Play Button
            self.play_button_rect = pygame.draw.rect(self.game_window, self.green, [150, 450, 100, 50])
            play_text, play_text_rect = self.display_message("Play", self.black, 0, "medium")
            self.game_window.blit(play_text, (150 + (100 - play_text_rect.width) // 2, 450 + (50 - play_text_rect.height) // 2))

            # Draw Quit Button
            self.quit_button_rect = pygame.draw.rect(self.game_window, self.red, [550, 450, 100, 50])
            quit_text, quit_text_rect = self.display_message("Quit", self.black, 0, "medium")
            self.game_window.blit(quit_text, (550 + (100 - quit_text_rect.width) // 2, 450 + (50 - quit_text_rect.height) // 2))
            
            pygame.display.update()

    def game_loop(self):
        game_over = False
        game_close = False

        x1, y1 = self.width / 2, self.height / 2
        x1_change, y1_change = 0, 0

        snake_list = []
        length_of_snake = 1

        foodx, foody = round(random.randrange(0, self.width - self.snake_block) / 10.0) * 10.0, round(random.randrange(0, self.height - self.snake_block) / 10.0) * 10.0

        score = 0

        while not game_over:

            while game_close:
                self.game_window.fill(self.black)
                
                score_text, score_text_rect = self.display_message("Your Score: {}".format(score), self.white, 50, "medium")
                self.game_window.blit(score_text, score_text_rect)

                # Draw Play Again Button
                play_again_button_rect = pygame.draw.rect(self.game_window, self.green, [150, 450, 200, 50])
                play_again_text, play_again_text_rect = self.display_message("Play Again", self.black, 0, "medium")
                self.game_window.blit(play_again_text, (150 + (200 - play_again_text_rect.width) // 2, 450 + (50 - play_again_text_rect.height) // 2))

                # Draw Quit Button
                quit_button_rect = pygame.draw.rect(self.game_window, self.red, [550, 450, 100, 50])
                quit_text, quit_text_rect = self.display_message("Quit", self.black, 0, "medium")
                self.game_window.blit(quit_text, (550 + (100 - quit_text_rect.width) // 2, 450 + (50 - quit_text_rect.height) // 2))


                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        elif event.key == pygame.K_c:
                            self.game_loop()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.is_mouse_over_button(play_again_button_rect):
                            self.game_loop()
                        elif self.is_mouse_over_button(quit_button_rect):
                            pygame.quit()
                            quit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -self.snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = self.snake_block
                        x1_change = 0

            if x1 >= self.width or x1 < 0 or y1 >= self.height or y1 < 0:
                game_close = True

            x1 += x1_change
            y1 += y1_change
            self.game_window.fill(self.black)

            pygame.draw.rect(self.game_window, self.white, [foodx, foody, self.snake_block, self.snake_block])

            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

            self.our_snake(snake_list)
            self.your_score(length_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx, foody = round(random.randrange(0, self.width - self.snake_block) / 10.0) * 10.0, round(random.randrange(0, self.height - self.snake_block) / 10.0) * 10.0
                length_of_snake += 1
                score += 10

            pygame.time.Clock().tick(self.snake_speed)

        self.display_final_score(score)

    def our_snake(self, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.game_window, self.green, [x[0], x[1], self.snake_block, self.snake_block])

    def your_score(self, score):
        value = pygame.font.SysFont(None, 35).render("Your Score: " + str(score*10), True, self.white)
        self.game_window.blit(value, [0, 0])

    def display_final_score(self, score):
        self.game_window.fill(self.black)

        final_score_text, final_score_text_rect = self.display_message("Your Final Score: {}".format(score), self.white, -50, "large")
        self.game_window.blit(final_score_text, final_score_text_rect)

        # Draw Play Again Button
        play_again_button_rect = pygame.draw.rect(self.game_window, self.green, [150, 450, 200, 50])
        play_again_text, play_again_text_rect = self.display_message("Play Again", self.black, 450, "medium")
        self.game_window.blit(play_again_text, play_again_text_rect)

        # Draw Quit Button
        quit_button_rect = pygame.draw.rect(self.game_window, self.red, [550, 450, 100, 50])
        quit_text, quit_text_rect = self.display_message("Quit", self.black, 450, "medium")
        self.game_window.blit(quit_text, quit_text_rect)

        pygame.display.update()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_mouse_over_button(play_again_button_rect):
                        waiting_for_input = False
                        self.game_loop()
                    elif self.is_mouse_over_button(quit_button_rect):
                        pygame.quit()
                        quit()

if __name__ == "__main__":
    snake_game = SnakeGame()
    snake_game.main_menu()
    snake_game.game_loop()

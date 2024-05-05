# Tic tac toe game using python
import sys
import pygame
import numpy as np
import random
import time
import copy

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption('TIC TAC TOE')
screen.fill((23,145,135))

class Board:
    def __init__(self):
        self.squares = np.zeros((3,3))
        self.empty_squares = self.squares # list of empty squares
        self.marked_squares = 0

    def final_state(self, show = False):
        # if draw then return 0
        # if player 1 wins then return 1
        # if player 2 wins then return 2

        # vertical wins
        for col in range(3):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = (239, 231, 200) if self.squares[0][col] == 2 else (146,142,133)
                    start = (col * 200  + 200 // 2, 20)
                    end = (col * 200 + 200 // 2, 580)
                    pygame.draw.line(screen, color, start, end, 8)
                return self.squares[0][col]
            
        # horizontal wins
        for row in range(3):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = (239, 231, 200) if self.squares[row][0] == 2 else (146,142,133)
                    start = (20, row * 200  + 200 // 2)
                    end = (580, row * 200  + 200 // 2)
                    pygame.draw.line(screen, color, start, end, 8)
                return self.squares[row][0]

        # descending diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = (239, 231, 200) if self.squares[1][1] == 2 else (146,142,133)
                start = (20, 20)
                end = (580, 580)
                pygame.draw.line(screen, color, start, end, 8)
            return self.squares[1][1]
        
        # ascending diagonal wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = (239, 231, 200) if self.squares[1][1] == 2 else (146,142,133)
                start = (20, 580)
                end = (580, 20)
                pygame.draw.line(screen, color, start, end, 8)
            return self.squares[1][1]
        
        # for no win
        return 0
    
    def mark_square(self, row: int, col: int, player: int):
        if self.squares[row][col] == 0:
            self.squares[row][col] = player
            self.marked_squares += 1

    def is_empty_square(self, row, col):
        return self.squares[row][col] == 0
    
    def is_full(self):
        return self.marked_squares == 9
    
    def is_empty(self):
        return self.marked_squares == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for rows in range(3):
            for col in range(3):
                if self.is_empty_square(rows, col):
                    empty_squares.append((rows, col))

        return empty_squares

class AI:
    def __init__(self, level = 0, player = 2):
        self.level = level
        self.player = player
    
    def random_choice(self, board: Board):
        empty_squares = board.get_empty_squares()
        return empty_squares[random.randrange(0, len(empty_squares))]
    
    def Minimax(self, board: Board, maximizing: bool):
        # Terminal state determination
        state = board.final_state()

        # Player 1 winning state
        if state == 1:
            return 1, None
        
        # Player 2 winning state
        elif state == 2:
            return -1, None
        
        # Draw
        elif board.is_full():
            return 0, None
        
        else:
            if maximizing:
                max_eval = -10
                best_move = None
                empty_squares = board.get_empty_squares()
                for (row, col) in empty_squares:
                    temp_board = copy.deepcopy(board)
                    temp_board.mark_square(row, col, 1)
                    eval = self.Minimax(temp_board, False)[0]
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (row, col)

                return max_eval, best_move

            else: 
                min_eval = 10 
                best_move = None
                empty_squares = board.get_empty_squares()
                for (row, col) in empty_squares:
                    temp_board = copy.deepcopy(board)
                    temp_board.mark_square(row, col, self.player)
                    eval = self.Minimax(temp_board, True)[0]
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (row, col)

                return min_eval, best_move
                

    def eval(self, main_board):
        if self.level == 0:  # random choice
            eval = 'random'
            move = self.random_choice(main_board)
            
        else:  # Minimax algorithm
            eval, move = self.Minimax(main_board, maximizing= False)  # AI is the minimizer

        print(f'AI has chosen to mark in {move} with {eval} evaluation')    
        return move

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 
        self.game_mode = 'PvP'
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_shape(row, col)
        self.next_player()

    def show_lines(self):
        screen.fill((23,145,135))

        #vertical lines
        pygame.draw.line(screen, (146,142,133), (200,0), (200,600), 8)
        pygame.draw.line(screen, (146,142,133), (400,0), (400,600), 8)

        #horizontal lines
        pygame.draw.line(screen, (146,142,133), (0,200), (600,200), 8)
        pygame.draw.line(screen, (146,142,133), (0,400), (600,400), 8)
    
    def draw_shape(self, row, col): # 1- cross, 2- circle
        if self.player == 1: 
            start_down = (col * 200 + 50, row * 200 + 50)
            end_down = (col * 200 + 150, row * 200 + 150)
            pygame.draw.line(screen, (66,66,66), start_down, end_down, 20)
            start_up = (col * 200 + 50, row * 200 + 150)
            end_up = (col * 200 + 150, row * 200 + 50)
            pygame.draw.line(screen, (66,66,66), start_up, end_up, 20)
            

        elif self.player == 2:
            center = (col * 200 + 100, row * 200 + 100)
            pygame.draw.circle(screen, (239,231,200), center, 50, 15)

    def next_player(self):
        self.player = self.player % 2 + 1

    def change_mode(self):
        self.game_mode = 'ai' if self.game_mode =='PvP' else 'PvP'

    def reset(self):
        self.__init__()
    
    def is_over(self):
        return self.board.final_state(show = True) != 0 or self.board.is_full()
        
# Main function
def main():
    #Object instatiation
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                print("Game exited")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # g for changing game mode
                if event.key == pygame.K_g:
                    game.change_mode()
                    print(f'Switched to {game.game_mode}')
                
                if event.key == pygame.K_0:
                    ai.level = 0
                    print('AI level 0')

                if event.key == pygame.K_1:
                    ai.level = 1
                    print('AI level 1')

                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                    print("Game reset")
                
                # Code for human player marking
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                row = position[1] // 200
                col = position[0] // 200

                if board.is_empty_square(row,col) and game.running:
                    game.make_move(row, col)

                    if game.is_over():
                        game.running = False

        # Code for ai marking
        if game.game_mode == 'ai' and game.player == ai.player and game.running:
            # Update the display
            pygame.display.update()

            # AI methods
            row, col = ai.eval(board)

            # Marking the board
            time.sleep(0.3)
            game.make_move(row, col)

            if game.is_over():
                game.running = False


        pygame.display.update()

if __name__ == '__main__':
    main()
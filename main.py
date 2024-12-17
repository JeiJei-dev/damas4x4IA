#
# José Bravo 
#

import pygame
import sys
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

BOARD_SIZE = 400
SQUARE_SIZE = BOARD_SIZE // 4

EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2

board = [
    [PLAYER2, EMPTY, PLAYER2, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, PLAYER1, EMPTY, PLAYER1]
]

screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Damas 4x4")

current_player = PLAYER1
move_count = 0
captures_made = False

def draw_board():
    # Dibuja el tablero de juego y las piezas en la pantalla.
    for row in range(4):
        for col in range(4):
            color = BLACK if (row + col) % 2 == 0 else WHITE
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board[row][col]
            if piece == PLAYER2:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
            elif piece == PLAYER1:
                pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)

def highlight_moves(selected_piece):
    #Resalta los movimientos válidos para la pieza seleccionada.
    row, col = selected_piece
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if board[row][col] == PLAYER1 else [(1, -1), (1, 1), (-1, -1), (-1, 1)]
    valid_moves = []

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        
        if is_in_bounds(new_row, new_col) and board[new_row][new_col] == EMPTY:
            pygame.draw.rect(screen, GREEN, (new_col * SQUARE_SIZE + 5,
                                               new_row * SQUARE_SIZE + 5,
                                               SQUARE_SIZE - 10,
                                               SQUARE_SIZE - 10))
            valid_moves.append((new_row, new_col))

        jump_row = new_row + dr
        jump_col = new_col + dc
        
        if is_in_bounds(jump_row, jump_col):
            if board[new_row][new_col] != EMPTY and board[new_row][new_col] != board[row][col]:
                if board[jump_row][jump_col] == EMPTY:
                    pygame.draw.rect(screen, RED, (jump_col * SQUARE_SIZE + 5,
                                                     jump_row * SQUARE_SIZE + 5,
                                                     SQUARE_SIZE - 10,
                                                     SQUARE_SIZE - 10))
                    valid_moves.append((jump_row, jump_col))

    return valid_moves

def is_in_bounds(row, col):
    # Verifica si una posición está dentro de los límites del tablero.
    return 0 <= row < 4 and 0 <= col < 4

def is_valid_move(start, end):
    # Verifica si un movimiento de una pieza es válido.
    start_row, start_col = start
    end_row, end_col = end
    
    if board[end_row][end_col] == EMPTY:
        return True
    
    if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2
        if board[middle_row][middle_col] != EMPTY and board[middle_row][middle_col] != board[start_row][start_col]:
            return True
            
    return False

def move_piece(start, end):
    # Mueve una pieza del tablero de su posición inicial a la final y realiza capturas si es necesario.
    global captures_made
    
    if is_valid_move(start, end):
        if abs(end[0] - start[0]) == 2:  
            middle_row = (start[0] + end[0]) // 2
            middle_col = (start[1] + end[1]) // 2
            board[middle_row][middle_col] = EMPTY
            captures_made = True
        
        board[end[0]][end[1]] = board[start[0]][start[1]]
        board[start[0]][start[1]] = EMPTY
        
def check_winner():
    # Verifica si hay un ganador en el juego.
    player1_count = sum(row.count(PLAYER1) for row in board)
    player2_count = sum(row.count(PLAYER2) for row in board)
    
    if player1_count == 0:
        return "CPU gana!"
    elif player2_count == 0:
        return "Player1 gana!"
    
    return None

def display_winner(winner_text):
    # Muestra el texto del ganador en la pantalla.
    font = pygame.font.Font(None, 74)
    text_surface = font.render(winner_text, True, RED)
    text_rect = text_surface.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2))
    
    screen.blit(text_surface, text_rect)

def get_valid_moves(player):
    # Obtiene todos los movimientos válidos para un jugador específico.
    valid_moves = []
    for row in range(4):
        for col in range(4):
            if board[row][col] == player:
                moves = highlight_moves((row,col))
                valid_moves.extend([(row,col), move] for move in moves)
    return valid_moves

def undo_move(start, end):
    # Deshace un movimiento y restaura la posición anterior de las piezas.
    moving_piece = board[end[0]][end[1]]
    
    board[start[0]][start[1]] = moving_piece
    board[end[0]][end[1]] = EMPTY
    
    if abs(end[0] - start[0]) == 2:  
        middle_row = (start[0] + end[0]) // 2
        middle_col = (start[1] + end[1]) // 2
        board[middle_row][middle_col] = PLAYER2 if moving_piece == PLAYER1 else PLAYER1

def minimax(depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
    # Implementa el algoritmo Minimax para determinar el mejor movimiento posible.
    winner_text = check_winner()
    
    if winner_text or depth == 0:
        return evaluate_board()

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_valid_moves(PLAYER2):
            start_pos = move[0]
            end_pos = move[1]
            move_piece(start_pos,end_pos)
            eval_score = minimax(depth-1 , alpha , beta , False)
            undo_move(start_pos,end_pos)
            max_eval = max(max_eval , eval_score)
            alpha = max(alpha , eval_score)
            if beta <= alpha:
                break  
        return max_eval
    
    else:
        min_eval = float('inf')
        for move in get_valid_moves(PLAYER1):
            start_pos=move[0]
            end_pos=move[1]
            move_piece(start_pos,end_pos)
            eval_score=minimax(depth-1 , alpha , beta , True)
            undo_move(start_pos,end_pos)
            min_eval=min(min_eval , eval_score)
            beta=min(beta , eval_score)
            if beta <= alpha:
                break  
        return min_eval

def evaluate_board():
    # Evalúa el estado actual del tablero y devuelve una puntuación basada en las piezas restantes.
    player1_score= sum(row.count(PLAYER1) for row in board)
    player2_score= sum(row.count(PLAYER2) for row in board)
    
    return player2_score - player1_score

def cpu_move():
    # Realiza el movimiento del CPU utilizando el algoritmo Minimax para decidir su mejor jugada.
    best_move=None
    best_value=float('-inf')
    
    for move in get_valid_moves(PLAYER2):
        start_pos=move[0]
        end_pos=move[1]
        
        move_piece(start_pos,end_pos)
        
        move_value=minimax(3 , float('-inf') , float('inf') , False) 
        
        undo_move(start_pos,end_pos)  
        
        if move_value>best_value:
            best_value=move_value
            best_move=move
            
    if best_move:
        move_piece(best_move[0], best_move[1])

def main():
    # Función principal que controla el flujo del juego y la interacción del usuario.
    global current_player   
    global move_count 
    global captures_made
    
    clock = pygame.time.Clock()
    
    selected_piece = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y=event.pos
                col=x//SQUARE_SIZE
                row=y//SQUARE_SIZE
                
                if selected_piece is None and board[row][col] == current_player:
                    selected_piece=(row,col)

                elif selected_piece is not None:
                    valid_moves=highlight_moves(selected_piece)
                    target_position=(row,col)

                    if target_position in valid_moves:
                        move_piece(selected_piece,target_position)

                        move_count += 1
                        captures_made |= captures_made

                        selected_piece=None
                    
                        current_player=PLAYER2
                    
                    elif not valid_moves:  
                        selected_piece=None   

                        if board[row][col] == current_player:  
                            selected_piece=(row,col)

        
        winner_text=check_winner()
        
        screen.fill(WHITE) 
        
        draw_board()
        
        if selected_piece:
            highlight_moves(selected_piece)

        if current_player == PLAYER2: 
            cpu_move()
            current_player=PLAYER1
            
        winner_text=check_winner() 

        if not winner_text and move_count >=64 and not captures_made: 
            winner_text="Empate!"

        if winner_text: 
            display_winner(winner_text)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

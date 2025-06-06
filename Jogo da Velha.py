import tkinter as tk
from tkinter import messagebox
import math
import random

# Representação do tabuleiro
board = [['' for _ in range(3)] for _ in range(3)]

# Função para verificar vitória
def check_winner():
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '':
            return row[0]
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            return board[0][col]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return board[0][2]
    
    return None

def restart_game():
    global board
    board = [['' for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text='', state=tk.NORMAL)

# Verifica se o tabuleiro está cheio
def is_full():
    for row in board:
        if '' in row:
            return False
    return True

# Algoritmo Minimax
def minimax(is_maximizing):
    winner = check_winner()
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

# Encontra a melhor jogada
def best_move():
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                score = minimax(False)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def disable_all_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=tk.DISABLED)

# Atualiza o tabuleiro com a jogada
def make_move(i, j, player):
    if board[i][j] == '' and not check_winner():
        board[i][j] = player
        buttons[i][j].config(text=player, state=tk.DISABLED)
        winner = check_winner()
        if winner:
            messagebox.showinfo("Fim de Jogo", f"{winner} venceu!")
            disable_all_buttons()
        elif is_full():
            messagebox.showinfo("Fim de Jogo", "Empate!")
            disable_all_buttons()
        elif player == 'X':
            i, j = best_move()
            if i is not None and j is not None:
                make_move(i, j, 'O')

# Interface gráfica
root = tk.Tk()
root.title("Jogo da Velha - Minimax")
buttons = [[None for _ in range(3)] for _ in range(3)]

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text='', font=('Arial', 24), width=5, height=2,
                                  command=lambda i=i, j=j: make_move(i, j, 'X'))
        buttons[i][j].grid(row=i, column=j)


# Decide aleatoriamente quem começa
if random.choice([True, False]):
    i, j = best_move()
    make_move(i, j, 'O')

restart_button = tk.Button(root, text="Reiniciar", font=('Arial', 14), command=restart_game)
restart_button.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()

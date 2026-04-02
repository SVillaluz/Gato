from flask import Flask, request, jsonify, render_template
import math
import os
import random
import copy

# Crear la aplicación Flask
app = Flask(__name__)

# Inicializar el tablero vacío 3x3 y el estado del juego
board = [[' ' for _ in range(3)] for _ in range(3)]
status = 'Empieza el juego'

def check_winner(b):
    """Verifica si hay un ganador en el tablero.
    Retorna el símbolo del ganador ('X' o 'O'), o None si no hay ganador.
    """
    # Check rows
    for row in b:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    
    # Check columns
    for j in range(3):
        if b[0][j] == b[1][j] == b[2][j] != ' ':
            return b[0][j]
    
    # Check diagonals
    if b[0][0] == b[1][1] == b[2][2] != ' ':
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] != ' ':
        return b[0][2]
    
    return None

def evaluate(b):
    """Evalúa el tablero para el algoritmo Minimax.
    Retorna: 10 si la IA gana, -10 si el jugador gana, 0 si es neutral.
    """
    winner = check_winner(b)
    if winner == 'O':
        return 10
    elif winner == 'X':
        return -10
    else:
        return 0

def is_moves_left(b):
    """Verifica si aún hay movimientos disponibles en el tablero.
    Retorna True si hay espacios vacíos, False si el tablero está lleno.
    """
    for i in range(3):
        for j in range(3):
            if b[i][j] == ' ':
                return True
    return False

def minimax(b, depth, is_max):
    """Algoritmo Minimax que explora todos los escenarios de juego posibles.
    - is_max=True: turno de la IA (maximiza puntuación)
    - is_max=False: turno del jugador (minimiza puntuación)
    Retorna el mejor puntaje posible para ese movimiento.
    """
    score = evaluate(b)
    if score == 10 or score == -10:
        return score
    if not is_moves_left(b):
        return 0
    
    if is_max:
        best = -1000
        for i in range(3):
            for j in range(3):
                if b[i][j] == ' ':
                    b[i][j] = 'O'
                    best = max(best, minimax(b, depth + 1, not is_max))
                    b[i][j] = ' '
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if b[i][j] == ' ':
                    b[i][j] = 'X'
                    best = min(best, minimax(b, depth + 1, not is_max))
                    b[i][j] = ' '
        return best

def find_best_move(b):
    """Encuentra el mejor movimiento para la IA usando el algoritmo Minimax.
    Evalúa todas las posiciones vacías y retorna la coordenada con mayor puntuación.
    """
    best_val = -1000
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if b[i][j] == ' ':
                b[i][j] = 'O'
                move_val = minimax(b, 0, False)
                b[i][j] = ' '
                if move_val >= best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move

def ai_move():
    """Ejecuta el movimiento de la IA.
    Usa find_best_move() para obtener la mejor posición y coloca una 'O' en el tablero.
    """
    i, j = find_best_move(board)
    if i != -1 and j != -1:
        board[i][j] = 'O'

# RUTAS DE LA APLICACIÓN

@app.route('/')
@app.route('/index')
def index():
    """Ruta principal que renderiza la página del juego.
    Envía el tablero y estado actual al template HTML.
    """
    return render_template('home.html', board=board, status=status)

@app.route("/move/<int:row>/<int:col>/<player>")
def make_move(row, col, player):
    """Procesa un movimiento en el juego.
    - row, col: coordenadas del movimiento
    - player: 'X' (jugador) o 'O' (IA)
    
    Valida si la celda está vacía, actualiza el tablero, verifica ganador,
    y ejecuta el movimiento de la IA si es necesario.
    Retorna el tablero actualizado y estado en formato JSON.
    """
    global status
    if board[row][col] == ' ':
        board[row][col] = player
        winner = check_winner(board)
        if winner:
            status = f'¡{winner} ya gano!'
        elif all(board[i][j] != ' ' for i in range(3) for j in range(3)):
            status = 'Empate'
        else:
            if player == 'X':
                ai_move()
                winner = check_winner(board)
                if winner:
                    status = f'¡{winner} ya gano!'
                elif all(board[i][j] != ' ' for i in range(3) for j in range(3)):
                    status = 'Empate'
                else:
                    status = 'Tu turno'
            else:
                status = 'Turno de la IA'
    return jsonify({'board': board, 'status': status})

@app.route("/reset")
def reset_game():
    """Reinicia el juego.
    Limpia el tablero (vuelve a llenar de espacios en blanco) y reinicia el estado.
    Retorna el tablero limpio y estado inicial en formato JSON.
    """
    global board, status
    board = [[' ' for _ in range(3)] for _ in range(3)]
    status = 'Tu turno'
    return jsonify({'board': board, 'status': status})

# Punto de entrada de la aplicación
if __name__ == '__main__':  
    # Ejecuta el servidor Flask en modo debug para desarrollo
    # Recarga automático al cambiar archivos y mejor manejo de errores
    app.run(debug=True)
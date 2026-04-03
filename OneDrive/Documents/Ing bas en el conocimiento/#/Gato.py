from flask import Flask, request, jsonify, render_template
import math
import os
import random
import copy

# Crear la aplicación Flask
app = Flask(__name__)

# Inicializar el tablero vacío 3x3 y el estado del juego
tablero = [[' ' for _ in range(3)] for _ in range(3)]
status = 'Tu turno'

def verificar_ganador(tablero):
    # Verificar filas, columnas y diagonales para determinar si hay un ganador
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != ' ':
            return tablero[i][0]
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != ' ':
            return tablero[0][i]
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != ' ':
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != ' ':
        return tablero[0][2]
    return None

def verificar_empate(tablero):
    # Verificar si el tablero está lleno sin un ganador, lo que indica un empate
    for row in tablero:
        if ' ' in row:
            return False
    return True

def minimax(tablero, depth, is_maximizing):
    # Implementación del algoritmo Minimax para la IA
    ganador = verificar_ganador(tablero)
    if ganador == 'O':
        return 10 - depth
    elif ganador == 'X':
        return depth - 10
    elif verificar_empate(tablero):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == ' ':
                    tablero[i][j] = 'O'
                    score = minimax(tablero, depth + 1, False)
                    tablero[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == ' ':
                    tablero[i][j] = 'X'
                    score = minimax(tablero, depth + 1, True)
                    tablero[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score
    
def movimiento_ia(tablero):
    # Determinar el mejor movimiento para la IA utilizando Minimax
    best_score = -math.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == ' ':
                tablero[i][j] = 'O'
                score = minimax(tablero, 0, False)
                tablero[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

@app.route('/')
@app.route('/home')
def home():
    # Renderiza la plantilla HTML para la página de inicio
    # Se pasan variables necesarias (tablero y status) a Jinja2
    return render_template('home.html', tablero=tablero, status=status)

@app.route("/move/<int:row>/<int:col>/<string:jugador>")
def movimiento(row, col, jugador):
    global status
    if tablero[row][col] == ' ':
        tablero[row][col] = jugador
        winner = verificar_ganador(tablero)
        if winner:
            status = f'¡{winner} gana!'
        elif verificar_empate(tablero):
            status = 'Empate'
        else:
            if jugador == 'X':
                ai_move = movimiento_ia(tablero)
                if ai_move:
                    tablero[ai_move[0]][ai_move[1]] = 'O'
                winner = verificar_ganador(tablero)
                if winner:
                    status = f'¡{winner} gana!'
                elif verificar_empate(tablero):
                    status = 'Empate'
                else:
                    status = 'Tu turno'
            else:
                status = 'Turno de la IA'
    return jsonify({'board': tablero, 'status': status})

@app.route("/reset")
def reset():
    global tablero, status
    tablero = [[' ' for _ in range(3)] for _ in range(3)]
    status = 'Tu turno'
    return jsonify({'board': tablero, 'status': status})

# Punto de entrada de la aplicación
if __name__ == '__main__':  
    # Ejecuta el servidor Flask en modo debug para desarrollo
    # Recarga automático al cambiar archivos y mejor manejo de errores
    app.run(debug=True)
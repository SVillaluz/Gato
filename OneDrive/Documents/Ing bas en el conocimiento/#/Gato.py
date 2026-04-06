from flask import Flask, request, jsonify, render_template  # Importar módulos de Flask para crear la aplicación web
import math  # Importar módulo de matemáticas para usar inf en Minimax
import os  # Importar módulo del sistema operativo (aunque no se usa actualmente)
import random  # Importar módulo de números aleatorios (aunque no se usa actualmente)
import copy  # Importar módulo para copiar objetos (aunque no se usa actualmente)

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
    ganador = verificar_ganador(tablero)  # Verificar si hay un ganador en el estado actual
    if ganador == 'O':  # Si la IA gana, devolver puntuación positiva menos profundidad
        return 10 - depth
    elif ganador == 'X':  # Si el jugador gana, devolver puntuación negativa más profundidad
        return depth - 10
    elif verificar_empate(tablero):  # Si es empate, devolver 0
        return 0

    if is_maximizing:  # Turno de maximizar (IA)
        best_score = -math.inf  # Inicializar mejor puntuación con infinito negativo
        for i in range(3):  # Recorrer filas
            for j in range(3):  # Recorrer columnas
                if tablero[i][j] == ' ':  # Si la celda está vacía
                    tablero[i][j] = 'O'  # Simular movimiento de IA
                    score = minimax(tablero, depth + 1, False)  # Llamada recursiva minimizando
                    tablero[i][j] = ' '  # Deshacer movimiento
                    best_score = max(score, best_score)  # Actualizar mejor puntuación
        return best_score
    else:  # Turno de minimizar (jugador)
        best_score = math.inf  # Inicializar mejor puntuación con infinito positivo
        for i in range(3):  # Recorrer filas
            for j in range(3):  # Recorrer columnas
                if tablero[i][j] == ' ':  # Si la celda está vacía
                    tablero[i][j] = 'X'  # Simular movimiento del jugador
                    score = minimax(tablero, depth + 1, True)  # Llamada recursiva maximizando
                    tablero[i][j] = ' '  # Deshacer movimiento
                    best_score = min(score, best_score)  # Actualizar mejor puntuación
        return best_score
    
def movimiento_ia(tablero):
    # Determinar el mejor movimiento para la IA utilizando Minimax
    best_score = -math.inf  # Inicializar mejor puntuación con infinito negativo
    best_move = None  # Inicializar mejor movimiento como None
    for i in range(3):  # Recorrer filas
        for j in range(3):  # Recorrer columnas
            if tablero[i][j] == ' ':  # Si la celda está vacía
                tablero[i][j] = 'O'  # Simular movimiento de IA
                score = minimax(tablero, 0, False)  # Calcular puntuación con Minimax
                tablero[i][j] = ' '  # Deshacer movimiento
                if score > best_score:  # Si esta puntuación es mejor
                    best_score = score  # Actualizar mejor puntuación
                    best_move = (i, j)  # Actualizar mejor movimiento
    return best_move  # Devolver el mejor movimiento encontrado

@app.route('/')
@app.route('/home')
def home():
    # Renderiza la plantilla HTML para la página de inicio
    # Se pasan variables necesarias (tablero y status) a Jinja2
    return render_template('home.html', tablero=tablero, status=status)

@app.route("/move/<int:row>/<int:col>/<string:jugador>")
def movimiento(row, col, jugador):
    global status  # Usar variable global status
    if tablero[row][col] == ' ':  # Si la celda está vacía
        tablero[row][col] = jugador  # Colocar la marca del jugador
        winner = verificar_ganador(tablero)  # Verificar si hay ganador
        if winner:  # Si hay ganador
            status = f'¡{winner} gana!'  # Actualizar status con mensaje de victoria
        elif verificar_empate(tablero):  # Si es empate
            status = 'Empate'  # Actualizar status con empate
        else:  # Si no hay ganador ni empate
            if jugador == 'X':  # Si el jugador es X (humano)
                ai_move = movimiento_ia(tablero)  # Calcular movimiento de IA
                if ai_move:  # Si hay movimiento válido
                    tablero[ai_move[0]][ai_move[1]] = 'O'  # Ejecutar movimiento de IA
                winner = verificar_ganador(tablero)  # Verificar ganador después de IA
                if winner:  # Si IA gana
                    status = f'¡{winner} gana!'  # Actualizar status
                elif verificar_empate(tablero):  # Si empate después de IA
                    status = 'Empate'  # Actualizar status
                else:  # Si continúa el juego
                    status = 'Tu turno'  # Actualizar status para turno del jugador
            else:  # Si el jugador no es X (no debería suceder)
                status = 'Turno de la IA'  # Actualizar status (aunque no se usa)
    return jsonify({'board': tablero, 'status': status})  # Devolver tablero y status en JSON

@app.route("/reset")
def reset():
    global tablero, status  # Usar variables globales
    tablero = [[' ' for _ in range(3)] for _ in range(3)]  # Reinicializar tablero vacío
    status = 'Tu turno'  # Reinicializar status
    return jsonify({'board': tablero, 'status': status})  # Devolver tablero y status en JSON

# Punto de entrada de la aplicación
if __name__ == '__main__':  
    # Ejecuta el servidor Flask en modo debug para desarrollo
    # Recarga automático al cambiar archivos y mejor manejo de errores
    app.run(debug=True)
import random
import matplotlib.pyplot as plt

# Base de conhecimento global
knowledge_base = []
# List to track the results of each game (1 = victory, -1 = loss, 0 = draw)
game_results = []


# 1. Função para atualizar os resultados após cada jogo
def update_game_results(winner):
    if winner == "X venceu!":
        game_results.append(1)  # 1 for victory
    elif winner == "O venceu!":
        game_results.append(-1)  # -1 for defeat
    elif winner == "Empate!":
        game_results.append(0)  # 0 for draw


# 2. Função para atualizar a base de conhecimento com a avaliação da jogada
def update_knowledge_with_rating(play, move, player, score, result):
    """
    Atualiza a base de conhecimento com o resultado de uma jogada e seu score.
    - result: 'win', 'loss' ou 'draw'
    """
    existing_record = next((record for record in knowledge_base if record['play'] == play), None)
    if existing_record:
        move_data = existing_record['Moves'].get(move, None)
        if move_data:
            # Ajusta o score com base no resultado da jogada
            if result == "win":
                move_data['score'] += 5  # Aumenta o score por uma vitória
            elif result == "loss":
                move_data['score'] -= 5  # Diminui o score por uma derrota
            elif result == "draw":
                move_data['score'] += 1  # Aumento pequeno para empate
        else:
            # Se não houver um registro anterior para esse movimento, cria-se um com o score inicial
            existing_record['Moves'][move] = {'score': score, 'result': result}
    else:
        # Se não houver um registro anterior para esse estado do tabuleiro, cria-se um novo
        knowledge_base.append({
            'play': play,
            'Moves': {move: {'score': score, 'result': result}}
        })


# 3. Função para selecionar a melhor jogada com base na base de conhecimento
def get_best_move_from_knowledge(board, player):
    possible_moves = [i for i, cell in enumerate(board) if cell == " "]
    best_move = None
    best_score = -float('inf')

    # Verifica se esse estado de tabuleiro já foi visto antes
    board_key = ''.join(board)  # Representa o tabuleiro como uma string para comparação fácil

    # Busca registros anteriores do estado do tabuleiro
    for record in knowledge_base:
        if record['play'] == board_key:
            # Se o tabuleiro foi visto, escolhe a melhor jogada com base na avaliação histórica
            for move in possible_moves:
                move_score_data = record['Moves'].get(move, None)
                if move_score_data:
                    move_score = move_score_data['score']
                    if move_score > best_score:
                        best_score = move_score
                        best_move = move
            break
    else:
        # Se não houver histórico, escolhe uma jogada aleatória
        best_move = random.choice(possible_moves)

    return best_move


# 4. Função do jogador inteligente utilizando a base de conhecimento
def intelligent_move(board):
    best_move = get_best_move_from_knowledge(board, 'X')
    board[best_move] = 'X'

    # Atualiza a base de conhecimento após a jogada
    play_key = ''.join(board)
    update_knowledge_with_rating(play_key, best_move, 'X', 0, 'win')  # Assume 'win' por enquanto

    return board


# 5. Exibir o tabuleiro
def display(board):
    visual_board = ""
    for i in range(3):
        visual_board += " | ".join(board[i * 3:(i + 1) * 3]) + "\n"
        if i < 2:
            visual_board += "---+---+---\n"
    print(visual_board)


# 6. Máquina simples para fazer jogadas
def machine(board, player):
    empty = [i for i in range(9) if board[i] == " "]
    if empty:
        board[random.choice(empty)] = player


# 7. Máquina campeã
def champion_machine(board):
    def check_win(board, player):
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                if check(board, player):
                    board[i] = " "
                    return i
                board[i] = " "
        return -1

    pos = check_win(board, 'O')
    if pos != -1:
        board[pos] = 'O'
        return
    pos = check_win(board, 'X')
    if pos != -1:
        board[pos] = 'O'
        return
    if board[4] == " ":
        board[4] = 'O'
        return
    for corner in [0, 2, 6, 8]:
        if board[corner] == " ":
            board[corner] = 'O'
            return
    for edge in [1, 3, 5, 7]:
        if board[edge] == " ":
            board[edge] = 'O'
            return


# 8. Verificar vitória ou empate
def check(tabuleiro, jogador):
    for i in range(0, 9, 3):
        if tabuleiro[i] == tabuleiro[i + 1] == tabuleiro[i + 2] == jogador:
            return True
    for i in range(3):
        if tabuleiro[i] == tabuleiro[i + 3] == tabuleiro[i + 6] == jogador:
            return True
    if tabuleiro[0] == tabuleiro[4] == tabuleiro[8] == jogador:
        return True
    if tabuleiro[2] == tabuleiro[4] == tabuleiro[6] == jogador:
        return True
    return False


# 9. Checar o estado final
def final_check(tabuleiro):
    if check(tabuleiro, 'O'):
        return "O venceu!"
    if check(tabuleiro, 'X'):
        return "X venceu!"
    if ' ' not in tabuleiro:
        return "Empate!"
    return None


# 10. Jogo no modo normal
def normal_game():
    board = [" " for _ in range(9)]
    moves = []
    while True:
        machine(board, 'X')
        moves.append(board[:])
        winner = final_check(board)
        if winner:
            break
        machine(board, 'O')
        moves.append(board[:])
        winner = final_check(board)
        if winner:
            break
    return moves, winner


# 11. Jogo no modo campeão
def champion_game():
    board = [" " for _ in range(9)]
    moves = []
    while True:
        machine(board, 'X')
        moves.append(board[:])
        winner = final_check(board)
        if winner:
            break
        champion_machine(board)
        moves.append(board[:])
        winner = final_check(board)
        if winner:
            break
    return moves, winner


# 12. Inteligente vs Normal
def intelligent_vs_normal_game():
    board = [" " for _ in range(9)]
    moves = []
    while True:
        intelligent_move(board)  # Intelligent player's move
        moves.append(board[:])  # Save the board after the intelligent player's move
        winner = final_check(board)  # Check if there is a winner
        if winner:
            # Update game_results based on the winner
            if winner == "X venceu!":
                game_results.append(1)  # Intelligent player wins (X)
            elif winner == "O venceu!":
                game_results.append(-1)  # Normal machine wins (O)
            else:
                game_results.append(0)  # Draw
            break

        machine(board, 'O')  # Normal machine's move (player O)
        moves.append(board[:])  # Save the board after the machine's move
        winner = final_check(board)  # Check if there is a winner
        if winner:
            # Update game_results based on the winner
            if winner == "X venceu!":
                game_results.append(1)  # Intelligent player wins (X)
            elif winner == "O venceu!":
                game_results.append(-1)  # Normal machine wins (O)
            else:
                game_results.append(0)  # Draw
            break

    return moves, winner


# 13. Inteligente vs Campeão
def intelligent_vs_champion_game():
    board = [" " for _ in range(9)]
    moves = []
    while True:
        intelligent_move(board)
        moves.append(board[:])
        winner = final_check(board)
        if winner:
            break
        champion_machine(board)
        moves.append(board[:])
        winner = final_check(board)
        if winner:
            break
    return moves, winner


# 14. Função para plotar o gráfico de desempenho
def plot_performance():
    # Count victories over time
    victories = 0
    victory_progress = []

    # Check if game_results is populated
    print(f"Game Results: {game_results}")

    for result in game_results:
        if result == 1:
            victories += 1
        elif result == -1:
            victories -= 1
        victory_progress.append(victories)

    print(f"Victory Progress: {victory_progress}")  # Debug output

    if not victory_progress:
        print("Nenhum resultado de jogo encontrado para plotar.")
        return

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(victory_progress, label='Vitórias Acumuladas', color='green', linestyle='-', markersize=5, linewidth=1)
    plt.scatter(range(len(victory_progress)), victory_progress, color='green', zorder=5)

    plt.title('Desempenho do Jogador Inteligente ao Longo dos Jogos')
    plt.xlabel('Número do Jogo')
    plt.ylabel('Vitórias Acumuladas')
    plt.legend()

    plt.show()



# 15. Função para exibir o progresso das jogadas
def display_move_progress():
    move_scores = {}

    # Coleta os scores de cada movimento
    for record in knowledge_base:
        for move, data in record['Moves'].items():
            if move not in move_scores:
                move_scores[move] = []
            move_scores[move].append(data['score'])

    # Ordena os movimentos pela média dos scores
    sorted_move_scores = sorted(move_scores.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True)

    # Cria um tabuleiro vazio
    board = [' ' for _ in range(9)]

    # Preenche o tabuleiro com as médias de score
    for move, scores in sorted_move_scores:
        avg_score = sum(scores) / len(scores)
        board[move] = f'{avg_score:.2f}'

    # Exibe o tabuleiro com as médias de score
    print("Tabuleiro de Movimentos:")
    for i in range(3):
        print(" | ".join(board[i * 3:(i + 1) * 3]))
        if i < 2:
            print("---+---+---")


# 16. Função para avaliar melhorias nas jogadas
def evaluate_move_improvement():
    move_scores = []
    for record in knowledge_base:
        for move, data in record['Moves'].items():
            move_scores.append(data['score'])

    if move_scores:
        avg_score = sum(move_scores) / len(move_scores)
        print(f"Média de score geral das jogadas: {avg_score:.2f}")
    else:
        print("Ainda não há jogadas registradas.")


# 17. Modo automático de jogo
def auto_game_mode():
    global knowledge_base
    knowledge_base = []  # Reinicia a base de conhecimento no início do modo automático
    print("Escolha o modo de jogo:")
    print("1. Normal")
    print("2. Champion")
    print("3. Intelligent vs Normal")
    print("4. Intelligent vs Champion")
    choice = input("Escolha o modo de jogo desejado (1/2/3/4): ")
    num_games = int(input("Digite o número de jogos: "))
    wins_x, wins_o = 0, 0

    for _ in range(num_games):
        if choice == '1':
            moves, winner = normal_game()
            mode = "Normal"
        elif choice == '2':
            moves, winner = champion_game()
            mode = "Champion"
        elif choice == '3':
            moves, winner = intelligent_vs_normal_game()
            mode = "Intelligent vs Normal"
        else:
            moves, winner = intelligent_vs_champion_game()
            mode = "Intelligent vs Champion"

        if winner == "X venceu!":
            wins_x += 1
        elif winner == "O venceu!":
            wins_o += 1

    print(f"\nResultado após {num_games} jogos em modo {mode}:")
    print(f"Vitórias de X: {wins_x}")
    print(f"Vitórias de O: {wins_o}")

    if choice == '3':
        plot_performance()

    print("\nProgresso das jogadas do jogador inteligente:")
    display_move_progress()

    print("\nAvaliação das melhorias nas jogadas:")
    evaluate_move_improvement()


# Ponto de entrada
if __name__ == "__main__":
    auto_game_mode()

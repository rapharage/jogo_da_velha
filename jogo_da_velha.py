import random
import os

knowledge_base = []

def save_win_rate_to_txt(wins_x, total_games, mode):
    """
    Salva a taxa de vitórias do jogador X a cada 100 jogos em um arquivo .txt.
    :param wins_x: Número de vitórias do jogador X.
    :param total_games: Total de jogos completados até o momento.
    :param mode: Modo de jogo (Inteligente Normal ou Inteligente Champion).
    """
    win_rate = (wins_x / total_games) * 100
    filename = f"win_rate_{mode}.txt"

    with open(filename, "a") as f:  # Modo 'a' para adicionar ao final do arquivo
        f.write(f"Jogos completados: {total_games}\n")
        f.write(f"Taxa de vitórias de X: {win_rate:.2f}%\n")
        f.write("=" * 30 + "\n")

def save_moves_to_txt(moves, winner, mode):
    """
    Salva as jogadas e o resultado em um arquivo .txt.
    :param moves: Lista dos estados do tabuleiro após cada jogada.
    :param winner: Resultado do jogo ('X', 'O' ou 'Draw').
    :param mode: Modo de jogo (Normal, Champion, Inteligente Normal, Inteligente Champion).
    """
    filename = f"game_records_{mode}.txt"
    with open(filename, "a") as f:
        f.write(f"Modo de Jogo: {mode}\n")
        f.write("Jogadas:\n")
        for i, move in enumerate(moves, 1):
            f.write(f"  Jogada {i}:\n")
            for j in range(0, 9, 3):
                f.write(f"    {' | '.join(move[j:j + 3])}\n")
            f.write("    -----------\n")
        f.write(f"Resultado: {winner}\n")
        f.write("=" * 30 + "\n\n")


def save_summary_to_txt(wins_x, wins_o, num_games, mode):
    """
    Salva o resumo das estatísticas (vitórias de X e O) em um arquivo .txt.
    :param wins_x: Número de vitórias do jogador X.
    :param wins_o: Número de vitórias do jogador O.
    :param num_games: Total de jogos.
    :param mode: Modo de jogo (Normal, Champion, Inteligente Normal, Inteligente Champion).
    """
    filename = f"game_summary_{mode}.txt"
    with open(filename, "a") as f:
        f.write(f"Modo de Jogo: {mode}\n")
        f.write(f"Total de Jogos: {num_games}\n")
        f.write(f"Vitórias do X: {wins_x}\n")
        f.write(f"Vitórias do O: {wins_o}\n")
        f.write("=" * 30 + "\n\n")


def save_knowledge_to_txt():
    filename = "knowledge_base.txt"
    print(f"Salvando {len(knowledge_base)} registros na base de conhecimento...")
    with open(filename, "w") as f:
        for record in knowledge_base:
            print(record)  # Para depuração
            f.write(f"Jogada: {record['play']}\n")
            f.write(f"  Vitórias: {record['Wins']}\n")
            f.write(f"  Derrotas: {record['Losses']}\n")
            f.write(f"  Empates: {record['Draws']}\n")
            f.write(f"  Total de Partidas: {record['Plays']}\n")
            f.write("-" * 30 + "\n")



def load_knowledge_from_txt():
    filename = "knowledge_base.txt"
    if not os.path.exists(filename):
        print(f"Arquivo {filename} não encontrado.")
        return []

    knowledge = []
    with open(filename, "r") as f:
        current_record = {}
        for line in f:
            line = line.strip()
            print(f"Lendo linha: {line}")  # Verifique a leitura do arquivo
            if line.startswith("Jogada:"):
                if current_record:
                    knowledge.append(current_record)
                current_record = {"play": line.split(": ")[1]}
            elif line.startswith("Vitórias:"):
                current_record["Wins"] = int(line.split(": ")[1])
            elif line.startswith("Derrotas:"):
                current_record["Losses"] = int(line.split(": ")[1])
            elif line.startswith("Empates:"):
                current_record["Draws"] = int(line.split(": ")[1])
            elif line.startswith("Total de Partidas:"):
                current_record["Plays"] = int(line.split(": ")[1])
        if current_record:
            knowledge.append(current_record)
    return knowledge

def update_knowledge_base(play, winner):
    # Atualiza a base de conhecimento
    existing_record = next((record for record in knowledge_base if record['play'] == play), None)
    if existing_record:
        # Atualiza o número de vitórias, derrotas, empates e partidas
        if winner == 'X':
            existing_record['Wins'] += 1
        elif winner == 'O':
            existing_record['Losses'] += 1
        else:
            existing_record['Draws'] += 1
        existing_record['Plays'] += 1
    else:
        # Cria um novo registro se não encontrar
        knowledge_base.append({
            'play': play,
            'Wins': 1 if winner == 'X' else 0,
            'Losses': 1 if winner == 'O' else 0,
            'Draws': 1 if winner == 'Draw' else 0,
            'Plays': 1
        })

def display(board):
    visual_board = ""
    for i in range(3):
        visual_board += " | ".join(board[i * 3:(i + 1) * 3]) + "\n"
        if i < 2:
            visual_board += "---+---+---\n"
    print(visual_board)


def check(board, player):
    for i in range(0, 9, 3):
        if all(board[i + j] == player for j in range(3)):
            return True
    for i in range(3):
        if all(board[i + j * 3] == player for j in range(3)):
            return True
    if all(board[i] == player for i in [0, 4, 8]) or all(board[i] == player for i in [2, 4, 6]):
        return True
    return False


def machine(board, player):
    empty = [i for i in range(9) if board[i] == " "]
    if empty:
        board[random.choice(empty)] = player


def champion_machine(board):
    def check_win(champ_board, player):
        for i in range(9):
            if champ_board[i] == " ":
                champ_board[i] = player
                if check(champ_board, player):
                    champ_board[i] = " "
                    return i
                champ_board[i] = " "
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


def intelligent_game(is_champion_mode=False):
    board = [" " for _ in range(9)]
    moves = []

    while True:
        # Jogador X (inteligente) faz a primeira jogada
        move = get_intelligent_move(board)
        board[move] = 'X'
        moves.append(board[:])
        winner = final_check(board)
        if winner:
            break

        if is_champion_mode:
            champion_machine(board)  # Jogador O (campeão) joga após X
        else:
            machine(board, 'O')  # Oponente (O) joga aleatoriamente

        moves.append(board[:])
        winner = final_check(board)
        if winner:
            break

    return moves, winner


def get_intelligent_move(board):
    """
    Retorna a próxima jogada inteligente baseada na base de conhecimento.
    Se não houver conhecimento suficiente, realiza uma jogada aleatória.
    """
    # Consulta a base de conhecimento para obter a melhor jogada (ou faz uma aleatória)
    possible_moves = [i for i, cell in enumerate(board) if cell == " "]

    # Aqui você pode implementar a lógica de consulta à base de conhecimento para escolher uma jogada inteligente
    for move in possible_moves:
        # Exemplo de como consultar a base de conhecimento
        best_move = consult_knowledge_base(board, move)
        if best_move is not None:
            return best_move

    # Se não houver jogada inteligente possível, retorna uma jogada aleatória
    return random.choice(possible_moves)


def consult_knowledge_base(board, move):
    """
    Consulta a base de conhecimento para verificar se a jogada é boa ou não.
    Esta função pode ser expandida para avaliar o movimento com base em dados anteriores.
    """
    # Implementação de consulta simples à base de conhecimento (exemplo)
    # Aqui você pode aplicar uma lógica baseada na base de conhecimento.
    # No momento, retornamos None, o que fará com que o jogador escolha aleatoriamente.
    return None

def final_check(board):
    if check(board, 'X'):
        return 'X'
    elif check(board, 'O'):
        return 'O'
    elif all(cell != " " for cell in board):
        return "Draw"
    return None

def auto_game_mode():
    global knowledge_base
    knowledge_base = load_knowledge_from_txt()
    print("Escolha o modo de jogo:")
    print("1. Normal")
    print("2. Champion")
    print("3. Inteligente Normal")
    print("4. Inteligente Champion")
    choice = input("Escolha o modo de jogo desejado (1/2/3/4): ")
    while choice not in ['1', '2', '3', '4']:
        print("Escolha inválida. Tente novamente.")
        choice = input("Escolha o modo de jogo desejado (1/2/3/4): ")
    num_games = int(input("Digite o número de jogos: "))
    wins_x = 0
    wins_o = 0
    completed_games = 0  # Contador de partidas já realizadas

    for _ in range(num_games):
        if choice == '1':
            moves, winner = normal_game()
        elif choice == '2':
            moves, winner = champion_game()
        elif choice == '3':
            moves, winner = intelligent_game(False)
        elif choice == '4':
            moves, winner = intelligent_game(True)

        save_moves_to_txt(moves, winner, choice)
        if winner == "X":
            wins_x += 1
        elif winner == "O":
            wins_o += 1

        completed_games += 1

        # Atualizar a base de conhecimento apenas para os modos inteligentes
        if choice in ['3', '4']:
            update_knowledge_base(str(moves[-1]), winner)

        # A cada 100 partidas, salvar a taxa de vitória (apenas para modos inteligentes)
        if choice in ['3', '4'] and completed_games % 100 == 0:
            save_win_rate_to_txt(wins_x, completed_games, choice)

    print(f"Modo de Jogo: {choice}")
    print(f"Total de jogos: {num_games}")
    print(f"Vitórias de X: {wins_x}")
    print(f"Vitórias de O: {wins_o}")
    save_summary_to_txt(wins_x, wins_o, num_games, choice)
    save_knowledge_to_txt()

    # Salvar a taxa de vitória final se o número de partidas não for múltiplo de 100
    if choice in ['3', '4'] and completed_games % 100 != 0:
        save_win_rate_to_txt(wins_x, completed_games, choice)

    print("Banco de conhecimento e taxa de vitória salvos.")

# Função principal
if __name__ == "__main__":
    auto_game_mode()

import random
import os

class Game:
    def __init__(self, player1_file, player2_file, game_map, max_moves):
        self.player1_file = player1_file
        self.player2_file = player2_file
        self.map = game_map
        self.max_moves = max_moves
        self.player1_store = {}
        self.player2_store = {}
        self.player1_position = None
        self.player2_position = None
        self.moves = 0
        self.game_over = False
        self.winner = None
        self.player_first = None
        self.player_moves_log = []

        # Проверяем карту и позиции игроков
        self.validate_map()
        self.find_players()

    def read_player_code(self, player_file):
        """Считываем код игрока из файла."""
        with open(player_file, 'r') as file:
            return file.read()

    def validate_map(self):
        """Проверяем карту на корректность значений и наличие фруктов и игроков."""
        fruit_count = 0
        player1_count = 0
        player2_count = 0

        for row in self.map:
            for cell in row:
                if cell not in [0, 1, 2, 3, 4, 5]:
                    raise ValueError('Invalid value in the map.')
                if cell == 2:
                    fruit_count += 1
                if cell == 3:
                    player1_count += 1
                if cell == 4:
                    player2_count += 1

        if fruit_count % 2 == 0:
            raise ValueError('The number of fruits must be odd.')
        if player1_count != 1 or player2_count != 1:
            raise ValueError('Both players must be present on the map.')

    def find_players(self):
        """Находим начальные позиции игроков."""
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if cell == 3:
                    self.player1_position = (i, j)
                elif cell == 4:
                    self.player2_position = (i, j)

    def run(self):
        """Основной цикл игры."""
        self.player_first = random.choice([3, 4])
        current_player = self.player_first
        while self.moves < self.max_moves and not self.game_over:
            if current_player == 3:
                player_code = self.read_player_code(self.player1_file)
                move_result = self.process_turn(player_code, 3)
                self.player_moves_log.append(move_result)  # Запись хода в лог
                current_player = 4
            else:
                player_code = self.read_player_code(self.player2_file)
                move_result = self.process_turn(player_code, 4)
                self.player_moves_log.append(move_result)  # Запись хода в лог
                current_player = 3

            self.moves += 1

        if self.moves >= self.max_moves and not self.game_over:
            self.game_over = True
            self.winner = None

        return self.game_summary()

    def process_turn(self, player_code, player_symbol):
        """Обрабатываем ход игрока."""
        field_around = self.get_field_around_player(player_symbol, 1)
        player_store = self.player1_store if player_symbol == 3 else self.player2_store

        store = {}  # Инициализируем store

        try:
            direction, store = exec(player_code,
                                    {'movePlayer': self.movePlayer, 'field_around': field_around, 'store': store})
        except Exception as e:
            self.game_over = True
            self.winner = 4 if player_symbol == 3 else 3
            self.player_moves_log.append({
                "player": player_symbol,
                "action": "error",
                "message": str(e),
                "store": store
            })
            return

        # Сохраняем новый store
        if player_symbol == 3:
            self.player1_store = store
        else:
            self.player2_store = store

        # Двигаем игрока
        self.map = self.move(direction, player_symbol)

        # Возвращаем информацию о ходе и сохраняем в логи
        move_info = {
            "player": player_symbol,
            "action": "move",
            "direction": direction,
            "new_position": (self.player1_position if player_symbol == 3 else self.player2_position),
            "store": store
        }
        self.player_moves_log.append(move_info)

    def check_game_end(self):
        """Проверяем условия окончания игры."""
        # Проверка на мины и захват игрока
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if cell == 5:  # Мина
                    if self.player1_position == (i, j):
                        self.winner = 4  # Игрок 2 выигрывает
                        self.player_moves_log.append("Player 1 stepped on a mine and lost!")
                        return True
                    elif self.player2_position == (i, j):
                        self.winner = 3  # Игрок 1 выигрывает
                        self.player_moves_log.append("Player 2 stepped on a mine and lost!")
                        return True
                if self.map[self.player1_position[0]][self.player1_position[1]] == self.map[self.player2_position[0]][self.player2_position[1]]:
                    self.winner = self.player1_position
                    self.player_moves_log.append(f"Player {self.winner} captured the other player and won!")
                    return True

        return False

    def movePlayer(self, field_around, store):
        """Функция для обработки движения игрока. Должна быть определена в коде игрока."""
        # Пример реализации, вам нужно добавить свою логику
        direction = 'right'  # Измените на свою логику
        return direction, store

    def get_field_around_player(self, player_symbol, radius):
        """Возвращает клетки вокруг игрока."""
        for i, row in enumerate(self.map):
            for j, element in enumerate(row):
                if element == player_symbol:
                    player_position = (i, j)
                    break

        field_around_player = []
        for i in range(max(0, player_position[0] - radius), min(len(self.map), player_position[0] + radius + 1)):
            row = []
            for j in range(max(0, player_position[1] - radius), min(len(self.map[0]), player_position[1] + radius + 1)):
                row.append(self.map[i][j])
            field_around_player.append(row)

        return field_around_player

    def move(self, direction, player):
        """Обрабатывает передвижение игрока."""
        player_position = [(i, row.index(player)) for i, row in enumerate(self.map) if player in row][0]

        new_position = None

        if direction == 'left':
            new_position = (player_position[0], player_position[1] - 1)
        elif direction == 'right':
            new_position = (player_position[0], player_position[1] + 1)
        elif direction == 'top':
            new_position = (player_position[0] - 1, player_position[1])
        elif direction == 'bottom':
            new_position = (player_position[0] + 1, player_position[1])

        if 0 <= new_position[0] < 15 and 0 <= new_position[1] < 15:
            if self.map[new_position[0]][new_position[1]] == 0:
                self.map[player_position[0]][player_position[1]] = 0
                self.map[new_position[0]][new_position[1]] = player
            elif self.map[new_position[0]][new_position[1]] == 5:
                self.game_over = True
                self.winner = 4 if player == 3 else 3
                self.player_moves_log.append(f"Player {player} stepped on a mine and lost!")
            elif self.map[new_position[0]][new_position[1]] == 3 or self.map[new_position[0]][new_position[1]] == 4:
                self.game_over = True
                self.winner = player
                self.player_moves_log.append(f"Player {player} captured the other player and won!")

        return self.map

    def game_summary(self):
        """Возвращаем исход игры с необходимыми данными."""
        if self.winner is None:
            result = {
                "result": "Draw",
                "first_player": self.player_first,
                "moves_log": self.player_moves_log,
                "stores": {
                    "player1_store": self.player1_store,
                    "player2_store": self.player2_store
                }
            }
        else:
            result = {
                "winner": self.winner,
                "reason": {
                    "move_number": self.moves,  # Последний ход
                    "current_player": self.winner,  # Победитель
                    # "map_state": self.map,  # Состояние карты на момент победы
                    "player1_store": self.player1_store,
                    "player2_store": self.player2_store
                },
                "first_player": self.player_first,
                "moves_log": self.player_moves_log,
                # "stores": {
                #     "player1_store": self.player1_store,
                #     "player2_store": self.player2_store
                # }
            }

        return result


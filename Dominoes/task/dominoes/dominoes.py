import random


def determine_max_double(pieces):
    max_double = [-1, -1]
    for piece in pieces:
        if piece[0] == piece[1] and piece[0] > max_double[0]:
            max_double = piece
    return max_double


class Dominoes:
    dominoes = []
    stock_pieces = []
    computer_pieces = []
    computer_counts = []
    computer_scores = []
    player_pieces = []
    domino_snake = []
    status = ""

    def __init__(self):
        for i in range(0, 7):
            for j in range(i, 7):
                self.dominoes.append([i, j])
        self.stock_pieces = self.dominoes
        for i in range(0, 7):
            self.computer_pieces.append(self.new_piece())
            self.player_pieces.append(self.new_piece())
        self.status = self.determine_starting_piece()

    def new_piece(self):
        new_piece = self.dominoes[random.randint(0, len(self.stock_pieces) - 1)]
        self.dominoes.remove(new_piece)
        return new_piece

    def determine_starting_piece(self):
        computer = determine_max_double(self.computer_pieces)
        player = determine_max_double(self.player_pieces)
        snake = max(computer, player)
        if snake == computer:
            self.computer_pieces.remove(snake)
            state = 'player'
        else:
            self.player_pieces.remove(snake)
            state = 'computer'
        self.domino_snake.append(snake)
        return state

    def get_player_pieces(self):
        pieces = ""
        for i in range(0, len(self.player_pieces)):
            pieces += f"\n{i + 1}:{self.player_pieces[i]}"
        return pieces

    def get_domino_snake(self):
        pieces = ""
        if len(self.domino_snake) > 6:
            for i in range(0, 3):
                pieces += f"{self.domino_snake[i]}"
            pieces += "." * 3
            for i in range(-3, 0):
                pieces += f"{self.domino_snake[i]}"
        else:
            for domino in self.domino_snake:
                pieces += f"{domino}"
        return pieces

    def is_draw(self):
        count = 0
        for domino in self.domino_snake:
            if domino[0] == self.domino_snake[0][0]:
                count += 1
            if domino[1] == self.domino_snake[0][0]:
                count += 1
        return self.domino_snake[0][0] == self.domino_snake[-1][1] and count == 8

    def is_game_over(self):
        return self.is_draw() or len(self.player_pieces) == 0 or len(self.computer_pieces) == 0

    def take_from_stock(self):
        piece_from_stock = self.stock_pieces[random.randint(0, len(self.stock_pieces) - 1)]
        self.stock_pieces.remove(piece_from_stock)
        return piece_from_stock

    def insert_piece(self, pieces, index, append=True):
        piece_to_insert = pieces[index][::-1] \
            if self.is_valid_move(pieces[index], append)[1] else pieces[index]
        if append:
            game.domino_snake.append(piece_to_insert)
        else:
            game.domino_snake.insert(0, piece_to_insert)

    def is_valid_move(self, choice, append=True):
        if append:
            flip = self.domino_snake[-1][1] == choice[1]
            valid = self.domino_snake[-1][1] == choice[0] or flip
        else:
            flip = self.domino_snake[0][0] == choice[0]
            valid = self.domino_snake[0][0] == choice[1] or flip
        return valid, flip

    def calc_computer_scores(self):
        self.computer_counts = [0 for _ in range(0, 7)]
        for piece in self.computer_pieces + self.domino_snake:
            self.computer_counts[piece[0]] += 1
            self.computer_counts[piece[1]] += 1
        self.computer_scores = [self.computer_counts[x[0]] + self.computer_counts[x[1]] for x in self.computer_pieces]

    def get_status(self):
        if len(self.player_pieces) == 0:
            return "The game is over. You won!"
        elif len(self.computer_pieces) == 0:
            return "The game is over. The computer won!"
        elif self.is_draw():
            return "The game is over. It's a draw!"
        elif self.status == "computer":
            return "Computer is about to make a move. Press Enter to continue..."
        elif self.status == "player":
            return "It's your turn to make a move. Enter your command."

    def __str__(self):
        return f"""{'=' * 70}
Stock size: {len(self.stock_pieces)}
Computer pieces: {len(self.computer_pieces)}
\n{self.get_domino_snake()}
\nYour pieces:{self.get_player_pieces()}
\nStatus: {self.get_status()}"""


game = Dominoes()
print(game)
while not game.is_game_over():
    if game.status == "player":
        number = None
        while number is None:
            try:
                number = int(input())
            except ValueError:
                pass
            if number not in range(-len(game.player_pieces), len(game.player_pieces) + 1):
                number = None
                print("Invalid input. Please try again.")
            elif number != 0 and not game.is_valid_move(game.player_pieces[abs(number)-1], number > 0)[0]:
                number = None
                print("Illegal move. Please try again.")
        if number == 0:
            if len(game.stock_pieces) > 0:
                game.player_pieces.append(game.take_from_stock())
        else:
            game.insert_piece(game.player_pieces, abs(number) - 1, number > 0)
            game.player_pieces.remove(game.player_pieces[abs(number) - 1])
        game.status = "computer"
    elif game.status == "computer":
        game.calc_computer_scores()
        computer_pieces = game.computer_pieces[:]
        input()
        while len(game.computer_scores) > 0:
            number = game.computer_scores.index(max(game.computer_scores))
            if game.is_valid_move(computer_pieces[number], True)[0]:
                game.insert_piece(computer_pieces, number, True)
                game.computer_pieces.remove(computer_pieces[number])
                break
            elif game.is_valid_move(computer_pieces[number], False)[0]:
                game.insert_piece(computer_pieces, number, False)
                game.computer_pieces.remove(computer_pieces[number])
                break
            else:
                game.computer_scores.remove(max(game.computer_scores))
                computer_pieces.remove(computer_pieces[number])
        if len(game.computer_scores) == 0 and len(game.stock_pieces) > 0:
            game.computer_pieces.append(game.take_from_stock())
        game.status = "player"
    print(game)

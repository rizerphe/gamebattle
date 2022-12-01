import random
import string
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from itertools import zip_longest
from typing import Generator
from typing import List
from typing import Literal
from typing import Optional


class Direction(Enum):
    right = (1, 0)
    down = (0, 1)
    left = (-1, 0)
    up = (0, -1)


@dataclass
class Ship:
    location: tuple[int, int]
    direction: Direction
    length: int

    def does_occupy_square(self, target):
        for analyzed in self.squares():
            if analyzed == target:
                return True
        return False

    def squares(self):
        x, y = self.location
        dx, dy = self.direction.value
        return zip_longest(
            range(x, x + self.length * dx, dx if dx else 1),
            range(y, y + self.length * dy, dy if dy else 1),
            fillvalue=x * abs(dy) + y * abs(dx),
        )


class Board:
    """The board for the game of battleship"""

    def __init__(self) -> None:
        self.board = [[False] * 10 for i in range(10)]
        self.ships: List[Ship] = []
        # Allowed lengths: 2, 3, 3, 4, 5
        self.allowed = {
            2: 1,
            3: 2,
            4: 1,
            5: 1,
        }

    def is_game_over(self):
        """Check if the game is over"""
        for i in range(10):
            for j in range(10):
                if self.get_square_state(i, j, True) == "ship":
                    return False
        return True

    def get_all_possible_fires(self) -> Generator[tuple[int, int], None, None]:
        """Get all possible fires"""
        for x in range(10):
            for y in range(10):
                if not self.board[y][x]:
                    yield x, y

    def count_ships(self, length: int) -> int:
        """Count the number of ships of the given length"""
        return len([1 for ship in self.ships if ship.length == length])

    def get_if_ship_allowed(self, length: int) -> bool:
        """Check if a ship of the given length is allowed
        to be placed on the board considering the current
        state of the board.
        """
        existing = self.count_ships(length)
        return existing < self.allowed.get(length, 0)

    def place_ship(
        self, location: tuple[int, int], direction: Direction, length: int
    ) -> None:
        """Place a ship on the board"""
        if not self.check_ship_placement_legality(location, direction, length):
            raise ValueError("Illegal ship placement")
        self.ships.append(Ship(location, direction, length))

    def check_ship_placement_legality(
        self, location: tuple[int, int], direction: Direction, length: int
    ) -> bool:
        """Check if a ship placement is legal"""
        x, y = location
        dx, dy = direction.value
        for analyzed in zip_longest(
            range(x, x + length * dx, dx if dx else 1),
            range(y, y + length * dy, dy if dy else 1),
            fillvalue=x * abs(dy) + y * abs(dx),
        ):
            if not self.is_legal_square(analyzed):
                return False
        return True

    def is_legal_square(self, target: tuple[int, int]) -> bool:
        """Check if you can place a new ship on the given square"""
        x, y = target
        if not 0 <= x < 10 or not 0 <= y < 10:
            return False
        for ship in self.ships:
            for location in [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
                (x, y),
            ]:
                if ship.does_occupy_square(location):
                    return False
        return True

    def get_square_state(
        self, x: int, y: int, show_ships: bool
    ) -> Literal["empty", "hit", "miss", "ship"]:
        """Get the state of a square"""
        for ship in self.ships:
            if ship.does_occupy_square((x, y)):
                if self.board[y][x]:
                    return "hit"
                if show_ships:
                    return "ship"
        if self.board[y][x]:
            return "miss"
        return "empty"

    def states(
        self, show_ships: bool
    ) -> Generator[
        Generator[Literal["empty", "hit", "miss", "ship"], None, None],
        None,
        None,
    ]:
        """Iterate over cell states"""
        for row in range(10):
            yield (
                self.get_square_state(col, row, show_ships)
                for col in range(10)
            )

    def fire_at(self, x: int, y: int) -> None:
        """Fire at a square"""
        self.board[y][x] = True

        # Automatically surround the ship with misses
        # when it's completely destroyed
        for ship in self.ships:
            taken_down = True
            for square in ship.squares():
                if not self.board[square[1]][square[0]]:
                    taken_down = False
                    break
            if taken_down:
                for square in ship.squares():
                    for location in [
                        (square[0] - 1, square[1]),
                        (square[0] + 1, square[1]),
                        (square[0], square[1] - 1),
                        (square[0], square[1] + 1),
                    ]:
                        if 0 <= location[0] < 10 and 0 <= location[1] < 10:
                            self.board[location[1]][location[0]] = True


class Agent(ABC):
    """The base class for all agents"""

    @abstractmethod
    def fire(self, board: Board) -> tuple[int, int]:
        """Choose the best location to fire at"""
        raise NotImplementedError


class Renderer:
    def __init__(
        self, boards: tuple[Board, Board], agent: Agent, encodings=None
    ) -> None:
        self.boards = boards
        if encodings is None:
            encodings = {
                "empty": "   ",
                "hit": " X ",
                "miss": " O ",
                "ship": " # ",
                "preview": " * ",
                "invalid_preview": " ! ",
            }
        self.encodings = encodings
        self.agent = agent

    def render(self, reveal=False):
        """Render the boards"""
        renders = [
            self.render_board(board, bool(i) or reveal)
            for i, board in enumerate(self.boards)
        ]
        for line in zip(*renders):
            print("\t".join(f"|{content}|" for content in line))
        print()

    def render_board(
        self, board, show_ships, preview_ship_placement: Optional[Ship] = None
    ):
        """Render a single board"""
        return [" " + "".join(f" {i} " for i in range(1, 10)) + " 10"] + [
            string.ascii_uppercase[i]
            + "".join(
                self.encodings[square]
                if (
                    preview_ship_placement is None
                    or not preview_ship_placement.does_occupy_square((j, i))
                )
                else (
                    self.encodings["preview"]
                    if board.check_ship_placement_legality(
                        preview_ship_placement.location,
                        preview_ship_placement.direction,
                        preview_ship_placement.length,
                    )
                    else self.encodings["invalid_preview"]
                )
                for j, square in enumerate(row)
            )
            for i, row in enumerate(board.states(show_ships))
        ]

    def _place_enter_direction(self) -> Direction:
        print("Enter ship direction (e.g. right): ")
        direction = input(">>> ").lower()
        return {
            "right": Direction.right,
            "down": Direction.down,
            "left": Direction.left,
            "up": Direction.up,
            "r": Direction.right,
            "d": Direction.down,
            "l": Direction.left,
            "u": Direction.up,
        }[direction]

    def _place_enter_location(self) -> tuple[int, int]:
        print("Enter ship location (e.g. A1): ")
        location = input(">>> ").upper()
        return int(location[1:]) - 1, string.ascii_uppercase.index(location[0])

    def _place_enter_length(self) -> int:
        print("You can still place the following ships:")
        for length, allowed_count in self.boards[1].allowed.items():
            active_count = self.boards[1].count_ships(length)
            if active_count < allowed_count:
                print(f"{length}-long ships: {allowed_count - active_count}")
        print()
        print("Enter ship length (e.g. 3): ")
        length = int(input(">>> "))
        if not self.boards[1].get_if_ship_allowed(length):
            print("You can't place more ships of this length.")
            raise ValueError
        return length

    def place_ship(self):
        """Place a ship on the board"""
        while True:
            try:
                print(
                    "\n".join(
                        self.render_board(
                            self.boards[1],
                            show_ships=True,
                        )
                    )
                )
                print()

                length = self._place_enter_length()
                location = self._place_enter_location()
                direction = self._place_enter_direction()

                ship = Ship(location, direction, length)
                print(
                    "\n".join(
                        self.render_board(
                            self.boards[1],
                            show_ships=True,
                            preview_ship_placement=ship,
                        )
                    )
                )

                is_legal = self.boards[1].check_ship_placement_legality(
                    ship.location, ship.direction, ship.length
                )
                if not is_legal:
                    print("This ship placement is illegal.")
                    raise ValueError

                print("Is this correct? (y/n)")
                if input(">>> ").lower() == "y":
                    self.boards[1].place_ship(location, direction, length)
                    return
            except (ValueError, IndexError, KeyError):
                print("Invalid input")

    def autoplace(self):
        """Place ships automatically"""
        # This does some recursive magic
        # It places the ship in a candidate spot
        # and then trying to place the next ship
        # if it fails, it tries the next candidate spot
        # if it runs out of candidate spots, it backtracks
        # and tries the next candidate spot for the previous ship
        # and so on
        #
        # Not the most efficient way, but it works
        board = self.boards[0]
        if all(
            board.count_ships(length) == allowed_count
            for length, allowed_count in board.allowed.items()
        ):
            return True
        for length, allowed_count in board.allowed.items():
            if board.count_ships(length) < allowed_count:
                directions = list(Direction)
                random.shuffle(directions)
                for direction in directions:
                    candidates = sum(
                        (
                            [(i, j) for i in range(10 - length + 1)]
                            for j in range(10)
                        ),
                        [],
                    )
                    random.shuffle(candidates)
                    for location in candidates:
                        is_legal = board.check_ship_placement_legality(
                            location,
                            direction,
                            length,
                        )
                        if is_legal:
                            board.place_ship(
                                location,
                                direction,
                                length,
                            )
                            further = self.autoplace()
                            if further:
                                return True
                            else:
                                del board.ships[-1]
                break
        return False

    def _fire_enter_location(self) -> tuple[int, int]:
        print("Enter fire location (e.g. A1): ")
        location = input(">>> ").upper()
        return int(location[1:]) - 1, string.ascii_uppercase.index(location[0])

    def fire(self):
        """Fire a shot and respond with the agent"""
        while True:
            try:
                location = self._fire_enter_location()
                self.boards[0].fire_at(*location)
                agent_fire = self.agent.fire(self.boards[1])
                self.boards[1].fire_at(*agent_fire)
                print(
                    f"Agent fired at {string.ascii_uppercase[agent_fire[1]]}{agent_fire[0] + 1}"
                )
                break
            except (ValueError, IndexError, KeyError):
                print("Invalid input")


class ParityHuntAndTargetAgent(Agent):
    """An agent that uses the parity hunt and target strategy

    Hunt and target means that it first looks at if there
    are any ships it just hit and expands those newly hit areas

    Parity hunt means that it targets every other square
    in a checkerboard pattern in its hunt phase
    """

    def fire(self, board) -> tuple[int, int]:
        """Choose the best location to fire at"""
        # Look for any recent hits
        for i, row in enumerate(board.states(False)):
            for j, square in enumerate(row):
                if square == "hit":
                    # Expand the hit area
                    # First we see if we can move
                    # in a reverse direction
                    # of another existing hit
                    # If we can, we do that
                    for direction in Direction:
                        # Source hit
                        x = j + direction.value[0]
                        y = i + direction.value[1]
                        if not (0 <= x < 10 and 0 <= y < 10):
                            continue
                        if board.get_square_state(x, y, False) == "hit":
                            # Target hit (unknown)
                            x_ = j - direction.value[0]
                            y_ = i - direction.value[1]
                            if not (0 <= x_ < 10 and 0 <= y_ < 10):
                                continue
                            if not board.board[y_][x_]:
                                # We can move in the direction of the target
                                return x_, y_

        for i, row in enumerate(board.states(False)):
            for j, square in enumerate(row):
                if square == "hit":
                    # If this is a lonely hit
                    # so we don't know where to
                    # expand to,
                    # we pick the direction randomly
                    # so that the human player
                    # can't strategize against it
                    directions = list(Direction)
                    random.shuffle(directions)
                    for direction in directions:
                        x = j + direction.value[0]
                        y = i + direction.value[1]
                        if 0 <= x < 10 and 0 <= y < 10:
                            if not board.board[y][x]:
                                return (x, y)

        # If there are no recent hits, hunt
        candidates = [
            candidate
            for candidate in board.get_all_possible_fires()
            if sum(candidate) % 2
        ]
        return random.choice(candidates)


def choose_charset():
    """Choose the character set to use"""
    print("Can you see these emojis? (y/n)")
    print("▫️🟥🟦🟩🟧")
    if input(">>> ").lower() == "y":
        return {
            "empty": "   ",
            "hit": "🟥 ",
            "miss": "▫️ ",
            "ship": "🟦 ",
            "preview": "🟩 ",
            "invalid_preview": "🟧 ",
        }
    return None


def main():
    """The main game loop"""
    charset = choose_charset()
    boards = (Board(), Board())
    renderer = Renderer(boards, ParityHuntAndTargetAgent(), charset)
    renderer.autoplace()
    for i in range(5):
        renderer.place_ship()
    while not any(board.is_game_over() for board in boards):
        renderer.render()
        renderer.fire()
    print("Game over")
    renderer.render(True)
    if boards[0].is_game_over():
        print("You won! Congratulations!")
    else:
        print("You lost. Better luck next time!")


if __name__ == "__main__":
    main()

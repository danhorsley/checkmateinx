# flaskb/chess_model.py


class ChessPiece:

    def __init__(self, piece_type, color, position):
        """
        Initialize a chess piece

        Args:
            piece_type (str): Type of piece ('p'=pawn, 'r'=rook, 'n'=knight, 'b'=bishop, 'q'=queen, 'k'=king)
            color (str): Color of piece ('w'=white, 'b'=black)
            position (tuple): Position on board as (row, col), where (0,0) is top-left
        """
        self.piece_type = piece_type
        self.color = color
        self.position = position

    def __repr__(self):
        return f"{self.color}{self.piece_type}@{self.position}"

    def to_dict(self):
        """Convert piece to dictionary for JSON serialization"""
        return {
            "type": self.piece_type,
            "color": self.color,
            "position": {
                "row": self.position[0],
                "col": self.position[1]
            }
        }


class ChessBoard:

    def __init__(self, missing_squares=None):
        """
        Initialize a chess board

        Args:
            missing_squares (list): List of (row, col) tuples representing inaccessible squares
        """
        self.pieces = []
        self.missing_squares = missing_squares or []
        self.size = 8  # Standard 8x8 chess board

    def add_piece(self, piece_type, color, position):
        """Add a piece to the board"""
        # Check if position is valid
        row, col = position
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise ValueError(f"Position {position} is out of bounds")

        # Check if position is a missing square
        if position in self.missing_squares:
            raise ValueError(
                f"Cannot place piece on missing square {position}")

        # Check if position is already occupied
        for piece in self.pieces:
            if piece.position == position:
                raise ValueError(f"Position {position} is already occupied")

        # Add the piece
        piece = ChessPiece(piece_type, color, position)
        self.pieces.append(piece)
        return piece

    def clear(self):
        """Clear all pieces from the board"""
        self.pieces = []

    def get_piece_at(self, position):
        """Get piece at a specific position, or None if empty"""
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    def to_dict(self):
        """Convert board to dictionary for JSON serialization"""
        return {
            "pieces": [piece.to_dict() for piece in self.pieces],
            "missingSquares": [{
                "row": row,
                "col": col
            } for row, col in self.missing_squares],
            "size":
            self.size
        }


class ChessPuzzle:

    def __init__(self, initial_board, moves_to_checkmate, difficulty=1):
        """
        Initialize a chess puzzle

        Args:
            initial_board (ChessBoard): The initial board setup
            moves_to_checkmate (int): Number of moves required to reach checkmate
            difficulty (int): Difficulty rating of the puzzle (1-5)
        """
        self.board = initial_board
        self.moves_to_checkmate = moves_to_checkmate
        self.difficulty = difficulty
        self.puzzle_id = None  # Will be set when saved

    def to_dict(self):
        """Convert puzzle to dictionary for JSON serialization"""
        return {
            "id": self.puzzle_id,
            "board": self.board.to_dict(),
            "movesToCheckmate": self.moves_to_checkmate,
            "difficulty": self.difficulty
        }


# Simple in-memory store for puzzles
# In a real app, this would use a database
class PuzzleStore:

    def __init__(self):
        self.puzzles = {}
        self.next_id = 1

    def add_puzzle(self, puzzle):
        """Add a puzzle to the store and assign it an ID"""
        puzzle_id = str(self.next_id)
        self.next_id += 1
        puzzle.puzzle_id = puzzle_id
        self.puzzles[puzzle_id] = puzzle
        return puzzle_id

    def get_puzzle(self, puzzle_id):
        """Get a puzzle by ID"""
        return self.puzzles.get(puzzle_id)

    def get_all_puzzles(self):
        """Get all puzzles"""
        return list(self.puzzles.values())

    def get_puzzles_by_difficulty(self, difficulty):
        """Get all puzzles with a specific difficulty"""
        return [p for p in self.puzzles.values() if p.difficulty == difficulty]


# Initialize the global puzzle store
puzzle_store = PuzzleStore()


# Create some sample puzzles
def create_sample_puzzles():
    # Puzzle 1: Checkmate in 1 move (Queen takes f7)
    board1 = ChessBoard()
    # Add white pieces
    board1.add_piece('q', 'w', (3, 3))  # Queen at d4
    board1.add_piece('k', 'w', (7, 4))  # King at e1
    # Add black pieces
    board1.add_piece('k', 'b', (0, 4))  # King at e8
    board1.add_piece('p', 'b', (1, 5))  # Pawn at f7
    board1.add_piece('p', 'b', (1, 3))  # Pawn at d7
    puzzle1 = ChessPuzzle(board1, moves_to_checkmate=1, difficulty=1)
    puzzle_store.add_puzzle(puzzle1)

    # Puzzle 2: Checkmate in 2 moves with missing squares
    board2 = ChessBoard(missing_squares=[(3, 3), (3, 4), (4, 3),
                                         (4, 4)])  # Center squares missing
    # Add white pieces
    board2.add_piece('r', 'w', (7, 0))  # Rook at a1
    board2.add_piece('k', 'w', (7, 4))  # King at e1
    # Add black pieces
    board2.add_piece('k', 'b', (0, 1))  # King at b8
    puzzle2 = ChessPuzzle(board2, moves_to_checkmate=2, difficulty=2)
    puzzle_store.add_puzzle(puzzle2)

    return [puzzle1, puzzle2]

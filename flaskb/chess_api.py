# flaskb/chess_api.py

from flask import Blueprint, jsonify, request
from .chess_model import puzzle_store, create_sample_puzzles, ChessBoard, ChessPuzzle

# Create the blueprint
chess_bp = Blueprint('chess', __name__, url_prefix='/api/chess')

# Initialize sample puzzles on startup
sample_puzzles = create_sample_puzzles()


@chess_bp.route('/puzzles', methods=['GET'])
def get_puzzles():
    """Get all puzzles or filter by difficulty"""
    difficulty = request.args.get('difficulty')

    if difficulty:
        try:
            difficulty = int(difficulty)
            puzzles = puzzle_store.get_puzzles_by_difficulty(difficulty)
        except ValueError:
            return jsonify({"error": "Difficulty must be an integer"}), 400
    else:
        puzzles = puzzle_store.get_all_puzzles()

    return jsonify({"puzzles": [puzzle.to_dict() for puzzle in puzzles]})


@chess_bp.route('/puzzles/<puzzle_id>', methods=['GET'])
def get_puzzle(puzzle_id):
    """Get a specific puzzle by ID"""
    puzzle = puzzle_store.get_puzzle(puzzle_id)

    if not puzzle:
        return jsonify({"error": "Puzzle not found"}), 404

    return jsonify(puzzle.to_dict())


@chess_bp.route('/puzzles', methods=['POST'])
def create_puzzle():
    """Create a new puzzle"""
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Extract puzzle data
        moves_to_checkmate = data.get('movesToCheckmate', 1)
        difficulty = data.get('difficulty', 1)

        # Create the board
        missing_squares = []
        if 'missingSquares' in data:
            for square in data['missingSquares']:
                row = square.get('row')
                col = square.get('col')
                if row is not None and col is not None:
                    missing_squares.append((row, col))

        board = ChessBoard(missing_squares=missing_squares)

        # Add pieces to the board
        if 'pieces' in data:
            for piece_data in data['pieces']:
                piece_type = piece_data.get('type')
                color = piece_data.get('color')
                position = (piece_data.get('position', {}).get('row'),
                            piece_data.get('position', {}).get('col'))

                if None in (piece_type, color, position[0], position[1]):
                    return jsonify({"error": "Invalid piece data"}), 400

                board.add_piece(piece_type, color, position)

        # Create the puzzle
        puzzle = ChessPuzzle(board, moves_to_checkmate, difficulty)
        puzzle_id = puzzle_store.add_puzzle(puzzle)

        return jsonify({
            "message": "Puzzle created successfully",
            "id": puzzle_id,
            "puzzle": puzzle.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@chess_bp.route('/daily', methods=['GET'])
def get_daily_puzzle():
    """Get the daily puzzle"""
    # In a real app, this would fetch or generate the puzzle of the day
    # For now, we'll just return the first sample puzzle
    puzzles = puzzle_store.get_all_puzzles()
    if not puzzles:
        return jsonify({"error": "No puzzles available"}), 404

    return jsonify({"daily": True, "puzzle": puzzles[0].to_dict()})

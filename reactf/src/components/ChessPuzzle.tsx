// reactf/src/components/ChessPuzzle.tsx
import React, { useState, useEffect } from "react";
import ChessBoard from "./ChessBoard";

interface Position {
  row: number;
  col: number;
}

interface ChessPiece {
  type: string;
  color: string;
  position: Position;
}

interface ChessBoard {
  pieces: ChessPiece[];
  missingSquares: Position[];
  size: number;
}

interface Puzzle {
  id: string;
  board: ChessBoard;
  movesToCheckmate: number;
  difficulty: number;
}

interface ChessPuzzleProps {
  puzzleId?: string; // Optional: if not provided, will fetch daily puzzle
}

const ChessPuzzle: React.FC<ChessPuzzleProps> = ({ puzzleId }) => {
  const [puzzle, setPuzzle] = useState<Puzzle | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPuzzle = async () => {
      try {
        setLoading(true);

        // Determine the API endpoint based on whether puzzleId is provided
        const apiUrl = puzzleId
          ? `/api/chess/puzzles/${puzzleId}`
          : "/api/chess/daily";

        // Fetch the puzzle
        const response = await fetch(apiUrl);

        if (!response.ok) {
          throw new Error(`Failed to fetch puzzle: ${response.statusText}`);
        }

        const data = await response.json();

        // Handle different response formats between daily and specific puzzles
        setPuzzle(data.puzzle || data);
        setError(null);
      } catch (err) {
        console.error("Error fetching puzzle:", err);
        setError("Failed to load the chess puzzle. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchPuzzle();
  }, [puzzleId]);

  if (loading) {
    return <div>Loading puzzle...</div>;
  }

  if (error) {
    return <div style={{ color: "red" }}>{error}</div>;
  }

  if (!puzzle) {
    return <div>No puzzle found</div>;
  }

  return (
    <div style={{ textAlign: "center" }}>
      <h2>Chess Puzzle</h2>
      <div>
        <p>Difficulty: {puzzle.difficulty}/5</p>
        <p>
          Find checkmate in {puzzle.movesToCheckmate} move
          {puzzle.movesToCheckmate > 1 ? "s" : ""}
        </p>
      </div>

      <ChessBoard
        pieces={puzzle.board.pieces}
        missingSquares={puzzle.board.missingSquares}
        size={puzzle.board.size}
      />

      <div style={{ marginTop: "20px" }}>
        <button>Show Solution</button>
      </div>
    </div>
  );
};

export default ChessPuzzle;

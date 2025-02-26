// reactf/src/components/ChessBoard.tsx
import React from "react";

// Define types for our chess pieces and board
interface Position {
  row: number;
  col: number;
}

interface ChessPiece {
  type: string;
  color: string;
  position: Position;
}

interface MissingSquare {
  row: number;
  col: number;
}

interface ChessBoardProps {
  pieces: ChessPiece[];
  missingSquares?: MissingSquare[];
  size?: number;
}

const ChessBoard: React.FC<ChessBoardProps> = ({
  pieces,
  missingSquares = [],
  size = 8,
}) => {
  // Convert piece type and color to Unicode chess piece
  const getPieceUnicode = (type: string, color: string): string => {
    const pieceMap: { [key: string]: { [key: string]: string } } = {
      k: { w: "♔", b: "♚" }, // King
      q: { w: "♕", b: "♛" }, // Queen
      r: { w: "♖", b: "♜" }, // Rook
      b: { w: "♗", b: "♝" }, // Bishop
      n: { w: "♘", b: "♞" }, // Knight
      p: { w: "♙", b: "♟" }, // Pawn
    };

    return pieceMap[type]?.[color] || "?";
  };

  // Check if a square is a "missing" square
  const isMissingSquare = (row: number, col: number): boolean => {
    return missingSquares.some(
      (square) => square.row === row && square.col === col,
    );
  };

  // Find a piece at a specific position
  const getPieceAt = (row: number, col: number): ChessPiece | undefined => {
    return pieces.find(
      (piece) => piece.position.row === row && piece.position.col === col,
    );
  };

  // Render the chess board
  const renderBoard = () => {
    const rows = [];

    for (let row = 0; row < size; row++) {
      const cols = [];

      for (let col = 0; col < size; col++) {
        // Determine square color (alternating black and white)
        const isBlackSquare = (row + col) % 2 === 1;
        const isMissing = isMissingSquare(row, col);
        const piece = getPieceAt(row, col);

        cols.push(
          <div
            key={`${row}-${col}`}
            style={{
              width: "60px",
              height: "60px",
              backgroundColor: isMissing
                ? "#999"
                : isBlackSquare
                  ? "#b58863"
                  : "#f0d9b5",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: "40px",
            }}
          >
            {!isMissing && piece && getPieceUnicode(piece.type, piece.color)}
          </div>,
        );
      }

      rows.push(
        <div key={row} style={{ display: "flex" }}>
          {cols}
        </div>,
      );
    }

    return rows;
  };

  return (
    <div
      style={{
        border: "2px solid #333",
        display: "inline-block",
        margin: "20px",
      }}
    >
      {renderBoard()}
    </div>
  );
};

export default ChessBoard;

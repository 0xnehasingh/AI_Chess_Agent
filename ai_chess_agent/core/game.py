from typing import List
import chess
import chess.svg


def available_moves(board: chess.Board) -> str:
    available_moves: List[str] = [str(move) for move in board.legal_moves]
    return "Available moves are: " + ",".join(available_moves)


def execute_move(board: chess.Board, move: str) -> str:
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move not in board.legal_moves:
            return f"Invalid move: {move}. Please call available_moves() to see valid moves."

        board.push(chess_move)

        board_svg = chess.svg.board(
            board,
            arrows=[(chess_move.from_square, chess_move.to_square)],
            fill={chess_move.from_square: "gray"},
            size=400,
        )

        moved_piece = board.piece_at(chess_move.to_square)
        if moved_piece is None:
            return f"No piece at {chess_move.to_square} after move."
        piece_unicode = moved_piece.unicode_symbol()
        piece_type_name = chess.piece_name(moved_piece.piece_type)
        piece_name = piece_type_name.capitalize() if piece_unicode.isupper() else piece_type_name

        from_square = chess.SQUARE_NAMES[chess_move.from_square]
        to_square = chess.SQUARE_NAMES[chess_move.to_square]
        move_desc = f"Moved {piece_name} ({piece_unicode}) from {from_square} to {to_square}."
        if board.is_checkmate():
            winner = 'White' if board.turn == chess.BLACK else 'Black'
            move_desc += f"\nCheckmate! {winner} wins!"
        elif board.is_stalemate():
            move_desc += "\nGame ended in stalemate!"
        elif board.is_insufficient_material():
            move_desc += "\nGame ended - insufficient material to checkmate!"
        elif board.is_check():
            move_desc += "\nCheck!"

        return move_desc
    except ValueError:
        return f"Invalid move format: {move}. Please use UCI format (e.g., 'e2e4')." 
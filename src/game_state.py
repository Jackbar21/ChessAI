"""
Game state representation for chess.

Encapsulates all game state information including turn, castling rights,
en passant square, and move counters.
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple
from src.constants import Color


@dataclass
class CastlingRights:
    """Represents castling rights for both players."""
    white_kingside: bool = True
    white_queenside: bool = True
    black_kingside: bool = True
    black_queenside: bool = True
    
    def can_castle_kingside(self, color: Color) -> bool:
        """Check if the given color can castle kingside."""
        return self.white_kingside if color == Color.WHITE else self.black_kingside
    
    def can_castle_queenside(self, color: Color) -> bool:
        """Check if the given color can castle queenside."""
        return self.white_queenside if color == Color.WHITE else self.black_queenside
    
    def set_kingside(self, color: Color, value: bool) -> None:
        """Set kingside castling right for the given color."""
        if color == Color.WHITE:
            self.white_kingside = value
        else:
            self.black_kingside = value
    
    def set_queenside(self, color: Color, value: bool) -> None:
        """Set queenside castling right for the given color."""
        if color == Color.WHITE:
            self.white_queenside = value
        else:
            self.black_queenside = value
    
    def revoke_all(self, color: Color) -> None:
        """Revoke all castling rights for the given color."""
        self.set_kingside(color, False)
        self.set_queenside(color, False)
    
    def to_fen(self) -> str:
        """Convert to FEN castling rights notation."""
        rights = ""
        if self.white_kingside:
            rights += "K"
        if self.white_queenside:
            rights += "Q"
        if self.black_kingside:
            rights += "k"
        if self.black_queenside:
            rights += "q"
        return rights if rights else "-"
    
    @classmethod
    def from_fen(cls, fen_str: str) -> 'CastlingRights':
        """Parse FEN castling rights notation."""
        return cls(
            white_kingside='K' in fen_str,
            white_queenside='Q' in fen_str,
            black_kingside='k' in fen_str,
            black_queenside='q' in fen_str,
        )
    
    def copy(self) -> 'CastlingRights':
        """Create a deep copy of castling rights."""
        return CastlingRights(
            white_kingside=self.white_kingside,
            white_queenside=self.white_queenside,
            black_kingside=self.black_kingside,
            black_queenside=self.black_queenside,
        )


@dataclass
class GameState:
    """
    Represents the complete game state for a chess position.
    
    Includes turn, castling rights, en passant square, and move counters.
    This matches the FEN notation standard.
    """
    turn: Color = Color.WHITE
    castling_rights: CastlingRights = field(default_factory=CastlingRights)
    en_passant_square: Optional[Tuple[int, int]] = None
    halfmove_clock: int = 0  # Moves since last pawn advance or capture (for 50-move rule)
    fullmove_number: int = 1  # Increments after Black's move
    
    def opponent_color(self) -> Color:
        """Get the opponent's color."""
        return Color.BLACK if self.turn == Color.WHITE else Color.WHITE
    
    def to_fen_fields(self) -> Tuple[str, str, str, str, str]:
        """
        Convert game state to FEN fields.
        
        Returns:
            Tuple of (turn, castling, en_passant, halfmove, fullmove) strings
        """
        # Turn
        turn_str = "w" if self.turn == Color.WHITE else "b"
        
        # Castling
        castling_str = self.castling_rights.to_fen()
        
        # En passant
        if self.en_passant_square:
            rank, file = self.en_passant_square
            ep_str = f"{'abcdefgh'[file]}{rank + 1}"
        else:
            ep_str = "-"
        
        # Move counters
        halfmove_str = str(self.halfmove_clock)
        fullmove_str = str(self.fullmove_number)
        
        return (turn_str, castling_str, ep_str, halfmove_str, fullmove_str)
    
    @classmethod
    def from_fen_fields(
        cls, 
        turn: str, 
        castling: str, 
        en_passant: str, 
        halfmove: str, 
        fullmove: str
    ) -> 'GameState':
        """
        Parse FEN game state fields.
        
        Args:
            turn: 'w' or 'b'
            castling: e.g. 'KQkq', 'Kq', '-'
            en_passant: e.g. 'e3', '-'
            halfmove: halfmove clock as string
            fullmove: fullmove number as string
        
        Returns:
            GameState object
        """
        # Parse turn
        color = Color.WHITE if turn == 'w' else Color.BLACK
        
        # Parse castling rights
        castling_rights = CastlingRights.from_fen(castling)
        
        # Parse en passant
        ep_square = None
        if en_passant != '-':
            file = 'abcdefgh'.index(en_passant[0])
            rank = int(en_passant[1]) - 1
            ep_square = (rank, file)
        
        # Parse move counters
        halfmove_clock = int(halfmove)
        fullmove_number = int(fullmove)
        
        return cls(
            turn=color,
            castling_rights=castling_rights,
            en_passant_square=ep_square,
            halfmove_clock=halfmove_clock,
            fullmove_number=fullmove_number,
        )
    
    def copy(self) -> 'GameState':
        """Create a deep copy of the game state."""
        return GameState(
            turn=self.turn,
            castling_rights=self.castling_rights.copy(),
            en_passant_square=self.en_passant_square,
            halfmove_clock=self.halfmove_clock,
            fullmove_number=self.fullmove_number,
        )

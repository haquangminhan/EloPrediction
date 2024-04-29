// Promotion.js
import React from 'react';

function Promotion({ onPromote, isVisible, color }) {
  if (!isVisible) {
    return null;
  }

  const pieces = ['q', 'r', 'b', 'n']; // Queen, Rook, Bishop, Knight
  const squareSize = `10vh`; // Size to match the chessboard pieces

  const handlePromotionChoice = (piece) => {
    onPromote(piece);
  };

  return (
    <div style={{
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      zIndex: 100,
      backgroundColor: 'rgb(52, 73, 85, 0.75)',
      padding: '20px',
      borderRadius: '50px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        {pieces.map((piece, index) => (
          <div key={index} onClick={() => handlePromotionChoice(piece)} style={{ margin: '10px', cursor: 'pointer', width: squareSize, height: squareSize }}>
            <img src={`/images/${color}${piece.toUpperCase()}.svg`} alt={piece} style={{ width: '100%', height: '100%' }} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default Promotion;

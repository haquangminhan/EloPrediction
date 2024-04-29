// Chessboard.js
import React, { useState, useEffect } from 'react';
import Piece from './Piece';
import Promotion from './Promotion';

function Chessboard({ boardState, setPredictionMessage }) {
  const [board, setBoard] = useState({});
  const [selectedPiece, setSelectedPiece] = useState(null);
  const [checkmateColor, setCheckmateColor] = useState(null);
  const [promotionPos, setPromotionPos] = useState(null); // Position where the promotion is happening
  const [promotionColor, setPromotionColor] = useState('');

  useEffect(() => {
    if (boardState) {
      setBoard(boardState);
      setCheckmateColor(null);
    } else {
      fetchBoard();
    }
  }, [boardState]); 

  const fetchBoard = () => {
    fetch('/board')
      .then(response => response.json())
      .then(data => {
        setBoard(data.board);
        setCheckmateColor(data.checkmateColor);
      });
  };

  const makeMove = (start, end, promotionPiece = '') => {
    console.log(`Making move: Start: ${start}, End: ${end}, Promotion: ${promotionPiece}`);
    const moveData = promotionPiece ? { start, end, promotion: promotionPiece } : { start, end };
    fetch('/move', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(moveData),
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        setBoard(data.board);
        if (data.prediction) {
          // console.log(data.prediction)
          setPredictionMessage(data.prediction);
        }
        if (promotionPiece) {
          setPromotionPos(null);
          setPromotionColor('');
        }
      } else {
        console.log('Move failed');
      }
      setCheckmateColor(data.checkmateColor);
      setSelectedPiece(null);
    });
  };

  const handleSquareClick = (position) => {
    if (selectedPiece) {
      const piece = board[selectedPiece];
      if (piece && (piece === 'wP' || piece === 'bP')) {
        const targetRow = position.charAt(0);
        if ((piece === 'wP' && targetRow === '0') || (piece === 'bP' && targetRow === '7')) {
          setPromotionPos(position);
          setPromotionColor(piece[0]);
          return;
        }
      }
      makeMove(selectedPiece, position);
    } else if (board[position]) {
      setSelectedPiece(position);
    }
  };

  const handlePromotion = (piece) => {
    if (selectedPiece && promotionPos) {
      makeMove(selectedPiece, promotionPos, piece);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexWrap: 'wrap',
      width: '80vh',
      height: '80vh',
      maxWidth: '100%',
    }}>
      
      {Array.from(Array(8).keys()).map(row =>
        Array.from(Array(8).keys()).map(column => {
          const position = `${row}${column}`;
          const piece = board[position];
          const isKingInCheckmate = piece && piece[0].toLowerCase() === checkmateColor && piece[1].toLowerCase() === 'k';

          return (
            <Piece
              key={`key-${position}`}
              piece={piece}
              position={position}
              handleClick={() => handleSquareClick(position)}
              isKingInCheckmate={isKingInCheckmate}
            />
          );
        })
      )}
      {promotionPos && (
        <Promotion
          onPromote={handlePromotion}
          isVisible={!!promotionPos}
          color={promotionColor}
        />
      )}
    </div>
  );
}

export default Chessboard;

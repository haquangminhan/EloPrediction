function Piece({ piece, position, handleClick, isKingInCheckmate }) {
    const squareSize = `10vh`;
    const baseColor = (parseInt(position[0], 10) + parseInt(position[1], 10)) % 2 === 0 ? 'rgb(238,238,213)' : 'rgb(120, 160, 131)';
    const squareColor = isKingInCheckmate ? 'red' : baseColor;
    const pieceImage = piece ? `/images/${piece}.svg` : null;
  
    return (
      <div
        onClick={() => handleClick(position)}
        style={{
          width: squareSize,
          height: squareSize,
          backgroundColor: squareColor,
          backgroundImage: pieceImage ? `url(${pieceImage})` : '',
          backgroundSize: 'contain',
          backgroundPosition: 'center',
          cursor: piece ? 'pointer' : 'default',
          boxSizing: 'border-box',
        }}
      />
    );
  }
  
  
export default Piece;
  
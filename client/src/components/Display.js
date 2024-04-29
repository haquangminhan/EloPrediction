// Display.js
import React from 'react';

function Display({ message, onNext }) {
  const labels = [
    "move_quality['small']",
    "move_quality['medium']",
    "move_quality['large']",
    "position_eval['small']",
    "position_eval['medium']",
    "position_eval['large']"
  ];

  return (
    <div style={{
      height: '78vh',
      width: '30vh',
      padding: '10px',
      margin: '10px',
      backgroundColor: 'rgb(80, 114, 123)',
      fontSize: '1.2em',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between'
    }}>
      <div>
      {message ? (
        <div>
          <strong>Elo: {Number(message[message.length - 1]).toFixed(0)} ± 92.8</strong>
          {message.slice(0, -1).map((item, index) => (
            <div key={index}>
              {`${labels[index]}: ${Number(item).toFixed(4)}`}
            </div>
          ))}
        </div>
      ) : (
        <strong>Elo: </strong>
      )}
      </div>
      <button onClick={onNext} style={{ marginTop: '20px', borderRadius: '10px', height: '10%', background: 'rgb(52, 73, 85)', fontSize: '100%', fontWeight: 'bold' }}>Reset</button>
    </div>
  );
}

export default Display;

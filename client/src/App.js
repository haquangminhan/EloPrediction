// App.js
import React, { useState } from "react";
import Chessboard from "./components/Chessboard";
import Display from "./components/Display";

function App() {
  // const fens = [
  //   '7K/P1p1p1p1/2P1P1Pk/6pP/3p2P1/1P6/3P4/8 w - - 0 1',
  //   'K6k/8/8/8/8/8/p7/8 b - - 0 1',
  //   '8/8/8/8/4p3/5k2/8/4K3 b - - 0 1',
  //   '5r1k/1p2rp2/p2Q2p1/2p1n3/2P1P3/2K2P1B/PP6/R7 b - - 0 31',
  //   '3r4/1p1Brpk1/2n3p1/p1Q5/2P1P3/2K2P2/PP6/7R w - - 2 35',
  //   'r3k2r/1ppnnpp1/p2p1q1p/4p3/2PbP3/P1NP1Q1P/1P1BBPP1/1R3RK1 b kq - 1 12',
  //   '3r3r/1k2bppp/2p5/Pp1p4/3P1B2/4RK2/5PPP/1R6 b - - 3 29',
  //   'r3kbnr/ppp1pppp/8/8/3P4/2nBB3/Pq2NPPP/R2QK2R w KQkq - 0 14',
  // ];

  const [boardState, setBoardState] = useState(null);
  const [predictionMessage, setPredictionMessage] = useState();


  const handleNext = () => {
    fetch('/next_fen')
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        setBoardState(data.board);  // Update the board state with the response
        setPredictionMessage();
        console.log('Board updated to new FEN.');
      } else {
        console.error('Failed to update board.');
      }
    });
  };

  console.log(predictionMessage)

  return (
    <div style={{
      backgroundColor: 'rgb(53, 55, 75)',
      height: '100vh',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      {<Chessboard boardState={boardState} setPredictionMessage={setPredictionMessage}/>}
      {<Display message={predictionMessage} onNext={handleNext} />}
    </div>
  );
}

export default App;

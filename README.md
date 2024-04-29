# Elo Prediction

This project is designed to predict Elo ratings using historical game data. It's built using React for the frontend and Flask for the backend, providing an interactive web interface for users to input data and view predictions.

## Getting Started

Follow these instructions to get the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed:
- Node.js
- npm
- Python 3

### Installation

Put the downloaded link inside the folder server and put the right directory in the chessEngine class inside chessEngine.py:

1. This is the link to the Leela Zero network (download 3 files and put them in the folder name ‘Lc0 networks’ inside the server file): https://lczero.org/play/networks/bestnets/

2. For macOS users, install Stockfish using Homebrew:

```bash
brew install stockfish
```

#### Frontend Setup

Navigate to the root directory where the React app is located, and install the required npm packages:

```bash
cd client
npm install
npm start
```

#### Backend Setup

Navigate to the server directory and install Python dependencies:

```bash
cd server
pip3 install -r requirements.txt
python3 server.py
```

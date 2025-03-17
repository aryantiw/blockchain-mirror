# Blockchain-Based Transaction System

## Overview
This project is a simple blockchain-based transaction system with a Proof of Work (PoW) consensus algorithm. It includes a Flask backend for handling transactions, mining new blocks, and retrieving blockchain data, along with an HTML/JavaScript frontend for interacting with the blockchain.

## Features
- Create new transactions between users
- Mine new blocks using a Proof of Work algorithm
- View the entire blockchain
- Simple web-based frontend for user interaction

## File Structure
- `blockchain.py`: Implements the blockchain, transaction handling, and mining logic using Flask.
- `pow_algorithm.py`: Implements a simple proof-of-work algorithm.
- `index.html`: Provides a user-friendly frontend to interact with the blockchain.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Flask
- Flask-CORS

### Steps
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```sh
   pip install flask flask-cors
   ```
3. Run the Flask server:
   ```sh
   python blockchain.py
   ```
4. Open `index.html` in a browser to interact with the blockchain.

## API Endpoints
- **GET `/mine`**: Mines a new block and adds it to the blockchain.
- **POST `/transaction/new`**: Creates a new transaction (requires `sender`, `recipient`, and `amount` in the request body).
- **GET `/chain`**: Returns the current blockchain.

## Frontend Usage
1. Open `index.html` in a browser.
2. Use the form to create transactions.
3. Click "Mine Block" to mine a new block.
4. Click "View Blockchain" to display the full chain.

## Proof of Work Algorithm
The proof-of-work mechanism ensures computational work is required to add a block, preventing spam and securing the blockchain. The algorithm finds a number `y` such that `sha256(f'{x*y}'.encode()).hexdigest()[-1] == "0"`.

## Future Improvements
- Implementing a more efficient consensus algorithm.
- Enhancing security with cryptographic signatures.
- Adding a distributed peer-to-peer network.

## License
This project is open-source and available under the MIT License.


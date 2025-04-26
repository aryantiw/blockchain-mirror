import hashlib
import json
import os
from flask import render_template


from time import time
from uuid import uuid4
from textwrap import dedent

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Now you can apply CORS to the app
CORS(app)

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transaction = []

        #create the genesis block that is the first block
        self.new_block(previous_hash=1, proof=100)



    def new_block(self, proof, previous_hash=None):
        #creates a new block and adds it to tha main pass

        """
        create new block in the blockchain
        :param proof: <int> proof given by proof of work algorithm
        :param previous_hash: (optional) <str> hash pf previous block
        :return: <dict> new block
        
        """

        block ={
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transactions': self.current_transaction,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transaction = []

        self.chain.append(block)
        print(f"New block added: {block}")
        return block

    def new_transaction(self, sender, recipient, amount):
        #adds a new transaction to the list of transactions
        """
        creates a new transaction to go into the next mined block
        :param sender: <str> address of sender
        :param recipient: <str> address of recipient
        :param amount: <int> amount being sent
        :return: <int> the index of block which holds this transaction        
        """

        self.current_transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        creates a SHA-256 hash of a block
        :param block: <dict> block
        :return: <str>
        """
        #we must make sure that the dictionary is ordered or we will have in consistent hashes
        
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, last_proof):
        """
        simple proof of work algorithm:
            -find a number p' such that hash(pp') contains leading 4 zeroes where p is the previous p'
        
            -p is the previous proof and p' is the new proof

        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof
    

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        validates the proof : does hash(last_proof, proof) contains 4 zeroes?

        :param last_proof: <int> previous proof
        :param proof: <int> current proof
        :return: <bool> True is correct False if not
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"



#instantiate the node
app = Flask(__name__)

CORS(app)
#generate a globally unique address for this

node_identifier = str(uuid4()).replace('-','')

#instantiate the blockchain

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    #we run the proof of work algorithm to get next proof

    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    #we must recieve a rewars for finding the proof
    #the sender is 0 to signify that this node has mined a new coin

    blockchain.new_transaction(
        sender = "0",
        recipient = node_identifier,
        amount = 1
    )

    #forge the new block by adding it to the chain

    previous_hash = blockchain.hash(last_block)
    block =  blockchain.new_block(proof, previous_hash)

    response = {

        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200



@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain), 
    }

    return jsonify(response), 200

@app.route('/transaction/new', methods=['POST'])
def new_transactions():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return jsonify({'error': 'Missing values'}), 400
    
    #create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message' : f'Transaction will be added to block {index}'}

    return jsonify(response), 201


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

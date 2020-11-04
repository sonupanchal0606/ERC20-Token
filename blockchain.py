#Module 1 - Create a Blockchain

#impoting the libraries 

import datetime #for timestamping the block
import hashlib #for hashing methods
import json #for creating funtion to encode the blocks before we hash them
from flask import Flask,jsonify #flask : for web application
                                 #jsonify : to interact with blockchain by postman messages
                                 
                                 
# part 1 : make the architecture of blockchain

#create a class blockchain and define all the components of the blockchain 
                                 
class Blockchain: 

#create a init function to initialise the blockchain and its argumrnt will be self . 
#self refer to the object that we make once the class is created 
    def __init__(self):
        self.chain=[] #chain contains the list of blocks 
        self.create_block(proof = 1, previous_hash = '0') #create genesis block. 
        #first block of the blockchain
        #each block will have its own proof.
        #lets we take proof =1
        #as its a genesis block ,there is no
        #previous hash.lets its 0. we take it as a string cos SHA 256 algo can only accept encoded strings 
        #this function is not only used to create the genesis block but also the other blocks of the blockchain
        #create block function is used right after mining the block . mine block function will get us the proof of work
        #once the proof is found , we will create a block with the just found proof                                                 
    def create_block(self, proof, previous_hash): #proof arg comes from mine block function
        #block is a dictionary variable which will uniquely identify the blocks using 4 variables
        #index of the block , time stamp: the exact time when the block was mined , proof of the block which will found after mining the block
        #previous hash , and then anything you want to add into this dictionary and call it data
        block = {'index': len(self.chain)+1, #length of the chain till now +1
                 'timestamp' : str(datetime.datetime.now()), #gives the exact time when we mine the block
                 'proof' : proof, #a proof of work function will return the proof
                 'previous_hash' : previous_hash
                 #data : u can include any data also
                 }
        self.chain.append(block)
        return block
    def get_previous_block(self): #to get the previous block
        return self.chain[-1]
    
    #proof of work is number that miners have to find in order to mine the block
    #it will return the proof arg
    #to mine the block , miners will have to solve a cryptographic puzzle
    #that puzzle(to find a number) will be challenging to solve but easy to verify
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False 
        while check_proof is False:
            #the more leading zeros u put , the harder it will be solve the puzzle
            hash_operation=hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    #returns the hash of a block passed 
    #we use json dumps libreary which take block(dictionary) and convert it into a stirng
    #block will get converted into a json string now 
    def hash(self,block): 
        encodeded_block=json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodeded_block).hexdigest()
    
    #a functioon to check the validity of the block
    #it checks if all blocks contains the proof of work of previous block
    #check validity of the blockchain
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return false
            previous_proof = previous_block['proof']
            proof = block['proof'] #current block proof
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    
    
#PART 2
"""
we will create the object of the blockchain and interact it with the help of flak(web application) by making some GET request 
in our postman user friendly interface
4 things

1) create a flask based applciation by making an object of flask clASS
    https://flask.palletsprojects.com/en/1.1.x/quickstart/
    
2) create a blockchain by crating an object of blockchain
3) first get request to mine a block in the blockchain by using proof of work problem
4) another get reuest to get the whole chain
"""

#1) creating a web app using f;ask
app = Flask(__name__)
            
#2) creating a blockchain
blockchain = Blockchain()

#3) mining a new block
#  https://flask.palletsprojects.com/en/1.1.x/quickstart/
#We then use the route() decorator to tell Flask what URL should trigger our function.
#which url will trigger our mine block function

@app.route('/mine_block' , methods=['GET']) #refer the documentation https://flask.palletsprojects.com/en/1.1.x/quickstart/#http-methods
def mine_block():
    previous_block = blockchain.get_previous_block() #to get the last blok of the blockchain
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    #now we have create a block and appended it to the end of the blockchain. now will use postman to display it in the blockchain
    #in respomse to this GET request 
    #reponse will b in postan which accept the json type. so here we will create a dictionary
    #we use jsonify to return response in  json format
    response = { 'message' : 'Congratulations Sonu! You have just mined a new block',
                 'index' : block['index'],
                 'timestamp' : block['timestamp'],
                 'proof' : block['proof'],
                 'previous_hash' : block['previous_hash']}
    return jsonify(response), 200 #200 is the https status code. check for status codes on wikipedia


#4) get a full blockchain
@app.route('/get_chain' , methods=['GET'])
def get_chain():
    response = { 'chain' : blockchain.chain,
                 'length' : len(blockchain.chain)}
    return jsonify(response), 200 

#to check the validity of the blockchain
@app.route('/is_valid' , methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = { 'message' : 'All Good! Blockchain is valid' }
    else:
        response = { 'message' : 'oops! there is a proble. Blockchain is not valid' }
    return jsonify(response), 200 

#Running the app 
#here we need two args host and the port. 
#refer the documentation https://flask.palletsprojects.com/en/1.1.x/quickstart/
""" as u can see our flask web app is runnign on  Running on http://127.0.0.1:5000/ """
app.run(host = '0.0.0.0' , port = 5000) #host =0.0.0.0 will have the blockchain public

#to execute : select the wholde code and just press windows/linux : Ctrl + enter and Mac : Cmd + Enter
#then start postpa. select methoda GET/POST and then and enter URL followed by the function you want to call
#eg http://127.0.0.1:5000/mine_block

    
    
    




        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                                                          
                                                          
                      
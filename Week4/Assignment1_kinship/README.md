# Learning Distributed Representations of Concepts (1986)
Support: http://www.cogsci.ucsd.edu/~ajyu/Teaching/Cogs202_sp12/Readings/hinton86.pdf

## Step 1: Data reading (kinship_reader.py)  
Use kinship_dataset method. It returns a dictionary with multiple fields:
* raw - a list of triplets (list of lists)
* enc_persons - a dictionary of encoding for persons
* enc_relations - a dictionary of encoding for relations
* p1 - list of encoded persons on the first position in the triplet relation
* r - list of encoded relations in the triplet relation
* p2 - list of encoded persons on the third position in the triplet relation
* len - dataset len (112)

## Step 2: Build the network as in paper  
You will find helper functions in TODO1_kinship.py


## Step 3: Obtain same performances. Try to do better.
How? Well chosen parameters.



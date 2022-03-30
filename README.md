# Optimization-Problem-HackRush-2022
This repository contains code and write-up for the optimization problem given during the HackRush 2022 Hackathon.

Write-Up:

I have created a directed graph from the given input data. For the bombs `i` and `j`, if `jth` bomb in in the exploding area of `ith` bomb, them I have added an edge from `j` to `i`.

Now, the DFS tree of vertex `i` gives all the bombs that we will have to defuse in order to prevent `ith` bomb from defusing. I have taken an assumption that the jammers will be put on the bombs itself. This will give higher cost but at a certain approximation. Now, I have taken a greedy step. I sorted the vertices in decreasing order of the exploding radius of the bombs. Then I took out the first bomb and built its DFS tree. Now, the probmlen becomes the independant set problem, i.e. I have to choose `k` bombs from these DFS tree so that all the bombs can be defused and `k` should be minimum. To calculate this, I used approximation algorithms: Highest Degree Algorithm and Maximal Matching Algorithm and then returned the answer which returns minimum number of jammers. Now, if the cost reduces after defusing these bombs then only I consider defusing these bombs else do not defuse these bombs. Repeat this for all the bombs.

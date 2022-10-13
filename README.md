[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8801035&assignment_repo_type=AssignmentRepo)
# Project 2: Suffix tree construction

You should implement a suffix tree construction algorithm. You can choose to implement the naive O(n²)-time construction algorithm as discussed in class or McCreight’s O(n) construction algorithm. After that, implement a search algorithm (similar to slow-scan) for finding all occurrences of a pattern. This algorithm should run in O(m+z) where m is the length of the pattern and z the number of occurrences.

Write a program, `st` using the suffix tree exact pattern search algorithm (similar to slow-scan) to report all indices in a string where a given pattern occurs. 

The program should take the same options as in project 1: `st genome.fa reads.fq`. The program should output (almost) the same SAM file. Because a search in a suffix tree is not done from the start to the end of the string the output might be in a different order, but if you sort the output from the previous project and for this program, they should be identical.

## Evaluation

Implement the tool `st` that does exact pattern matching using a suffix tree. Test it to the best of your abilities, and then fill out the report below.

# Report

## Implementation
We tried implemented both the naive quadratic time algorithm and McCreight’s linear time algorithm. But when timing our implementation of McCreight’s algorithm, we realised we forgot a crucial edge case, which made it run as slow as the naive. We did not fix it before the deadline. 

## Insights
Indecies are again your enemy. 

Pretty printing is very much needed for nested classes like trees. 

Using the verbose argument is nice, since it makes it easy to switch between whether to print or not. 

## Problems encountered if any.

For the naive, we had problems with splitting edges/nodes. This was solved by pen and paper, going sytematicly through cases, and using pretty printing. 

As mentioned above, we missed an edge case for McCreight’s algorithm, which resulted in it being half-way done in this version of the handin. 

## Correctness

### Building the tree
We started by using small examples, which could be done by hand and verified. 

We then used random examples and tested whether the output of the algorithms gave a 'valid' tree. A 'valid' tree might not be the correct one, but it contains all the expected leaves.

### Search 

Likewise we first used some known examples for verifying the implementation of search. 

We then compared the results of the search algorithm on the trees for random strings with the results from the kmp implementation from the last handin. 

### Conclusion of correctness

With these different methods of testing the contruction of trees and search, we are confident, the trees construction for the naive algorithm and search are correct. 

## Running time

We can see on plots, that it is O(n²), but we want to go to bed now, bye. 

*Describe experiments that verifies that your implementation of `st` uses no more time than O(n) or O(n²) (depending on the algorithm) for constructing the suffix tree and no more than O(m) for searching for a given read in it. Remember to explain your choice of test data. What are “best” and “worst” case inputs?*

*If you have graphs that show the running time--you probably should have--you can embed them here like we did in the previous project.*


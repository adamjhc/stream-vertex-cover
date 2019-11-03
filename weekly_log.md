# Final Year Project Weekly Log

## Semester 1 Week 1 - 30/09

Friday 11:30:

- Met with Rajesh for the first time. We talked about our areas of interest; his being graph theory and algorithms surrounding it, mine being more of software engineering and hardware. 
- I was flexible with the topic of my project so we decided it was best if it was based in graph theory. Possibly implementation and testing of graph algorithms that have not yet been put into practice.

## Semester 1 Week 2 - 07/10

Tuesday 11:00:

- Rajesh explained to me the concept of k-core and how it can used to model how to keep a social network alive.
- We went over different topics within graph theory: k-core, privacy, and streaming algorithms. Rajesh posed these as possible areas that I could focus my project on.
- K-Core is about keeping as many vertices as possible connected to k other vertices. This can be either done as "buying" out other vertices to stay connected or manually adding edges to increase connections.
- K-Anonymity is a technique used to anonymise survey data so that findings from said surveys can be published while preserving the participants identities.
- Big data has brought about the rise of algorithms to be used in a streaming environment (where we cannot store all the data in memory at once). There are particular ones for finding matchings in sparse graphs and vertex cover that would be interesting to implement.

Rajesh sent me some papers from each of the three topics for me to get an idea of the area I'd be researching. Streaming algorithms seems most interesting since I've never had any exposure to big data technologies such as MapReduce and Hadoop plus would be a great area to have at least a beginner level experience in.

## Semester 1 Week 3 - 14/10

Monday 14:00:

- I told Rajesh that streaming is more interesting of an area to me and that I'd like to focus on that, with k-core algorithms being held as a backup/side project. He seemed on board as it seemed to serve both of us well; he has written papers on such algorithms.

Rajesh sent me a couple more papers to look over.

Rajesh had asked me to figure out if the matching.cpp code was an implementation of an algorithm written in a paper he had sent me and after looking at the code for a while I confirmed that it was.

## Semester 1 Week 4 - 21/10

Monday 14:00:

- Rajesh showed me algorithms for finding whether a graph has a vertex cover of size k. There were a couple variations on one algorithm in which you could choose to use less memory but do significantly more passes or do one pass and use more memory. Also a streaming version of the algorithm.

Submitted the project proposal. I noted that the project was on k-core/streaming graph algorithms and looking into the motivations for such algorithms. Which I should hopefully be able to put the knowledge towards a usable program such as an app which makes use of the algorithms studied.

## Semester 1 Week 5 - 28/10

Monday 14:00

- Rajesh introduced me to another vertex cover algorithm that he thought would be good to implement. It was a kernelization algorithm which is a group of algorithms that I haven't encountered before so the idea was slightly strange at first.

Started implementing graph representations and algorithms in python.

Python seems a good choice for quick implementations, clear readability, and is used in streaming environments. C may be a better choice for trying to get speedy code while I'm still testing on my laptop.

Finally got round to typing up the last 5 weeks worth of week logs.

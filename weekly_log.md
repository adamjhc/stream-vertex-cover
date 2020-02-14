# Final Year Project Weekly Log

## Semester 1 - Week 01 - 30/09

Friday 11:30:

- Met with Rajesh for the first time. We talked about our areas of interest; his being graph theory and algorithms surrounding it, mine being more of software engineering and hardware.
- I was flexible with the topic of my project so we decided it was best if it was based in graph theory. Possibly implementation and testing of graph algorithms that have not yet been put into practice.

## Semester 1 - Week 02 - 07/10

Tuesday 11:00:

- Rajesh explained to me the concept of k-core and how it can used to model how to keep a social network alive.
- We went over different topics within graph theory: k-core, privacy, and streaming algorithms. Rajesh posed these as possible areas that I could focus my project on.
- K-Core is about keeping as many vertices as possible connected to k other vertices. This can be either done as "buying" out other vertices to stay connected or manually adding edges to increase connections.
- K-Anonymity is a technique used to anonymise survey data so that findings from said surveys can be published while preserving the participants identities.
- Big data has brought about the rise of algorithms to be used in a streaming environment (where we cannot store all the data in memory at once). There are particular ones for finding matchings in sparse graphs and vertex cover that would be interesting to implement.

Rajesh sent me some papers from each of the three topics for me to get an idea of the area I'd be researching. Streaming algorithms seems most interesting since I've never had any exposure to big data technologies such as MapReduce and Hadoop plus would be a great area to have at least a beginner level experience in.

## Semester 1 - Week 03 - 14/10

Monday 14:00:

- I told Rajesh that streaming is more interesting of an area to me and that I'd like to focus on that, with k-core algorithms being held as a backup/side project. He seemed on board as it seemed to serve both of us well; he has written papers on such algorithms.

Rajesh sent me a couple more papers to look over.

Rajesh had asked me to figure out if the matching.cpp code was an implementation of an algorithm written in a paper he had sent me and after looking at the code for a while I confirmed that it was.

## Semester 1 - Week 04 - 21/10

Monday 14:00:

- Rajesh showed me algorithms for finding whether a graph has a vertex cover of size k. There were a couple variations on one algorithm in which you could choose to use less memory but do significantly more passes or do one pass and use more memory. Also a streaming version of the algorithm.

Submitted the project proposal. I noted that the project was on k-core/streaming graph algorithms and looking into the motivations for such algorithms. Which I should hopefully be able to put the knowledge towards a usable program such as an app which makes use of the algorithms studied.

## Semester 1 - Week 05 - 28/10

Monday 14:00

- Rajesh introduced me to another vertex cover algorithm that he thought would be good to implement. It was a kernelization algorithm which is a group of algorithms that I haven't encountered before so the idea was slightly strange at first.

Started implementing graph representations and algorithms in python.

Python seems a good choice for quick implementations, clear readability, and is used in streaming environments. C may be a better choice for trying to get speedy code while I'm still testing on my laptop.

Finally got round to typing up the last 5 weeks worth of week logs.

## Semester 1 - Week 06 - 04/11

Monday 14:00

- Rajesh and I talked over the kind on timeline I would have over the remaining weeks: to have the given graph algorithms implemented locally and tested by Christmas, over Christmas learn streaming frameworks and in the new year start testing algorithms in a streaming environment.

## Semester 1 - Week 07 - 11/11

Monday 14:00

- Another short meeting setting in stone the aims of the project.

Started on implementation of vertex cover kernelization algorithm as well as setting up types for the graph implementations and tests for each.

## Semester 1 - Week 08 - 18/11

## Semester 1 - Week 09 - 25/11

## Semester 1 - Week 10 - 02/12

## Semester 1 - Week 11 - 09/12

Had my inspection meeting.

Work hasn't been progressing these past few weeks due to:

- Tonsillitis
- Unnecessarily massive robotics team project
- End-of-term assignment deadlines
- The early onset of glandular fever

## Christmas Holiday

Suffered from glandular fever for the most part. In the final week managed to get some things in order:

- Decided to ditch implementing graph data structure myself as that isn't the main aspect of the project so opted to use the NetworkX python package
- Implemented kernelization algorithm locally (still yet to test)
- Started on report, making drafts of sections, and adding notes
- Started research on streaming technologies that I would need to create my own streaming environment for testing these algorithms properly
- Started on binary search tree algorithms

## Semester 2 - Week 01 - 13/01

Main focus of this week has been on getting the non-streaming algorithms correctly implemented locally. Working through what is and what isn't the correct way of implementing both of the algorithms. Starting performance testing using Jupyter. Had a meeting with Rajesh on Thursday clarifying the algorithms I'd be covering as well as what kind of structure to have in the report.

### Plan for Semester 2

- Week 02:
  - Finish local implementations
  - Layout runtime analysis requirements
  - Find suitable datasets
  - Test
- Week 03-04:
  - Build streaming/batch processing pipeline
  - Implement streaming algorithms
- Week 05-06:
  - Streaming testing
- Week 07-11:
  - Report writing

### Report guidelines

Your report should have a minimum of 1.25 line spacing, a minimum of 10.5pt. font and a minimum of 2.5cm margins (all edges).

## Semester 2 - Week 02 - 20/01

Started playing around with runtime analysis, setting out the requirements for the testing. Testing packages such as tqdm and pandas for data analysis. Created an plan for the rest of term.

Meeting with Rajesh covered testing methods and that I should be testing the streaming algorithms locally to simply compare against the older non-streaming algorithms.

## Semester 2 - Week 03 - 27/01

Slowly iterating on the runtime analysis of the non-streaming algorithms. Think I'm at a point now that I should be able to pull the trigger once the streaming algorithms have been implemented and random graphs have been set up. Looking more into pandas for data analysis and seems like I can just about get what I want out of it even if it is fiddly. Implemented streaming branch algorithm again as I had already done that previously so only required finding it and making tweaks to it from what I've learnt through this process. Finally learnt what `m` is as well. Only found a wordy outline of how the kernel streaming algorithm is implemented so haven't got round to that yet.

Met with Rajesh and talked a lot more on time complexity and how the point of all this isn't to make it efficient since it's an NP-Hard problem and so, by definition, can't be. It's so that this problem can even be tackled at large scales. The memory capacity needed for some of these real world graphs just isn't possible and so this is the only way to tackle it.

Spent the weekend researching and designing the streaming pipeline. About 90% sure I'm going with MongoDB (or some NoSQL DB) into Apache Kafka into Apache Spark. MongoDB is obviously on a server, Kafka seems to run in some kind of cluster and then Spark will be run locally from the looks of things.

## Semester 2 - Week 04 - 03/02

Working through design of streaming platform. Eventually came to the conclusion that Big Data streaming platforms weren't necessarily needed after spending perhaps too much time trying to learn them. Settled on two versions of a streaming implementation: first, streaming "locally" line by line from a text file and, second, using Kafka as a streaming platform to stream edges from a database.

Told Rajesh about this and he seemed happy to continue with this idea of having two stages of streaming. He said to focus on the memory profiling of each implementation since as we've spoke about in previous weeks these algorithms aren't about time complexity. This makes most of the work I've done so far on the runtime analysis redundant but oh well.

Spent a lot of time collating datasets and information on them. Have a pretty good collection of real world graphs now, just need to generate some synthetic ones for comparison. Cleaned up the Trello board a bit as I haven't been that active in using it but have a clear path of my next tasks.

## Semester 2 - Week 05 - 10/02

### Demonstration

#### Info

- "very likely" to be the second marker for your project
- 20 min slot
  - 10-15 presentation/demo
  - 5 mins for questions
- Not directly assessed
  - making an impression of your project will help them form at opinion

#### Presentation

- Start with introducing the problem you're trying to solve at a high level
  - Don't assume they will know about the area of your work or the specific topic you're working on
- You should highlight important aspects, challenges and decisions
- You're trying to tell a story about the project, the work you've done, the decisions you've made
- You're trying to convince them that you've done work that's good and interesting

#### My Ideas

- Show kernel stream algorithm working live with an updating kernel as the stream runs
- memory usage graphs for each implementation

## Semester 2 - Week 06 - 17/02

## Semester 2 - Week 07 - 24/02

## Semester 2 - Week 08 - 02/03

## Semester 2 - Week 09 - 09/03

## Semester 2 - Week 10 - 16/03

## Semester 2 - Week 11 - 23/03

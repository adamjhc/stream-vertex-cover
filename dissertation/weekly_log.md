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

Finished up this phase of my graph collation. Started on getting the local stream versions implemented. Spent a lot of time choosing a library for handling command line arguments. Clarified with Rajesh the details on the implementation of the stream kernel algorithm: once an edge is in the matching anything connected to that edge is considered a neighbour even if that edge links to another edge in the matching. We also talked about the demonstrations and how I should present the project.

With the working implementation of the stream kernel and demonstrations on my mind I started working on a demonstration script and gif creator so I'll have something to show in the presentation.

Made notes on the demonstration talk below:

### Demonstration

#### Info

- "very likely" to be the second marker for your project
- 20 min slot
  - 10-15 presentation/demo
  - 5 mins for questions
- Not directly assessed
  - making an impression of your project will help them form an opinion

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

Made big strides this week, completing implementations of the kernel and branching methods in local_stream and designing a utility for them to be used with. This includes the base kernel and branching algorithms, as well as a command to run a binary search using the kernel algorithm to find the size of the minimum vertex cover and a command to run the kernel on a stream and then follow with the branching algorithm. Made a script to generate many Erdos-Renyi graphs and a script to convert an edgelist to a stream format. Although, this "stream" format I think might a normal edgelist since neither the kernel or branching algorithm actually needs the number of nodes or edges. Yes, the branching algorithm in words does use the value `m` as the number of edges but I think this can be replaced with a `next` function which would be aware of when the stream is at it's end.

Showed Rajesh the demo animation I had made. He gave pointers of adding more information and detail of what was being shown: k value of kernel, edges being thrown away, percentage size of kernel compared to whole graph. These should be added along with more constructed graphs using multiple star graphs posing as "famous people" and adding single connections between them to simulate a simple model of a social graph. He also said it would be a good idea to have a simpler PowerPoint-style "animation" of the kernel algorithm at work to be able to see it step-by-step before moving to the animation so it's easier to know what's going on. We also talked about how this project is about contributing to an effort of his work. With that should come proper documentation and tools so that if someone wanted to continue with this work they would be able to with ease. This means setting up documentation properly and having help pages.

Spent the weekend setting up Sphinx documentation and started on the stream implementation (just trying to get the Zookeeper and Kafka docker images working first)

## Semester 2 - Week 07 - 24/02

Got Kafka working within docker containers and created a producer script to send edges from a file to a Kafka topic. I've kind of given up on the idea of configuring Kafka Connect to work with a database/other data source since this is mostly a proof of concept. Getting it all working running through Kafka one way or another is still enough to get me displayable results of memory usage. Started playing around with Faust's web views to see if a user friendly dashboard can be made and seems like something can be done writing some JS to make a POST request which Faust can handle.

```sequence
App->Requests (Topic): ../edgelist.txt
Requests (Topic)->Producer: ../edgelist.txt
Note over Producer:Opens paths
Producer->Edges (Topic): u,v
Edges (Topic)->App: u,v
Producer->Edges (Topic): u,v
Edges (Topic)->App: u,v
Producer->Edges (Topic): ...
Edges (Topic)->App: ...
Producer->Edges (Topic): end
Edges (Topic)->App: end
Note over App: Finish up
```

Something like this is what I've got in my head. Will have to figure out how to signify the start and end of edges:

- something like u=-1,v=-1 might be easy hack
- flag in edge model to signify end
- whole new topic for each edge list but still doesn't say when it stops

Other things to consider:

- Can an agent handle two topics?
- How to request another pass (e.g in the case of the branching algorithm)
- Multiple agents for different algorithms?

In the weekly meeting with Rajesh, we mainly went over how the demonstration works but that has now been extended till after exams. He also gave me some ideas of what to show a user in terms of details of the running algorithm

> Potential things to store at each timestamp:
>
> - numbers of edges seen so far (number of the current timestamp)
> - how many edges stored in the kernel
> - value of k
> - current size of VC
> - (delay parameter)

He may have been mainly thinking about the visualiser but it's a good start.

## Semester 2 - Week 08 - 02/03

> In theory, there is no difference between theory and practice. But, in practice, there is. - Benjamin Brewster, 1882

Did this week:

- Statically type checked the entire project
- Created read DIMACS format function
- Created read labelled edgelist function
- Tried to use a package called `doit` to create actions but eventually went back to `make` since that was far simpler to use. I felt a little bad about using make as a task runner but it works so...
- Added tqdm progress bars to things like local_stream and utils
- Got a version of kernel-exists working in Faust. Works with an external 'request' being made and then some handling between the producer and the kernerlizer is done.
- Refactored visuals methods a little
- Rewrote convert edgelist to labelled edgelist script so that it doesn't use NetworkX, makes it massively more memory efficient since it doesn't have to load the entire graph. It actually works with big graphs now.

Spoke with Rajesh about report writing and how contributing something back to the community is a big part of this project.

## Semester 2 - Week 09 - 09/03

## Semester 2 - Week 10 - 16/03

## Semester 2 - Week 11 - 23/03

# Software Requirements Specification (SRS)

## Scope & goals:
The scope is tho build a fully locally runnable deep researcher using langchain deep agents framework. 
To do this, a stepwise approach is used. 
For now, the first step is to use https://github.com/langchain-ai/deepagents-quickstarts/tree/main/deep_research as a central starting point and in the first step that is to be implemented now, the deep researcher must using a fully local LLM and be able to do a web search and answer a question based on that search. The deep researcher shall be used via a simple streamlit GUI by the user. 
The GUI as well as the deep researcher will be updated by subsequent steps not yet in the scope.
In the end, i.e. in the final step, the functionalities shall be close to those in https://github.com/ToHeinAC/KB_BS_local-rag-he and there app_v2_1g.py. This means essentially that the deep researcher must be able to connect to a local vector database and be able to do agentic research based on an initial user query which is concretized by an initial human-in-the-loop (HITL) process. This initial HITL process must be able to understand the humans query and make deep questions by the deep researcher to be answered by the human in order to get a better understanding of the topic, i.e. an optimized context, to be more precise in the search for information. 

## deepagents-quickstarts/deep_research github repo
https://github.com/langchain-ai/deepagents-quickstarts/tree/main/deep_research

## Deepagent docs
https://docs.langchain.com/oss/python/deepagents/overview

## Very good resource video for exactly doing this  
https://www.youtube.com/watch?v=geTtqyFnyHA
### Transscript
In this video, we'll use deep agents to
0:02
create a deep research example. You can
0:05
see here the final result. It'll be an
0:07
agent that can write to-dos and then
0:10
track them as well. It can also kick off
0:13
sub aents. So, it has a research sub
0:15
aent and we can see that it will use
0:17
this to do specific research queries.
0:19
And then we can also see that it has a
0:22
critique agent at the end that does
0:25
specific critiques as well. And then it
0:27
will also write its final output to this
0:30
final report.mmd file. And we'll get
0:32
back this pretty comprehensive report
0:35
for any question that we ask. So in this
0:38
video, we'll see how to build this from
0:39
scratch using deep agents, a new package
0:42
we released for creating agents that can
0:45
plan over longer time horizons and go
0:47
deeper into particular tasks. Let's see
0:49
how it works.
0:52
All right, so I'm going to start from
0:53
scratch with a blank file. The first
0:56
thing I'm going to do is implement a
0:58
search tool. Now, this is important
0:59
because my deep researcher will need to
1:01
do search to find out the answers to
1:04
specific sub questions. So, in order to
1:06
implement this tool, we're going to use
1:08
Tavilli. Tavilli is a search tool for
1:11
connecting agents to the web. So, you
1:13
can go in, sign up here, get an API key
1:15
and all of that. Once we've done that,
1:18
let's go back into our code. We're going
1:20
to import the Tavilli client from
1:21
Tavilli. We can then go ahead and create
1:24
an instance of this Tavilli client.
1:26
We're going to be looking in our
1:27
environment variables for a Tavilla API
1:29
key. And so you'll need to make sure to
1:31
expose that. So let's import the OS
1:33
package so we can import it there.
1:36
Great. Now that we have this client,
1:37
we're going to write a function that
1:38
will be the tool that we give the agent.
1:41
So we can write something like this. a
1:43
function that takes in a query which is
1:45
a string and then also can optionally
1:47
take in an integer which is the max
1:49
results to include and then also
1:51
optionally take in a boolean of whether
1:54
to include the raw content or not and
1:56
then the description of this of this
1:58
function this is important this will be
1:59
the description that we give to the
2:00
agent when we give it this tool so now
2:03
we've got this tool this is going to be
2:04
the backbone of our research agent let's
2:07
go ahead and actually create a really
2:09
simple research agent that just has this
2:11
and uses as deep agents. So in order to
2:14
do that, we're just going to import
2:16
create deep agent from deep agents.
2:18
We're going to write some custom
2:20
instructions for the deep agent. So
2:22
let's call this instructions.
2:29
This is pretty basic and that's because
2:31
I'm going to actually improve it a bunch
2:32
later on, but this is a good placeholder
2:35
for now. And then let's just do agent
2:37
equals create deep agent
2:41
instructions equals instructions tools
2:45
equals internet search. And that's
2:48
basically it. I now have a deep agent
2:51
that will go ahead and do some research.
2:55
So let's actually see how to use this.
2:59
In order to use it, I'm going to create
3:00
this langraph.json file. This is where I
3:03
point to the file that contains the
3:06
agent and then the name of the variable
3:08
where my agent is stored.
3:11
From here I can go into the terminal. I
3:13
can install langraph C cli and then
3:16
after I install this I can do langraph
3:19
dev to run a developer server for this
3:23
agent.
3:24
Going in here I can see the basic agent
3:26
here. Let's add in a message and let's
3:29
ask it something to research. So let's
3:31
ask it what is langraph
3:38
and we can see that it starts
3:40
by spinning up
3:45
this general purpose research sub aent
3:47
to research lang graph comprehensively
3:49
and all of that. Now while this is
3:52
running I'm actually going to improve
3:53
the agent.
3:57
So let's go back.
4:00
So let's go back to this file and let's
4:03
add in two sub aents and then improve
4:06
the system prompt. So the first sub
4:09
agent we're going to add is a dedicated
4:11
researcher agent. In order to do that,
4:14
we're going to add a dedicated system
4:16
prompt just for this researcher.
4:21
So this is the subress research prompt
4:22
here. And we're then going to create a
4:24
dictionary representing this sub
4:27
research agent. So we're going to give
4:29
it a name, research agent. We're going
4:31
to give it a description. And so this is
4:32
going to be used by the main agent to
4:34
send questions to it. So use to research
4:36
more in-depth questions. Only give this
4:38
researcher one topic at a time. Do not
4:40
pass multiple sub questions to this
4:41
researcher. And then I'm going to give
4:43
it the prompt. So this is the subress
4:44
research prompt above. And then I'm
4:46
going to give it access to tools that I
4:48
want it to have. And so I want it
4:49
specifically to only have access to this
4:50
internet search tool. So great, I'm
4:52
going to define that there. Now I'm
4:54
going to define another sub aent that
4:56
I'm going to call the critique sub aent.
4:59
And so this is going to be an agent
5:00
that's specifically used to critique the
5:04
final report that's been generated so
5:06
far. So now one thing that I have to
5:08
think through is how does this critique
5:09
agent know where the final report is?
5:12
And for that I'm going to use the file
5:14
system, the virtual file system that
5:15
comes built in with deep agents. So, I'm
5:17
going to modify the system prompt in a
5:19
second to say, "Hey, when you've got
5:21
this final report, write it to a file
5:23
called final report.md." And then this
5:26
critique agent is going to know to look
5:28
for that final report.md
5:31
and then and then and then critique
5:32
that. Great. So, let's do this. I now
5:36
have this critique prompt. You are
5:38
dedicated editor. You bring task to
5:40
critique a report. And so, you can see
5:42
here that I say you can find the report
5:43
at final report.md.
5:46
And then you can see here that I also
5:48
say you can find the question topic for
5:49
this report at question.ext. So one
5:51
thing I'm also going to want to do is
5:53
prompt this general agent to write down
5:55
the original question into question.ext.
5:58
So this file system can basically be how
6:01
these agents can communicate with each
6:02
other in a more structured manner
6:04
besides just the messages that they send
6:06
in and out. So this research sub agent,
6:08
this just used the messages. It just
6:10
took in a question that was the message
6:12
and it outputed its response as a
6:13
message and and it communicated with the
6:15
main agent via messages. This critique
6:17
agent is now using files in the file
6:20
system to communicate. And so this is a
6:22
this is a more token efficient way than
6:24
passing in the final report every time
6:26
to this to this critique agent. So after
6:29
I have this prompt, I can create the
6:30
dictionary representing the critique
6:32
agent. I'm going to give it a name. I'm
6:34
going to give it a description. And then
6:36
I'm going to give it a prompt. I'm not
6:38
going to give it any tools. And so by
6:39
default, it will inherit all the tools
6:41
that the main agent has access to,
6:43
including reading and writing from
6:45
files, internet search, to-do list,
6:48
things like that. Now, I'm going to go
6:50
ahead and modify the instructions. And
6:53
so, I'm going to write a lot more
6:54
detailed instructions, and there's going
6:55
to be a few key parts of that.
6:59
So, a lot of this a lot of this prompt
7:02
is taken from the deep research repo
7:03
that we created earlier and that I'll
7:05
link to. And so that's where a lot of
7:07
this this detailed prompts comes from.
7:10
But I added in a few things specific to
7:12
deep agents. So the first thing you
7:14
should do is write the original user
7:16
question to question.ext. So remember
7:19
this is how we communicate the question
7:21
the original question that the user
7:23
asked to the to the critique agent. So
7:25
we tell this this main agent to write it
7:27
down. We're then going to use the
7:29
research agent. So we're we're
7:30
referencing this this specific research
7:32
agent above. We're going to use this to
7:33
conduct deep research. And then when we
7:36
have enough fi information, we're going
7:38
to write a final report and we're going
7:39
to write it to final report.md. So
7:41
again, this is the same file name as we
7:43
pass the critique agent. So this is how
7:45
it knows how to write to those files.
7:49
You you can then call the critique agent
7:51
to get a critique of the final report.
7:52
After that, if needed, you can do more
7:54
research. So we're giving you
7:55
instructions on basically how and when
7:56
to call these sub agents in a very
7:58
dedicated manner. And that's because
8:00
this this general purpose research agent
8:02
needs those that kind of like knowledge
8:04
of when to use these different agents
8:06
and and and how we want to
8:10
and how we want it to use those those
8:13
different agents. And so we're passing
8:14
that in the prompt. And so now the last
8:17
thing we're going to do is we're going
8:20
to go back down here and we're going to
8:22
pass in the sub aents that we have.
8:32
One last little thing that we're going
8:34
to do, we're actually going to set the
8:35
recursion limit of this agent to a,000.
8:37
So, by default, this is 25, which means
8:39
that this agent can run basically 25
8:42
different steps, but this is a deep
8:43
research agent. It might run for a
8:45
while. So, we're going to increase that
8:46
all the way up to a,000. If we go back
8:49
up to Studio, we can see that the agent
8:51
has finished running and it's created
8:53
this uh report. It's not super long and
8:56
that's because we're using the more
8:57
simple prompt and no sub aents that we
8:59
had before. So, we're going to try again
9:01
with these better sub aents and this
9:04
better prompt. Before doing that, we're
9:06
actually going to set up deep agents UI
9:09
to be able to interact with this agent.
9:12
So, this is a GitHub repo that Nick on
9:14
our team created and it's basically a UI
9:16
for specifically interacting with these
9:18
deep agents. It visualizes the to-dos,
9:20
it visualizes the sub aents, it shows
9:21
the file system. This is what you saw at
9:23
the start of the video.
9:25
So we've got this running and we're now
9:27
going to give it a go. So let's ask it a
9:29
question like what is langraph?
9:33
And when we kick it off, we can now see
9:35
that it streams things back in a nice
9:38
manner. So first we can see that it
9:40
writes this question.ext to a file.
9:42
Again, this is what we prompted it to
9:44
do. Now it's creating to-dos. And so if
9:46
we go over to the tasks, we can see a
9:48
list of what it's doing. And now it's
9:49
got one in progress. It's researching
9:50
Langraph basics. What is its purpose and
9:52
key features? It now spins up a sub
9:55
agent. So if we click on this, we can
9:56
see the input. And we're going to wait a
9:58
little bit for the research agent to
9:59
come back, the sub research agent to
10:01
come back because that's the research
10:03
agent that's doing all of the work.
10:08
Here we are about halfway through the
10:09
process. And so we can see here that the
10:11
original subress research agent came
10:13
back with its response and then it
10:15
kicked off a few more. And so it's now
10:16
running on a third. We can see here that
10:18
the tasks two are done. One is in
10:20
progress and then it's still got some to
10:22
go. So let's check back in at the end.
10:25
We can see here that it's created its
10:26
research. And so if we look in the
10:28
files, we can see this final report MD.
10:30
And we can see that we get back a much
10:33
better and more detailed report than
10:36
before. So this shows the power of using
10:38
sub aents and also the importance of
10:39
having a really detailed prompt. This is
10:41
this is one of the key parts of uh deep
10:43
agents in general. They have detailed
10:45
prompts. So this is a full endto-end
10:48
example of how to build deep researcher
10:50
on top of deep agents. Hope you enjoyed.

### In scope:
- Deep researcher 
- fully local implementation using gpt-oss:20b from ollama
- nice streamlit app web interface that also adresses the to-do list, its status and also basic intermediary results

### Out of scope (for now, but shorter term needs in the following iterations):
- enable a local vector database retireval (see https://github.com/ToHeinAC/KB_BS_local-rag-he and there app_v2_1g.py; teh local vector database as the knowledge base is already there and can be used)
- display of all relevant preliminary results (use expanders)

### Out of scope (for many following iterations):
- long term memory
- user profile and logins
- session management
- vector database generation, management etc. (this is done elsewhere for now)

## User stories:
- As the end-user I want to have a GUI for a good user experience tho work with the deep researcher in order to deploy the solution in the end to less technically experienced users. 
- As the end-user, In the GUI, I want to be able to see the current researcher step and the previous step to be able to get a good sense of what is happening behind the scenes.  
- As the software architect, behind the scenes, I want the deep researcher to be able to verify the most important steps in the workflow (i.e. reflection) in order to guarantee the highest quality of the final answer generation. Moreover, reflections shall be used to check if the quality of the answer has a good level.
- As the software architect, behind the scenes, I want the deep researcher to be able stop the deep research loops after a maximum number of attempts in order to prevent infinite loops. When this happens, this must be displayed in the GUI in order to let the end-user know if there could be a quality issue in case the maximum number of attemps was reached.

## Functional requirements:
- A streamlit application file taking into account all the GUI-specific user stories
- A backend that implements the deep researcher but in a way that it can be used by the streamlit app

## Non‑functional requirements:
- all files must be in the /showroom folder
- fully rely the example https://github.com/langchain-ai/deepagents-quickstarts/tree/main/deep_research and the deepagents framework https://github.com/langchain-ai/deepagents


### tech constraints:
- The LLM must be fully local, use gpt-oss:20b from ollama (already locally installed/available)
- You must implement the researcher strictly using langchains deep agents framework https://docs.langchain.com/oss/python/deepagents/overview#deep-agents-overview. Make use at least of the core capabilities "Planning and task decomposition", "Context management" and "Subagent spawning", that is use the Deep Agents Middleware architecture
- Use uv for virtual environment management and running the researcher
- make sure that version control is used (github/ToHeinAC/KB_BS_local-deep-researcher-he)
- make sure that a nice app for runnig is there (must be streamlit, the port should be 8508)

## Success criteria: 
- The implementation is the same or at least extreamly close to https://github.com/langchain-ai/deepagents-quickstarts/tree/main/deep_research
- The solution is compatible with the local LLM which is gpt-oss:20b from ollama
- The frontend GUI is a streamlit app
- Each implementation step is well documented
- The tech constraints are fulfilled
- The core capabilities of the deep agents framework as stated in the tech constraints are used
- The functional requirements are fulfilled
- The non-functional requirements are fulfilled

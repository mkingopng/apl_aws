## feedback
- need to talk to Thomas about stuff required to fix the OPL file
- talk to Dan about stuff required to fix Liftercast: flight etc
- i noticed that data was hard to read, sometimes missing (openers, weight class, age, pin height etc)
- talk to Rochelle & Jess & Dan & Thomas about various questions

## Streaming
- OBS crashes. can we containerize it?
- need more HDMI outputs? how many? why not just googlecast everything?
- probably makes sense to build a dedicated rig, low cost GPU(s) with lots of outputs
- how many audio channels?
- How many video channels?
- setup of OBS can be improved
- no logging so its hard to see why things went wrong
- OBS has a Python API
- what data do we get from streaming?
- what A/B testing do we do?

## Technical
- can we run multiple terminals off a single box?
- how do we deal with internet quality problems?

## Data & Resources
- is there a membership list? can i get a copy?
- if not, can i build one from what i have?
- Lots of fields should be driven off the member ID & membership record-> entry, weigh in, everything
- get APL logo and Zero Logo from Dan
- resources for liftercast
- install and learn OBS and its python API
- judges scoring system (leon craven?) -> how do we get judges decision directly into the computer?

## AV
- show thomas why he needs an SM58 microphone
- need 3x cameras for AI judging, one for each judge position, to collect data 
  to train a vision model.
- 4k? 1040p?
- need >2 cameras for livestream. 
- Having a single camera with minimal interaction for the stream is boring
- it can be improved by including more camera angles
- There is a simple audio mixer. other audio inputs?
- how and where to mount?
- can we use a drone in confined spaces with people?
- audio: what is the best solution?
- what other cool technology is there for AV and streaming?
- can we connect cameras and monitors using wireless or is cabled required?
- 

# Observations:
- same total and same BW -> requires lot numbers which we don't have yet. 
- problem with weigh in data
- this is really based on datetim of weigh in but its hard to collect this running from multiple locations
- LOTS of data double handling that can be fixed by finishing this app
- need dedicated export to csv for liftercast and OPL until i have a solution to import directly
- need to set up RAG to help commentator on livestream. this should actually be an easy kill. Dan uses this a LOT!
- need to replicate liftercast functionality & merge with OPL functionality
- there are things that OpenLifter has that users like, but there are also the same for LifterCast
- Its problematic running both
- This is something I'd do anyway for fun
- Streaming commentator needs to be focused not entering data. 
- Do we need a live commentator and streaming? -> YES!
- a smooth platform is an efficient meet. loaders, spotters and judges/refs
- for the tech desk, the main job is: entering judges decisions; entering/updating next attempts; starting timers
- 

## LLM app -> this is an easy kill. make it happen
- data store containing csv from Open Powerlifting
- vectorize and store in pinecone
- FAISS and semantic search
- langchain or similar to string things together
- options on different models. maybe use bedrock or some such thing to go live
- prompt from model to commentator when approaching a record attempt
- standardised prompts

## Vision app -> this is hard but rewarding
- Google Pose: Google ML Kit
- need lots of labeled data to fine tune / train
- need vision from 3 angles matching the judge position
- we may need 3 models
- how much compute do i need to train?
- for inference?
- does the data set need to be balanced?
- convert judging criteria to code
- deploy using Fargate or equivalent
- 

## Homework
- open lifter
- liftercast
- OBS
- `obs-websocket-py` for doing overlays
- how to do a live stream?

## Nationals
June 20 - 23
300+ lifters
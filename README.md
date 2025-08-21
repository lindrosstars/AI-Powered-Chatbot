# AI-Powered-Chatbot
A discord bot that sets up an integration environment with three LLM's (Gemini , Groq , Mistral) 

A basic python based discord bot which sets up a listener on a specific discord server channel and redirects queries to a webhook . This webhook forwards the query to the requested large language model using flags (!gemini OR !groq OR !mistral) and utilizes the LLM's API to generate a response . The response is parsed and split into message chunks to comply with discord's 2000 character limit using javascript , the output is posted back to the channel by the bot.

The discord bot instance is hosted locally using docker.

N8N for creating a workflow and process automation 
N8N instance is hosted locally using docker.



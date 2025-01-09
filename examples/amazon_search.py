"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

# import os
# import sys

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import asyncio

# from langchain_openai import ChatOpenAI

# from browser_use import Agent

# llm = ChatOpenAI(model='gpt-4o')
# agent = Agent(
# 	task='Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result',
# 	llm=llm,
# )


# async def main():
# 	await agent.run(max_steps=3)
# 	agent.create_history_gif()


# asyncio.run(main())



from langchain_anthropic import ChatAnthropic
#from browser_use import Agent
from browser_use.agent.service import Agent
import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Initialize Claude
llm = ChatAnthropic(
    model_name="claude-3-5-sonnet-20240620",
    temperature=0.0,
    anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Create agent with Claude
agent = Agent(
    task='Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result',
    llm=llm,
)


async def main():
	await agent.run(max_steps=3)
	agent.create_history_gif()


asyncio.run(main())

# async def main():
#     await agent.run(max_steps=3)
#     #print(result)
#     agent.create_history_gif()

# async def main():
#     result = await agent.run(max_steps=3)
    
#     # Make sure history exists and contains screenshots before creating GIF
#     if hasattr(agent, 'history') and agent.history.history:
#         try:
#             agent.create_history_gif(
#                 output_path='agent_history.gif',
#                 show_goals=True,
#                 show_task=True
#             )
#         except AttributeError as e:
#             print(f"Error creating GIF: {e}")
#     else:
#         print("No history available to create GIF")
        
# if __name__ == "__main__":
#     asyncio.run(main())
    

# async def main():
#     result = await agent.run(max_steps=3)
    
#     Access history if needed
#     if hasattr(agent, 'history'):
#         print("Action History:")
#         for action in agent.history:
#             print(f"- {action}")
    
#     print("\nFinal Result:", result)


# if __name__ == "__main__":
#     asyncio.run(main())
	

# import anthropic
# import os
# import sys
# from browser_use import Agent
# import asyncio


# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# async def main():
#     client = anthropic.Anthropic(
#         api_key=os.environ.get("ANTHROPIC_API_KEY")
#     )
    
#     agent = Agent(
#         task="Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result",
#         llm=client,
#         model="claude-3-5-sonnet-20241022"
#     )
    
#     result = await agent.run()
#     print(result)

# if __name__ == "__main__":
#     asyncio.run(main())
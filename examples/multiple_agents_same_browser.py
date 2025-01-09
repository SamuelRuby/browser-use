import os
import sys

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from browser_use import Agent, Browser, Controller


# Video: https://preview.screen.studio/share/8Elaq9sm
# async def main():
# 	# Persist the browser state across agents

# 	browser = Browser()
# 	async with await browser.new_context() as context:
# 		model = ChatAnthropic(model='claude-3-5-sonnet-20240620')

# 		# Initialize browser agent
# 		agent1 = Agent(
# 			task='Open 2 tabs with wikipedia articles about the history of the meta and one random wikipedia article.',
# 			llm=model,
# 			browser_context=context,
# 		)
# 		agent2 = Agent(
# 			task='Considering all open tabs give me the names of the wikipedia article.',
# 			llm=model,
# 			browser_context=context,
# 		)
# 		await agent1.run()
# 		await agent2.run()


# asyncio.run(main())





async def run_agents(context, model):
    try:
        # Initialize browser agents
        agent1 = Agent(
            task='Open 2 tabs with wikipedia articles about the history of the meta and one random wikipedia article.',
            llm=model,
            browser_context=context,
        )
        agent2 = Agent(
            task='Considering all open tabs give me the names of the wikipedia article.',
            llm=model,
            browser_context=context,
        )
        
        # Run agents sequentially
        await agent1.run()
        await agent2.run()
    except Exception as e:
        print(f"Error during agent execution: {e}")
        raise

async def main():
    browser = None
    try:
        # Initialize browser
        browser = Browser()
        async with await browser.new_context() as context:
            # Initialize model
            model = ChatAnthropic(model='claude-3-5-sonnet-20240620')
            
            # Run agents
            await run_agents(context, model)
    except Exception as e:
        print(f"Error in main execution: {e}")
        raise
    finally:
        # Ensure browser is properly closed
        if browser:
            await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript terminated by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
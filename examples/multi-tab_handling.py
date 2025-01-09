"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from browser_use import Agent

# video: https://preview.screen.studio/share/clenCmS6
llm = ChatAnthropic(model='claude-3-5-sonnet-20240620')
agent = Agent(
	#task='open 3 tabs with elon musk, trump, and steve jobs, then go back to the first and stop',
	task='open 3 tabs with toshiba hardrive, sam altman news, and updates in gen ai, then go back to the first and stop',
	llm=llm,
)


async def main():
	await agent.run()


asyncio.run(main())

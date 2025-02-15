import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

#from langchain_openai import AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from pydantic import SecretStr

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig

browser = Browser(
	config=BrowserConfig(
		headless=False,  # This is True in production
		disable_security=True,
		new_context_config=BrowserContextConfig(
			disable_security=True,
			minimum_wait_page_load_time=3,  # 3 on prod
			maximum_wait_page_load_time=15,  # 20 on prod
			# no_viewport=True,
			browser_window_size={
				'width': 1920,
				'height': 1080,
			},
			# trace_path='./tmp/web_voyager_agent',
		),
	)
)
# llm = AzureChatOpenAI(
# 	model='gpt-4o',
# 	api_version='2024-10-21',
# 	azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
# 	api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
# )

llm = ChatAnthropic(
    model_name="claude-3-5-sonnet-20240620",
    temperature=0.0,
    anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# TASK = """
# Find the lowest-priced one-way flight from Cairo to Montreal on February 21, 2025, including the total travel time and number of stops. on https://www.google.com/travel/flights/
# """
# TASK = """
# Browse Coursera, which universities offer Master of Advanced Study in Engineering degrees? Tell me what is the latest application deadline for this degree? on https://www.coursera.org/"""
# TASK = """
# Find and book a hotel in Paris with suitable accommodations for a family of two adults and two children offering free cancellation for the dates of February 14-21, 2025. on https://www.booking.com/
# """
place = ['Paris: France']

TASK = f"""
Find and book a hotel in {place} with suitable accommodations for a family of four (two adults and two children) offering free cancellation for the dates of February 14-21, 2025. on https://www.booking.com/
After entering the search location as 'Paris, France', verify that 'Paris, France' appears in the search results before proceeding.
After setting guest count to 2 adults and 2 children, verify the count is correct before searching.
"""


async def main():
	agent = Agent(
		task=TASK,
		llm=llm,
		browser=browser,
		validate_output=True,
	)
	history = await agent.run(max_steps=30) #50
	history.save_to_file('./tmp/history.json')


if __name__ == '__main__':
	asyncio.run(main())

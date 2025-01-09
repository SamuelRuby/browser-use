import os
import sys
import asyncio
from pydantic import BaseModel, SecretStr
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from browser_use.agent.service import Agent
from browser_use import Controller
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#dotenv.load_dotenv()

#initialize browser
browser = Browser(
    config=BrowserConfig(
        headless=False,
        disable_security=True,
        new_context_config=BrowserContextConfig(
            disable_security=True,
            minimum_wait_page_load_time=3,
            maximum_wait_page_load_time=15,
            browser_window_size={'width': 1920, 'height': 1080}
        )
    )
)

#qatar_airways_website = 'https://www.qatarairways.com/en/homepage.html' #https://www.qatarairways.com/en/homepage.html
# class FlightBookingInfo(BaseModel):
#     from_city: str = 'Madrid, Spain'
#     to_city: str = 'Tokyo, Japan'
#     month: str = 'February'

#controller = Controller()

llm = ChatAnthropic(
    model_name="claude-3-5-sonnet-20240620",
    temperature=0.0,
    anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# @controller.action('Search for flights', param_model=FlightBookingInfo)
# def search_flights(flight_info: FlightBookingInfo):
#     return f"Searching flights from {flight_info.from_city} to {flight_info.to_city} in {flight_info.month}"

async def main():
    agent = Agent(
        task = (
        'Objective: Find the most economical flight option from Madrid to Tokyo in February\n\n'
        'Primary Steps:\n'
        '1. Access Qatar Airways official website (www.qatarairways.com)\n'
        '2. Input flight parameters:\n'
        '   - Origin: Madrid (MAD), Spain\n'
        '   - Destination: Tokyo (NRT/HND), Japan\n'
        '   - Date Range: Any dates in February\n'
        '   - Search for lowest fare available\n\n'
        'Required Output:\n'
        '- Departure date and time\n'
        '- Arrival date and time\n'
        '- Total flight duration\n'
        '- Number of stops (if any)\n'
        '- Total fare (specify currency)\n'
        'Alternative Instructions:\n'
        'If Qatar Airways website is inaccessible:\n'
        '1. Search reliable alternative flight search engines (e.g., Skyscanner, Kayak, Google Flights)\n'
        '2. Filter for Qatar Airways flights only\n'
        '3. Provide the same flight details as requested above\n\n'
        'Note: Task is complete once the cheapest flight option is identified and all required details are provided.\n'
        'End task when objective is achieved, regardless of remaining steps.'
        ),
        llm=llm,
        browser=browser,
        validate_output=True
    )

    #agent = Agent(task, model, controller=controller, use_vision=True, browser=browser, validate_output=True)
    result= await agent.run(max_steps=50)
    print(result.text)

if __name__ == '__main__':
    asyncio.run(main())



# task = (
    #     'Go to the Qatar Airways website. '
    #     'Search for the cheapest flight from Madrid, Spain to Tokyo, Japan for any date in February. '
    #     'Provide the details of the flight found in this order: departure date, arrival date and time, flight duration, number of stops(if any), total fare, and what dates they are for.'
    #     'Note: if unable to access the website, search other sources for details on the cheapest flight from Madrid, Spain to Tokyo, Japan for any date in February.'
    #     'end task before getting to given maximum number of steps, if task is deemed completed'
    # )
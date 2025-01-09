import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel

from browser_use import ActionResult, Agent, Controller

load_dotenv()

# controller = Controller()

# @controller.registry.action('Done with task')
# async def done(text: str):
#     import smtplib
#     from email.mime.text import MIMEText
#     from email.mime.multipart import MIMEMultipart

#     # Yahoo Mail SMTP settings
#     SMTP_SERVER = "smtp.mail.yahoo.com"
#     SMTP_PORT = 587
#     SENDER_EMAIL = "mili4all@yahoo.com"
#     APP_PASSWORD = "vfelyghfadfbfxnz"  # Generate this in Yahoo Mail settings

#     try:
#         # Create the email message
#         message = MIMEMultipart()
#         message["From"] = SENDER_EMAIL
#         message["To"] = "youreajockey@gmail.com"
#         message["Subject"] = "Test Email"

#         # Add body to email
#         body = f"result\n: {text}"
#         message.attach(MIMEText(body, "plain"))

#         # Create SMTP session
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()  # Enable TLS
#             server.login(SENDER_EMAIL, APP_PASSWORD)
            
#             # Send email
#             server.send_message(message)
            
#         print("Email sent successfully!")
        
#     except Exception as e:
#         print(f"Error sending email: {e}")

# async def main():
# 	task = """
#         1. Navigate to browser-use.com
#         2. Once the page is loaded successfully, send an email report about the completed task
#         End task when objective is achieved, regardless of remaining steps
#         """
# 	model = ChatAnthropic(model='claude-3-5-sonnet-20240620')
# 	agent = Agent(task=task, llm=model, controller=controller)

# 	await agent.run()


# if __name__ == '__main__':
# 	asyncio.run(main())



controller = Controller()

# Add a flag to track if email has been sent
email_sent = False

@controller.registry.action('Done with task')
async def done(text: str):
    global email_sent
    
    # If email has already been sent, return immediately
    if email_sent:
        return

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Yahoo Mail SMTP settings
    SMTP_SERVER = "smtp.mail.yahoo.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "mili4all@yahoo.com"
    APP_PASSWORD = "vfelyghfadfbfxnz"

    # List of recipient emails
    BCC_EMAILS = [
        "youreajockey@gmail.com",
        "novamova.ruby@gmail.com"  # Add more email addresses as needed
        # "third@example.com",
    ]

    try:
        # Create the email message
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = SENDER_EMAIL  # Send to yourself
        message["Bcc"] = ", ".join(BCC_EMAILS)  # Add BCC recipients
        message["Subject"] = "Test Email"

        # Add body to email
        body = f"result\n: {text}"
        message.attach(MIMEText(body, "plain"))

        # Create SMTP session
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS
            server.login(SENDER_EMAIL, APP_PASSWORD)
            
            # Send email to all recipients
            server.send_message(message)
            
        print("Email sent successfully!")
        email_sent = True  # Set flag to True after successful send

        import sys
        sys.exit()  # Exit the script after sending email
        
    except Exception as e:
        print(f"Error sending email: {e}")

async def main():
    task = """
        1. Navigate to browser-use.com
        2. Once the page is loaded successfully, send an email report about the completed task.
        End job when task has completed successfully.
        """
    model = ChatAnthropic(model='claude-3-5-sonnet-20240620')
    agent = Agent(task=task, llm=model, controller=controller)

    await agent.run()

if __name__ == '__main__':
    asyncio.run(main())
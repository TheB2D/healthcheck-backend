import os

import dotenv
import openai
import requests
from googlesearch import search

dotenv.load_dotenv()
# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API")

def askme(query, language: str):

    question = query + f"\n\n Please re-write this it in layman's terms in the language of {language} for everyday people to understand, make it 5 sentence MAXIMUM, and include your sources in the response"

    links = []
    for idx, url in enumerate(search(query)):
        if idx >= 3:  # Stop after 3 results
            break
        links.append(url)

    sys_message = '''
    You are an AI Medical Assistant trained on a vast dataset of health information. Please be thorough and
    provide an informative answer. If you don't know the answer to a specific medical inquiry, advise seeking professional help.
    '''

    # Create the messages list with system and user input
    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": question}
    ]

    # Use the correct endpoint for chat models
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can also use "gpt-4" if you have access
        messages=messages,
        max_tokens=300,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Extract the answer from the response
    answer = response['choices'][0]['message']['content'].strip()
    return f"{answer}\n\nFor more information, you can check the following resources:\n" + "\n".join(links)


# # Example usage
# language = "Mandarin"
# question0 = f"Please re-write it in simple terms, in {language} for everyday people to understand, in bullet point form, and include your sources in the response: "
# admin_input = "The omentum and small bowel are swept cephalad. The fold of Treves or antimesenteric fat can be used to identify the terminal ileum; follow this to the cecum. In normal anatomy, the appendix can be identified at the confluence of the taeniae coli. If the appendix is retrocecal, mobilization of the retroperitoneal attachments of the cecum and ascending colon may be required. Proper patient positioning, as described above, facilitates the identification of the appendix. For a right-handed surgeon, the right-hand instrument retracts the most distal ileal loop, and the left-hand instrument optimizes cecal exposure. The preferred approach in patients with the subserosal appendix is the complete, meticulous dissection of the visceral peritoneum. "
#
# question = f"{question0} {admin_input}"
#
# response = askme(question)
#
# print(f'Question: {question}')
# print(f'Simplified: {response}')
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from retrieve import retrieve

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Search HR policy documents for relevant information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A math expression to evaluate, like '20 - 5'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

def search_documents(query):
    results = retrieve(query)
    return "\n\n".join([content for content, similarity in results])

def calculate(expression):
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Could not calculate that expression"

def run_agent(question):
    messages = [
        {"role": "system", "content": "You are an HR assistant. Use the search_documents tool to find information in HR policies. Use the calculate tool when you need to do math. Always search before answering."},
        {"role": "user", "content": question}
    ]

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message)
            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if name == "search_documents":
                    result = search_documents(args["query"])
                elif name == "calculate":
                    result = calculate(args["expression"])

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        else:
            return message.content

if __name__ == "__main__":
    question = input("\nAsk a question: ")
    print(f"\nAnswer: {run_agent(question)}")
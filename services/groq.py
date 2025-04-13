from groq import Groq
import re
import json
import os

api_key = os.getenv('GROQ_API_KEY')

client = Groq(api_key=api_key)

def chat(context):
    completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "system",
            "content": f'''You are a information retrieval system from a given context.
                        The context is: {context}'''+'''
                        Expected output:{
                            "PNR": fill in the blank strictly with PNR, not reference or ny other code,
                            "Vehicle Number": fill in the blank with  train/bus/flight number,
                            "Vehicle Name": fill in the blank with train/bus/flight name,
                            "Mode of Transport": fill in the blank with your answer,
                            "From Destination": fill in the blank with your answer,
                            "To Destination": fill in the blank with your answer,
                            "Date of Travel": fill in the blank with your answer,
                            "Time of Travel": fill in the blank with your answer,
                            "Date of Arrival": fill in the blank with your answer,
                            "Time of Arrival": fill in the blank with your answer,
                            "Distance" fill in with the total distance of the travel,
                            "Passenger details": list of dicts with all passenger details(name, age, sex, seat no, type(Sleeper, AC, Economy, Business and so on) etc.),
                            "Amount": fill in the blank with your answer,
                            "Additional Conditions: fill in with luggage, food, and other conditions,"
                        }
                        Note: Keep fields empty if not available in the context. Do not add wrong information.
                        '''
                        
        }
    ],
    temperature=0,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
    )
    
    response_text = ''.join(chunk.choices[0].delta.content or "" for chunk in completion)
    
    match = re.search(r'```(.*?)```', response_text, re.DOTALL)

    return json.loads(match[1].strip()) if match else {"error": "No JSON found in response"}

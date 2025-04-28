import logger,perception
from dotenv import load_dotenv
import google.generativeai as genai
import os

def generate_plan(preception_output:str):
    data = eval(preception_output)
    perception_result = perception.preception(**data)
    
    logger.loggingInfo("decision invoking layer")
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt=f"""You are ticket booking agent, having ticket booking tools access to book the tickets.
            Booking tools:
            1. train_ticket
            2. bus_ticket
            3. cinema_ticket

            Choose the any one of the booking tool in given format(no additional text):
              1. FUNCTION_CALL:function_name

            Guidelines:
            - Respond using EXACTLY ONE of the formats above per step.
            - Do NOT include extra text, explanation, or formatting.
            - Use nested keys (e.g., input.string) and square brackets for lists.
            Input summary:
            - User input:"{perception_result.user_query}"
            - Intent:"{perception_result.intent}"
            - Channel:"{perception_result.channel}"
            - Entities:"{perception_result.entities}"
            Examples:
            - FUNCION_CALL: train_ticket
            - FUNCTION_CALL: bus_ticket
            - FUNCTION_CALL: cinema_ticket

            Important:
            - Do NOT invent tools. Use only the tools listed above.
            - Give the exact output above mentioned in example format.
            """
    try:
        response = model.generate_content(prompt)
        logger.loggingInfo(f"decision prompt: {prompt}")
        response_str = response.text.strip()
        logger.loggingInfo(f"decision funciton calling {response_str}")
        if response_str.strip().startswith("FUNCTION_CALL:") or response_str.strip().startswith("FINAL_ANSWER:"):
            return response_str.strip()

    except Exception as e:
        logger.loggingError("plan", f"⚠️ Decision generation failed: {e}")
        return "FINAL_ANSWER: [unknown]"
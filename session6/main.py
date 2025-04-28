import logger
from dotenv import load_dotenv
import google.generativeai as genai
import os
import perception
import asyncio
import memorylayer
import action,decision
import uuid


def loadenv():
    load_dotenv()

async def main(user_input:str):
    logger.loggingInfo("===starting the connection establishing===")
    try:
        # Access your API key and initialize Gemini client correctly
        loadenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        #loads the default values
        memory = memorylayer.Memory()
        # check the user input already queried in memory layer
        memory_item = memory.retreive_data(memorylayer.MemoryItem(user_query=user_input,type="preference"))
        if(not memory_item):
            #user query not available in memory
            preception_result = perception.extract_perception(user_input)
            result_handler(preception_result)
        else:
            preception_output = str(memory_item.llm_output)
            # invoke decision layer
            resp = decision.generate_plan(preception_output)
            logger.loggingInfo(f"decision layer resp: {resp}")
            # invoke action layer
            call_action(resp)

    except Exception as e:
        logger.loggingError("configuration error:",e)

def call_action(resp:str):
    if(resp.startswith("FUNCTION_CALL")):
        logger.loggingInfo(f"final response from the ticket booking agent:{resp}")
        function_tool = resp.split(":")[-1].strip()
        action_executed = action.execute_tool(function_tool)
        logger.loggingInfo(f"ticket booking action executed successfully - {action_executed}")

def result_handler(response:dict):
    if(response.get("json_response")):
        llm_resp = response.get("json_response")
        llm = eval(llm_resp)
        percep = perception.preception(**llm)
        random_uuid = str(uuid.uuid4())
        memory = memorylayer.Memory()
        memory_item = memorylayer.MemoryItem(user_query=percep.user_query,
                          type="preference",
                          session_id=random_uuid,
                          tool_name=percep.channel,llm_output=percep.model_dump())
        
        memory.load_data(item=memory_item)
        # invoke decision layer
        resp = decision.generate_plan(llm_resp)
        logger.loggingInfo(f"decision layer resp: {resp}")
        # invoke action layer
        call_action(resp)

    elif(response.get("missing_fields")):
        missing_fields = response.get("missing_fields")
        prompt_str = f"\n some of fields are missing {missing_fields}"
        print(prompt_str)
        user_showcase_str = '''can you please provide a query like this.
        \n some of suggestions:
        \n 1. can you able to book a train ticket from tambaram to tenkasi tomorrow for 2 peoples or 
        \n 2. can you able to book a bus ticket from tambaram to tenkasi tomorrow for 2 peoples
        \n Enter:'''
        user_corrected_input = input(user_showcase_str)
        #print(user_corrected_input)
        #invoke the preception layer again with user input:
        corrected_result = perception.extract_perception(user_input=user_corrected_input)
        result_handler(corrected_result)
    elif(response.get(response.get("parsing_fields"))):
        parsing_fields = response.get("parsing_fields")
        prompt_str = f"\n please provide input correctly {parsing_fields}"
        user_showcase_str = '''can you please provide correct format of query, it will be useful to search."
        \n some of suggestions:
        \n 1. can you able to book a train ticket from tambaram to tenkasi tomorrow for 2 peoples or 
        \n 2. can you able to book a bus ticket from tambaram to tenkasi tomorrow for 2 peoples
        \n Enter: '''
        user_corrected_input = input(user_showcase_str+"\n")
        #print(user_corrected_input)
        corrected_result = perception.extract_perception(user_input=user_corrected_input)
        result_handler(corrected_result)

if __name__ == "__main__":
    print("===============Ticket booking agent Starts=============")
    #user_input = "can you able to book a train ticket from tambaram to tenkasi tomorrow for 2 peoples."
    user_input = input('''provide a query to book a tickets(train,bus,cinema)\n some of sample queries: 
                       \n 1. can you able to book a train ticket from tambaram to tenkasi tomorrow for 2 peoples or 
                       \n 2. can you able to book a bus ticket from tambaram to tenkasi tomorrow for 2 peoples or
                       \n Enter input:''')
    asyncio.run(main(user_input))
    print("===============Ticket booking agent Ends===============")

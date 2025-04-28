from pydantic import BaseModel,ValidationError
from typing import Optional
import logger
from dotenv import load_dotenv
import google.generativeai as genai
import os
import ValidationHandler

class Entities(BaseModel):
    ticket_type: Optional[str]
    from_location: Optional[str]
    to_location: Optional[str]
    date_time: Optional[str] | None
    number_of_people: Optional[int] | None

class preception(BaseModel):
    user_query: str
    intent : Optional[str]
    channel : Optional[str]
    entities: Optional[Entities]

data = '''{
  "user_query": "book train ticket",
  "intent": "book_train_ticket",
  "channel":"train_ticket",
  "entities":{
    "ticket_type": "train",
    "from_location":"chennai",
    "to_location":"tenkasi",
    "date_time": "tomorrow",
    "number_of_people": "2"
  }
}'''
#d = eval(data)
#def addvalue():
#    try:
#        perp = preception(**d)
#        print(perp.user_query)
#    except ValidationError as valid:
#        for err in valid.errors():
#            print(err)

#addvalue()

def extract_perception(user_input: str):
    '''extract the intent and entities from the user input'''
    prompt= f"""You are AI agent extract the key facts from the given input and return the response as json structured format. 
    response should contain following key facts
    - user_query
    - intent 
    - channel
    - entities
    example use case: {data} \n User input: {user_input}"""
    
    logger.loggingInfo(message=f"start extract perception prompt: {prompt}")
    try:
        # Access your API key and initialize Gemini client correctly
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        response_str = response.text.strip()
        
        json_string = response_str.replace("```json", "").replace("```", "").strip()
        logger.loggingInfo(f"preception llm response :{json_string}")
        json_string = eval(json_string)
        # validating the extracted facts of user input
        perception_json = preception(**json_string)
        str = perception_json.model_dump_json()
        response = {"json_response":str}
        logger.loggingInfo(f"response {response}")
        return response
    except ValidationError as validation:
        ErrorDetail = validation.errors();
        handler = validation_handler(ErrorDetail)
        return handler
    except Exception as e:
        logger.loggingError("configuration error:",e)

def validation_handler(ErrorDetails: list):
    missing_fields = []
    missing_fields_message = []
    parsing_fields = []
    parsing_fields_message =[]

    for error in ErrorDetails:
        if(error.get('type')=="missing"):
            missing_fields.append(error.get('loc')[-1])
            missing_fields_message.append(error.get('msg'))
     
        elif("parsing" in error.get('type')):
            parsing_fields.append(error.get('loc')[-1])
            parsing_fields_message.append(error.get('msg'))

    handler={"missing_fields":missing_fields,"missing_fields_message":missing_fields_message,
             "parsing_fields":parsing_fields,
             "parsing_fields_message":parsing_fields_message}
    return handler

        
        

            
#print(f"print preception value:{precep.model_dump_json()}")

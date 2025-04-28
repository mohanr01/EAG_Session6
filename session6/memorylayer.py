from typing import List, Optional, Dict, Any,Literal
from pydantic import BaseModel
from datetime import datetime
import logger

class MemoryItem(BaseModel):
    user_query:str
    type: Literal["preference","keyfacts","output"]
    timestamp: Optional[str] = datetime.now().isoformat()
    tool_name: Optional[str] = None
    session_id:Optional[str] = None
    llm_output:Optional[dict] = None

class Memory:
    def __init__(self):
        # Create a memory instance outside the class
        logger.loggingInfo("loading mock model data in memory......")
        train_data = {
            "user_query": "can you able to book a train ticket from tambaram to tenkasi tomorrow for 2 peoples.",
            "intent": "book_train_ticket",
            "channel":"train_ticket",
            "entities": {
                "ticket_type": "train",
                "from_location":"chennai",
                "to_location":"tenkasi",
                "date_time": "tomorrow",
                "number_of_people": "2"
                }
            }
        bus_data = {
            "user_query": "can you able to book a bus ticket from tambaram to tenkasi tomorrow for 2 peoples",
            "intent": "book_bus_ticket",
            "channel":"bus_ticket",
            "entities": {
                "ticket_type": "train",
                "from_location":"chennai",
                "to_location":"tenkasi",
                "date_time": "tomorrow",
                "number_of_people": "2"
                }
            }
        self.memory_list = [MemoryItem(user_query="can you able to book a train ticket from tambaram to tenkasi tomorrow for 2 peoples.",
                          type="preference",
                          session_id="abc_1234_dcd",
                          tool_name="train_ticket_channel",llm_output=train_data),
               MemoryItem(user_query="can you able to book a bus ticket from tambaram to tenkasi tomorrow for 2 peoples",
                          type="preference",
                          session_id="efg_1234_dcd",
                          tool_name="bus_ticket_channel",llm_output=bus_data)                
                          ]
    
    def load_data(self, item:MemoryItem):
        self.memory_list.append(item)
        logger.loggingInfo(f"new memory item is added {self.memory_list}")

    def retreive_data(self, item:MemoryItem):
        logger.loggingInfo("retriving data......")
        for mem in self.memory_list:
            if(mem.user_query == item.user_query):
                logger.loggingInfo(f"retrived  data {mem.user_query} from memory")
                return mem
            
#memory = Memory()
#memory.load_data()
#print(memory.retreive_data(MemoryItem(user_query="can you able to book a train ticket from tambaram to tenkasi tomorrow for 2 peoples.",type="preference")))




        
    

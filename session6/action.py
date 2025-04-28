import logger,perception

# mocked data
def execute_tool(call_function_tool:str):
    if(call_function_tool=="train_ticket"):
       return train_ticket_tool()
    elif(call_function_tool=="bus_ticket"):
        return bus_ticket_tool()
    elif(call_function_tool=="cinema_ticket"):
        return cinema_ticket_tool()



def train_ticket_tool():
    logger.loggingInfo("train ticket booking tool invoked")
    str='''Train ticket is booked \n
            PNR-431667889
            Trn-12661
            Frm TBM to TSI
            Cls: 3A
            p1-B4 70
            Boarding allowed from TBM only'''
    return str

def bus_ticket_tool():
    logger.loggingInfo("bus ticket booking tool invoked")
    str = '''Bus ticket is booked \n
    PNR-34343434
    BusNo- TN11AE6549
    SeatNo- W8
    Boarding point will be updated shortly.'''
    return str

def cinema_ticket_tool():
    logger.loggingInfo("cinema ticket is booked")
    str = '''Ticket booked for a film
    ticket - Q1'''
    return str
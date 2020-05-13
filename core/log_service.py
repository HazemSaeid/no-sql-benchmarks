import asyncio

async def log_event(description):
    log_file = open(r"logs\benchmark.log","a")
    log_file.write(description + " \n")
    log_file.close()

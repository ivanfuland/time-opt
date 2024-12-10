from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import pytz
import time

app = FastAPI()

class TimestampRequest(BaseModel):
    timestamp: int

class LongDateRequest(BaseModel):
    long_date: str

def convert_timestamp_to_week_number_and_formatted_date(timestamp: int):
    # 将时间戳转换为datetime对象
    date = datetime.datetime.fromtimestamp(timestamp, pytz.utc)
    # 转换为东八区时间
    tz = pytz.timezone('Asia/Shanghai')
    date_east_8 = date.astimezone(tz)
    # 获取对应的ISO周数
    week_number = date_east_8.isocalendar()[1]
    # 将datetime对象格式化为指定格式
    formatted_date = date_east_8.strftime("%B %d, %Y %I:%M %p")
    return week_number, formatted_date

def convert_timestamp_to_long_date(timestamp: int):
    # 将时间戳转换为datetime对象
    date = datetime.datetime.fromtimestamp(timestamp, pytz.utc)
    # 转换为东八区时间
    tz = pytz.timezone('Asia/Shanghai')
    date_east_8 = date.astimezone(tz)
    # 将datetime对象格式化为指定格式
    formatted_date = date_east_8.strftime("%B %d, %Y %I:%M %p")
    return formatted_date

def convert_long_date_to_timestamp(long_date: str):
    # 将长时间格式转换为datetime对象
    tz = pytz.timezone('Asia/Shanghai')
    date = datetime.datetime.strptime(long_date, "%B %d, %Y %I:%M %p")
    date_east_8 = tz.localize(date)
    # 转换为UTC时间戳
    timestamp = int(date_east_8.astimezone(pytz.utc).timestamp())
    return timestamp

@app.post("/get_week_number/")
def get_week_number(request: TimestampRequest):
    week_number, formatted_date = convert_timestamp_to_week_number_and_formatted_date(request.timestamp)
    return {"week_number": week_number, "formatted_date": formatted_date}

@app.post("/get_current_week/")
def get_current_week():
    current_timestamp = int(time.time())
    week_number, formatted_date = convert_timestamp_to_week_number_and_formatted_date(current_timestamp)
    return {"week_number": week_number, "formatted_date": formatted_date}

@app.post("/convert_timestamp_to_long_date/")
def convert_timestamp_to_long_date_endpoint(request: TimestampRequest):
    formatted_date = convert_timestamp_to_long_date(request.timestamp)
    return {"formatted_date": formatted_date}

@app.post("/convert_long_date_to_timestamp/")
def convert_long_date_to_timestamp_endpoint(request: LongDateRequest):
    timestamp = convert_long_date_to_timestamp(request.long_date)
    return {"timestamp": timestamp}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=32180)

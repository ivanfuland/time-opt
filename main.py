from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import pytz
import time

app = FastAPI()

class TimestampRequest(BaseModel):
    timestamp: int

class DateRequest(BaseModel):
    date: str

def convert_timestamp_to_week_number_and_formatted_date(timestamp: int):
    # 将时间戳转换为datetime对象
    date = datetime.datetime.fromtimestamp(timestamp, pytz.utc)
    # 转换为东八区时间
    tz = pytz.timezone('Asia/Shanghai')
    date_east_8 = date.astimezone(tz)
    # 获取对应的ISO周数
    week_number = date_east_8.isocalendar()[1]
    # 将datetime对象格式化为指定格式
    formatted_date = date_east_8.strftime("%Y-%m-%d %H:%M:%S")
    return week_number, formatted_date

@app.post("/get_week_number/")
def get_week_number(request: TimestampRequest):
    week_number, formatted_date = convert_timestamp_to_week_number_and_formatted_date(request.timestamp)
    return {"week_number": week_number, "formatted_date": formatted_date}

@app.post("/get_current_week/")
def get_current_week():
    current_timestamp = int(time.time())
    week_number, formatted_date = convert_timestamp_to_week_number_and_formatted_date(current_timestamp)
    return {"week_number": week_number, "formatted_date": formatted_date}

@app.post("/timestamp_to_date/")
def timestamp_to_date(request: TimestampRequest):
    try:
        date = datetime.fromtimestamp(request.timestamp)
        return {"date": date.strftime('%Y-%m-%d %H:%M:%S')}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/date_to_timestamp/")
def date_to_timestamp(request: DateRequest):
    try:
        date = datetime.strptime(request.date, '%Y-%m-%d %H:%M:%S')
        timestamp = int(date.timestamp())
        return {"timestamp": timestamp}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=32180)

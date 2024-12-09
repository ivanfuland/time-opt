from fastapi import FastAPI
from pydantic import BaseModel
import datetime

app = FastAPI()

class TimestampRequest(BaseModel):
    timestamp: int

@app.route("/get_week_number/", methods=["POST"])
def get_week_number(request: TimestampRequest):
    # 将时间戳转换为datetime对象
    date = datetime.datetime.utcfromtimestamp(request.timestamp)
    # 获取对应的ISO周数
    week_number = date.isocalendar()[1]
    return {"week_number": week_number}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=32179)

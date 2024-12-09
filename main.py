
import datetime

# 获取当前时间
current_date = datetime.datetime.now()

# 获取当前日期的ISO周数
week_number = current_date.isocalendar()[1]


print(f"当前日期是: {current_date}")

# 输出结果
print(f"当前周数是: {week_number}")
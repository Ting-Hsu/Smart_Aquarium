from datetime import datetime

# dd/mm/YY H:M:S
dt_string = datetime.now().strftime("%H:%M:%S")
print(dt_string)
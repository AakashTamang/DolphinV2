from datetime import datetime, date

entry_date = "2018-09-09"
exit_date = ""

if not exit_date:
    exit_date = str(date.today())

total_exp_days = abs(datetime.strptime(exit_date, "%Y-%m-%d")-datetime.strptime(entry_date, "%Y-%m-%d")).days

print(total_exp_days)
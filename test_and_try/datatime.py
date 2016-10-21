import datetime
import time




# main_start_time = 1477005806
main_start_time = 1476911806
# time.time()


print datetime.datetime.today()
print time.time()

print datetime.datetime.fromtimestamp(time.time())
a = datetime.datetime.date( datetime.datetime.today() )
print a

print datetime.datetime.toordinal(a)

working_time = time.time() - main_start_time
working_days = working_time // (60 * 60 * 24)
working_days_local = working_time / (60 * 60 * 24)
working_hours = ((working_days_local - working_days) * (60 * 60 * 24)) // (60 * 60)
working_hours_local = ((working_days_local - working_days) * (60 * 60 * 24)) / (60 * 60)
working_minutes = (working_hours_local - working_hours) * 60


print working_time
print working_days_local
print working_days
print working_hours_local
print working_hours
print working_minutes

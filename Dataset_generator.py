import csv
from random import randint, randrange

def data_entry(monthly):
    with open("Expense.csv",'a') as data:
        csv_writer = csv.DictWriter(data, fieldnames=fieldnames)
        csv_writer.writerow({"Mthly_HH_Income":monthly,
                             "Mthly_HH_Expense":randint(int(minlimit),int(maxlimit))})
    data.close()

def limited(monthly, maxlimit=0, minlimit=0):
    ml=maxlimit
    mil=minlimit
    if monthly <= 20000:
        save=0
        estimate=0
        maxlimit=monthly 
        minlimit=monthly
    elif monthly<=25000:
        save=20
        estimate=save * 12
        maxlimit = monthly - 20
        minlimit = 20000
    elif monthly<=29999:
        save = monthly-20000
        estimate = save*12
        maxlimit = monthly
        minlimit = monthly-save
    elif monthly<=50000:
        save = (30/100) * monthly
        estimate = save*12
        maxlimit = monthly
        minlimit = monthly-save
    elif monthly<=100000:
        save= (40/100)*monthly
        estimate =save * 12
        maxlimit = monthly - ((20/100)*monthly)
        minlimit = monthly - save
    else:
        save = (70/100)*monthly
        estimate = save *12
        maxlimit = monthly - ((30/100)*monthly)
        minlimit = monthly - save
    return [minlimit, maxlimit, estimate]
      

fieldnames=["Mthly_HH_Income", "Mthly_HH_Expense"]
for i in range(100):
    monthly=randrange(30000,90000)
    global maxlimit
    global minlimit

    d=limited(monthly)
    minlimit, maxlimit, estimate = d[0], d[1] ,d[2]
    data_entry(monthly)

        

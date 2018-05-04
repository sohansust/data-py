import requests
import csv
    
    
cookies = dict(cookies_are='')

def get_data(settings):
    #set the initial settings
   
    #initial url for loop
    url_raw = 'https://my.euroclear.com/bin/euroclear/db/monthlystockloan.search.json?month=eq:{month}&year=eq:{year}&limit={limit}&search=1&order=asc:abbreviation&&t=1525112162330'

    #add settings in the url_raw
    url=url_raw.format(**settings)
  
    #get the response and save it to r
    loan_data = requests.get(url, cookies=cookies)
    return loan_data.json()

def process_data(settings):
    #save stock loan data in monthly_data
    month_x_data = get_data(settings)
    #save the total data in total_month_x_data
    total_month_x_data=month_x_data['results']             

    #save amount of monthly data in a page in amount_of_records

    amount_of_records = month_x_data['amountofrecords']
    #loop to navigate other pages (limit)
    while amount_of_records == 50:
        settings['limit'] = settings['limit'] + 1
        month_x_data = get_data(settings)
        amount_of_records = month_x_data['amountofrecords']
        total_month_x_data = total_month_x_data + month_x_data['results']
    #assign value of month_x(cuurent month) to x_date
    
    x_date = str(settings['year'])+'m'+str(settings['month'])

    for row in total_month_x_data:
        row['date']=x_date
    return total_month_x_data

settings = {
        'month': 1,
        'year': 2006,
        'limit': 0
        }

#loop over month

data = []
for i in range(2006,2019):
    settings['year'] = i
    for i in range(1,13):
        settings['month']=i
        settings['limit']=0
        data = data + process_data(settings)
    

keys = data[0].keys()
with open('stock_loan_monthly.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)



import pandas as pd
import datetime
import dateutil
import string as str

read_addsToCart = pd.read_csv(r'DataAnalyst_Ecom_data_addsToCart.csv', header=0)
read_ecomDataSessionCounts = pd.read_csv(r'DataAnalyst_Ecom_data_sessionCounts.csv', header=0)

read_ecomDataSessionCounts['ECR'] = read_ecomDataSessionCounts['transactions']/read_ecomDataSessionCounts['sessions']

print("read_addsToCart = ", read_addsToCart)
print("")

print("read_ecomDataSessionCounts = ", read_ecomDataSessionCounts)
print("")



# Convert data from string to date
read_ecomDataSessionCounts['dim_date'] = read_ecomDataSessionCounts['dim_date'].astype('datetime64[ns]')

read_ecomDataSessionCounts.index = pd.to_datetime(read_ecomDataSessionCounts['dim_date'], format='%m/%d/%y')

# Cumulating transactions per month per device type
ecomDataSessionCounts_byMonth = read_ecomDataSessionCounts\
    .groupby([read_ecomDataSessionCounts['dim_date'].dt.year, read_ecomDataSessionCounts['dim_date'].dt.month, read_ecomDataSessionCounts['dim_deviceCategory']])\
    ['dim_deviceCategory'].count()





print("final read_ecomDataSessionCounts = ", read_ecomDataSessionCounts)
print("")

print("final ecomDataSessionCounts_byMonth = ", ecomDataSessionCounts_byMonth)
print("")


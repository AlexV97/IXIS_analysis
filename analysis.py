import pandas as pd
import dateutil
import string as str

read_addsToCart = pd.read_csv(r'DataAnalyst_Ecom_data_addsToCart.csv')
read_ecomDataSessionCounts = pd.read_csv(r'DataAnalyst_Ecom_data_sessionCounts.csv')

print("read_addsToCart_csv = ", read_addsToCart)
print("")

print("read_ecomDataSessionCounts_csv = ", read_ecomDataSessionCounts)
print("")

# Convert data from string to date
read_ecomDataSessionCounts['dim_date'] = read_ecomDataSessionCounts['dim_date']

read_ecomDataSessionCounts.index = pd.to_datetime(read_ecomDataSessionCounts['dim_date'], format='%m/%d/%y')
#read_ecomDataSessionCounts.groupby(by=[read_ecomDataSessionCounts.index.year, read_ecomDataSessionCounts.index.month])
read_ecomDataSessionCounts.groupby(pd.Grouper(freq='M')).sum()

print("final read_ecomDataSessionCounts_csv = ", read_ecomDataSessionCounts)
print("")


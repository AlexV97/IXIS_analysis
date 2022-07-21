import pandas as pd

read_addsToCart = pd.read_csv(r'DataAnalyst_Ecom_data_addsToCart.csv', header=0)
read_ecomDataSessionCounts = pd.read_csv(r'DataAnalyst_Ecom_data_sessionCounts.csv', header=0)

read_ecomDataSessionCounts['ECR'] = read_ecomDataSessionCounts['transactions']/read_ecomDataSessionCounts['sessions']

# Convert data from string to date
read_ecomDataSessionCounts['dim_date'] = read_ecomDataSessionCounts['dim_date'].astype('datetime64[ns]')
read_ecomDataSessionCounts.index = pd.to_datetime(read_ecomDataSessionCounts['dim_date'], format='%m/%d/%y')

# Cumulating transactions per month per device type
firstSheetColumns_list = ['sessions', 'transactions', 'QTY', 'ECR']

ecomDataSessionCounts_byMonth = read_ecomDataSessionCounts\
    .groupby([read_ecomDataSessionCounts['dim_date'].dt.year, read_ecomDataSessionCounts['dim_date'].dt.month, read_ecomDataSessionCounts['dim_deviceCategory']])\
    [['sessions', 'transactions', 'QTY', 'ECR']].sum()


from xlsxwriter.utility import xl_cell_to_rowcol,xl_range
with pd.ExcelWriter("DataAnalyst_Ecom_data_Report.xlsx", engine='xlsxwriter') as writer:
    workbook = writer.book
    #read_ecomDataSessionCounts.to_excel(writer, sheet_name= "Try", index=True)
    ecomDataSessionCounts_byMonth.to_excel(writer, sheet_name= "PerMonthPerDevice", index=True)

print("Wrote Excel Report")
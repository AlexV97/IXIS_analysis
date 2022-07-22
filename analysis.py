import pandas as pd


read_addsToCart = pd.read_csv(r'DataAnalyst_Ecom_data_addsToCart.csv', header=0)
#dim_year,dim_month
#read_addsToCart['dim_date'] = pd.to_datetime([read_addsToCart['dim_year'], read_addsToCart['dim_month']])
print("read_addsToCart=", read_addsToCart)
print("read_addsToCart.columns=", read_addsToCart.columns)

read_ecomDataSessionCounts = pd.read_csv(r'DataAnalyst_Ecom_data_sessionCounts.csv', header=0)

### Per Month Per Device
# Convert data from string to date
read_ecomDataSessionCounts['dim_date'] = read_ecomDataSessionCounts['dim_date'].astype('datetime64[ns]')
read_ecomDataSessionCounts.index = pd.to_datetime(read_ecomDataSessionCounts['dim_date'], format='%m/%d/%y')
read_ecomDataSessionCounts['dim_year_sc'] = read_ecomDataSessionCounts['dim_date'].dt.year
read_ecomDataSessionCounts['dim_month_sc'] = read_ecomDataSessionCounts['dim_date'].dt.month


# Cumulating transactions per month per device type
firstSheetColumns_list = ['sessions', 'transactions', 'QTY', 'ECR']

ecomDataSessionCounts_byMonth = read_ecomDataSessionCounts\
    .groupby([read_ecomDataSessionCounts['dim_date'].dt.year, read_ecomDataSessionCounts['dim_date'].dt.month, read_ecomDataSessionCounts['dim_deviceCategory']])\
    [['sessions', 'transactions', 'QTY']].sum()
ecomDataSessionCounts_byMonth['ECR'] = ecomDataSessionCounts_byMonth['transactions']/ecomDataSessionCounts_byMonth['sessions']

### Month Over Month Comparison
ecomDataSessionCounts_monthOverMonth = read_ecomDataSessionCounts\
    .groupby([read_ecomDataSessionCounts['dim_year_sc'],read_ecomDataSessionCounts['dim_month_sc']])\
    [['dim_date', 'dim_browser', 'sessions', 'transactions', 'QTY']].sum()

ecomDataSessionCounts_monthOverMonth['ECR'] = ecomDataSessionCounts_monthOverMonth['transactions']/ecomDataSessionCounts_monthOverMonth['sessions']

monthOverMonth = pd.merge(ecomDataSessionCounts_monthOverMonth, read_addsToCart, how='inner',\
                          left_on= 'dim_month_sc', \
                          right_on= 'dim_month')

monthOverMonth_transposed = monthOverMonth.T

print("monthOverMonth=", monthOverMonth)


from xlsxwriter.utility import xl_cell_to_rowcol,xl_range
with pd.ExcelWriter("DataAnalyst_Ecom_data_Report.xlsx", engine='xlsxwriter') as writer:
    workbook = writer.book
    ecomDataSessionCounts_byMonth.to_excel(writer, sheet_name= "PerMonthPerDevice", index=True)
    monthOverMonth_transposed.to_excel(writer, sheet_name= "MonthOverMonthComparison", index=True)

print("Wrote Excel Report")
import pandas as pd


read_addsToCart = pd.read_csv(r'DataAnalyst_Ecom_data_addsToCart.csv', header=0)

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
ecomDataSessionCounts_byMonth['QtyPerTransaction'] = ecomDataSessionCounts_byMonth['QTY']/ecomDataSessionCounts_byMonth['transactions']

### Transactions per device type by month - reverse order grouping vs. previous
ecomDataSessionCounts_byDevMonth = read_ecomDataSessionCounts\
    .groupby([read_ecomDataSessionCounts['dim_deviceCategory'], read_ecomDataSessionCounts['dim_date'].dt.year, read_ecomDataSessionCounts['dim_date'].dt.month])\
    [['sessions', 'transactions', 'QTY']].sum()
ecomDataSessionCounts_byDevMonth['ECR'] = ecomDataSessionCounts_byDevMonth['transactions']/ecomDataSessionCounts_byDevMonth['sessions']
ecomDataSessionCounts_byDevMonth['QtyPerTransaction'] = ecomDataSessionCounts_byDevMonth['QTY']/ecomDataSessionCounts_byDevMonth['transactions']

### Month Over Month Comparison
ecomDataSessionCounts_monthOverMonth = read_ecomDataSessionCounts\
    .groupby([read_ecomDataSessionCounts['dim_year_sc'],read_ecomDataSessionCounts['dim_month_sc']])\
    [['dim_date', 'dim_browser', 'sessions', 'transactions', 'QTY']].sum()

ecomDataSessionCounts_monthOverMonth['ECR'] = ecomDataSessionCounts_monthOverMonth['transactions']/ecomDataSessionCounts_monthOverMonth['sessions']
ecomDataSessionCounts_monthOverMonth['QtyPerTransaction'] = ecomDataSessionCounts_monthOverMonth['QTY']/ecomDataSessionCounts_monthOverMonth['transactions']

monthOverMonth = pd.merge(read_addsToCart, ecomDataSessionCounts_monthOverMonth, how='outer',\
                          left_on = ['dim_year','dim_month'], \
                          right_on= ['dim_year_sc','dim_month_sc'] )

last2Months_diff = monthOverMonth.iloc[-1]-monthOverMonth.iloc[-2]
last2Months_diff_rel = last2Months_diff / monthOverMonth.iloc[-2]

# Month Over Month - last 2 months
monthOverMonth_diff = monthOverMonth.tail( n=2 )

# transposing for ease of use in Escel report
monthOverMonth_transposed = monthOverMonth_diff.T
# adding columns for calculation/comparison of last 2 months: absolute difference and relative difference
monthOverMonth_transposed['abs_diff'] = last2Months_diff
monthOverMonth_transposed['rel_diff'] = last2Months_diff_rel

# clean up of meaningless cells
monthOverMonth_transposed.at['dim_year', 'abs_diff'] = ""
monthOverMonth_transposed.at['dim_year', 'rel_diff'] = ""
monthOverMonth_transposed.at['dim_month', 'abs_diff'] = ""
monthOverMonth_transposed.at['dim_month', 'rel_diff'] = ""

# Writing Excel Report
from xlsxwriter.utility import xl_cell_to_rowcol,xl_range
with pd.ExcelWriter("DataAnalyst_Ecom_data_Report.xlsx", engine='xlsxwriter') as writer:
     workbook = writer.book
     ecomDataSessionCounts_byMonth.to_excel(writer, sheet_name= "PerMonthPerDevice", index=True)
     ecomDataSessionCounts_byDevMonth.to_excel(writer, sheet_name= "PerDevicePerMonth", index=True)
     monthOverMonth_transposed.to_excel(writer, sheet_name= "MonthOverMonthComparison", index=True)


print("Wrote Excel Report. analysis.py completed")
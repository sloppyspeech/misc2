import xlsxwriter
from datetime import datetime

# 1. Initialize Workbook and Worksheet
workbook = xlsxwriter.Workbook('Executive_Readiness_Dashboard.xlsx')
worksheet = workbook.add_worksheet('Dashboard')
data_sheet = workbook.add_worksheet('RawData')

# 2. Define Dashboard Styles
bg_color = '#262626'  # Dark Grey
text_white = workbook.add_format({'font_color': 'white', 'font_name': 'Calibri'})
header_format = workbook.add_format({'font_color': 'white', 'font_size': 18, 'bold': True, 'font_name': 'Calibri'})

# Set Dashboard Background
worksheet.set_column('A:Z', 12)
for i in range(100):
    worksheet.set_row(i, 20, workbook.add_format({'bg_color': bg_color}))

# Add Main Title
worksheet.write('B2', 'EXECUTIVE ENVIRONMENT READINESS DASHBOARD', header_format)

# 3. Prepare Raw Data
headers = ['Target Date', 'App Count', 'Status', 'DateValue']
data = [
    ['2025-12-05', 5, 'Completed', 46000],
    ['2025-12-19', 5, 'Completed', 46014],
    ['2026-01-13', 7, 'In Progress', 46039],
    ['2026-01-19', 6, 'In Progress', 46045],
    ['2026-01-23', 1, 'Planned', 46049],
    ['2026-01-30', 3, 'Planned', 46056],
    ['2026-02-06', 4, 'Planned', 46063],
    ['2026-03-20', 2, 'Planned', 46105],
]

data_sheet.write_row('A1', headers)
for row_num, row_data in enumerate(data, start=1):
    data_sheet.write_row(row_num, 0, row_data)

# 4. CHART 1: Environment Preparation Status (Donut)
donut = workbook.add_chart({'type': 'doughnut'})
donut.add_series({
    'name': 'Status Distribution',
    'categories': '=RawData!$C$2:$C$9',
    'values':     '=RawData!$B$2:$B$9',
    'points': [
        {'fill': {'color': '#70AD47'}}, # Completed (Green)
        {'fill': {'color': '#70AD47'}}, 
        {'fill': {'color': '#ED7D31'}}, # In Progress (Orange)
        {'fill': {'color': '#ED7D31'}},
        {'fill': {'color': '#A5A5A5'}}, # Planned (Grey)
    ],
    'data_labels': {'percentage': True, 'font': {'color': 'white'}},
})
donut.set_title({'name': 'PREPARATION STATUS', 'name_font': {'color': 'white'}})
donut.set_chartarea({'fill': {'color': bg_color}, 'border': {'none': True}})
donut.set_plotarea({'fill': {'color': bg_color}, 'border': {'none': True}})
donut.set_legend({'none': True})
worksheet.insert_chart('B4', donut)

# 5. CHART 2: Completion Timeline (Stacked Column)
column_chart = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
column_chart.add_series({
    'name': 'Completed',
    'categories': '=RawData!$A$2:$A$9',
    'values':     '=RawData!$B$2:$B$3',
    'fill': {'color': '#70AD47'}
})
column_chart.set_title({'name': 'COMPLETION TIMELINE', 'name_font': {'color': 'white'}})
column_chart.set_x_axis({'num_font': {'color': 'white'}, 'line': {'color': 'white'}})
column_chart.set_y_axis({'num_font': {'color': 'white'}, 'major_gridlines': {'visible': False}})
column_chart.set_chartarea({'fill': {'color': bg_color}, 'border': {'none': True}})
column_chart.set_plotarea({'fill': {'color': bg_color}, 'border': {'none': True}})
worksheet.insert_chart('H4', column_chart)

# 6. CHART 3: App Distribution (Bubble)
bubble = workbook.add_chart({'type': 'bubble'})
bubble.add_series({
    'categories': '=RawData!$D$2:$D$9', # X-axis (Dates as numbers)
    'values':     '=RawData!$B$2:$B$9', # Y-axis (Count)
    'bubbles':    '=RawData!$B$2:$B$9', # Size
    'fill':       {'color': '#4472C4', 'transparency': 30},
})
bubble.set_title({'name': 'APP DISTRIBUTION BY DATE', 'name_font': {'color': 'white'}})
bubble.set_chartarea({'fill': {'color': bg_color}, 'border': {'none': True}})
bubble.set_plotarea({'fill': {'color': bg_color}, 'border': {'none': True}})
bubble.set_x_axis({'num_format': 'dd-mmm', 'num_font': {'color': 'white'}})
bubble.set_y_axis({'num_font': {'color': 'white'}})
worksheet.insert_chart('B18', bubble)

workbook.close()
print("Dashboard generated successfully!")

import json
import csv
import pandas as pd

# Converting JSON to CSV
with open('D:\Development\PythonProjects\DataFolder\cat.json') as json_file:
    json_data = json.load(json_file)
 
json_data_array = json_data['data']
csv_file = open('D:\Development\PythonProjects\DataFolder\cat-converted-emptyrows.csv', 'w')
csv_writer = csv.writer(csv_file)

count = 0

for per_data in json_data_array:
    if count == 0:
        header = per_data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(per_data.values())
 
csv_file.close()

# Removing empty rows
df = pd.read_csv('D:\Development\PythonProjects\DataFolder\cat-converted-emptyrows.csv')
df.to_csv('D:\Development\PythonProjects\DataFolder\cat-converted-noemptyrows.csv', index=False)
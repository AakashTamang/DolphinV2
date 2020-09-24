import pandas as pd
import numpy as np

df = pd.read_excel("../datasets/train_data.xlsx")

df['Text'].replace('', np.nan, inplace=True)

df.dropna(subset=['Text'], inplace=True)
print(len(df))
print(df.info())

writer = pd.ExcelWriter('final_train_data.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
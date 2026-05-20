import pandas as pd
df = pd.read_csv('d:/lorens/Lorenix/auto-data-cleaner/sample_dataset.csv')
df.to_excel('d:/lorens/Lorenix/auto-data-cleaner/sample_dataset.xlsx', index=False)

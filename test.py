import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath('wind_months.csv'))
wind_month_day_df = pd.read_csv(dir_path + '\wind_months.csv', header=0)
col = wind_month_day_df['January']
print(wind_month_day_df)
for i, num_days in enumerate(col[:-1]): 
        num_secs = num_days * 86400
        print(num_days, wind_month_day_df['Wind Speed (km/h)'][i])

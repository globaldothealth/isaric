# Corrects temperatures recorded in farenheit to celsius based on max human internal temperature.

import pandas as pd

def convert_temperature_units(value):
    if value <= 90:
        return value
    elif value > 90:
        return (value - 32) * 5/9

# import data
df = pd.read_csv("ISARIC RAPID/ISARICCOVID19RAPIDFo_DATA_2022-07-06_0932.csv")

# create new columns with the converted data
df['temp_vsorres_new'] = df.apply(lambda x: convert_temperature_units(x.temp_vsorres), axis=1)
df['daily_temp_vsorres_new'] = df.apply(lambda x: convert_temperature_units(x.daily_temp_vsorres), axis=1)

# save the new file
df2 = df.convert_dtypes()
df2.to_csv("ISARIC RAPID/ISARICCOVID19RAPIDFo_DATA_2022-07-06_0932_temperaturefix.csv", index=False)

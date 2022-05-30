import requests
import pandas as pd
from time import time, sleep
# https://api.census.gov/data/timeseries/intltrade/imports/hs?get=CTY_CODE,CTY_NAME,I_COMMODITY,I_COMMODITY_SDESC,GEN_VAL_MO&YEAR=1992&MONTH=01&COMM_LVL=HS10&I_COMMODITY=0*&key=decfaa8ca0437d2f9d284402ce6d8901b8a5884e
expo_impo = 'exports' #set 'exports' to get expos / 'imports' to get impos!
generated_key = '150bc88465f0b44811aef129e58a5a3904624e1f' # When expires, get a fresh one in http://api.census.gov/data/key_signup.html 
ecommodities = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11' , '12']
#years = [2018, 2019, 2020]
years = [2018, 2019, 2020]

# Resume after error! Comment this lines if there is no error!
#years = [2018, 2019, 2020]
#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11' , '12']

print(f'***************************\n***Scraping for {expo_impo}***\n***************************\n')
for year in years:
	print(f'\nCurrent Year: {year}')
	for month in months:
		print(f'\n>Current Month: {month}')
		complete_data = pd.DataFrame() # Initialize empty Dataframe
        
		for commodity in ecommodities:
        
			print(f'>>Current Commodity: {commodity}')
			if (expo_impo == 'exports'):
				url = f'https://api.census.gov/data/timeseries/intltrade/{expo_impo}/hs?get=CTY_CODE,CTY_NAME,E_COMMODITY,E_COMMODITY_SDESC,ALL_VAL_MO&YEAR={year}&MONTH={month}&COMM_LVL=HS10&E_COMMODITY={commodity}*&key={generated_key}'
			else:
				url = f'https://api.census.gov/data/timeseries/intltrade/{expo_impo}/hs?get=CTY_CODE,CTY_NAME,I_COMMODITY,I_COMMODITY_SDESC,GEN_VAL_MO&YEAR={year}&MONTH={month}&COMM_LVL=HS10&I_COMMODITY={commodity}*&key={generated_key}'
			result = None
			while result is None:
				try:
					result = requests.get(url).json()
				except:
					print(f'>>Error on commodity: {commodity}. Rescraping!')
					sleep(1.5)
					pass
			data = pd.DataFrame(result)
			print(f'>>>Commodity length: {len(data)}')
			
            #print('Current data: \n{data}')
			if (commodity == 0):
				complete_data = complete_data.append(data, ignore_index = True) # Append to complete_data
			else:
				complete_data = complete_data.append(data[1:], ignore_index = True) #Removes header and append to complete_data
            
			#print(f'>>>Total length: {len(complete_data)}')
			if (commodity == 9):
				filename = f'{expo_impo}_USA_{year}_{month}.csv'
				print(f'>>>>Saving {filename}\n')
				complete_data.to_csv(filename, index = False)

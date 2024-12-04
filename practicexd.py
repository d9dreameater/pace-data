import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
import json

fig, ax = plt.subplots()

yr = input('Please enter the year which you would like to access: [2023,2024]')
tracki = input('Please enter the track which you would like to access: ')
sessioni = input('Please enter the session which you would like to access: ')
driveri = input('Please enter the driver which you would like to access: ')
#input(f'You are requesting laptime data for {driver} during the {yr} {track} {session}. Is this correct?(Y/N) ')

meetings = urlopen(f'https://api.openf1.org/v1/meetings?year={yr}')
wknd = json.loads(meetings.read().decode('utf-8'))
wdf = pd.DataFrame(wknd)

sessions = urlopen('https://api.openf1.org/v1/sessions')
ssns = json.loads(sessions.read().decode('utf-8'))
sdf = pd.DataFrame(ssns)

ddf = pd.DataFrame(np.array([['1', 'Max Verstappen', 'VER'],['2','Logan Sargeant','SAR'],['3','Daniel Ricciardo','RIC'],['4','Lando Norris','NOR'],['10','Pierre Gasly','GAS'],['11','Sergio Perez','PER'],['14','Fernando Alonso','ALO'],['16', 'Charles Leclerc', 'LEC'],['18','Lance Stroll','STR'],['20','Kevin Magnussen','MAG'],['21','Nyck de Vries','DEV'],['22','Yuki Tsunoda','TSU'],['23','Alexander Albon','ALB'],['24','Zhou Guanyu','ZHO'],['27','Nico Hulkenberg','HUL'],['30','Liam Lawson','LAW'],['31','Esteban Ocon','OCO'],['33','Max Verstappen','VER'],['43','Franco Colapinto','COL'],['44','Lewis Hamilton','HAM'],['55', 'Carlos Sainz Jr.', 'SAI'],['63','George Russell','RUS'],['77','Valtteri Bottas','BOT'],['81','Oscar Piastri','PIA']]), columns=['driver_number', 'driver_name', 'driver_acronym'])
 
drivero = ddf.loc[ddf['driver_name'] == driveri, 'driver_number'].iloc[0]
tracko = wdf.loc[wdf['circuit_short_name'] == tracki, 'meeting_key'].iloc[0]
sessiono = sdf.loc[sdf['meeting_key'] == tracko, 'session_key'].iloc[-1]

laps = urlopen(f'https://api.openf1.org/v1/laps?session_key={sessiono}&driver_number={drivero}')
data = json.loads(laps.read().decode('utf-8'))
ldf = pd.DataFrame(data)
#df.plot.line(x='lap_number',y='lap_duration')

raceControl = urlopen(f'https://api.openf1.org/v1/race_control?session_key={sessiono}')
data2 = json.loads(raceControl.read().decode('utf-8'))
df2 = pd.DataFrame(data2)

#if category == safety car, then line color changes to yellow until category == safety car

x_values = ldf['lap_number']
y_values = ldf['lap_duration']

for i in range(len(x_values) - 1):
    if int(df2.loc[df2['category'] == 'SafetyCar', 'lap_number'].iloc[0]) <= x_values[i] <= int(df2.loc[df2['category'] == 'SafetyCar', 'lap_number'].iloc[1]):
        plt.plot(x_values[i:i+2], y_values[i:i+2], color='yellow')
    else:
        plt.plot(x_values[i:i+2], y_values[i:i+2], color='black')
plt.xlabel('Lap Number')
plt.ylabel('Lap Duration')
#ax.set_ylim([90,140])
plt.show()
print(df2.loc[df2['category'] == 'SafetyCar', 'lap_number'])

'''THINGS TO WORK ON/FIX
    *what to do if no safety car/multiple safety cars
    *what to do if red flag/race restart
    *show lap duration on plot as minutes:seconds:milliseconds
    *run user input again if user input is incorrect/not recognized
    *scale down plot to show significant differences in laptimes, ie remove outliers due to sc or pit
    *maybe identify tire compound
    *properly identify sessionkey based on user input
    *all i can think of for now, keep grinding lil fella
'''
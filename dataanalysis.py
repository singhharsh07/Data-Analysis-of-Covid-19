import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime

covid_df =pd.read_csv("F:/covid_19_india.csv")
covid_df.head(10)
covid_df.info()
covid_df.describe()

vaccine_df =pd.read_csv("F:/covid_vaccine_statewise.csv")
vaccine_df.head(7)
covid_df.drop(["Sno","Time","ConfirmedIndianNational","ConfirmedForeignNational"],inplace =True,axis =1)
covid_df.head()

covid_df['Date'] =pd.to_datetime(covid_df['Date'],format ='%Y-%m-%d')
covid_df.head()

#active cases

covid_df['Active_Cases'] =covid_df['Confirmed']-(covid_df['Cured']+covid_df['Deaths'])
covid_df.tail()

statewise =pd.pivot_table(covid_df, values =["Confirmed","Deaths","Cured"],index ="State/UnionTerritory",aggfunc =max)
statewise["Recovery Rate"] =statewise["Cured"]*100/statewise["Confirmed"]
statewise["Mortality Rate"] =statewise["Deaths"]*100/statewise["Confirmed"]
statewise =statewise.sort_values(by ="Confirmed",ascending =False)
statewise.style.background_gradient(cmap ="cubehelix")

top_10_active_cases =covid_df.groupby(by ='State/UnionTerritory').max()[['Active_Cases','Date']].sort_values(by =['Active_Cases'],ascending =False).reset_index()
fig =plt.figure(figsize =(16,9))
plt.title("top 10 states with most active cases in India")
ax =sns.barplot(data =top_10_active_cases.iloc[:10],y ="Active_Cases",x ="State/UnionTerritory",linewidth =2,edgecolor ="red")

#tp 10 active cases state
top_10_active_cases =covid_df.groupby(by ='State/UnionTerritory').max()[['Active_Cases','Date']].sort_values(by =['Active_Cases'],ascending =False).reset_index()
fig =plt.figure(figsize =(16,9))
plt.title("top 10 states with most active cases in India")
ax =sns.barplot(data =top_10_active_cases.iloc[:10],y ="Active_Cases",x ="State/UnionTerritory",linewidth =2,edgecolor ="red")
plt.xlabel('states')
plt.ylabel("total active cases")
plt.show()

#top states with highest deaths
top_10_deaths=covid_df.groupby(by ='State/UnionTerritory').max()[['Deaths','Date']].sort_values(by =['Deaths'],ascending =False).reset_index()

fig =plt.figure(figsize =(18,5))

plt.title("top 10 states with most deaths",size =25)
ax =sns.barplot(data =top_10_deaths.iloc[:12],y ="Deaths",x ="State/UnionTerritory",linewidth =2,edgecolor ="black")
plt.xlabel("states")
plt.ylabel("total death cases")
plt.show()

#growth trend

fig =plt.figure(figsize =(12,6))

selected_states = ['Maharashtra', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Uttar Pradesh']
filtered_df = covid_df[covid_df['State/UnionTerritory'].isin(selected_states)]

# Plotting with Seaborn
ax = sns.lineplot(data=filtered_df, x='Date', y='Active_Cases', hue='State/UnionTerritory')

# Show the plot
plt.show()

ax.set_title("top 5 affected states in India",size=16)
vaccine_df.head()

vaccine_df.rename(columns ={'Updated On' : 'Vaccine Date'}, inplace =True)
vaccine_df.head(10)
vaccine_df.info()
vaccine_df.isnull().sum()

vaccination = vaccine_df.drop(columns = ['Sputnik V (Doses Administered)','AEFI','18-44 Years (Doses Administered)','45-60 Years (Doses Administered)','60+ Years (Doses Administered)'],axis=1)
vaccination.head()

# male vs female vaccination
male =vaccination["Male(Individuals Vaccinated)"].sum()
female =vaccination["Female(Individuals Vaccinated)"].sum()
px.pie(names =["Male" ,'Female'],values =[male,female],title ="male and female vaccination")

# remove rows where state =India
vaccine =vaccine_df[vaccine_df.State!='India']
vaccine

vaccine.rename(columns = {"Total Individuals Vaccinated": "Total"},inplace =True)
vaccine.head()

# most vaccinated state
max_vac = vaccine.groupby('State')['Total'].sum().to_frame("Total")
max_vac =max_vac.sort_values('Total',ascending =False)[:5]
max_vac

fig =plt.figure(figsize =(10,5))
plt.title("top 5 vaccinated states in india", size =20)
x =sns.barplot(data = max_vac.iloc[:10],y = max_vac.Total, x =max_vac.index, linewidth =2,edgecolor ='black')
plt.xlabel("states")
plt.ylabel("vaccination")
plt.show()

# least vaccinated state
min_vac = vaccine.groupby('State')['Total'].sum().to_frame("Total")
min_vac =min_vac.sort_values('Total',ascending =True)[:5]
min_vac

fig =plt.figure(figsize =(20,10))
plt.title("least 5 vaccinated states in india", size =20)
x =sns.barplot(data = min_vac.iloc[:10],y = min_vac.Total, x =min_vac.index, linewidth =2,edgecolor ='red')
plt.xlabel("states",size =20)
plt.ylabel("vaccination",size =20)
plt.show()

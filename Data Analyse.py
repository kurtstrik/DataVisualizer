import pandas as pd
import numpy as np
import requests, sys, csv, unicodedata, matplotlib
import os
from bs4 import BeautifulSoup

r = requests.get('https://www.tuwien.at/tu-wien/ueber-die-tuw/zahlen-und-fakten#c9048')

if (r.status_code == 404):
    sys.exit()

soup = BeautifulSoup(r.content, 'html.parser')

s = soup.find('table', class_='contenttable')

head = s.find_all('th')
row = []
counter = 0
linecontent = []

for x1 in head:
    
    linecontent.append(x1.text)
    if (counter >= 5):
        row.append(linecontent)
        linecontent = []
        counter = 0


    else:
        counter += 1
    
content = s.find_all('td')

rowcontent = []
absolute = []
counter = 0
for x2 in content: 
    inserttext = x2.text

    normalized_str = unicodedata.normalize("NFKD", inserttext)
    rowcontent.append(normalized_str)
    if (counter >= 5):
        row.append(rowcontent)
        rowcontent = []
        counter = 0
        continue
    if (counter == 4):
        absolute.append(int(normalized_str.replace('.',''))) #format 5.349
        counter += 1        
    else:
        counter += 1


with open('data/TU_numbers.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(row)

df = pd.read_csv('data/TU_numbers.csv', sep=',', thousands='.', decimal=',', encoding='latin1')

entries = len(df['Studien gesamt'])
total = df['Studien gesamt'][20]

truepercent = []


for pick in range(entries):
    percentage = str(round( ( (df.loc[pick,'Studien gesamt']) / total )*100, 3) ) + ' %'
    truepercent.append(percentage)

df['Studium in % Anteil'] = truepercent
df.style.set_caption("Stand: 6.1.2024")
edit = df.loc[:, ~df.columns.isin(['Frauen in %', 'Studien in % von Gesamt-TUW'])].sort_values('Studien gesamt',ascending=False)

#edit.to_csv('edited.csv')
#print(edit.to_string(index=False)) #or df.index=[''] * len(df)

edit = edit[1:]#remove first row
#edit = edit[:-1] #remove last row

rest = []
restf = edit.tail(6)['Frauen'].sum()
restm = edit.tail(6)['Männer'].sum()
restall = edit.tail(6)['Studien gesamt'].sum()  
restallp = str(round(  (restall / total) * 100, 3)) + ' %'

rest = pd.DataFrame(columns= ['Studienrichtung','Frauen','Männer','Studien gesamt','Studium in % Anteil'])
rest.loc[0] = ['Sonstige', restf, restm, restall, restallp]

edit = edit[:-6]
edit = pd.concat([edit, rest])

print(edit.to_string(index=False))
females = edit['Frauen']
females = females.iloc[::-1]#reverse the DataFrame for the hbar
males = edit['Männer']
males = males.iloc[::-1]#reverse the DataFrame for the hbar
studies = edit['Studienrichtung']
x_axis = np.arange(len(studies))
studies = studies.iloc[::-1]
shortnames = ['A', 'Inf', 'B', 'E', 'Mas', 'TP', 'WIng', 'TC', 'TM', 'RR', 'WInf', 'V', 'BE', 'VG', 'Sonst']


plot = matplotlib.pyplot
#plot.title('Studierende TU Wien 06.01.2024')
fig, (ax1,ax2) = plot.subplots(2,1)

#fig.set_figwidth(15)
fig.set_size_inches(16,7)
#fig.tight_layout()




#for i,j in zip(males, females):
#ax1.barh(x_axis, [males, females],)
x_axis2 = np.arange(0, len(studies)*2, step=2.0)

ax1.barh(x_axis2 , males, 1.25, color = '#069AF3', label='Männer')
ax1.barh(x_axis2 , females, 1.25, color = '#DC143C', label='Frauen', left=males)

# TODO: set yticks!


ax1.set_yticks(x_axis2, studies)
ax1.set_xlabel("Studenten")
ax1.grid(axis='x',linestyle='--')


#xticks = np.linspace(0, 5500, 12) if finer grid spacing is required
#ax1.set_xticks(xticks)


ax1.legend()





''' VERTICAL BAR CHARTS
ax1.bar(x_axis - 0.2, females, 0.4, color = '#DC143C', label='Frauen')
ax1.bar(x_axis + 0.2, males, 0.4, color = '#069AF3', label='Männer')
ax1.set_xticks(x_axis, shortnames)
ax1.set_ylabel("Studenten")
#ax1.xticks(x_axis, shortnames)
#ax1.ylabel("Studenten")
ax1.grid(axis='y',linestyle='--')
ax1.legend()'''

ax1.set_title('Studierende TU Wien 06.01.2024')
#ax1.title('Studierende TU Wien 06.01.2024')
totals = edit['Studien gesamt'].sort_values()
inc = 0

for total in totals:
    maxgender = max(edit['Frauen'].iloc[inc], edit['Männer'].iloc[inc])

    men = males.iloc[inc]
    women = females.iloc[inc]
   
    ax1.text(men/2, (inc*2)-0.7, men, ha='center', color='black')
    
    wwidth = (women/2) if inc != 0 else women
    ax1.text(wwidth + (men), (inc*2)-0.7, women, ha='center', color='black')    
    ax1.text(total + 150, (inc*2)-0.7, total, ha='center', weight ='bold') # total/2
    inc+=1


values = edit['Studien gesamt']
labels = edit['Studienrichtung']

# https://stackoverflow.com/questions/23577505/how-to-avoid-overlapping-of-labels-autopct-in-a-pie-chart
ratios = 100.*values/ values.sum()

legendtext = ["{0} - {1:1.2f} %".format(i,j) for i,j in zip(labels, ratios)]

inc2 = 0
newtext = []
for tex in legendtext:
    boldtext = '$\\bf{'+shortnames[inc2]+'}$'
    newtext.append(boldtext+' '+tex)
    inc2 += 1

patches, texts = ax2.pie(values, labels=shortnames,labeldistance= 1.2, radius = 1.0) # , autopct='%.3f'
ax2.legend( newtext,loc='right',bbox_to_anchor=(2.25, 0.5),fontsize=8)


# labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, porcent)]

plot.subplots_adjust(left=0.195, right=0.993, top =0.945)
ax2.set_position([-0.1 , 0.04, 0.5, 0.5])
#plot.rcParams.update({'figure.autolayout': True})
plot.show()
#fig.show()

second = soup.find(id="c9020")
head2nd = second.find_all('th')
content2nd = second.find_all('td')

#print(head2nd)
#print(content2nd)
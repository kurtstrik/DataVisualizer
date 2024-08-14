import pandas as pd
import numpy as np
import requests, sys, csv, unicodedata, matplotlib
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
males = edit['Männer']
studies = edit['Studienrichtung']
x_axis = np.arange(len(studies))
shortnames = ['A', 'Inf', 'B', 'E', 'Mas', 'TP', 'WG', 'TC', 'TM', 'RR', 'WInf', 'V', 'BE', 'VG', 'Sonst']


plot = matplotlib.pyplot
#plot.title('Studierende TU Wien 06.01.2024')
fig, (ax1,ax2) = plot.subplots(2,1)

#fig.set_figwidth(15)
fig.set_size_inches(15,7)
fig.tight_layout()


ax1.bar(x_axis - 0.2, females, 0.4, color = '#DC143C', label='Frauen')
ax1.bar(x_axis + 0.2, males, 0.4, color = '#069AF3', label='Männer')
ax1.set_xticks(x_axis, shortnames)
ax1.set_ylabel("Studenten")
#ax1.xticks(x_axis, shortnames)
#ax1.ylabel("Studenten")
ax1.grid(axis='y',linestyle='--')
ax1.legend()

ax1.set_title('Studierende TU Wien 06.01.2024')
#ax1.title('Studierende TU Wien 06.01.2024')
totals = edit['Studien gesamt'].sort_values(ascending=False)
inc = 0

for total in totals:
    maxgender = max(edit['Frauen'].iloc[inc], edit['Männer'].iloc[inc])
    ax1.text(inc, total/2, total, ha='center', weight ='bold', rotation = 20) # total/2
    inc+=1


values = edit['Studien gesamt']
labels = edit['Studienrichtung']

# https://stackoverflow.com/questions/23577505/how-to-avoid-overlapping-of-labels-autopct-in-a-pie-chart
ratios = 100.*values/ values.sum()

legendtext = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, ratios)]
patches, texts = ax2.pie(values, labels=shortnames, radius = 1.2) # , autopct='%.3f'
ax2.legend( legendtext,loc='right',bbox_to_anchor=(3.0, 0.6),fontsize=8)

# labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, porcent)]

plot.subplots_adjust(left=0.05, right=0.96, top =0.945)
plot.show()
#fig.show()

# TODO: legend - shortnames


second = soup.find(id="c9020")
head2nd = second.find_all('th')
content2nd = second.find_all('td')

#print(head2nd)
#print(content2nd)
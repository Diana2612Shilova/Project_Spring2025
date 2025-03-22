import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv('pubs.csv')
print(df.head())
df['subject'] = df['address'].str.split(',').str[-1].str.strip()
grouped = df['subject'].value_counts().reset_index()
grouped.columns = ['subject', 'count']
sns.barplot(x='count', y='subject', data=grouped, palette='viridis')
plt.ylabel('Город/Регион')
plt.xlabel('Количество ресторанов')
plt.title('Количество ресторанов по регионам')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
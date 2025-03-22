import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv('pivy.csv')
solods = df['солод'].str.split(', ').explode()
data_solods = solods.value_counts()
plt.figure(figsize=(10, 5))
sns.barplot(x=data_solods.values, y=data_solods.index)
plt.ylabel('Тип солода')
plt.xlabel('Количество упоминаний')
plt.title('частота солодов')
plt.tight_layout()
plt.show()
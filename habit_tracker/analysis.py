import pandas as pd
import matplotlib.pyplot as plt
from app import db, Habit

# Fetch data from database
habits = Habit.query.all()
data = [{'name': habit.name, 'date': habit.date, 'status': habit.status} for habit in habits]

# Convert to Pandas DataFrame
df = pd.DataFrame(data)

# Habit completion rate
completion_rate = df['status'].mean() * 100

# Plotting
plt.figure(figsize=(6, 4))
df['status'].value_counts().plot(kind='bar', color=['red', 'green'])
plt.title(f'Habit Completion Rate: {completion_rate:.2f}%')
plt.xticks([0, 1], ['Incomplete', 'Complete'])
plt.ylabel('Count')
plt.show()

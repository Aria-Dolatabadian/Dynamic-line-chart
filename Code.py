import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import MonthLocator, DateFormatter

# Read data from CSV
temperature_data = pd.read_csv('temperature_data.csv')

# Convert 'Day' column to datetime format
temperature_data['Day'] = pd.to_datetime(temperature_data['Day'], format='%j')
temperature_data.set_index('Day', inplace=True)

# Create the initial line chart
fig, ax = plt.subplots(figsize=(10, 6))
lines, = ax.plot([], [], label='Region 1')
lines2, = ax.plot([], [], label='Region 2')

# Add vertical lines at the beginning of each month
locator = MonthLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(DateFormatter('%b'))

# Add vertical broken lines to separate months
for month_start in pd.date_range(start=temperature_data.index[0], end=temperature_data.index[-1], freq='MS'):
    ax.axvline(month_start, color='gray', linestyle='--', linewidth=0.8)

# Add labels and title
ax.set_xlabel('Month')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Daily Temperature Changes in Two Regions')
ax.legend()

# Update function for the animation
def update(frame):
    if frame < len(temperature_data):
        lines.set_data(temperature_data.index[:frame], temperature_data['Region1'][:frame])
        lines2.set_data(temperature_data.index[:frame], temperature_data['Region2'][:frame])
        ax.set_xlim(temperature_data.index[0], temperature_data.index[-1])
        ax.set_ylim(
            min(temperature_data[['Region1', 'Region2']].min().min(), 0),  # Adjusted for negative values
            max(temperature_data[['Region1', 'Region2']].max().max(), 0)   # Adjusted for negative values
        )

        day_of_year = temperature_data.index[frame].strftime("%j")
        month_name = temperature_data.index[frame].strftime("%B")

        ax.set_title(f'Daily Temperature Changes - {month_name} {day_of_year} ({frame + 1}/{len(temperature_data)})')

# Create the animation
animation = FuncAnimation(fig, update, frames=len(temperature_data) + 1, interval=50, repeat=False)

# Save the dynamic line chart as a GIF
animation.save('Temperature_Changes_Animation.gif', writer='imagemagick')

# Display the dynamic line chart
plt.show()

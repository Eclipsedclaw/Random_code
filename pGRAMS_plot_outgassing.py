import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
from scipy.optimize import curve_fit

# 1. Setup actual timestamps
dates = [
    datetime(2026, 3, 6, 13, 53),
    datetime(2026, 3, 9, 8, 50),
    datetime(2026, 3, 10, 8, 20),
    datetime(2026, 3, 12, 11, 40),
    datetime(2026, 3, 12, 16, 19),
    datetime(2026, 3, 16, 9, 39),
    datetime(2026, 3, 17, 8, 41),
    datetime(2026, 3, 18, 10, 28),
    datetime(2026, 3, 19, 16, 7)
]

# 2. Data
outgassing_rate = np.array([8.723, 0.78, 0.6186, 0.5280, 0.5492, 0.3722, 0.41263, 0.33997, 0.34551])
starting_pressure = np.array([2.487e-5, 3.368e-6, 2.93e-6, 2.53e-6, 2.67e-6, 2.12e-6, 2.08e-6, 2.08e-6, 2.10e-6])

# --- Strict Fitting Logic ---
t_days = np.array([(d - dates[0]).total_seconds() / 86400 for d in dates])

# Using a three-parameter power law for a stricter fit to early decay
def power_law_strict(t, a, b, t0):
    return a * np.power(t + t0, b)

# Fit the model (p0 is the initial guess)
popt, _ = curve_fit(power_law_strict, t_days, outgassing_rate, p0=[1, -1, 0.1])

# Extend x-axis to 2 weeks beyond the last data point
end_date = dates[-1] + timedelta(days=14)
total_days_range = (end_date - dates[0]).total_seconds() / 86400

t_smooth = np.linspace(0, total_days_range, 500)
y_smooth = power_law_strict(t_smooth, *popt)
dates_smooth = [dates[0] + timedelta(days=s) for s in t_smooth]

# 3. Create the Plot
fig, ax1 = plt.subplots(figsize=(10, 7))

# --- Outgassing (Primary) ---
color1 = 'black'
ax1.plot(dates_smooth, y_smooth, color='gray', linestyle='--', alpha=0.8, 
         label=f'Power Law Fit ($b={popt[1]:.2f}$)')
ax1.plot(dates, outgassing_rate, marker='o', color=color1, linewidth=0, markersize=8)

ax1.set_yscale('log')

# Labeling outgassing values
for i, val in enumerate(outgassing_rate):
    ax1.annotate(f'{val:.2f}', (dates[i], outgassing_rate[i]), textcoords="offset points", 
                 xytext=(0, 10), ha='center', fontsize=10, fontweight='bold')

ax1.set_xlabel('Date (2026)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Outgassing Rate (pascal/h)', fontsize=12, fontweight='bold', color=color1)

# --- Pressure (Secondary) ---
ax2 = ax1.twinx()
color2 = 'red'
ax2.scatter(dates, starting_pressure, marker='s', color=color2, s=80, label='Starting Pressure')
ax2.set_ylabel('Starting Pressure (torr)', fontsize=12, fontweight='bold', color=color2)
ax2.set_yscale('log')

# Labeling starting pressure values
#for i, val in enumerate(starting_pressure):
#    ax2.annotate(f'{val:.2e}', (dates[i], starting_pressure[i]), textcoords="offset points", 
#                 xytext=(40, 0), ha='center', fontsize=10, fontweight='bold', color=color2)

# --- Formatting ---
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.set_xlim(dates[0] - timedelta(hours=12), end_date) # Extended X-axis
today = datetime.now()
ax1.axvline(today, color='blue', linestyle='--', linewidth=1.5, label='Right now')
plt.title('Outgassing Projection: Current Data + 2 Week Forecast', fontsize=14, fontweight='bold')

ax1.grid(True, alpha=0.3, linestyle='--')
ax1.minorticks_on()
ax1.grid(True, which='minor', alpha=0.1, linestyle=':')

# Combine Legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.tight_layout()
plt.savefig('Outgassing_2Week_Projection.png', dpi=300)
plt.show()
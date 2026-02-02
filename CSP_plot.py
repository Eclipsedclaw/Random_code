import matplotlib.pyplot as plt
import numpy as np

# Data from the tables
data = {
    "50 pF, Jan 28th": {
        "shaping_time": [0.5, 1, 2, 3, 6, 10],
        "FWHM": [44.62, 35.11, 24.18, 19.29, 12.95, 15.97]
    },
    "50 pF, Feb 2nd": {
        "shaping_time": [0.5, 1, 2, 3, 6, 10],
        "FWHM": [43.96, 31.23, 27.65, 16.33, 15.11, 6.53]
    #},
    #"Jon CSP v7.1": {
    #    "shaping_time": [0.5, 1, 2, 3, 6, 10],
    #    "FWHM": [30.32, 24.51, 15.53, 20.36, 9.86, 9.62]
    }
}

# Create the plot
plt.figure(figsize=(10, 7))

# Colors for each curve
colors = ['blue', 'green', 'red', 'purple']
markers = ['o', 's', '^', 'D']

# Plot each dataset
for i, (label, dataset) in enumerate(data.items()):
    x = dataset["shaping_time"]
    y = dataset["FWHM"]
    
    # Calculate error bars based on 8000 events statistics
    # Statistical uncertainty on FWHM: FWHM / sqrt(N)
    errors = [fwhm / np.sqrt(8000) for fwhm in y]
    
    plt.errorbar(x, y, 
                 yerr=errors,
                 marker=markers[i], 
                 color=colors[i], 
                 linewidth=2, 
                 markersize=8,
                 capsize=5,
                 capthick=2,
                 label=label)

# Add goal line
plt.axhline(y=5, color='red', linestyle='--', linewidth=2, label='Goal (5 keV)')
plt.text(0.2, 5.5, 'Goal (5 keV)', fontsize=10, color='red', fontweight='bold')

# Customize the plot
plt.xlabel('Shaping Time (μs)', fontsize=12, fontweight='bold')
plt.ylabel('FWHM (keV)', fontsize=12, fontweight='bold')
plt.title('FWHM vs Shaping Time for Different Capacitances', fontsize=14, fontweight='bold')
plt.legend(title='Capacitance', fontsize=10, title_fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')

# Set x-axis to show all shaping times
plt.xticks([0.5, 1, 2, 3, 6, 10])
plt.xlim(0, 11)

# Make y-axis start from 0 for better visualization
plt.ylim(0, max([max(d["FWHM"]) for d in data.values()]) * 1.1)

# Add minor grid for better readability
plt.minorticks_on()
plt.grid(True, which='minor', alpha=0.2, linestyle=':')

plt.tight_layout()
plt.show()

# Optional: Save the figure
plt.savefig('FWHM_vs_ShapingTime.png', dpi=300, bbox_inches='tight')
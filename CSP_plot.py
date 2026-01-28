import matplotlib.pyplot as plt
import numpy as np

# Data from the tables
data = {
    "0 pF": {
        "shaping_time": [0.5, 1, 2, 3, 6, 10],
        "FWHM": [20.33, 14.31, 12.39, 10.82, 11.39, 7.25]
    },
    "15 pF": {
        "shaping_time": [0.5, 1, 2, 3, 6, 10],
        "FWHM": [25.42, 18.36, 13.92, 14.8, 15.19, 12.51]
    },
    "30 pF": {
        "shaping_time": [0.5, 1, 2, 3, 6, 10],
        "FWHM": [31.76, 23.56, 19.76, 13.93, 14.60, 7.16]
    },
    "50 pF": {
        "shaping_time": [0.5, 1, 2, 3, 6, 10],
        "FWHM": [44.62, 35.11, 24.18, 19.29, 12.95, 15.97]
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
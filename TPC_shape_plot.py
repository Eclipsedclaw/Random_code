import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# --- 1. Global Font Size Setting ---
# This scales almost all text elements automatically
plt.rcParams.update({'font.size': 14}) 

# Data
TPC_900 = np.array([6507, 6891, 7212, 7771, 8099, 8605, 8708, 8591, 8176, 6788, 4570, 2050])/1e7
TPC_1100 = np.array([8930, 9060, 9559, 10110, 10645, 11325, 11611, 12217, 12767, 12267, 11145, 9407])/1e7
TPC_1300 = np.array([11045, 11481, 11556, 12223, 13019, 13560, 14384, 15204, 16053, 17069, 16719, 15667, 1137])/1e7
TPC_1500 = np.array([13091, 13380, 13384, 13941, 14833, 15385, 16548, 17403, 19208, 20523, 21120, 20807, 9412])/1e7

# --- 1. Define Master X-Axis Values ---
x_values_master = np.array([50, 60, 70, 80, 90, 100, 110, 120, 140, 160, 180, 200, 300, 600])

# Function for smooth line
def plot_smooth(data, label, marker, color):
    # --- 2. Slice to Match Data Length ---
    x = x_values_master[:len(data)]
    
    # Dot plot - slightly increased marker size (s) to match text
    plt.scatter(x, data, marker=marker, label=label, color=color, s=60)
    
    # Smooth line
    X_Y_Spline = make_interp_spline(x, data)
    X_ = np.linspace(x.min(), x.max(), 500)
    Y_ = X_Y_Spline(X_)
    plt.plot(X_, Y_, color=color, linestyle='--', alpha=0.5)

# Creating the plot
# --- 2. Increased Figure Size ---
# Larger font often looks better with a larger canvas
plt.figure(figsize=(14, 9)) 

# Plotting the data sets with smooth lines
plot_smooth(TPC_900, 'detector 900kg', 'o', 'blue')
plot_smooth(TPC_1100, 'detector 1100kg', 's', 'orange')
plot_smooth(TPC_1300, 'detector 1300kg', '^', 'green')
plot_smooth(TPC_1500, 'detector 1500kg', 'x', 'red')

# Adding labels and title (fontsize here overrides global if needed)
plt.title('LArTPC capture efficiency vs TPC shape (1 million events generated)', fontsize=20)
plt.xlabel('TPC length [cm]', fontsize=16) 
plt.ylabel('Capture efficiency', fontsize=16)

# Adding grid and legend
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()

# Save the plot
plt.savefig('LArTPC_shape.png')
print("Plot saved as LArTPC_shape.png")
import numpy as np
import matplotlib.pyplot as plt

# US Standard Atmosphere 1976 parameters for layers up to 40 km
# h_base (m), T_base (K), L (K/m), P_base (Pa)
# We can compute P_base sequentially
g = 9.80665
M = 0.0289644
R = 8.31432  # US Standard Atmosphere constant

layers = [
    {"h0": 0, "h1": 11000, "T0": 288.15, "L": -0.0065},
    {"h0": 11000, "h1": 20000, "T0": 216.65, "L": 0.0},
    {"h0": 20000, "h1": 32000, "T0": 216.65, "L": 0.0010},
    {"h0": 32000, "h1": 47000, "T0": 228.65, "L": 0.0028}
]

P0 = 101325.0 # Pa (760 torr)
current_P = P0

for i in range(len(layers)):
    layers[i]["P0"] = current_P
    h0 = layers[i]["h0"]
    h1 = layers[i]["h1"]
    T0 = layers[i]["T0"]
    L = layers[i]["L"]
    
    if L != 0:
        P1 = current_P * (1 + L * (h1 - h0) / T0) ** (-g * M / (R * L))
    else:
        P1 = current_P * np.exp(-g * M * (h1 - h0) / (R * T0))
    current_P = P1

def get_pressure(h):
    # h in meters, returns P in torr
    # 1 Pa = 760 / 101325 torr
    P_pa = 0
    for layer in layers:
        if layer["h0"] <= h <= layer["h1"]:
            h0 = layer["h0"]
            T0 = layer["T0"]
            L = layer["L"]
            P0_layer = layer["P0"]
            if L != 0:
                P_pa = P0_layer * (1 + L * (h - h0) / T0) ** (-g * M / (R * L))
            else:
                P_pa = P0_layer * np.exp(-g * M * (h - h0) / (R * T0))
            break
    return P_pa * 760.0 / 101325.0

heights = np.linspace(0, 40000, 400) # up to 40 km
pressures = [get_pressure(h) for h in heights]

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(heights / 1000.0, pressures, 'b-', lw=2.5, label='Atmospheric Pressure')
ax.set_xlabel('Height / Altitude (km)', fontsize=12)
ax.set_ylabel('Pressure (torr)', fontsize=12)
ax.set_title('Atmospheric Pressure vs. Altitude (0 - 40 km)', fontsize=14, pad=15)
ax.set_xlim(0, 40)
ax.set_ylim(0, 800)
ax.grid(True, linestyle='--', alpha=0.5)

# 10000 feet release height
P_10000 = get_pressure(3048)
ax.plot(3.048, P_10000, 'ro')
ax.text(5, P_10000, '10,000 feet (3.048 km)', fontsize=10, color='darkred')

# 35km operation altitude
P_35000 = get_pressure(35000)
ax.plot(35.0, P_35000, 'go')
ax.text(36.0, P_35000 + 20, '35 km Operation', fontsize=10, color='darkgreen')

# Add some landmark annotations
# Mt Everest ~8.8 km
#P_everest = get_pressure(8848)
#ax.plot(8.848, P_everest, 'ro')
#ax.text(9.5, P_everest, 'Mt. Everest (8.8 km)', fontsize=10, color='darkred')

# Armstrong limit ~19 km
#P_armstrong = get_pressure(19000)
#ax.plot(19.0, P_armstrong, 'go')
#ax.text(20.0, P_armstrong + 20,`` 'Armstrong Limit (19 km)', fontsize=10, color='darkgreen')

plt.tight_layout()
plt.savefig('pressure_vs_altitude.png', dpi=300)
print("Plot successfully saved.")
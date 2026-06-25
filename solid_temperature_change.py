import numpy as np
import matplotlib.pyplot as plt

# import or copy these from your existing scripts
from pressure_altitude_plot import get_pressure
from argon_phase_study import T_tp, P_tp, B_sub

def argon_sublimation_temp(P_torr):
    P_torr = np.asarray(P_torr, dtype=float)
    T = np.full_like(P_torr, np.nan, dtype=float)

    # Sublimation line is physically valid only at or below the triple-point pressure
    mask = (P_torr > 0) & (P_torr <= P_tp)
    T[mask] = 1.0 / (1.0 / T_tp - np.log(P_torr[mask] / P_tp) / B_sub)
    return T

# altitude grid
heights_m = np.linspace(0, 40000, 400)
pressures_torr = np.array([get_pressure(h) for h in heights_m])

# convert pressure -> argon sublimation temperature
argon_T = argon_sublimation_temp(pressures_torr)

# plot temperature vs altitude
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(heights_m / 1000.0, argon_T, 'r-', lw=2.5)
ax.set_xlabel('Altitude (km)')
ax.set_ylabel('Argon sublimation temperature (K)')
ax.set_title('Argon Solid-Line Temperature vs Altitude')
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('temperature_vs_altitude.png', dpi=300)
plt.show()
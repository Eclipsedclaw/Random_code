import numpy as np
import matplotlib.pyplot as plt

from pressure_altitude_plot import get_pressure
from argon_phase_study import T_tp, P_tp, B_sub

def argon_sublimation_temp(P_torr):
    P_torr = np.asarray(P_torr, dtype=float)
    T = np.full_like(P_torr, np.nan, dtype=float)
    mask = (P_torr > 0) & (P_torr <= P_tp)
    T[mask] = 1.0 / (1.0 / T_tp - np.log(P_torr[mask] / P_tp) / B_sub)
    return T

heights_m = np.linspace(0, 40000, 400)
pressures_torr = np.array([get_pressure(h) for h in heights_m])

sub_mask = pressures_torr <= P_tp
melt_mask = pressures_torr > P_tp

argon_sub_T = argon_sublimation_temp(pressures_torr)
argon_melt_T = np.full_like(pressures_torr, T_tp, dtype=float)

fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(heights_m[sub_mask] / 1000.0, argon_sub_T[sub_mask],
        'r-', lw=2.5, label='Solid-Gas Boundary')
ax.plot(heights_m[melt_mask] / 1000.0, argon_melt_T[melt_mask],
        'g-', lw=2.5, label='Solid-Liquid Boundary')

ax.axhline(T_tp, color='gray', ls='--', lw=1, alpha=0.6)
ax.set_xlabel('Altitude (km)')
ax.set_ylabel('Argon boundary temperature (K)')
ax.set_title('Argon Solid Boundaries vs Altitude')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend()

plt.tight_layout()
plt.savefig('argon_boundaries_vs_altitude.png', dpi=300)
plt.show()
import numpy as np
import matplotlib.pyplot as plt

# Reference constants for Argon
T_tp = 83.806   # Triple point temperature (K)
P_tp = 516.8    # Triple point pressure (torr)
T_bp = 87.302   # Normal boiling point temperature (K)
P_bp = 760.0    # Normal boiling point pressure (torr)

# 1. Sublimation Line (Solid - Gas)
B_sub = np.log(P_tp / 0.2) / (1/60.0 - 1/T_tp)
T_sub = np.linspace(60, T_tp, 200)
P_sub = P_tp * np.exp(-B_sub * (1/T_sub - 1/T_tp))

# 2. Vaporization Line (Liquid - Gas) extended up to 1500 torr
B_vap = np.log(P_bp / P_tp) / (1/T_tp - 1/T_bp)
T_at_1500 = 1 / (1/T_tp - np.log(1500.0 / P_tp) / B_vap)
T_vap = np.linspace(T_tp, T_at_1500, 200)
P_vap = P_tp * np.exp(-B_vap * (1/T_vap - 1/T_tp))

# 3. Melting Line (Solid - Liquid) extended up to 1500 torr
P_melt = np.linspace(P_tp, 1500, 100)
T_melt = np.full_like(P_melt, T_tp)

# Plotting with T from 60 to 100 K to un-squish the diagram
fig, ax = plt.subplots(figsize=(9, 6))

ax.plot(T_sub, P_sub, 'r-', lw=2.5, label='Sublimation Line (Solid - Gas)')
ax.plot(T_vap, P_vap, 'b-', lw=2.5, label='Vaporization Line (Liquid - Gas)')
ax.plot(T_melt, P_melt, 'g-', lw=2.5, label='Melting Line (Solid - Liquid)')

# Mark key points
ax.plot(T_tp, P_tp, 'ko', markersize=8, label=f'Triple Point ({T_tp:.2f} K, {P_tp:.1f} torr)')
ax.plot(T_bp, P_bp, 'mo', markersize=8, label=f'Normal Boiling Point ({T_bp:.2f} K, {P_bp:.1f} torr)')

# Phase labels
ax.text(75, 800, 'SOLID', fontsize=14, fontweight='bold', color='darkred', ha='center')
ax.text(85, 1100, 'LIQUID', fontsize=14, fontweight='bold', color='darkgreen', ha='center')
ax.text(95, 200, 'GAS / VAPOR', fontsize=14, fontweight='bold', color='darkblue', ha='center')

# Formatting
ax.set_title('Argon Phase Diagram Zoomed (60 - 100 K, 0 - 1500 torr)', fontsize=14, pad=15)
ax.set_xlabel('Temperature (K)', fontsize=12)
ax.set_ylabel('Pressure (torr)', fontsize=12)
ax.set_xlim(60, 100)
ax.set_ylim(0, 1500)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig('argon_phase_diagram.png', dpi=300)
print("Saved zoomed plot (60-100 K).")
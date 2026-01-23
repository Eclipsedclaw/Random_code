import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patheffects as pe
from cartopy.feature import NaturalEarthFeature
import aacgmv2
from datetime import datetime, timezone

# =========================
# load SIP data
# =========================
filename = "sip_position.txt"

res = []
with open(filename, "r") as f:
    for line in f:
        row = [float(x) for x in line.strip().split()]
        res.append(row)

res = np.array(res)

times = res[:, 0]   # UNIX time [s], UTC
alts  = res[:, 1]
lats  = res[:, 2]
lons  = res[:, 3]

# =========================
# UTC datetime
# =========================
times_utc = pd.to_datetime(times, unit="s", utc=True)

# =========================
# UTC date
# =========================
dates = times_utc.date
date_change_idx = np.where(dates[1:] != dates[:-1])[0] + 1
date_labels = times_utc[date_change_idx].strftime("%m/%d")

# =========================
# num circ
# ========================
base_time = times.min()
week_sec  = 12 * 24 * 3600 - 5 * 3600

mask_week1 = times < base_time + week_sec
mask_week2 = times >= base_time + week_sec
mask_last  = times >= base_time + 24 * 24 * 3600

# def lon_diff(lon, lon0):
#     """
#     lon, lon0 : degrees (-180 .. 180)
#     return    : signed difference in (-180 .. 180)
#     """
#     return ((lon - lon0 + 180) % 360) - 180


# mask_mcm = (
#     (lats > mcm_lat - dlat) & (lats < mcm_lat + dlat) &
#     (np.abs(lon_diff(lons, mcm_lon)) < dlon)
# )

plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.SouthPolarStereo())

ax.set_extent([-180, 180, -90, -60], ccrs.PlateCarree())
# # =========================
# # around MCM
# # =========================
# mcm_lat = -77.8419
# mcm_lon = 166.6863

# dlat = 2.0
# dlon = 15.0

# ax.set_extent(
#     # [mcm_lon - 3, mcm_lon + 15,
#     #  mcm_lat - 3, mcm_lat + 3],
#     [mcm_lon - 8, mcm_lon + dlon,
#      mcm_lat - dlat, mcm_lat + dlat],
#     crs=ccrs.PlateCarree()
# )

# mask_extent = (
#     (lons >= lon_min) & (lons <= lon_max) &
#     (lats >= lat_min) & (lats <= lat_max)
# )

# map
ax.add_feature(cfeature.OCEAN, facecolor="lightblue", zorder=0) #

ice = NaturalEarthFeature(
    category="physical",
    name="antarctic_ice_shelves_polys",
    scale="10m",
    facecolor="white", # whitesmoke
    edgecolor="gray"
)
ax.add_feature(ice, zorder=1)

ax.add_feature(cfeature.LAND, facecolor="white", zorder=2)
ax.add_feature(cfeature.COASTLINE, edgecolor="grey", zorder=3) #

gl = ax.gridlines(
    crs=ccrs.PlateCarree(),
    draw_labels=True,
    linewidth=0.5,
    color='gray',
    alpha=0.5,
    linestyle='--'
)
gl.xlocator = plt.FixedLocator(np.arange(-180, 181, 30))
gl.ylocator = plt.FixedLocator(np.arange(-90, -59, 5))
gl.xlabel_style = {'size': 8}
gl.ylabel_style = {'size': 8}

# SIP trajectory
ax.scatter(
    lons[mask_week1],
    lats[mask_week1],
    s=1,
    color="blue",
    transform=ccrs.PlateCarree(),
    label="circulation 1",
    zorder=4
)

ax.scatter(
    lons[mask_week2],
    lats[mask_week2],
    s=1,
    color="red",
    transform=ccrs.PlateCarree(),
    label="circulation 2",
    zorder=4
)


# =========================
# point per * hpur（UTC）
# =========================
# df = pd.DataFrame({
#     "time": times_utc,
#     "lat": lats,
#     "lon": lons
# })

# df = df[mask_mcm&mask_last].copy()
# df["hour"] = df["time"].dt.floor("1h")
# df_hourly = df.groupby("hour").first().reset_index()

# ax.scatter(
#     df_hourly["lon"],
#     df_hourly["lat"],
#     s=5,
#     color="grey",
#     transform=ccrs.PlateCarree(),
#     label="UTC hourly",
#     zorder=5
# )

# for i, (_, row) in enumerate(df_hourly.iterrows()):
#     if i % 2 == 0:
#         continue

#     ax.text(
#         row["lon"],
#         row["lat"] + 0.3,
#         row["hour"].strftime("%H"),
#         fontsize=6,
#         ha="center",
#         va="bottom",
#         transform=ccrs.PlateCarree(),
#         path_effects=[pe.withStroke(linewidth=2, foreground="white")],
#         zorder=6
#     )


# UTC date change
ax.scatter(
    lons[date_change_idx],
    lats[date_change_idx],
    s=10,
    color="black",
    transform=ccrs.PlateCarree(),
    label="UTC Date Change",
    zorder=5
)

lat_offset = 0.3
for lon, lat, label in zip(lons[date_change_idx], lats[date_change_idx], date_labels):
    ax.text(
        lon,
        lat + lat_offset,
        label,
        fontsize=7,
        transform=ccrs.PlateCarree(),
        ha="center",
        va="bottom",
        path_effects=[pe.withStroke(linewidth=2, foreground="white")],
        zorder=6
    )




# =========================
# 2025 magnetic south pole
# =========================
magnetic_pole_lat = -63.812
magnetic_pole_lon = 134.920

ax.scatter(
    magnetic_pole_lon,
    magnetic_pole_lat,
    color="magenta",
    s=60,
    marker="*",
    transform=ccrs.PlateCarree(),
    # label="Magnetic South Pole",
    zorder=7
)

# =========================
# landing point
# =========================
def dms_to_deg(d, m, s, hemi):
    """
    d : degrees (int)
    m : minutes (int)
    s : seconds (float)
    hemi : 'N','S','E','W'
    """
    deg = d + m / 60.0 + s / 3600.0
    if hemi in ["S", "W"]:
        deg *= -1
    return deg


landing_lat = dms_to_deg(78, 28, 49.0, "S")
landing_lon = dms_to_deg(169, 52, 71.0, "E")

ax.scatter(
    landing_lon,
    landing_lat,
    s=10,
    color="green",
    transform=ccrs.PlateCarree(),
    label="Landing point",
    zorder=8
)



# =========================
# cutoff rigidity
# =========================
lon_grid = np.linspace(-180, 180, 361)
lat_grid = np.linspace(-90, -50, 281)
LON, LAT = np.meshgrid(lon_grid, lat_grid)

ALT = 0.0  # 地表
contour_time = datetime(2025, 12, 31, tzinfo=timezone.utc)

lambda_mag = np.zeros(LAT.shape)

for i in range(LAT.shape[0]):
    for j in range(LAT.shape[1]):
        mlat, mlon, _ = aacgmv2.get_aacgm_coord(
            LAT[i, j],
            LON[i, j],
            ALT / 1000.0,
            contour_time,
            method="ALLOWTRACE"
        )
        lambda_mag[i, j] = mlat

Rc = 14.9 * np.cos(np.deg2rad(lambda_mag))**4  # [GV]

levels = [0.2, 0.5, 1.0, 2.0]

cs = ax.contour(
    LON,
    LAT,
    Rc,
    levels=levels,
    colors="black",
    linewidths=0.6,
    transform=ccrs.PlateCarree(),
    zorder=3.5
)

ax.clabel(cs, fmt="%.1f GV", fontsize=7)

# =========================
# show
# =========================
# plt.title("Payload Position with Geomagnetic Cutoff Rigidity (2025-12-31)")
plt.legend(loc="lower left")
# plt.tight_layout()
plt.show()






# # =========================
# # cutoff rigidity by Kozai tool
# # =========================
# cutoff_file = Path("/home/kaoyama/GAPS/analysis/Flight2026/trajectory/CutOff/data/cutoff_rigidity.dat")

# data = np.loadtxt(cutoff_file, skiprows=1)
# lats = data[:, 0]
# lons = data[:, 1]
# cutoff = data[:, 4]

# fig = plt.figure(figsize=(8, 8))
# ax = plt.axes(projection=ccrs.SouthPolarStereo())
# ax.set_extent([-180, 180, -90, -50], crs=ccrs.PlateCarree())

# ax.add_feature(cfeature.LAND, facecolor="lightgray")
# ax.add_feature(cfeature.OCEAN, facecolor="white")
# ax.gridlines(draw_labels=True)

# sc = ax.scatter(
#     lons, lats,
#     c=cutoff,
#     cmap="viridis",
#     s=80,
#     # edgecolors="k",
#     transform=ccrs.PlateCarree(),
#     norm=LogNorm(vmin=0.01, vmax=3.)  # log scale
# )

# cbar = plt.colorbar(sc, ax=ax, orientation="vertical", shrink=0.7)
# cbar.set_label("Cutoff Rigidity [GV]")


# # plt.title("Payload Position with Geomagnetic Cutoff Rigidity (2025-12-31)")
# plt.tight_layout()
# plt.show()=

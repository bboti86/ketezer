import folium
from folium.plugins import HeatMap

# Magyarország középpontja és az alapértelmezett nagyítási szint
magyarorszag_terkep = folium.Map(location=[47.1625, 19.5033], zoom_start=7, tiles='CartoDB positron')

# Városok koordinátái (Szélesség, Hosszúság) és a támogatások száma (Súly)
varosok_adatai = [
    [47.4979, 19.0402, 41], # Budapest
    [47.5316, 21.6273, 11], # Debrecen
    [47.6875, 17.6504, 9],  # Győr
    [48.1035, 20.7784, 8],  # Miskolc
    [46.9062, 19.6913, 6],  # Kecskemét
    [47.5800, 18.3965, 6],  # Tatabánya
    [47.1899, 18.4103, 6],  # Székesfehérvár
    [47.9554, 21.7167, 5],  # Nyíregyháza
    [46.0727, 18.2323, 5],  # Pécs
    [47.1818, 20.1837, 4],  # Szolnok
    [47.0929, 17.9138, 4],  # Veszprém
    [47.9025, 20.3731, 4],  # Eger
    [47.7472, 18.1189, 4],  # Komárom
    [46.8400, 16.8439, 3],  # Zalaegerszeg
    [47.5000, 19.9167, 3]   # Jászberény
]

# Hőtérkép réteg hozzáadása a térképhez
HeatMap(
    varosok_adatai,
    radius=25,
    blur=15,
    max_zoom=10,
    gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 1.0: 'red'}
).add_to(magyarorszag_terkep)

# Térkép elmentése HTML fájlként
kimeneti_fajl = 'tamogatasok_hoterkep.html'
magyarorszag_terkep.save(kimeneti_fajl)
print(f"✅ A hőtérkép sikeresen elkészült: {kimeneti_fajl}. Nyisd meg egy böngészőben!")

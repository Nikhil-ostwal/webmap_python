#Importing modules
import folium
import pandas as pd

#Importing data
data = pd.read_csv("Volcanoes.csv")

lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

#Base Layer
map = folium.Map(location=[38.4, -99.43], zoom_start= 6, tiles="Stamen Terrain")
fgv= folium.FeatureGroup(name="Volcanoes")

def color_selector(elev):
    if elev > 0 and elev < 2000 : return "green"
    elif elev >= 2000 and elev < 4000 : return "orange"
    else: return "red"

#Marker Layer
for lt,ln,elv,nme in zip(lat,lon,elev,name):
    iframe = folium.IFrame(html=html % (nme, nme, elv), width=200, height=100)
    #fgv.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = color_selector(elv))))
    
    #For circle markers
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe), fill_color = color_selector(elv), radius=10, color= color_selector(elv), fill=True ))
    

fgp= folium.FeatureGroup(name="Population")

#To diplay a Polygraph OR Ploygon Layer
fgp.add_child(folium.GeoJson(data=(open("world.json","r",encoding='utf-8-sig').read()),
 style_function=lambda x : {'fillColor': 'green' if x['properties']['POP2005'] < 1000000 else 'orange' 
 if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'} ))

#Adding features to the map
map.add_child(fgv)
map.add_child(fgp)

#Layer control
map.add_child(folium.LayerControl())

#Saving the map
map.save("Map.html")
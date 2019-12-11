import xml.etree.ElementTree as ET
import sqlite3
from io import StringIO


MIN_LAT = 22.407008333
MAX_LAT = 22.628430556
MIN_LON = 113.72729722
MAX_LON = 113.957263889


print("Criterion: {0} {1} {2} {3}".format(MIN_LAT,MAX_LAT, MIN_LON, MAX_LON))
print("Querying database...")

conn = sqlite3.connect("20191205.sqlite")
cursor = conn.cursor()
cursor.execute("""
-- in 3
select distinct(mmsi)
from dachan20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00'
and latitude between  {0} and {1}
and longitude between {2} and {3}
and mmsi in
(
select distinct(mmsi)
from local20191205
where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00'
and latitude between  {0} and {1}
and longitude between {2} and {3}
)
and mmsi IN
(
select distinct(mmsi)
from aisdata
where lat/1000000.0 between  {0} and {1}
and lon/1000000.0 between {2} and {3}
and utc between 1575508860 and 1575509700
)
""".format(MIN_LAT,MAX_LAT, MIN_LON, MAX_LON))
rows = cursor.fetchall()
print("Boats in criterion: {0}".format(len(rows)))

mmsis = list(map(lambda x:x[0], rows))



print("Generating kml...")

root = ET.Element('kml')
doc = ET.SubElement(root, 'Document')
doc_name = ET.SubElement(doc, 'name')
doc_name.text = 'AIS'
style = ET.SubElement(doc, 'Style', {'id': 'yellowLineGreenPoly'})
line_style = ET.SubElement(style, 'LineStyle')
line_color = ET.SubElement(line_style, 'color')
line_color.text = 'ffd347ff'
line_width = ET.SubElement(line_style, 'width')
line_width.text = '4'

poly_style = ET.SubElement(style, 'PolyStyle')
poly_color = ET.SubElement(poly_style, 'color')
poly_color.text = 'ffd34700'

style = ET.SubElement(doc, 'Style', {'id': 'orangeLine'})
line_style = ET.SubElement(style, 'LineStyle')
line_color = ET.SubElement(line_style, 'color')
line_color.text = 'ff26b5fe'
line_width = ET.SubElement(line_style, 'width')
line_width.text = '2'

poly_style = ET.SubElement(style, 'PolyStyle')
poly_color = ET.SubElement(poly_style, 'color')
poly_color.text = '7f00ff00'


style = ET.SubElement(doc, 'Style', {'id': 'redLine'})
line_style = ET.SubElement(style, 'LineStyle')
line_color = ET.SubElement(line_style, 'color')
line_color.text = 'ff263dfe'
line_width = ET.SubElement(line_style, 'width')
line_width.text = '2'

poly_style = ET.SubElement(style, 'PolyStyle')
poly_color = ET.SubElement(poly_style, 'color')
poly_color.text = '7f00ff00'


style = ET.SubElement(doc, 'Style', {'id': 'greenLine'})
line_style = ET.SubElement(style, 'LineStyle')
line_color = ET.SubElement(line_style, 'color')
line_color.text = 'ff07b900'
line_width = ET.SubElement(line_style, 'width')
line_width.text = '2'

poly_style = ET.SubElement(style, 'PolyStyle')
poly_color = ET.SubElement(poly_style, 'color')
poly_color.text = '7f00ff00'



print("Drawing criterion square...")

place_mark = ET.SubElement(doc, 'Placemark')
place_mark_name = ET.SubElement(place_mark, 'name')
place_mark_name.text = 'Criterion'
ET.SubElement(place_mark, 'styleUrl').text = '#yellowLineGreenPoly'

line_string = ET.SubElement(place_mark, 'LineString')
ET.SubElement(line_string, 'tessellate').text = '1'
coordinates = ET.SubElement(line_string, 'coordinates')
coordinates.text = "{0},{1},1\n{0},{2},1\n{3},{2},1\n{3},{1},1\n{0},{1},1".format(MIN_LON,MIN_LAT,MAX_LAT,MAX_LON)



print("Drawing lanes...")

folder = ET.SubElement(doc, 'Folder')
folder_name = ET.SubElement(folder, 'name')
folder_name.text = '临时基站'
folder_open = ET.SubElement(folder, 'open')
folder_open.text = '1'

for mmsi in mmsis:
    cursor.execute("""
        select timestamp, mmsi, latitude, longitude
        from dachan20191205
        where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00'
        and latitude between  {0} and {1}
          and longitude between {2} and {3}
        --and mmsi = ?
        order by timestamp
        """.format(MIN_LAT, MAX_LAT, MIN_LON, MAX_LON), [])
    
    rows = cursor.fetchall()

    place_mark = ET.SubElement(folder, 'Placemark')
    place_mark_name = ET.SubElement(place_mark, 'name')
    place_mark_name.text = mmsi
    ET.SubElement(place_mark, 'styleUrl').text = '#orangeLine'

    line_string = ET.SubElement(place_mark, 'LineString')
    ET.SubElement(line_string, 'tessellate').text = '1'
    coordinates = ET.SubElement(line_string, 'coordinates')
    coordinates_str = StringIO()
    for row in rows:
        coordinates_str.write("{0},{1},0\n".format(row[3],row[2]))
    coordinates.text = coordinates_str.getvalue()



folder = ET.SubElement(doc, 'Folder')
folder_name = ET.SubElement(folder, 'name')
folder_name.text = '山顶基站'
folder_open = ET.SubElement(folder, 'open')
folder_open.text = '1'

for mmsi in mmsis:
    cursor.execute("""
        select timestamp, mmsi, latitude, longitude
        from local20191205
        where timestamp between '2019-12-05 01:21:00' and '2019-12-05 01:35:00'
        and latitude between  {0} and {1}
          and longitude between {2} and {3}
        --and mmsi = ?
        order by timestamp
        """.format(MIN_LAT, MAX_LAT, MIN_LON, MAX_LON), [])
    
    rows = cursor.fetchall()

    place_mark = ET.SubElement(folder, 'Placemark')
    place_mark_name = ET.SubElement(place_mark, 'name')
    place_mark_name.text = mmsi
    ET.SubElement(place_mark, 'styleUrl').text = '#redLine'

    line_string = ET.SubElement(place_mark, 'LineString')
    ET.SubElement(line_string, 'tessellate').text = '1'
    coordinates = ET.SubElement(line_string, 'coordinates')
    coordinates_str = StringIO()
    for row in rows:
        coordinates_str.write("{0},{1},0\n".format(row[3],row[2]))
    coordinates.text = coordinates_str.getvalue()




folder = ET.SubElement(doc, 'Folder')
folder_name = ET.SubElement(folder, 'name')
folder_name.text = '数据库'
folder_open = ET.SubElement(folder, 'open')
folder_open.text = '1'

for mmsi in mmsis:
    cursor.execute("""
        select datetime(utc, 'unixepoch') as timestamp, mmsi, lat/1000000.0 as latitude, lon/1000000.0 as longitude from aisdata 
        where lat/1000000.0 between  {0} and {1}
        and lon/1000000.0 between {2} and {3}
        and utc between 1575508860 and 1575509700
        -- and mmsi = ?
        order by utc
        """.format(MIN_LAT, MAX_LAT, MIN_LON, MAX_LON), [])
    
    rows = cursor.fetchall()

    place_mark = ET.SubElement(folder, 'Placemark')
    place_mark_name = ET.SubElement(place_mark, 'name')
    place_mark_name.text = mmsi
    ET.SubElement(place_mark, 'styleUrl').text = '#greenLine'

    line_string = ET.SubElement(place_mark, 'LineString')
    ET.SubElement(line_string, 'tessellate').text = '1'
    coordinates = ET.SubElement(line_string, 'coordinates')
    coordinates_str = StringIO()
    for row in rows:
        coordinates_str.write("{0},{1},0\n".format(row[3],row[2]))
    coordinates.text = coordinates_str.getvalue()




root.set('xmlns','http://www.opengis.net/kml/2.2')
tree = ET.ElementTree(root)
tree.write("square.kml",encoding="utf-8", xml_declaration=True)




cursor.close()
conn.close()

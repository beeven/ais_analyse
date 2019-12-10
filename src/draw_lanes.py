import xml.etree.ElementTree as ET
import sqlite3


MIN_LAT = 22.500000000
MAX_LAT = 22.528400000
MIN_LON = 113.83600000
MAX_LON = 113.85900000



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
print("Count: {0}".format(len(rows)))











root = ET.Element('kml')
doc = ET.SubElement(root, 'Document')
doc_name = ET.SubElement(doc, 'name')
doc_name.text = 'AIS'
style = ET.SubElement(doc, 'Style', {'id': 'yellowLineGreenPoly'})
line_style = ET.SubElement(style, 'LineStyle')
line_color = ET.SubElement(line_style, 'color')
line_color.text = '7fff00ff'
line_width = ET.SubElement(line_style, 'width')
line_width.text = '4'

poly_style = ET.SubElement(style, 'PolyStyle')
poly_color = ET.SubElement(poly_style, 'color')
poly_color.text = '7f00ff00'

style = ET.SubElement(doc, 'Style', {'id': 'yellowLineGreenPoly'})
line_style = ET.SubElement(style, 'LineStyle')
line_color = ET.SubElement(line_style, 'color')
line_color.text = 'ff7f00ff'
line_width = ET.SubElement(line_style, 'width')
line_width.text = '2'

poly_style = ET.SubElement(style, 'PolyStyle')
poly_color = ET.SubElement(poly_style, 'color')
poly_color.text = '7f00ff00'



place_mark = ET.SubElement(doc, 'Placemark')
place_mark_name = ET.SubElement(place_mark, 'name')
place_mark_name.text = 'Criterion'
ET.SubElement(place_mark, 'styleUrl').text = '#yellowLineGreenPoly'

line_string = ET.SubElement(place_mark, 'LineString')
ET.SubElement(line_string, 'tessellate').text = '1'
coordinates = ET.SubElement(line_string, 'coordinates')
coordinates.text = "{0},{1},1\n{0},{2},1\n{3},{2},1\n{3},{1},1\n{0},{1},1".format(MIN_LON,MIN_LAT,MAX_LAT,MAX_LON)

root.set('xmlns','http://www.opengis.net/kml/2.2')
tree = ET.ElementTree(root)
tree.write("square.kml",encoding="utf-8", xml_declaration=True)




cursor.close()
conn.close()

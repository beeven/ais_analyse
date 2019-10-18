import datetime
from datetime import timezone,timedelta
from decimal import Decimal
from io import StringIO
import xml.etree.ElementTree as ET
import pynmea2


def GGAGenerator(path):
    with open(path, 'r', encoding="utf-8-sig") as f:
        for line in f:
            if not line.startswith('$GNGGA'): continue
            yield line.strip()

def make_gpx(path):
    root = ET.Element('kml')
    doc = ET.SubElement(root, 'Document')
    doc_name = ET.SubElement(doc, 'name')
    doc_name.text = 'AIS GPS'
    style = ET.SubElement(doc, 'Style', {'id': 'yellowLineGreenPoly'})
    line_style = ET.SubElement(style, 'LineStyle')
    line_color = ET.SubElement(line_style, 'color')
    line_color.text = '7f00ffff'
    line_width = ET.SubElement(line_style, 'width')
    line_width.text = '4'

    poly_style = ET.SubElement(style, 'PolyStyle')
    poly_color = ET.SubElement(poly_style, 'color')
    poly_color.text = '7f00ff00'
    place_mark = ET.SubElement(doc, 'Placemark')
    place_mark_name = ET.SubElement(place_mark, 'name')
    place_mark_name.text = 'GPS'
    ET.SubElement(place_mark, 'styleUrl').text = '#yellowLineGreenPoly'

    line_string = ET.SubElement(place_mark, 'LineString')
    ET.SubElement(line_string, 'tessellate').text = '1'
    coordinates = ET.SubElement(line_string, 'coordinates')

    coordiniates_str = StringIO()

    for gga in GGAGenerator(path):
        try:
            msg = pynmea2.parse(gga)
            if msg.altitude is None: continue
            coordiniates_str.write(','.join([str(msg.longitude), str(msg.latitude), str(msg.altitude)]) + ' \n')
        except Exception as ex:
            print(ex.args)
            continue
    coordinates.text = coordiniates_str.getvalue()
    return root


if __name__=="__main__":
    gpx = make_gpx("20190917-ais.log")
    gpx.set('xmlns','http://www.opengis.net/kml/2.2')
    tree = ET.ElementTree(gpx)
    tree.write('20190917-ais-gps.kml',encoding="utf-8", xml_declaration=True)

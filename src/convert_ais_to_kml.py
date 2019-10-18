import datetime
from datetime import timezone, tzinfo, timedelta
from decimal import Decimal
from io import StringIO
import xml.etree.ElementTree as ET
import simpleais

def ais_stream_generator(path):
    with open(path, 'r', encoding="utf-8-sig") as f:
        for line in f:
            if not line.startswith('!AIV'): continue
            line = line.strip()
            #print(line)
            yield line

def ais_msg_generator(path) -> simpleais.Sentence:
    msg_stack = []
    for line in ais_stream_generator(path):
        msg = simpleais.parse(line)
        if msg is None: 
            #print("msg is None")
            continue
        if isinstance(msg, simpleais.SentenceFragment):
            msg_stack.append(msg)
            if not msg.last():
                continue
            else:
                sentence = simpleais.parse([m.text for m in msg_stack])
                msg_stack.clear()
                yield sentence[0]
        else:
            yield msg
        

def get_location_points(path):
    station_datetime: datetime.datetime
    for msg in ais_msg_generator(path):
        d = msg.as_dict()
        if d['type'] == 4:
            station_datetime = datetime.datetime(d['year'], d['month'], d['day'], d['hour'], d['minute'], d['second'],tzinfo=timezone.utc)
            #print(station_datetime)
            continue
        elif d['mmsi'] == '412000000' and d['type'] != 24:
            #print(d)
            if d['second'] < 60:
                time = datetime.datetime(station_datetime.year, station_datetime.month, station_datetime.day, station_datetime.hour, station_datetime.minute, d['second'],tzinfo=timezone.utc)
            else:
                time = station_datetime
            yield { 'timestamp': time, 'latitude': d['lat'], 'longitude': d['lon']}


def make_gpx(in_path):
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
    place_mark = ET.SubElement(doc, 'Placemark')
    place_mark_name = ET.SubElement(place_mark, 'name')
    place_mark_name.text = 'GPS'
    ET.SubElement(place_mark, 'styleUrl').text = '#yellowLineGreenPoly'

    line_string = ET.SubElement(place_mark, 'LineString')
    ET.SubElement(line_string, 'tessellate').text = '1'
    coordinates = ET.SubElement(line_string, 'coordinates')

    coordiniates_str = StringIO()
    
    for ais in get_location_points(in_path):
        
        try:
            coordiniates_str.write(','.join([str(ais['longitude']), str(ais['latitude']), '0']) + '\n')
            
        except Exception as ex:
            print(ex.args)
            continue
    coordinates.text = coordiniates_str.getvalue()
    return root


if __name__=="__main__":
    gpx = make_gpx("20190917-ais.log")
    gpx.set('xmlns','http://www.opengis.net/kml/2.2')
    tree = ET.ElementTree(gpx)
    tree.write('20190917-ais.kml',encoding="utf-8", xml_declaration=True)

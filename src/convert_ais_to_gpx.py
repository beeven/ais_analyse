import datetime
from datetime import timezone, tzinfo, timedelta
from decimal import Decimal
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
            print("msg is None")
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
        if d is None:
            print("msg as_dict is None: {0}".format(msg))
        if d['type'] == 4:
            station_datetime = datetime.datetime(d['year'], d['month'], d['day'], d['hour'], d['minute'], d['second'],tzinfo=timezone.utc)
            print(station_datetime)
            continue
        elif d['mmsi'] == '412000000' and d['type'] != 24:
            print(d)
            if d['second'] < 60:
                time = datetime.datetime(station_datetime.year, station_datetime.month, station_datetime.day, station_datetime.hour, station_datetime.minute, d['second'],tzinfo=timezone.utc)
            else:
                time = station_datetime
            yield { 'timestamp': time, 'latitude': d['lat'], 'longitude': d['lon']}


def make_gpx(in_path):
    root = ET.Element('gpx')
    trk = ET.SubElement(root, 'trk')
    trk_name = ET.SubElement(trk, 'name')
    trk_name.text = '20190917-ais'
    trkseg = ET.SubElement(trk, 'trkseg')
    for ais in get_location_points(in_path):
        
        try:
            trkpt = ET.Element('trkpt')
            trkpt.attrib['lat'] = str(ais['latitude'])
            trkpt.attrib['lon'] = str(ais['longitude'])
            ele = ET.SubElement(trkpt, 'ele')
            ele.text = str(0)
            t = ET.SubElement(trkpt, 'time')
            t.text = ais['timestamp'].astimezone(timezone.utc).isoformat()
            trkseg.append(trkpt)
        except Exception as ex:
            print(ex.args)
            continue
    return root


if __name__=="__main__":
    gpx = make_gpx("20190917-ais.log")
    gpx.set('xmlns','http://www.topografix.com/GPX/1/1')
    gpx.set('version', '1.1')
    tree = ET.ElementTree(gpx)
    tree.write('20190917-ais.gpx',encoding="utf-8", xml_declaration=True)

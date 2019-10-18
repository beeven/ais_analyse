import datetime
from datetime import timezone,timedelta
from decimal import Decimal
import xml.etree.ElementTree as ET
import pynmea2


def GGAGenerator(path):
    with open(path, 'r', encoding="utf-8-sig") as f:
        for line in f:
            if not line.startswith('$GNGGA'): continue
            yield line.strip()

def make_gpx(path):
    root = ET.Element('gpx')
    trk = ET.SubElement(root, 'trk')
    trk_name = ET.SubElement(trk, 'name')
    trk_name.text = '20190917-ais-gps'
    trkseg = ET.SubElement(trk, 'trkseg')
    for gga in GGAGenerator(path):
        try:
            msg = pynmea2.parse(gga)
            if msg.altitude is None: continue
            trkpt = ET.Element('trkpt')
            trkpt.attrib['lat'] = str(msg.latitude)
            trkpt.attrib['lon'] = str(msg.longitude)
            ele = ET.SubElement(trkpt, 'ele')
            ele.text = str(msg.altitude)
            t = ET.SubElement(trkpt, 'time')
            t.text = datetime.datetime.combine(datetime.date(2019,9,17),msg.timestamp, tzinfo=timezone.utc).astimezone(timezone.utc).isoformat()
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
    tree.write('20190917-ais-gps.gpx',encoding="utf-8", xml_declaration=True)

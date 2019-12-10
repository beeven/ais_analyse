
import datetime
from datetime import timezone, tzinfo, timedelta
from decimal import Decimal
import xml.etree.ElementTree as ET
import simpleais
import pynmea2
import argparse
import sys

def generate_ais_stream(path):
    with open(path, 'r', encoding="utf-8-sig") as f:
        for line in f:
            if not line.startswith('!AIV'): continue
            line = line.strip()
            #print(line)
            yield line

def generate_ais_msg(path) -> simpleais.Sentence:
    msg_stack = []
    for line in generate_ais_stream(path):
        msg = simpleais.parse(line)
        if msg is None: 
            print("msg is None")
            continue
        if isinstance(msg, simpleais.SentenceFragment):
            print("Fragment: {0}".format(msg))
            msg_stack.append(msg)
            if not msg.last():
                continue
            else:
                sentence = simpleais.parse([m.text for m in msg_stack])
                msg_stack.clear()
                if len(sentence) > 0:
                    yield sentence[0]
        else:
            yield msg


def generate_ais_locations(path):
    station_datetime = datetime.datetime(2019,10,17,0,0,0)
    for msg in generate_ais_msg(path):
        d = msg.as_dict()
        if d is None:
            print("msg as_dict is None: {0}".format(msg))
        if d['type'] == 4:
            try:
                station_datetime = datetime.datetime(d['year'], d['month'], d['day'], d['hour'], d['minute'], d['second'],tzinfo=timezone.utc)
                print(station_datetime)
            except Exception as ex:
                print(ex, file=sys.stderr)
            continue
        elif d['type'] in (1,2,3):#d['mmsi'] == '412000000' and d['type'] != 24:
            print(d)
            if d['second'] < 60:
                time = datetime.datetime(station_datetime.year, station_datetime.month, station_datetime.day, station_datetime.hour, station_datetime.minute, d['second'],tzinfo=timezone.utc)
            else:
                time = station_datetime
            yield { 'timestamp': time,'mmsi':d['mmsi'], 'latitude': d['lat'], 'longitude': d['lon']}
        else:
            print(d)
        

def generate_nmea_stream(path):
    with open(path, 'r', encoding="utf-8-sig") as f:
        for line in f:
            if not line.startswith('$GNGGA'): continue
            yield line.strip()


def generate_nmea_msg(path):
    for line in generate_nmea_stream(path):
        try:
            msg = pynmea2.parse(line)
            time = datetime.datetime.combine(datetime.date(2019,10,17),msg.timestamp, tzinfo=timezone.utc).astimezone(timezone.utc)
            yield {'timestamp': time, 'latitude': msg.latitude, 'longitude': msg.longitude}
        except Exception as ex:
            #print(ex.args)
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("aisfile")
    parser.add_argument("-o", "--out", help="output file. Default to stdout.")
    args = parser.parse_args()
    if args.out is not None:
        output = open(args.out, "w")
    else:
        output = sys.stdout
    
    for point in generate_ais_locations(args.aisfile):
        output.write("{0},{1},{2},{3}\n".format(point['timestamp'], point['mmsi'], point['latitude'], point['longitude']))
    
    for point in generate_nmea_msg(args.aisfile):
        output.write("{0},self,{1},{2}\n".format(point['timestamp'], point['latitude'], point['longitude']))
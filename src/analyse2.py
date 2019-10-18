import pyAISm
import pynmea2
import sys
import simpleais
import datetime
from datetime import timezone, tzinfo, timedelta


with open ("20191018dachan.log","r") as f:
    data = f.readlines()

output = open("output.txt", "w", encoding="utf-8")

adata = filter(lambda s: s.startswith('!AIV') or s.startswith('$GNGGA'), data)
adata = map(lambda s: s.strip(), adata)

tz = timezone(timedelta(hours=8))
timestamp = None

for a in adata:
    msg_stack = []
    if a.startswith('!AIV'):
        msg = simpleais.parse(a)
        if msg is None: 
            #print("msg is None")
            continue
        if isinstance(msg, simpleais.SentenceFragment):
            #print("Fragment: {0}".format(msg))
            msg_stack.append(msg)
            if not msg.last():
                continue
            else:
                sentence = simpleais.parse([m.text for m in msg_stack])
                msg_stack.clear()
                if len(sentence) > 0:
                    d = sentence[0].as_dict()
        else:
            d = msg.as_dict()

        if d['type'] in (1,2,3):
            if timestamp is None or d['second']>=60:
                msg_time = "unknown"
                #continue
            else:
                msg_time = datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, d['second'], tzinfo=tz).isoformat()
                
            print("AIS,{0},{1},{2},{3}".format(msg_time, d['mmsi'],d['lat'], d['lon']))
                        

    else:
        try:
            msg = pynmea2.parse(a)
            timestamp = datetime.datetime.combine(datetime.date(2019,10,17),msg.timestamp, tzinfo=timezone.utc).astimezone(tz)
            print("GPS,{0},self,{1},{2}".format(timestamp.isoformat(), msg.latitude, msg.longitude))
            #output.write("Ship GPS TimeStamp: {0}\n".format(msg.timestamp))
        except Exception as ex:
            print(ex,file=sys.stderr)



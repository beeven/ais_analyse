import pyAISm
import pynmea2
import sys


with open ("20191018dachan.log","r") as f:
    data = f.readlines()

output = open("output.txt", "w", encoding="utf-8")

adata = filter(lambda s: s.startswith('!AIV') or s.startswith('$GNGGA'), data)
adata = map(lambda s: s.strip(), adata)

for a in adata:
    if a.startswith('!AIV'):
        try:
            ais_data = pyAISm.decod_ais(a)
            #if ais_data.get('type', '-1') != 4 and ais_data.get('mmsi', '0') != 412000000: continue 
            ais_format = pyAISm.format_ais(ais_data)
            print(ais_data)
            if ais_data.get('type','-1') == 4:
                output.write('Station Timestamp: {0}:{1}:{2}\n'.format(ais_data['hour'], ais_data['minute'], ais_data['second']))
            else:
                output.write(str(ais_data) + "\n")
        except pyAISm.UnrecognizedNMEAMessageError as e:
            print(e,file=sys.stderr)
        except pyAISm.BadChecksumError as e:
            print(e,file=sys.stderr)
        except Exception as e:
            print(e,file=sys.stderr)
    else:
        try:
            msg = pynmea2.parse(a)
            print(msg)
            output.write("Ship GPS TimeStamp: {0}\n".format(msg.timestamp))
        except Exception as ex:
            print(ex,file=sys.stderr)



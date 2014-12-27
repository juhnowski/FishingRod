google_appengine/dev_appserver.py --address=0.0.0.0 sensor/ &
cd sensor
./Bridge-simple.py &
python webserver.py &
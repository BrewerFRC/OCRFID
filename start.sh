cd /home/pi/OCRFID
source env/bin/activate

sudo env/bin/python3 start_tracker.py &
sudo env/bin/python3 start_gunicorn.py

sudo killall python3
deactivate

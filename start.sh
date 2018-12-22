cd /home/pi/OCRFID
source env/bin/activate

sudo env/bin/python3 start_tracker.py &
sudo env/bin/gunicorn start_gunicorn:app --worker-class eventlet -w 1 -b 0.0.0.0:5000 --log-file gunicorn.log

sudo killall python3
deactivate

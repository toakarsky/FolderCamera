#!/bin/bash
                                                  #ADRESIP:PORT
gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:1935 folderCamera:app
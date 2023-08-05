Copyright (c) 2016 David Übelacker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Description: dht22 to mqtt for Raspberry Pi
        =============================
        
        Reads the temperature and humidity from a dht22 sensors and sends it to a mqtt broker.
        
        
        Installation:
        -------------------
        
            pip install rpi-dht22-mqtt
        
        Configuration:
        -------------------
        
        Needs a json configuration file as follows (don't forget to change ip and credentials ;-)):
        
        .. code:: json
        
            {
              "mqtt_client_id": "rpi-dht22",
              "mqtt_host": "192.168.0.210",
              "mqtt_port": "1883",
              "verbose": "true",
              "topics": {
                "temperature": "halti/datacenter/temperature",
                "humidity": "halti/datacenter/humidity",
              }
            }
        
        Start:
        -------------------
        
            rpi-dht22-mqtt config.json
        
Platform: UNKNOWN

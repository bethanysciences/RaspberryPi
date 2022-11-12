import sys
import psutil
import subprocess
import time
from flask import Flask, escape, request

app = Flask(__name__)
app.config["DEBUG"] = True


def GetCurrTime():
    return time.strftime('%D %H:%M:%S %Z')


def GetHost():
    output = subprocess.run(['hostname'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    host = output.stdout.replace('\n', '')
    return host


def GetIPAddress():
    output = subprocess.run(['hostname', '-I'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    return output.stdout.replace('\'', '').replace('\n', '')


def GetUpTime():
    output = subprocess.run(['uptime', '-p'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    return str(output.stdout.replace('up ', '').replace('\n', ''))


def GetCPUTemp():
    output = subprocess.run(['vcgencmd', 'measure_temp'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    return str(output.stdout.replace('temp=', '').
               replace('\'C\n', '')) + '°C'


def GetCPUUtilization():
    return str(psutil.cpu_percent()) + '%'


def GetCPUCount():
    return str(psutil.cpu_count())


def GetMemoryUsed():
    return str(psutil.virtual_memory()[2]) + '%'


def GetDiskUsed():
    return str(psutil.disk_usage('/')[3]) + '%'


def GetSSID(iface):
    output = subprocess.run(['iwconfig', 'wlan0'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    return output.stdout[output.stdout.find('ESSID:')+7:
                         output.stdout.find('\n')].replace('\"', '')


def GetFrequency(iface):
    output = subprocess.run(['iwconfig', 'wlan0'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    return output.stdout[output.stdout.find('Frequency:')+10:
                         output.stdout.find('Access Point:')]


def GetBitRate(iface):
    output = subprocess.run(['iwconfig', 'wlan0'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    return output.stdout[output.stdout.find('Bit Rate=')+9:
                         output.stdout.find('Tx-Power=')]


def GetLinkQuality(iface):
    output = subprocess.run(['iwconfig', 'wlan0'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    return output.stdout[output.stdout.find('Link Quality=')+13:
                         output.stdout.find('  Sig')]


def SignalQuality(iface):
    output = subprocess.run(['iwconfig', 'wlan0'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    return output.stdout[output.stdout.find('nal level=')+10:
                         output.stdout.find(' dBm  \n')] + ' dBm'


def GetNetworkUsage(iface):
    output = psutil.net_io_counters(pernic=True)[iface]
    mbSent = bytes2human(output.bytes_sent)
    mbReceived = bytes2human(output.bytes_recv)
    return (mbSent, mbReceived)


def bytes2human(n, format="%(value).1f%(symbol)s"):
    symbols = ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)


@app.route('/')
def sysstats_page():

    return(" --- Raspberry PI System Statistics at " +
           GetCurrTime() + " ---" +
           "<br>Host: " + GetHost() + ".local" +
           "<br>IP address:" + GetIPAddress() +
           "<br>CPU temperature: " + GetCPUTemp() +
           "<br>&emsp;up time: " + GetUpTime() +
           "<br>&emsp;utilization: " + GetCPUUtilization() +
           "<br>&emsp;memory: " + GetMemoryUsed() +
           "<br>&emsp;disk: " + GetDiskUsed() +
           "<br>Network ssid: " + GetSSID('wlan0') +
           "<br>&emsp;frequency: " + GetFrequency('wlan0') +
           "<br>&emsp;bit rate: " + GetBitRate('wlan0') +
           "<br>&emsp;link quality: " + GetLinkQuality('wlan0') +
           "<br>&emsp;signal quality: " + SignalQuality('wlan0'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')


"""
sudo vim /etc/supervisor/conf.d/flaskshell.conf

[program:stats]
directory = /home/user/workspace/flaskshell/src
command = /home/user/workspace/flaskshell/bin/python app.py
redirect_stderr = true
stdout_logfile = /home/user/workspace/flaskshell/logs/out.log
stderr_logfile = /home/user/workspace/flaskshell/logs/error.log


sudo supervisorctl update stats
sudo supervisorctl start stats
"""

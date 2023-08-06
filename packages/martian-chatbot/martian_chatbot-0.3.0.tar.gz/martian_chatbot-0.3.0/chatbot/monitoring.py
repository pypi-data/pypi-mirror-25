import psutil
import time
import requests

from threading import Thread


class ChatbotMonitoring:

    def __init__(self, pid, config, logFile):
        self.logFile = logFile
        self.process = psutil.Process(pid)
        self.dbname = config.monitoring['dbname']
        self.interval = config.monitoring['interval']
        self.monitor = Thread(target=self.run, name='Monitoring')
        self.url = config.monitoring['monitor_url']

    def start_monitoring(self):
        self.monitor.start()

    def run(self):
        while True:
            self.check_process()
            self.check_logs()
            time.sleep(self.interval)


    def check_process(self):
        data = {
            'process_pid': self.process.pid,
            'dbname': self.dbname,
            'cpu_percent': self.process.cpu_percent(),
            'memory_percent': self.process.memory_percent(memtype='rss'),
            'status': self.process.status(),
            'num_threads': self.process.num_threads(),
            'connections': len(self.process.connections())
        }
        r = requests.post(self.url + '/process', json=data)

    def check_logs(self):
        logFile = open(self.logFile, 'r')
        data = logFile.read()
        with open(self.logFile, 'w') as file:
            file.truncate()
        if 'Incoming message!' in data:
            for message in data.split('Incoming message!')[1:]:
                user_id = message.split('ID: ')[1].split('\n')[0]
                data = {
                    'user_id': user_id,
                    'dbname': self.dbname
                }
                r = requests.post(self.url + '/logs', json=data)


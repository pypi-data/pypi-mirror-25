import psutil
import time

from threading import Thread
from influxdb import InfluxDBClient


class ChatbotMonitoring:

    def __init__(self, pid, config, logFile):
        self.logFile = logFile
        self.process = psutil.Process(pid)
        self.host = config.monitoring['host']
        self.port = config.monitoring['port']
        self.dbname = config.monitoring['dbname']
        self.interval = config.monitoring['interval']
        self.monitor = Thread(target=self.run, name='Monitoring')
        self.client = InfluxDBClient(host=self.host, port=self.port, database=self.dbname)
        self.client.create_database(self.dbname)

    def start_monitoring(self):
        self.monitor.start()

    def run(self):
        while True:
            self.check_process()
            self.check_logs()
            time.sleep(self.interval)


    def check_process(self):
        measurement = [
            {
                'measurement': 'process',
                'tags': {
                    'process_id': self.process.pid,
                    'process_name': self.dbname
                },
                'fields': {
                    'CPU': self.process.cpu_percent(),
                    'Memory': self.process.memory_percent(memtype='rss'),
                    'Status': self.process.status(),
                    'Num_threads': self.process.num_threads(),
                    'Num_connections': len(self.process.connections())
                }
            }
        ]
        self.client.write_points(measurement)

    def check_logs(self):
        logFile = open(self.logFile, 'r')
        data = logFile.read()
        with open(self.logFile, 'w') as file:
            file.truncate()
        if 'Incoming message!' in data:
            for message in data.split('Incoming message!')[1:]:
                result = self.client.query('select * from user_analytics')
                user_id = message.split('ID: ')[1].split('\n')[0]
                messages = 1
                for user in list(result.get_points()):
                    if user_id == user['user_id']:
                            messages = user['messages'] + 1
                            result = self.client.query('drop series from user_analytics where user_id=\'' + user_id + '\'')
                            break
                measurement = [
                    {
                        'measurement': 'user_analytics',
                        'tags': {
                            'bot_name': self.dbname,
                            'user_id': user_id
                        },
                        'fields': {
                            'messages': messages
                        }
                    }
                ]
                self.client.write_points(measurement)

                result = self.client.query('select messages from user_analytics')
                total_users = len(list(result.get_points()))
                total_messages = 0
                for point in list(result.get_points()):
                    total_messages += point['messages']
                measurement = [
                    {
                        'measurement': 'analytics',
                        'tags': {
                            'bot_name': self.dbname,
                        },
                        'fields': {
                            'users': total_users,
                            'messages': total_messages,
                            'avg_per_user': total_messages/total_users
                        }
                    }
                ]
                self.client.write_points(measurement)


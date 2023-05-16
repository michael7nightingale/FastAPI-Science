import logging
import os

print(os.getcwd() + '/log/app.log')
logging.basicConfig(filename=os.getcwd().replace('configuration', 'log') + 'app.log', format="%(asctime)s %(levelname)s %(message)s")

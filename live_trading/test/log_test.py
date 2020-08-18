import sys 
sys.path.append('../logs_use')
import logging_funcs as lf

l = lf.Logging()

print(l.get_all_logs())
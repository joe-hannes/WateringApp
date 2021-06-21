import thread_test
import time

print('sleeping')

time.sleep(5)

thread_test.test.set_value(2)

time.sleep(5)
thread_test.test.set_finished(True)

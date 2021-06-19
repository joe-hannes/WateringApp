import time
import threading
import concurrent.futures as cf

class TestClass(object):

    def __init__(self):

        super(TestClass, self).__init__()
        self.finished = False
        self.executor = cf.ThreadPoolExecutor()
        self.__value = 0

        self.startThreadedMethod()

    def do_something(self):
        # print(f'Sleeping {seconds} Second(s)...')
        i = 0
        while not self.finished:
            i+=1
            print(f'value: {self.__value} from {self}')
            print(i)
            time.sleep(1)

    def set_value(self, value):
        print('set_value')
        self.__value = value

    def set_finished(self, finished_arg):
        # self.finished = finished
        print('set_finished')
        self.finished = finished_arg

    def startThreadedMethod(self):
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        t1 = self.executor.submit(self.do_something)
        # t1.result()

test = TestClass()

# test.startThreadedMethod()
# time.sleep(2)
# test.set_value(5)
# time.sleep(5)
# test.set_finished(True)


    # results = [executor.submit(do_something, sec) for sec in secs]
    # f1 = executor.submit(do_something, 1)
    # f2 = executor.submit(do_something, 1)


    # for result in results:
    #     print(result)

    # for f in concurrent.futures.as_completed(results):
    #     print(f.result())
    # print(results)


# threads = []
#
# for _ in range(10):
#     t = threading.Thread(target=do_something, args=[1])
#     t.start()
#     threads.append(t)
#
#
# for thread in threads:
#     thread.join()


# finish = time.perf_counter()

# print(f'finished in {round(finish-start, 2)} second(s)')

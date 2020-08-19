from multiprocessing import Process

def test(num):
    print(num)
for i in range(3):
    Process(target=test, args=(i,)).start()
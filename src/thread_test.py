import threading

def f():
    print("hey")

t = threading.Thread(target=f)
t.start()
t.join()
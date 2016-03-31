import multiprocessing
import time
import numpy as np
from sklearn.svm import SVC
from sklearn import datasets

def mp_worker(q):
    print("Entered worker")
    clf = SVC()
    iris = datasets.load_iris()
    clf.fit(iris.data, iris.target_names[iris.target])
    while 1:
        str = q.get()
        l = [float(i) for i in str.split(',')]
        print("Got list:", l )
        print(clf.predict(l))
    print("Exited worker")
        
def mp_handler():
    q = multiprocessing.Queue()
    pr = multiprocessing.Process(target=mp_worker, args=(q,))
    pr.daemon = True
    pr.start()
    import ipdb; ipdb.set_trace()
    while 1:
        num = raw_input("What did you say?\n")
        q.put(num)
    q.close()
    q.join_thread()    

if __name__ == '__main__':
    mp_handler()

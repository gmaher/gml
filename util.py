import time
import threading
import Queue

def makeNthreads(ReaderThreadClass, num_threads, q, file_list, reader_fn):
    threads = []
    for i in range(num_threads):
        t = ReaderThreadClass(q,file_list,reader_fn,name='producer'+str(i))
        t.setDaemon(True)
        t.start()
        readers.append(t)
    return readers

class FileReaderThread(threading.Thread):
    """Note this class is a thread, so it runs in a separate thread parallel
    to the main program"""
    def __init__(self, q, file_list, reader_fn, group=None, target=None, name="producer",
                 args=(), kwargs=None, verbose=None):
        super(FileReaderThread,self).__init__()
        self.target    = target
        self.name      = name
        self.file_list = file_list
        self.reader_fn = reader_fn
        self.q         = q

    def run(self):
        while True:
            if not self.q.full():
                file_ = np.random.choice(self.file_list)
                item_ = self.reader_fn(file_)
                self.q.put(item_)
                time.sleep(random.random())
        return

class BatchGetter(object):
    def __init__(self, preprocessor_fn, batch_processor_fn, num_batch, queue_size):
        self.q                  = Queue.Queue(queue_size)
        self.preprocessor_fn    = preprocessor_fn
        self.batch_processor_fn = batch_processor_fn
        self.num_batch          = num_batch

    def get_batch(self):
        items = []
        while len(items) < self.num_batch:
            item_ = self.q.get()
            try:
                item_ = self.preprocessor_fn(item_)
                items.append(item_)
            except:
                time.sleep(random.random())

        return self.batch_processor_fn(items)

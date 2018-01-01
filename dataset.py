from interface import AbstractDataset
from util import makeNthreads, FileReaderThread, BatchGetter

class SequentialFileDataset(AbstractDataset):
    """
    Dataset that sequentially reads from a list of identifiers
    templated over reading and post processing the files
    """
    def __init__(self, file_list, reader, post_processor):
        self.file_list = file_list
        self.reader = reader
        self.post_processor = post_processor
        self.index = 0

    def next(self):
        fn = self.file_list[self.index]
        T  = self.reader(fn)
        T  = self.post_processor(T)
        self.index += 1
        return T

class ThreadedBatchFileDataset(AbstractDataset):
    """
    Dataset that will continuously read files into a queue in a separate thread
    and return random batches when next is called
    """
    def __init__(self, file_list, reader, post_processor, batch_processor,
        num_threads=1, num_batch=16, queue_size=500):
        self.file_list       = file_list
        self.reader          = reader
        self.post_processor  = post_processor
        self.batch_processor = batch_processor
        self.num_threads     = num_threads
        self.num_batch       = num_batch

        self.batch_getter = BatchGetter(post_processor, batch_processor,
            num_batch, queue_size)

        self.threads = makeNthreads(FileReaderThread, num_threads,
            self.batch_getter.q, file_list, reader)

    def next(self):
        return self.batch_getter.get_batch()

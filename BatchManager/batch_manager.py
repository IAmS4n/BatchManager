import random

from tqdm import tqdm

class BatchManager:
    def __init__(self, sample_keys, batch_size=64, samples=[]):
        """
        :param sample_keys: each sample is a dict that maps all of this sample_keys to value
        :param batch_size: default batch size
        :param samples: list of sample for init class
        """
        self._batch_size = batch_size
        self._sample_keys = sample_keys
        self._batch_inx = 0
        self._epoch_num = 0
        self._epoch_num_end = None
        self._batch_num = 0
        self._batch_num_end = None
        self._unseen_epoch = True
        self._samples = []

        if len(samples) > 0:
            self.extend(samples)

    def append(self, sample):
        self._samples.append(sample)

    def extend(self, samples):
        self._samples.extend(samples)

    def __add__(self, other):
        pass

    def __len__(self):
        return len(self._samples)

    def shuffle(self):
        random.shuffle(self._samples)

    def _batch_unpacker(self, batch_data):  # convert "list of dict" to "dict of list"
        out = {key: [] for key in self._sample_keys}
        for x in batch_data:
            for key in self._sample_keys:
                out[key].append(x[key])
        return out

    def _prepare_get_batch(self, batch_size):  # usage in get_batch function
        old_end = self._batch_inx
        new_end = (old_end + batch_size) % self.__len__()
        if new_end > old_end:
            batch_data = self._samples[old_end:new_end]
        else:  # new epoch
            batch_data = self._samples[old_end:] + self._samples[:new_end]
            self._epoch_num += 1
            self._unseen_epoch = True
            self.shuffle()
        self._batch_num += 1
        self._batch_inx = new_end
        return batch_data

    def get_batch(self, batch_unpack=True, batch_size=None):
        if batch_size is None:
            batch_size = self._batch_size
        batch_data = self._prepare_get_batch(batch_size)
        if batch_unpack:
            return self._batch_unpacker(batch_data)
        return batch_data

    def __iter__(self):
        return self

    def __next__(self):
        if self._epoch_num_end is not None and self._epoch_num > self._epoch_num_end:
            raise StopIteration
        if self._batch_num_end is not None and self._batch_num > self._batch_num_end:
            raise StopIteration
        return self.get_batch()

    def __call__(self, batch_num_end=None, epoch_num_end=None, desc=None):
        assert batch_num_end == None or epoch_num_end == None

        number_itration = None
        if batch_num_end is not None:
            self._batch_num_end = self._batch_num + batch_num_end
            number_itration = batch_num_end
        elif epoch_num_end is not None:
            self._epoch_num_end = self._epoch_num + epoch_num_end
            number_itration = epoch_num_end * self.batch_per_epoch

        return tqdm(self, total=number_itration, desc=desc)

    def subsample(self, size):
        if size is None:
            subsample_data = self._samples
        else:
            subsample_data = random.sample(self._samples, size)  # sampling without repetitive
        return self._batch_unpacker(subsample_data)

    @property
    def epoch_num(self):
        return self._epoch_num

    @property
    def batch_num(self):
        return self._batch_num

    @property
    def batch_size(self):
        return self._batch_size

    @property
    def batch_per_epoch(self):
        return int(len(self._samples) / self._batch_size)

    def check_unseen_epoch(self):
        if self._unseen_epoch:
            self._unseen_epoch = False
            return True
        return False

    def reset(self):
        self._batch_inx = 0
        self._epoch_num = 0
        self._epoch_num_end = None
        self._batch_num = 0
        self._batch_num_end = None
        self._unseen_epoch = True


if __name__ == "__main__":
    pass

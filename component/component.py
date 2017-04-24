import logging
import random
import time
import multiprocessing


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)

class Factory:

    TOTAL_CONVEYER_BELT_SIZE = 20
    SLOT_LENGTH = 2
    COMPONENT = ['A', 'B']

    def __init__(self):
        self.slot_size = int(self._set_slot_size(length=self.SLOT_LENGTH))

    def _get_component(self):
        # Get random Component
        component = random.sample(self.COMPONENT, 1)
        return ''.join(component)

    def shift(self, queue):
        '''
        shift slot by 1 from right
        :param queue: queue fixed size slot
        :return:
        '''
        while True:
            queue.insert(0, queue.pop())
            logger.info('shifted %s ' % queue)
            _wait_interval()

    def sent_component_to_slot(self, queue):
        '''
        sent component to slot after certain interval
        :param queue: queue fixed size slot
        '''
        add_only_size = self.slot_size
        while add_only_size != 0:
            queue.insert(0, self._get_component())
            logger.info('Add Component to slot %s' % queue)
            add_only_size -= 1
            _wait_interval()

    def _set_slot_size(self, length):
        return (self.TOTAL_CONVEYER_BELT_SIZE / length)


def _wait_interval():
    # Random Interval between 3 and 6 seconds
    start = time.clock()
    random_delay = random.randint(3, 6)
    while time.clock() - start < random_delay:
        pass


class Worker:

    WORKER_PAIRS = [
        {'w1': [], 'w2': []},
        {'w3': [], 'w4': []},
        {'w5': [], 'w6': []}
    ]

    def __init__(self):
        super().__init__()

    def _worker_has_both_components(self, worker):
        if 'A' in worker and 'B' in worker:
            del worker[:]
            worker.append('P')
        return worker

    def _worker_has_product(self, worker):
        return ('P' in worker) == True

    def _insert_product_to_slot(self, queue, slot, worker):
        if not queue[slot]:
            del worker[:]
            del queue[slot]
            queue.insert(slot, 'P')

    def _set_worker_pair(self, workers):
        w1 = None
        w2 = None
        if workers == self.WORKER_PAIRS[0]:
            w1 = workers.get('w1')
            w2 = workers.get('w2')
        elif workers == self.WORKER_PAIRS[1]:
            w1 = workers.get('w3')
            w2 = workers.get('w4')
        elif workers == self.WORKER_PAIRS[2]:
            w1 = workers.get('w5')
            w2 = workers.get('w6')

        return w1, w2

    def _pick_component(self, workers, component, slot, queue):
        # pick components and replace components back into the queue
        w1, w2 = self._set_worker_pair(workers)

        if (len(w1) >= 0 and len(w1) < 2) and (component not in w1) and component != '' and 'P' not in w1:
            w1.append(component)
            del queue[slot]
            queue.insert(slot, '')
            component = '' # comppnent is set to '' so that w2 does no execute

        if (len(w2) >= 0 and len(w2) < 2) and (component not in w2) and component != '' and 'P' not in w2:
            w2.append(component)
            del queue[slot]
            queue.insert(slot, '')

        # if a worker has both 'a' and 'b' then delete both components and append a 'P'
        w1 = self._worker_has_both_components(w1)
        w2 = self._worker_has_both_components(w2)

        if self._worker_has_product(w1):
            self._insert_product_to_slot(queue=queue, slot=slot, worker=w1)

        if self._worker_has_product(w2):
            self._insert_product_to_slot(queue=queue, slot=slot, worker=w2)

        logger.info("Worker Insight on %s", workers)

    def work(self, queue):
        WORKERS_SLOT_1 = 2
        WORKERS_SLOT_2 = 3
        WORKERS_SLOT_3 = 4

        while queue is not None:
            for slot_index, component in enumerate(queue):

                if slot_index == WORKERS_SLOT_1:
                    self._pick_component(workers=self.WORKER_PAIRS[0], component=component, slot=slot_index,
                                    queue=queue)

                if slot_index == WORKERS_SLOT_2:
                    self._pick_component(workers=self.WORKER_PAIRS[1], component=component, slot=slot_index,
                                    queue=queue)

                if slot_index == WORKERS_SLOT_3:
                    self._pick_component(workers=self.WORKER_PAIRS[2], component=component, slot=slot_index,
                                    queue=queue)

            logger.info("Components on the fixed size slot %s Size %s" % (queue, len(queue)))

            _wait_interval()

def run():
    factory = Factory()
    worker = Worker()
    manager = multiprocessing.Manager()
    queue = manager.list()
    pool = multiprocessing.Pool(processes=3)
    pool.apply_async(factory.sent_component_to_slot, args=[queue])
    pool.apply_async(worker.work, args=[queue])
    pool.apply_async(factory.shift, args=[queue])

    pool.close()
    pool.join()



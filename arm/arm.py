import random
import sys
import time
import multiprocessing
import logging

from arm.constants import (COMPONENTS,
                           BELT_MOVE_TIME_SECONDS,
                           STEPS)

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)

worker_pairs = [
    ({'w1': [], 'w2': []}),
    ({'w3': [], 'w4': []}),
    ({'w5': [], 'w6': []})
]


def generate_components():
    try:
        return random.choice(COMPONENTS)
    except IndexError:
        print('No Components available for production')
        sys.exit(1)


def _get_length_slot():
    return len(worker_pairs)


def _sleep(interval=BELT_MOVE_TIME_SECONDS):
    time.sleep(interval)


def start_conveyer_belt(slot_queue):
    '''
    Generate components on to the moving belt
    '''
    slot_availability = STEPS

    while slot_availability != 0:
        component = generate_components()
        slot_queue.append(component)
        logger.info("Creating Component %s on to the conveyer belt at %s" % (component, slot_availability))
        slot_availability = slot_availability - 1
        _sleep()


def shift_conveyer_belt(slot_queue):
    '''
    Continue to move the belt until the workers have finished
    combining the productions
    '''
    while True:
        _sleep(20)
        slot_queue.insert(0, slot_queue.pop())
        logger.info('shifting slots %s Size %s' % (slot_queue, len(slot_queue)))


def pick_component(workers, component, slot, slot_queue):
    '''
    pick components and replace components back into the queue
    '''
    w1 = None
    w2 = None

    if workers == worker_pairs[0]:
        w1 = workers.get('w1')
        w2 = workers.get('w2')
    elif workers == worker_pairs[1]:
        w1 = workers.get('w3')
        w2 = workers.get('w4')
    elif workers == worker_pairs[2]:
        w1 = workers.get('w5')
        w2 = workers.get('w6')

    # list of worker pairs should be less than 2 and greater than 0 to append to their list
    # empty component should not be added
    # and same component should not be in the workers list
    # and 'P' should not be in the list to get a component added as it is waiting to get back into the lost
    if (len(w1) >= 0 and len(w1) < 2) and (component not in w1) and component != '' and 'P' not in w1:
        w1.append(component)
        del slot_queue[slot]
        slot_queue.insert(slot, '')
        component = ''

    if (len(w2) >= 0 and len(w2) < 2) and (component not in w2) and component != '' and 'P' not in w2:
        w2.append(component)
        del slot_queue[slot]
        slot_queue.insert(slot, '')
        component = ''

    # if a worker has both 'a' and 'b' then delete both components and append a 'P'
    if 'A' in w1 and 'B' in w1:
        del w1[:]
        w1.append('P')

    if 'A' in w2 and 'B' in w2:
        del w2[:]
        w2.append('P')

    # if the slot queue is empty for the workers put 'P' into the slot, and delete the 'P'
    # if the shifting of conveyer belt is too fast, require code change here as slot can become non-empty
    if not slot_queue[slot]:
        if 'P' in w1:
            del w1[:]
            del slot_queue[slot]
            slot_queue.insert(slot, 'P')

        if 'P' in w2:
            del w2[:]
            del slot_queue[slot]
            slot_queue.insert(slot, 'P')

    logger.info("pick components %s", workers)


def start_workers(slot_queue):
    WORKERS_SLOT_1 = 2
    WORKERS_SLOT_2 = 3
    WORKERS_SLOT_3 = 4

    while slot_queue is not None:
        for slot_index, component in enumerate(slot_queue):

            if slot_index == WORKERS_SLOT_1:
                pick_component(workers=worker_pairs[0], component=component, slot=slot_index, slot_queue=slot_queue)

            if slot_index == WORKERS_SLOT_2:
                pick_component(workers=worker_pairs[1], component=component, slot=slot_index, slot_queue=slot_queue)

            if slot_index == WORKERS_SLOT_3:
                pick_component(workers=worker_pairs[2], component=component, slot=slot_index, slot_queue=slot_queue)


        logger.info("Components with Workers %s", worker_pairs)
        logger.info("Components on slots %s Size %s" % (slot_queue, len(slot_queue)))

        _sleep()

    print("Workers Stopped working for some reason")


def simulation():
    manager = multiprocessing.Manager()
    slot_queue = manager.list()

    pool = multiprocessing.Pool(processes=4)

    pool.apply_async(start_workers, args=[slot_queue])
    pool.apply_async(start_conveyer_belt, args=[slot_queue])
    pool.apply_async(shift_conveyer_belt, args=[slot_queue])


    pool.close()
    pool.join()

    return


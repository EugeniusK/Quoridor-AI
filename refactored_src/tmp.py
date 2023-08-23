import numpy as np
from numba import njit


@njit(cache=True)
def enqueue(queue, front, rear, data):
    # condition if queue is full
    if (rear + 1) % 5 == front:
        print(" Queue is Full\n")

    # condition for empty queue
    elif front == -1:
        front = 0
        rear = 0
        queue[rear] = data
    else:
        # next position of rear
        rear = (rear + 1) % 5
        queue[rear] = data


queue = np.zeros(5)
front, rear = -1, -1

import multiprocessing as mp
import wings
import stage
#from time import time

def main():
    mp.set_start_method('fork') # Using 'fork' instead of 'spawn' is orders of magnitude faster, but that's only on Linux. Once we care about multiplatform we can re-examine this. We definitely shouldn't rely on process spawn semantics one way or the other if we can help it.
    conn1, conn2 = mp.Pipe()

    proc_stage = mp.Process(target=stage.main, args=(conn1,))
    proc_stage.start()

    proc_wings = mp.Process(target=wings.main, args=(conn2,))
    proc_wings.start()

    proc_stage.join()
    proc_wings.join()

if __name__ == "__main__":
    main()

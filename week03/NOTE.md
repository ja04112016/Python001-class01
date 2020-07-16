学习笔记
（1）学习了多线程、多进程的概念及使用方法、使用场景；
（2）学习了通过队列、锁等方法解决竞争资源的问题；
下面是在学习过程中记录的笔记：
异步库
# async def main():
#     print("hello")
#     await asyncio.sleep(1)
#     print("world")
# 协程如果不用asyncio.run是无法加入执行日程的
# print(main())
# asyncio.run(main())

# async def say_after(delay, what):
#     await asyncio.sleep(delay)
#     print(what)
#
# def main():
#     print(f"Job start at {time.strftime('%X')}")
#     asyncio.run(say_after(1, "hello"))
#     asyncio.run(say_after(2, "world"))
#     print(f"Job end at {time.strftime('%X')}")
# main()

# 通过这个例子可以看出，程序是阻塞的，并不能并发的执行程序
# 要想实现异步，使用asyncio.create_task()创建并发任务
# async def main():
#     task1 = asyncio.create_task(say_after(1, "hello"))
#     task2 = asyncio.create_task(say_after(2, "world"))
#     print(f"Job Start at {time.strftime('%X')}")
#     await task1
#     await task2
#     print(f"Job Start at {time.strftime('%X')}")
#
# asyncio.run(main())

# Job Start at 08:57:06
# hello
# world
# Job Start at 08:57:08
# 执行上面的程序后，可以看到两个任务并行执行了，并且执行时间以执行时间最长的任务为准

# 如果一个对象可以在await语句中使用，那么它就是一个可等待对象，个人理解可等待就是等待结果返回，在这期间可以切换到其它的程序继续执行
# 可等待对象主要分为三个类型：
# 1.协程
# 协程函数
# async def nested():
#     return 42
# 协程对象：由协程函数生成的函数对象被称为协程函数
# async def main():
    # 不调用await是无法让他加入到执行日程的
    # nested()
    # 调用后加入到执行日程
    # print(await nested())
# 2.任务
# asyncio.create_task(coro, *, debug=False)
# 3.future
# 特殊的底层对象，表示一个异步操作的结果，一般不会在应用层使用，多用于库和异步api的编写，用作可等待对象

# 运行异步程序的方法
# asyncio.run(): 同一个线程中只允许运行一个，无法重复调用。函数总会创建一个新的时间循环，并在结束时关闭。应当作为程序主入口，并仅被调用一次
# 创建异步任务
# asyncio.create_task(coro): 将协程(coro)打包为一个任务，记入日程等待执行。会在asyncio.get_running_loop()返回的事件循环中执行，如果当前线程无事件循环，则会抛出RuntimeError的错误:
# 下面就是抛出的错误
# asyncio.get_running_loop()
# Traceback (most recent call last):
#   File "<input>", line 1, in <module>
# RuntimeError: no running event loop
# 需要注意的是，这个方法是在python 3.7中增加的，在之前的版本你需要用ensure_future代替

# 休眠
# asyncio.sleep(delay, result=None)
# 参数delay是休眠时间，如果指定result，则在休眠结束后将结果返回给调用者。sleep总会挂起当前任务，让其他任务运行
# async def give_me_time():
#     loop = asyncio.get_running_loop()
#     end_time = loop.time() + 5
#     while True:
#         print(datetime.datetime.now())
#         if (loop.time() + 1) > end_time:
#             break
#         await asyncio.sleep(1, result="test")
# asyncio.run(give_me_time())

# 并发运行任务
# asyncio.gather(*aws, loop=None, return_exception=False)
# 并发运行aws序列中的可等待对象，如果可等待对象为协程，将会作为任务自动加入任务日程
# 如果aws中的所有可等待对象都执行完成，将会返回由所有返回值聚合成的列表，顺序与aws可等待对象顺序一致
# 如果return_exception为True，则aws中某个可等待对象产生错误后，excetion对象会记录在返回的列表中
# 如果gather被取消，则后续未执行的可等待对象也会被取消
# 如果gather中的某个task/future被取消，则其它未执行task/future的不会被取消
# 3.7的更改，如果gather()被取消，则run_exception无论为何值，消息都会传播

多进程库
# 数据共享：内存、管道、队列
# 解决以下问题：
# num = 100
# def run():
#     print(f"紫禁城开始: {os.getpid()}")
#     global num
#     num += 1
#     print(f"打印num变量值: {num}")
#     print("紫禁城结束")
#
# p = Process(target=run)
# p.start()
# p.join()
# print(f"打印num变量值: {num}")
# 打印
# 紫禁城开始: 99547
# 打印num变量值: 101
# 紫禁城结束
# 打印num变量值: 100
# (1)队列
# from multiprocessing.queues import Queue
# from multiprocessing import Queue, Process
#
# def run(q):
#     q.put("lalala")
#
# q = Queue()
#
# p = Process(target=run, args=(q,))
# p.start()
# print(q.get())
# p.join()

# 队列可以定义大小，所以读、写也会出现阻塞
# def write(q):
#     print(f"写进程开始...({os.getpid()})")
#     for i in range(10):
#         q.put(i)
#         time.sleep(1)
#     print(f"写进程结束...({os.getpid()})")
#
# def read(q):
#     print(f"读进程开始...({os.getpid()})")
#     while True:
#         print(f"读到数据: {q.get(True)}")
#     print(f"读进程结束...({os.getpid()})")
#
# from multiprocessing import Queue, Process
#
# q = Queue()
# pw = Process(target=write, args=(q, ))
# pr = Process(target=read, args=(q,))
#
# pw.start()
# pr.start()
#
# pw.join()
# pr.join()
# 不加这个就会死锁
# pr.terminate()

# 进程池
# from multiprocessing import Pool
# p = Pool(multiprocessing.cpu_count())
# for i in range(10):
#     p.apply_async(print, args=(f"No.{i}_{os.getpid()}",))
# p.close()
# p.join()
# with Pool(multiprocessing.cpu_count()) as p:
#    output = p.apply_async(print, args=("test", ))
#    # print(output.get(1))
#    result = p.apply_async(time.sleep, args=(3, ))
#    print(result.get(1))

线程库
# threading练习
# def run():
#     print(threading.current_thread())
#
# def main():
#     t1 = threading.Thread(target=run)
#     t2 = threading.Thread(target=run)
#     t1.start()
#     t2.start()
#     print("over")
#
# main()
#
# class MyThread(threading.Thread):
#     def __init__(self, num):
#         self.num = num
#         super().__init__()
#
#     def run(self):
#         print(f"execute thread {self.num}")
#
# t3 = MyThread(3)
# t4 = MyThread(4)
# t3.start()
# t4.start()
# print(t3.getName())
# print(t4.getName())
# print(t3.is_alive())
#
# t3.join()
# t4.join()

import time
n = 0
mutex = threading.Lock()

# def add():
#     global  n
#     n += 1
#     time.sleep(1)
#     print(f"n's value is {n}\n")
#
# def main():
#     for i in range(10):
#         t = threading.Thread(target=add)
#         t.start()
        # t.join()
# main()
#普通锁
# n = 0
#
#
# class MyThread(threading.Thread):
#     def run(self):
#         global n
#         time.sleep(1)
#         if mutex.acquire(1):
#             n += 1
#             print(f"threadname: {self.name} , n's value is {n}")
#         mutex.release()
#
# def main():
#     for i in range(10):
#         mt = MyThread()
#         mt.start()
#
# main()

#嵌套锁
# mutex = threading.RLock()
# class MyThread(threading.Thread):
#     def run(self):
#         time.sleep(1)
#         if mutex.acquire(1):
#             print(f"当前线程是{self.name}")
#             mutex.acquire(1)
#             mutex.release()
#         mutex.release()
#
# for i in range(5):
#     mt = MyThread()
#     mt.start()

# 条件锁
# 需要注意条件锁的wait、wait_for和notify
# wait_for(func, timeout=None) 这个方法相当于：
# while not func:
#     condition.wait()
# 对于一个消费者、生产证模型，大致的流程是这样的:
# 生产者：
# 获取锁 --> 向队列写入数据 --> 通知其他线程(notify) --> 等待(wait_for, 直到条件满足)，如此循环
# 消费者：
# 获取锁 --> 从队列读取数据 --> 通知其他线程(notify) --> 等待(wait_for, 直到条件满足)，如此循环
from threading import Thread, Condition
import random
import queue
# q = queue.Queue(5)
# c = Condition()
# q = []
# wait_time = [0.5, 1, 1.5, 2, 2.5, 3]
#
# def producer_condition():
#     if len(q) < 5:
#         return True
#     print(f"队列满{q}，等待消费...")
#     return False
#
# def consumer_condition():
#     if 0 < len(q) <= 5:
#         return True
#     print("队列空，等待生产...")
#     return False
# # def producer(num, c):
# def producer(q, num, c):
#     for i in range(num):
#         c.acquire()
#         # time.sleep(random.choice(wait_time))
#         q.append(i)
#         c.notify()
#         c.wait_for(producer_condition)
#         # c.notify()
#         print(f"{{producer}} 写入数据{i}，当前队列长度: {len(q)}\n")
#         c.release()
#
# def consumer(q, c):
#     while True:
#         if len(q) > 0:
#             c.acquire()
#             # time.sleep(random.choice(wait_time))
#             time.sleep(10)
#             n = q.pop()
#             c.notify()
#             c.wait_for(consumer_condition)
#             # c.notify()
#             print(f"{{consumer}}获取到队列中的值：{n}, 当前队列长度：{len(q)}\n")
#
# p = threading.Thread(target=producer, args=(q, 30, c,))
# c = threading.Thread(target=consumer, args=(q,c,))
#
# p.start()
# c.start()
# c.join()
# p.join()
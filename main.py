import time
import InitProcessing
import queue
import random
import threading

q = queue.Queue(maxsize=10000)


# 任务执行函数
def wokers(msg):
    print("msg:执行任务%s" % msg[0])
    threads = []
    p = threading.Thread(target=mainThreadProd, args=(q, msg[0] + '.txt', msg[1]))
    threads.append(p)
    c = threading.Thread(target=logThreadCons, args=(q, msg[0] + '.txt',), daemon=True)
    threads.append(c)
    for t in threads:
        t.setDaemon(True)
        t.start()
    threads[0].join()
    print("%s end" % msg[0])
    return "done %s" % msg[1]


# 进程下面的生产者，负责生产日志消息，并执行任务的主线程
def mainThreadProd(que, task_fn, do_fn):
    for ids in range(10):
        time.sleep(random.randint(1, 5))
        que.put("%s put值为%d" % (task_fn, ids))
        ids += 1
        print("%s 目前执行到 %d \n" % (task_fn, ids))


# 进程下面的消费者，负责消费记录日志消息，并生成日志文件 主线程结束后自动关闭
def logThreadCons(que, log_fn):
    # print("获取到队列中的消息：%s \n" % que.get())
    while 1:
        print(q.qsize())  # 即时消费，
        info = que.get()
        print("获取到队列中的消息：%s \n" % info)
        with open("../logs/" + log_fn, 'a', encoding='utf-8') as f:
            if log_fn == "task2.txt":
                info = info + '--task2'
            f.writelines("获取到队列中的消息：%s \n" % info)


if __name__ == '__main__':
    # 初始化进程池的数量为2
    mtpool = InitProcessing.MultiProcessPool(2)
    # 任务列表 【 任务模块，任务文件】
    task = [['task1', 'a'], ['task2', 'b']]
    for idx in task:
        mtpool.run(wokers, idx)
    mtpool.keepToDone()
    result = mtpool.getResult()
    for res in result:
        print(":::", res.get())
    print("所有进程已完成任务.")

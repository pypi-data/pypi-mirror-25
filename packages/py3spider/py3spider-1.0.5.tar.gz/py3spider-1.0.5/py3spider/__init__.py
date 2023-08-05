import asyncio
import aiohttp
import warnings
import abc
from multiprocessing import Process, Queue


__all__ = ['Request', 'Response', 'Spider', 'Middleware', 'Scheduler']


class Request:

    def __init__(self, url, callback, meta=None):
        self.url = url
        self.callback = callback
        self.meta = meta


class Response:

    def __init__(self, body, url, meta=None, callback=None):
        self.body = body
        self.url = url
        self.meta = meta
        self.callback = callback


class Spider(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def start_urls(self): pass

    @abc.abstractmethod
    def parse(self, response): pass


class Middleware:

    def init(self, web):
        self.web = web

    @asyncio.coroutine
    def get(self, req):
        response = yield from self.web.get(req.url)
        body = yield from response.read()
        response.close()
        return Response(body, req.url, req.meta, req.callback)

    def save(self, data):
        print(data)


class Scheduler:

    def __init__(self, spider, middleware=Middleware()):
        self.web = aiohttp.ClientSession()
        self.__spider = spider
        self.__midw = middleware
        self.__midw.init(self.web)
        self.__request = []  # 请求队列
        self.__response = []  # 回应队列
        self.__data = Queue()  # 数据队列
        self.thread_num = 16  # 线程数

    def __del__(self):
        self.web.close()

    def __start(self):
        for url in self.__spider.start_urls:
            self.__request.append(Request(url, self.__spider.parse))

    def __putRequest(self):
        loop = asyncio.get_event_loop()

        def putRes(fur):
            self.__response.append(fur.result())
        tasks = []
        while self.__request:
            try:
                num = 0
                if len(self.__request) < self.thread_num:
                    num = len(self.__request)
                else:
                    num = self.thread_num
                for i in range(num):
                    task = asyncio.ensure_future(
                        self.__midw.get(self.__request.pop()))
                    task.add_done_callback(putRes)
                    tasks.append(task)
                if tasks:
                    loop.run_until_complete(asyncio.wait(tasks))
                    self.__doResponse()
                tasks.clear()
            except Exception as e:
                warnings.warn(e)
        loop.close()
        self.__data.put('THE_CLOSE')

    def __doResponse(self):
        while self.__response:
            res = self.__response.pop()
            try:
                for req in res.callback(res):
                    if type(req) == Request:
                        self.__request.append(req)
                    else:
                        self.__data.put(req)
            except Exception as e:
                warnings.warn(e)

    def pipSave(self, midw):
        while 1:
            item = self.__data.get()
            if item == 'THE_CLOSE':
                self.__data.close()
                break
            else:
                midw.save(item)

    def start(self):
        m = Process(target=self.pipSave, args=(self.__midw,))
        m.start()
        self.__start()
        self.__putRequest()
        m.join()
        print('The End !')

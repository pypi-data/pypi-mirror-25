import asyncio
import aiohttp
import warnings
import abc
from multiprocessing import Process, Queue


__all__ = ['Request', 'Response', 'Spider', 'Save', 'Scheduler']


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


class Downloader:

    def __init__(self):
        self.web = aiohttp.ClientSession()

    def __del__(self):

        try:
            self.web.close()
        except:
            pass

    @asyncio.coroutine
    def get(self, req):
        response = yield from self.web.get(req.url)
        body = yield from response.read()
        response.close()
        return Response(body, req.url, req.meta, req.callback)


class Save:

    def saveItem(self, item): pass


class Scheduler:

    def __init__(self, spider, save=Save, debug=True, downloader=Downloader):
        if type(save) != type:
            raise Exception('save参数不要实例化')
        if type(downloader) == type:
            self.__downloader = downloader()
        else:
            self.__downloader = downloader
        if type(spider) == abc.ABCMeta:
            self.__spider = spider()
        else:
            self.__spider = spider
        self.__save = save
        self.debug = debug
        self.__request = []  # 请求队列
        self.__response = []  # 回应队列
        self.__items = Queue()  # 数据队列
        self.thread_num = 16  # 线程数

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
                        self.__downloader.get(self.__request.pop()))
                    task.add_done_callback(putRes)
                    tasks.append(task)
                if tasks:
                    loop.run_until_complete(asyncio.wait(tasks))
                    self.__doResponse()
                tasks.clear()
            except Exception as e:
                warnings.warn(e)
        loop.close()
        self.__items.put('THE_CLOSE')

    def __doResponse(self):
        while self.__response:
            res = self.__response.pop()
            try:
                for req in res.callback(res):
                    if type(req) == Request:
                        self.__request.append(req)
                    else:
                        self.__items.put(req)
            except Exception as e:
                warnings.warn(e)

    def pipSave(self, save, debug):
        st = save()
        while 1:
            item = self.__items.get()
            if debug:
                print(item)
            if item == 'THE_CLOSE':
                break
            else:

                try:
                    st.saveItem(item)
                except Exception as e:
                    warnings.warn(e)

    def start(self):
        m = Process(target=self.pipSave, args=(self.__save, self.debug,))
        m.start()
        self.__start()
        self.__putRequest()
        m.join()
        self.__items.close()
        print('The End !')

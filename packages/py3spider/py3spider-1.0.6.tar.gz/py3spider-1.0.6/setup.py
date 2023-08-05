from setuptools import setup, find_packages

setup(
    name="py3spider",
    version="1.0.6",
    keywords=["crawl", "spider", "asyncio", "aiohttp", "定向爬虫", "异步爬虫"],
    description="仿Scrapy实现，基于py3.4+的多线程异步网络爬虫，实例请访问https://github.com/ChenL1994/py3spider/tree/master/examples",
    license="MIT",
    author="陈粮",
    author_email="1570184051@qq.com",
    packages=find_packages(),
    install_requires=["aiohttp>=2.2.5"],
    platforms="any",
    zip_safe=False
)

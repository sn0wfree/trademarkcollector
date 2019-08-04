# coding=utf8
import requests
import time
import asyncio
from pyppeteer import launch

from trademarkcollector.para.url import main_page_trademark_url

async def windows(url):
    # headless参数设为False，则变成有头模式
    browser = await launch(
        # headless=False
    )

    page = await browser.newPage()

    # 设置页面视图大小
    await page.setViewport(viewport={'width': 1280, 'height': 800})

    # 是否启用JS，enabled设为False，则无渲染效果
    await page.setJavaScriptEnabled(enabled=True)

    await page.goto(url)

    # 打印页面cookies
    print(await page.cookies())

    # 打印页面文本
    print(await page.content())

    # 打印当前页标题
    print(await page.title())

    # 关闭浏览器
    await browser.close()


if __name__ == '__main__':
    r = windows(url)

    pass

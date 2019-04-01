import os
import requests
from GameCrawler import Crawler
from Game import Game

# 你岛当前地址
ACurl = "adnmb2.com"

# 你的饼干，使用任何A岛APP以外的工具扫描你的饼干二维码
# 你会得到类似{"cookie":"xxxxx"}的文本，把xxxxx的部分填入这里
myCookie = ""

# 本次游戏的串号
threadID = "17388370"

if __name__ == "__main__":
    # 先读取最后一次更新的页码和上次抓取时最后一个回复的串号
    lastCrawedPage = 1
    lastCrawedID = ""
    if os.path.exists('LastInfo'):
        lastInfo = open('LastInfo', "r", encoding='utf-8')
        lastCrawedPage = int(lastInfo.readline())
        lastCrawedID = lastInfo.readline()
        print("已获取最后一次抓取信息，使用设置信息抓取")
    else:
        print("未能找到上次抓取信息，将执行默认设置")
    print("开始抓取")
    # 根据设置，抓取指定串从上次抓取到现在的所有回复
    crawler = Crawler(lastCrawedPage, lastCrawedID)
    replyData = crawler.Crawl(ACurl, myCookie, threadID)
    # 读取完后，将信息写入文件
    lastInfo = open('LastInfo', "w", encoding='utf-8')
    # -1是因为上次读到最后一页没东西了，但是倒数第二页可能还没回复满，
    # 所以下次从倒数第二页开始
    lastInfo.write(str(crawler.readingPage - 1) + "\n" + crawler.lastCrawTID)
    lastInfo.close()
    if len(replyData) == 0:
        print("似乎自上次抓取以来还没有新的回复")
    else:
        # 根据你设置的游戏规则，获得输出
        game = Game()
        gameText = game.Action(replyData)
        print("根据你编辑的游戏规则，输出内容如下")
        print("---------------------------------------------------\n")
        print(gameText)
        print("\n---------------------------------------------------")
        print("以上内容可选中后按Ctrl+C复制到剪贴板")
    os.system("pause")

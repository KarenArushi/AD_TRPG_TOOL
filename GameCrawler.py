import requests

class Crawler:
    def __init__(self, readPage, lastTID):
        # 抓取页数
        self.readingPage = readPage
        # 抓取串号
        self.lastCrawTID = lastTID
        # 记录当前已抓取的信息
        self.readedData = []
        # 是否已经抓取到最后一次抓取的回复
        self.lastTIDCatched = False

    def Crawl(self, url, cookie, TID):
        # 如果最后抓取串号为空，则认为已经抓到最后一次回复的串号
        if self.lastCrawTID == "":
            self.lastTIDCatched = True
        # 循环抓取自上次抓取以来所有的内容
        while True:
            # 抓取一页的文本
            print("正在抓取第" + str(self.readingPage) + "页")
            pageText = self.ReadOnePage(url, cookie, TID)
            # 读取一页的信息
            # 返回true，说明加入正常，如果返回flase，说明读取失败，或者说读完了
            if not self.ReadPageData(pageText):
                break
            # 抓完了一页，开始抓下一页
            self.readingPage += 1
        # 返回字典信息
        return self.readedData

    def ReadPageData(self, pageText):
        # 首先去尾
        pageText = pageText.split("<ul class=\"uk-pagination uk-pagination-left h-pagination\">")[0]
        # 然后尝试分割
        splitText = pageText.split("<div class=\"h-threads-item-reply-main\">")
        # 检查一下分割的数组，如果分割后只有一个元素且与原文本相等那说明这一页没有回复，退出
        if len(splitText) == 1 and splitText[0] == pageText:
            print("本页没有回复，读取完成")
            return False
        # 如果没毛病的话，继续进行
        # 第一段是用不上的其它信息，删掉
        del splitText[0]
        # 循环加入信息
        replyAddCount = 0
        for strItem in splitText:
            # 先获取这个回复的串号
            TID = strItem.split("class=\"h-threads-info-id\">")[1].split("</a>")[0]
            # 如果是广告，直接略过
            if TID == "No.9999999":
                continue
            # 如果和已经抓到的最后一个串号相等，确认抓取并从下一次循环开始正式抓取
            if TID == self.lastCrawTID:
                self.lastTIDCatched = True
                continue
            # 如果已经抓过最后一次回复的串号
            if self.lastTIDCatched:
                # 整理一下回复文本
                rpyText = strItem.split("<div class=\"h-threads-content\">")[1].split("</div>")[0]
                # 去空格
                rpyText = rpyText.replace(" ","")
                # 将该回复的信息灌入字典
                replyData = {
                    "title" : strItem.split("<span class=\"h-threads-info-title\">")[1].split("</span>")[0],
                    "email" : strItem.split("<span class=\"h-threads-info-email\">")[1].split("</span>")[0],
                    "time" : strItem.split("<span class=\"h-threads-info-createdat\">")[1].split("</span>")[0],
                    "UID" : strItem.split("<span class=\"h-threads-info-uid\">")[1].split("</span>")[0],
                    "TID" : TID,
                    "text" : rpyText
                }
                # 加入信息并增加计数
                self.readedData.append(replyData)
                self.lastCrawTID = TID
                replyAddCount += 1
        # 检查加入计数，如果本页的循环没有加入，说明这一页只有一个广告，返回false
        if replyAddCount == 0:
            print("本页只有广告，读取完成")
            return False
        else:
            return True

    def ReadOnePage(self, url, cookie, TID):
        jar = requests.cookies.RequestsCookieJar()
        jar.set('userhash', cookie, domain=url)
        r = requests.get("https://" + url + "/t/" + TID + "?page=" + str(self.readingPage), cookies=jar)
        re = r.text
        r.close()
        return re

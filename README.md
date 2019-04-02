# AD_TRPG_TOOL
这是一个[A岛](https://adnmb.com)的跑团辅助工具  
并不，这特么就是一个爬虫  
欢迎各种姿势的修改  
因为github访问太慢所以不会经常看  
不其实应该完全不会看  
创建了pull requests请发邮件到zerocastlecoder#foxmail.com提醒我

## 它如何工作？
首先你需要发一个串，告诉工具你的串号和饼干后，运行它。  
工具将会自动将自上次运行以来的所有回复整理进字典列表中，并传递给你的游戏主逻辑。

## 如何使用
1.你需要安装[python3.7及以上版本](https://www.python.org/downloads/)才能使用本工具  
2.你需要安装第三方库[requests](http://docs.python-requests.org)才能使用本工具  
3.编辑Main.py文件填入你的饼干和你的跑团串号  
4.编辑Game.py写入你的游戏逻辑  
5.脚本将调用Game的Action方法，并传入名为replyData的字典列表  
虽然说这么多，总共也没几行，而且还写了一堆注释，自己看看也搞的定

## replyData字典列表的内容
replyData =  
[{  
    "title" :  这个回复的标题("无标题")  
    "email" : 这个回复的EMAIL("无名氏")  
	"time" : 这个回复的发串时间("0000-00-00(五)00:00:00")  
	"UID" : 这个回复发送者的饼干("ID:ATM")  
    "TID" : 这个回复的编号("No.9999999")  
	"text" : 这个回复的内容("无本文")  
}]  

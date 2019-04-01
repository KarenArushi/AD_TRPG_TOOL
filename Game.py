# 游戏名 whatWarOfMine
# 现在是战争时期，你作为被H军侵占领土的G国人，继承了你二舅的财产——H军占领区的一家饭店。
# 你的目标是经营好这家饭店，让你和你的人别饿死，然后度过这个苦难的岁月。
#
# 本串每日更新一次。
# 11时至14时以及18时至20时的回复统计为客流量，该时段内所有回复位数相加即为本日盈利额。
# 0计做10，重复回复无效。
# 每个回复中若位数小于7大于等于1则消耗一单位蔬菜，大于等于7则消耗一单位肉类，若有位数0则消耗一单位珍贵配料。
#
# 在配料不足的情况下：
# 0会消耗肉类，盈利按7计算，若肉类也不足则计为无效。
# 7~9中，8会消耗蔬菜，盈利按1计算，若蔬菜也不足则计为无效，7与9会直接计为无效。
# 1~6在蔬菜不足的情况下计为无效。
# 
# 每日都会按员工数量固定消耗材料，低价值材料将被优先消耗。
# 
# 每日20点后为闭店时间，将发布当日统计及新闻，同时决定次日材料购买情况及决定重大决议。
# 
# 战况是从-1到1的区间，若达到-1则H军胜利，若达到1则G军胜利，同时游戏结束。
# 战争倾向是店铺对战争双方的讨好倾向，将会决定各类事件的发生概率，如果达到1或-1会有不好的事情发生。
# 以上两个数值都会由游戏事件推进。 

import json
import os
import Tools

class Game:
    def __init__(self):
        self.gameData = {}
        # 先读取游戏存档
        save = open("whatWarOfMine.json", "r", encoding="utf-8")
        self.gameData = json.loads(save.read())
        save.close()

    def Action(self, replyData):
        profit = 0
        rareSell = 0
        metSell = 0
        vegSell = 0
        checkedCooike = []
        # 检查所有回复
        for rep in replyData:
            # 先检查回复时间
            replyHour = Tools.GetReplyTimeByHour(rep["time"])
            if (replyHour >= 11 and replyHour < 14) or (replyHour >= 18 and replyHour < 20):
                # 然后检查饼干
                if (rep["UID"] not in checkedCooike):
                    # 有效回复，开始主逻辑
                    # 获取串号最后一位
                    lastNum = int(rep["TID"][len(rep["TID"]) - 1])
                    # 吃点啥
                    if lastNum == 0:
                        if self.gameData["rare"] > 0:
                            self.gameData["rare"] -= 1
                            rareSell += 1
                            profit += 10
                        elif self.gameData["met"] > 0:
                            self.gameData["met"] -= 1
                            metSell += 1
                            profit += 7
                    elif lastNum >= 7:
                        if self.gameData["met"] > 0:
                            self.gameData["met"] -= 1
                            metSell += 1
                            profit += lastNum
                        elif lastNum == 8 and self.gameData["veg"] > 0:
                            self.gameData["veg"] -= 1
                            vegSell += 1
                            profit += 1
                    else:
                        if self.gameData["veg"] > 0:
                            self.gameData["veg"] -= 1
                            vegSell += 1
                            profit += lastNum
                    # 加入已检查列表
                    checkedCooike.append(rep["UID"])
        
        # 员工消耗
        vegEat = 0
        metEat = 0
        rareEat = 0
        unFeedCrew = self.gameData["crewNum"]
        if self.gameData["veg"] >= unFeedCrew:
            self.gameData["veg"] -= unFeedCrew
            vegEat += unFeedCrew
        else:
            unFeedCrew -= self.gameData["veg"]
            vegEat += self.gameData["veg"]
            self.gameData["veg"] = 0
            if self.gameData["met"] >= unFeedCrew:
                self.gameData["met"] -= unFeedCrew
                metEat += unFeedCrew
            else:
                unFeedCrew -= self.gameData["met"]
                metEat += self.gameData["met"]
                self.gameData["met"] = 0
                if self.gameData["rare"] >= unFeedCrew:
                    self.gameData["rare"] -= unFeedCrew
                    rareEat += unFeedCrew
                else:
                    unFeedCrew -= self.gameData["rare"]
                    rareEat += self.gameData["rare"]
                    self.gameData["rare"] = 0
                    self.gameData["starving"] = unFeedCrew

        
        self.gameData["money"] += profit

        save = open("whatWarOfMine.json", "w", encoding="utf-8")
        save.write(json.dumps(self.gameData))
        save.close()

        re = "一天结束了\n本日盈利额：" + str(profit)
        re += "\n本日客流量：" + str(len(checkedCooike))
        re += "\n剩余金钱：" + str(self.gameData["money"])
        re += "\n当前员工数：" + str(self.gameData["crewNum"])
        re += "\n本日销售情况：【蔬菜:" + str(vegSell) + "】"
        re += "【肉类：" + str(metSell) + "】" + "【稀有材料：" + str(rareSell) + "】"
        re += "\n本日员工消耗：【蔬菜:" + str(vegEat) + "】"
        re += "【肉类：" + str(metEat) + "】" + "【稀有材料：" + str(rareEat) + "】"
        re += "\n挨饿员工：" + str(self.gameData["starving"])
        re += "\n剩余材料：【蔬菜:" + str(self.gameData["veg"]) + "】"
        re += "【肉类：" + str(self.gameData["met"]) + "】" + "【稀有材料：" + str(self.gameData["rare"]) + "】"
        re += "\n材料价格：(自行填写)"
        return str(re)

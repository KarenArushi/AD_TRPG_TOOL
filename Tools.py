def GetReplyTimeByHour(timeStr):
    timeStr = timeStr.split(")")[1]
    return int(timeStr.split(":")[0])

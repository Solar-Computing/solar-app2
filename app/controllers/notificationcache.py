from datetime import datetime, timedelta

notifications = []

def getNotifications():
    return notifications

def clearNotifications():
    notifications = []

def addNotification(notification):
    if notification["message"]:
        notifications.append(notification)



# --------------- time function logic ---------------

def getTimeDeltaSinceLastNofication(n_type):
    timestamps = [n["timestamp"] for n in notifications if n["type"] == n_type ]
    return datetime.now() - max(timestamps) if timestamps else None

def notificationInLastInterval(n_type, interval):
    timeSinceLast = getTimeDeltaSinceLastNofication(n_type)
    return interval > timeSinceLast if timeSinceLast else False



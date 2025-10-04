from rest_framework.throttling import UserRateThrottle

class SixtyPerMinuteUserThrottle(UserRateThrottle):
  rate = "60/min"
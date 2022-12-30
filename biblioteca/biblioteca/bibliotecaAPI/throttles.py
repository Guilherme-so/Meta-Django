from rest_framework.throttling import UserRateThrottle

class FiveCallsPerMinute(UserRateThrottle):
    scope= 'five'
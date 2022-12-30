from rest_framework.throttling import UserRateThrottle


class TenCallsPerMinute(UserRateThrottle):
    scope = 'ten'
    
class TwentyCallsPerMinute(UserRateThrottle):
    scope = 'twenty'
    
class TwentyCallsPerDay(UserRateThrottle):
    scope = 'twenty_day'
import json

class Server:

    __slots__ = ['id', 'name', 'region', 'icon', 'large', 'unavailable', 'created_at', 'member_count', 'splash_url', 'icon_url']

    def __init__(self, id, name, region, icon, large, unavailable, created_at, member_count, splash_url, icon_url=None):
        self.id = id
        self.name = name
        self.region = region.__str__()
        self.icon = icon
        self.icon_url = icon_url
        self.large = large
        self.member_count = member_count
        self.unavailable = unavailable
        self.splash_url = splash_url
        self.created_at = created_at.__str__()

    def __dict__(self):
        d = {}
        for item in self.__slots__:
            d[item] = getattr(self, item)
        return d
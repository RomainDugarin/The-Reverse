
class Member:

    __slots__ = ['id', 'name', 'mention', 'created_at', 'avatar_url']

    def __init__(self, id, name, mention, created_at, avatar_url=None):
        self.id = id
        self.name = name
        self.mention = mention
        self.created_at = created_at.__str__()
        self.avatar_url = avatar_url

    def __dict__(self):
        d = {}
        for item in self.__slots__:
            d[item] = getattr(self, item)
        return d
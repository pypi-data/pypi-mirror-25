class AsyncIterator:
    def __init__(self, objects):
        self.iter = iter(objects)

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration
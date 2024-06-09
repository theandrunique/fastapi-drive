from abc import abstractmethod, ABC


class BaseS3Client(ABC):
    @abstractmethod
    async def get(self): ...

    @abstractmethod
    async def put(self): ...

    @abstractmethod
    async def delete(self): ...

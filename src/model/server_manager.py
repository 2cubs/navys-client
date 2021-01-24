from model.base_manager import BaseManager


class ServerManager(BaseManager):

    def server_info(self) -> dict:
        return self._remote.server_info()

    def server_time(self) -> str:
        return self._remote.server_time()
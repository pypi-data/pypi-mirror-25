import os

from onyxerp.core.api.request import Request
from onyxerp.core.services.cache_service import CacheService
from onyxerp.core.services.onyxerp_service import OnyxErpService


class FileService(Request, OnyxErpService):

    jwt = None
    cache_service = object()
    cache_path = str()

    def __init__(self, base_url: str(), app: object(), cache_root="/tmp/"):
        super(FileService, self).__init__(app, base_url)
        self.cache_service = CacheService(cache_root, "StorageAPI")
        self.cache_path = cache_root

    def get_file_info(self, file_id: str()):

        file_name = "{0}/StorageAPI/json/doc/{1}.json" .format(
            self.cache_path, file_id
        )

        if os.path.isfile(file_name):
            return CacheService.read_file(file_name)

        request = self.get("/v2/doc/%s/" % file_id)

        status = request.get_status_code()
        response = request.get_decoded()

        if status == 200:
            CacheService.write_file(file_name, response['data']['StorageAPI'])
            return response['data']['StorageAPI']
        else:
            return False

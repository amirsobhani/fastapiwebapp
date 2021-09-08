from starlette.requests import Request

from services import user_service, package_service
from viewmodels.shared.viewmodel_base import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.package_count: int = 0
        self.release_count: int = 0
        self.user_count: int = 0
        self.packages: list = []

    async def load(self):
        self.package_count: int = await package_service.package_count()
        self.release_count: int = package_service.release_count()
        self.user_count: int = await user_service.user_count()
        self.packages: list = package_service.latest_packages(limit=5)

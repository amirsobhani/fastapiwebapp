from typing import Optional

from starlette.requests import Request

from services import user_service
from viewmodels.shared.viewmodel_base import ViewModelBase


class RegisterViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.name: Optional[str] = None
        self.password: Optional[str] = None
        self.email: Optional[str] = None

    async def load(self):
        form = await self.request.form()
        self.name = form.get('name')
        self.email = form.get('email')
        self.password = form.get('password')

        if not self.name or not self.name.strip():
            self.error = "Name is required"

        elif not self.email or not self.email.strip():
            self.error = "email is required"

        elif not self.password or not len(self.password) > 5:
            self.error = "password is required and must be at 5 character"
        elif user_service.get_user_by_email(self.email):
            self.error = "the email has exist"

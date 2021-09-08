import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from infrastructure import cookie_auth
from services import user_service
from viewmodels.account.accountviewmodel import AccountViewModel
from viewmodels.account.loginviewmodel import LoginViewModel
from viewmodels.account.registerviewmodel import RegisterViewModel

router = fastapi.APIRouter()


@router.get('/account')
@template()
def index(request: Request):
    vm = AccountViewModel(request)

    return vm.to_dict()


@router.get('/account/register')
@template()
def register(request: Request):
    vm = RegisterViewModel(request)

    return vm.to_dict()


@router.post('/account/register')
@template()
async def register(request: Request):
    vm = RegisterViewModel(request)
    await vm.load()

    if vm.error:
        return vm.to_dict()

    account = await user_service.create_account(vm.name, vm.email, vm.password)

    res = fastapi.responses.RedirectResponse(url='/account', status_code=status.HTTP_302_FOUND)

    cookie_auth.set_auth(res, account.id)

    return res


@router.post('/account/login')
@template()
async def login(request: Request):
    vm = LoginViewModel(request)

    await vm.load()

    if vm.error:
        return vm.to_dict()

    user = await user_service.login_user(vm.email, vm.password)

    if not user:
        vm.error = "the account does not exists or password is wrong"
        return vm.to_dict()

    res = fastapi.responses.RedirectResponse(url='/account', status_code=status.HTTP_302_FOUND)

    cookie_auth.set_auth(res, user.id)

    return res


@router.get('/account/login')
@template()
def login(request: Request):
    vm = LoginViewModel(request)

    return vm.to_dict()


@router.get('/account/logout')
def logout(request: Request):
    res = fastapi.responses.RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

    cookie_auth.logout(res)

    return res

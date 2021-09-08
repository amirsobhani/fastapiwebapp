import fastapi
from fastapi_chameleon import template
from starlette.requests import Request

from viewmodels.packages.detailpackageviewmodel import DetailPackageViewModel

router = fastapi.APIRouter()


@router.get('/project/{package_name}')
@template(template_file='packages/detail.pt')
def detail(package_name: str, request: Request):
    vm = DetailPackageViewModel(package_name, request)
    return vm.to_dict()

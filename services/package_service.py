import datetime
from typing import Optional

import sqlalchemy.orm
from sqlalchemy import select, func

from data import db_session
from data.package import Package
from data.release import Release


async def package_count() -> int:
    async with db_session.create_async_session() as session:
        query = select(func.count(Package.id))
        result = await session.execute(query)
        return result.scalar()


def release_count() -> int:
    session = db_session.create_session()
    try:
        return session.query(Release).count()
    finally:
        session.close()


def latest_packages(limit: int = 5) -> list[Package]:
    session = db_session.create_session()
    try:
        releases = session.query(Release).options(
            sqlalchemy.orm.joinedload(Release.package)
        ).order_by(Release.created_date.desc()).limit(limit).all()
    finally:
        session.close()

    return [r.package for r in releases]


def get_package_by_name(package_name: str) -> Optional[Package]:
    session = db_session.create_session()
    try:
        package = session.query(Package).filter(Package.id == package_name).first()
    finally:
        session.close()

    # package = Package(
    #     id=package_name, summary="This is the summary", description="Full details here!",
    #     home_page="https://fastapi.tiangolo.com/", license="MIT", author_name="Sebastián Ramírez"
    # )

    return package


def get_latest_release_for_package(package_name: str) -> Optional[Release]:
    session = db_session.create_session()
    try:
        release = session.query(Release).options(
            sqlalchemy.orm.joinedload(Release.package)
        ).order_by(Release.created_date.desc()).filter(Package.id == package_name).first()
    finally:
        session.close()

    return release

    # return Release(major_ver=1, minor_ver=2, build_ver=0, created_date=datetime.datetime.now())

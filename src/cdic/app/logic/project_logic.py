# coding: utf-8
import datetime
from io import StringIO
import os

from backports.typing import Iterable, List

from flask import abort
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.query import Query
from sqlalchemy.sql import true, or_, false

from .. import app
from ..constants import SourceType
from ..exceptions import PatchDockerfileException, FailedToFindProjectByDockerhubName
from ..models import Project, User
from ..forms.project import ProjectForm


def get_all_projects_query() -> Query:
    return Project.query.order_by(Project.created_on.desc())


def get_projects_by_user(user: User) -> List[User]:
    """
    :param User user: user instance
    :return query to List[Project]: projects owned by `user`
    """
    return Project.query.filter(Project.user_id == user.id).all()


def get_project_by_title(user: User, title: str) -> Project:
    """
    :raises NoResultFound: when no such project exists
    """
    return Project.query.filter(Project.user_id == user.id).filter_by(title=title).one()


def get_project_by_id(ident: int) -> Project:
    """
    :raises NoResultFound: when no such project exists
    """
    return Project.query.get(ident)


def get_project_by_dockerhub_name(name: str) -> Project:
    prefix =app.config["REPO_PREFIX"]
    if not name.startswith(prefix):
        raise FailedToFindProjectByDockerhubName(
            "Name should start with `{}`, got: {}".format(prefix, name))
    rest = name.replace(prefix, "")
    parts = rest.split(sep="-", maxsplit=1)
    if len(parts) < 2:
        raise FailedToFindProjectByDockerhubName(
            "Got malformed dockerhub name".format(name))
    username, title = parts
    return (
        Project.query
        .join(User)
        .filter(User.username == username)
        .filter(Project.title == title)
    ).one()


def get_running_projects() -> List[Project]:
    return Project.query.filter(Project.build_is_running == true()).all()

def get_projects_to_create_dh() -> List[Project]:
    return (
        Project.query
        .filter(Project.github_repo_exists == true())
        .filter(Project.dockerhub_repo_exists == false())
    ).all()

def get_projects_to_update_dh_status() -> List[Project]:
    return [
        project for project in
        (Project.query
            .filter(Project.dockerhub_repo_exists == true())
            .filter(Project.local_repo_pushed_on.isnot(None)).all())
        if not project.is_dh_build_finished
    ]

def get_project_waiting_for_push() -> List[Project]:
    return (
        Project.query
        .filter(Project.build_is_running == true())  # just to be sure,
        # we write content to the file only after the  user press `Run Build`
        .filter(Project.github_repo_exists)
        .filter(Project.local_repo_changed_on.isnot(None))
        .filter(or_(
            Project.local_repo_pushed_on.is_(None),
            Project.local_repo_changed_on > Project.local_repo_pushed_on
        ))
    )


def exists_for_user(user: User, title: str) -> bool:
    try:
        get_project_by_title(user, title)
        return True
    except NoResultFound:
        return False


def add_project_from_form(user: User, form: ProjectForm) -> Project:
    if exists_for_user(user, form.title.data):
        abort(400)
    else:
        return Project(
            user=user,
            title=form.title.data,
            source_mode=form.source_mode.data,
        )


def update_project_from_form(project: Project, form: ProjectForm) -> Project:
    project.source_mode = form.source_mode.data
    project.local_text = form.local_text.data
    project.git_url = form.git_url.data
    return project


def path_dockerfile_for_project(project: Project, dockerfile: str=None) -> str:
    dockerfile = dockerfile or ""
    coprs_names = [lc.full_name for lc in project.linked_coprs]  # type: List[str]
    return patch_dockerfile(coprs_names, dockerfile)

BEGIN_CDIC_SECTION = ("### DOPR START, code until tag `DOPR END`"
                      " was auto-generated by dopr service\n\n")
END_CDIC_SECTION = "### DOPR END\n\n"


def patch_dockerfile(copr_names: Iterable[str], dockerfile: str) -> str:

    out = StringIO()
    before_from = True

    def write_copr_enabler():
        out.write(BEGIN_CDIC_SECTION)
        out.write("RUN yum install -y dnf dnf-plugins-core \\\n"
                  "    && mkdir -p /etc/yum.repos.d/\n")
        if copr_names:
            out.write("RUN ")

            out.write(" && \\\n    ".join([
                "dnf copr enable -y {}".format(copr)
                for copr in copr_names
            ]))
        # out.write("\n")
        # out.write("RUN dnf clean all\n")
        out.write("\n")
        out.write(END_CDIC_SECTION)

    for raw_line in dockerfile.split(os.linesep):
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("FROM"):
            if before_from:
                before_from = False
                out.write("{}\n".format(line))
                write_copr_enabler()
            else:
                raise PatchDockerfileException("Unexpected command, "
                                               "encountered FROM command twice")

        else:
            if before_from:
                raise PatchDockerfileException("Unexpected command, Dockerfile "
                                               "should start with FROM command")
            else:
                out.writelines("{}\n".format(line))
    return out.getvalue()


def update_patched_dockerfile(project: Project):
    # TODO: should be called auto-magically
    if project.source_mode == SourceType.LOCAL_TEXT:
        patched = path_dockerfile_for_project(project, project.local_text)
    else:
        raise NotImplementedError("Dockerfile patching for {} not implemented yet"
                                  .format(project.source_mode))

    project.patched_dockerfile = patched
    project.local_repo_changed_on = datetime.datetime.utcnow()
    return project




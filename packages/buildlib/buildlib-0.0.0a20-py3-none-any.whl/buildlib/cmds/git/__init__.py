from processy import run, ProcResult
from cmdinter import CmdFuncResult, Status
from typing import Optional
from buildlib.cmds.git import prompt


def add_all() -> CmdFuncResult:
    """"""
    title = 'Git Add All.'

    p: ProcResult = run(cmd=['git', 'add', '--all'])

    if p.return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=p.return_code,
        return_msg=status + title,
        return_val=None
    )


def commit(
    msg: str
) -> CmdFuncResult:
    """"""
    title = 'Git Commit.'

    p: ProcResult = run(cmd=['git', 'commit', '-m', msg])

    if p.return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=p.return_code,
        return_msg=status + title,
        return_val=None
    )


def tag(
    version: str,
    branch: str,
) -> CmdFuncResult:
    """"""
    title = 'Git Tag.'

    p: ProcResult = run(cmd=['git', 'tag', version, branch])

    if p.return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=p.return_code,
        return_msg=status + title,
        return_val=None
    )


def push(branch: str) -> CmdFuncResult:
    """"""
    title = 'Git Push.'

    p: ProcResult = run(cmd=['git', 'push', 'origin', branch, '--tags'])

    if p.return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=p.return_code,
        return_msg=status + title,
        return_val=None
    )


def get_default_branch() -> CmdFuncResult:
    """"""
    title = 'Get Default Branch.'

    branch: Optional[str] = None
    return_code: int = 0

    p1 = run(
        cmd=['git', 'show-branch', '--list'],
        return_stdout=True
    )

    if p1.out.find('No revs') == -1 and p1.return_code == 0:
        p2 = run(
            cmd=['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            return_stdout=True
        )

        branch: str = p2.out.replace('\n', '')
        return_code: int = p2.return_code

    if return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=return_code,
        return_msg=status + title,
        return_val=branch,
    )


def status() -> CmdFuncResult:
    """"""
    title = 'Git Status.'

    p: ProcResult = run(cmd=['git', 'status'])

    if p.return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=p.return_code,
        return_msg=status + title,
        return_val=None
    )


def diff() -> CmdFuncResult:
    """"""
    title = 'Git Diff.'

    p: ProcResult = run(cmd=['git', 'diff'])

    if p.return_code == 0:
        status: str = Status.ok

    else:
        status: str = Status.error

    return CmdFuncResult(
        return_code=p.return_code,
        return_msg=status + title,
        return_val=None
    )

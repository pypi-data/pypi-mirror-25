import traceback
import sys
import os
import io
from typing import Optional, Callable, Any, NamedTuple
from contextlib import redirect_stdout


class Status(object):
    ok: str = '[OK]'
    error = '[ERROR]'
    skip = '[SKIP]'


class CmdFuncResult(NamedTuple):
    returncode: int
    returnvalue: Any
    summary: str


class CmdResult(NamedTuple):
    returncode: int
    returnvalue: Any
    summary: str
    stdout: Optional[str]
    stderr: Optional[str]
    traceback: Optional[str]


def _get_multi_writer(
    streams: list
):
    """"""
    writer = type('obj', (object,), {})
    writer.write = lambda s: [stream.write(s) for stream in streams]

    return writer


def _silent_call(
    func: Callable,
    *args: Optional[tuple],
    **kwargs: Optional[dict]
):
    args: tuple = args if args else ()
    kwargs: dict = kwargs if kwargs else {}

    with redirect_stdout(open(os.devnull, 'w')):
        returnvalue = func(*args, **kwargs)

    return returnvalue


def _catch_func_output(
    func: Callable,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
    silent: bool = False,
) -> tuple:
    """"""
    args: tuple = args if args else ()
    kwargs: dict = kwargs if kwargs else {}
    streams: list = []

    streams.append(io.StringIO())

    if not silent:
        streams.append(sys.stdout)

    with redirect_stdout(_get_multi_writer(streams)):
        func_returnvalue: Any = func(*args, **kwargs)

    output: Optional[str] = streams[0].getvalue()

    return func_returnvalue, output


def _handle_cmd_function(
    silent: bool,
    return_stdout: bool,
    catch_err: bool,
    func: Callable,
    args: Optional[tuple],
    kwargs: Optional[dict],
) -> CmdResult:
    """"""
    args = args if args else ()
    kwargs = kwargs if kwargs else {}
    func_result = None
    output = None
    error = None
    trace = None

    try:
        if return_stdout:
            result_with_output: tuple = _catch_func_output(
                func=func,
                args=args,
                kwargs=kwargs,
                silent=silent
            )

            func_result: CmdFuncResult = result_with_output[0]
            output: str = result_with_output[1]

        else:
            if silent:
                func_result: CmdFuncResult = _silent_call(
                    func=func,
                    *args,
                    **kwargs
                )

            else:
                func_result = func(*args, **kwargs)

            output = None

        if type(func_result) != CmdFuncResult:
            raise TypeError('Command function not returning type: '
                            'CmdFuncResult.')

    except Exception as e:
        trace: str = traceback.format_exc()

        not silent and print(trace)

        if catch_err:
            error = e

        else:
            raise e

    return CmdResult(
        returnvalue=func_result and getattr(func_result, 'returnvalue'),
        returncode=func_result and getattr(func_result, 'returncode'),
        summary=func_result and getattr(func_result, 'summary'),
        stdout=output,
        stderr=error,
        traceback=trace
    )


def run_cmd(
    silent: bool = False,
    return_stdout: bool = False,
    catch_err: bool = False,
) -> Callable:
    """
    This function works in combination with functions that return a
    'CmdFuncResult' object. With `run_cmd()` you get a some more control over
    these functions.

    Call it like this:

        run_cmd(silent=True, return_stdout=True)(my_func, args, kwargs)

    The curried function returns a `CmdResult` object.

    @silent: Mute child output of child function if set to True.
    @return_stdout: Return stdout of child function.
    @catch_err: Catch errors that are raised by child functions and return error
                message with 'CmdResult' object.
    """
    return lambda func, *args, **kwargs: \
        _handle_cmd_function(
            silent=silent,
            return_stdout=return_stdout,
            catch_err=catch_err,
            func=func,
            args=args,
            kwargs=kwargs
        )

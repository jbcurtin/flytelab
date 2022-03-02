"""
Hello World
------------
This simple workflow calls a task that returns "Hello World" and then just sets that as the final output of the workflow.
"""
import time
import typing

from datetime import datetime

from flytekit import task, workflow

DELAY = 10

@task
def one() -> str:
    return str(datetime.utcnow().timestamp())

@task
def two() -> str:
    time.sleep(DELAY)
    return str(datetime.utcnow().timestamp())

@workflow
def my_wf() -> typing.Tuple[str, str]:
    first = one()
    second = two()
    return first, second

@task
def alpha() -> str:
    return str(datetime.utcnow().timestamp())

@task
def beta() -> str:
    time.sleep(DELAY)
    return str(datetime.utcnow().timestamp())

@workflow
def greek_wf() -> typing.Tuple[str, str]:
    alpha_out = alpha()
    beta_out = beta()
    return alpha_out, beta_out

@workflow
def central() -> typing.Tuple[str, str, str, str]:
    one, two = my_wf()
    three, four = greek_wf()
    return one, two, three, four

if __name__ == "__main__":
    print('Running Workflow')
    print(f"Results: { central() }")

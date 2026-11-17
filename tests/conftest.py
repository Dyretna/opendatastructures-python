import pytest
from implementations import (
    ALL_IMPLS,
    DEQUE_IMPLS,
    INDEX_IMPLS,
    QUEUE_IMPLS,
    STACK_IMPLS,
)


def _param_ids(cls):
    return cls.__name__


@pytest.fixture(params=DEQUE_IMPLS, ids=_param_ids)
def deque_seq(request):
    return request.param()


@pytest.fixture(params=INDEX_IMPLS, ids=_param_ids)
def index_seq(request):
    return request.param()


@pytest.fixture(params=QUEUE_IMPLS, ids=_param_ids)
def queue_seq(request):
    return request.param()


@pytest.fixture(params=STACK_IMPLS, ids=_param_ids)
def stack_seq(request):
    return request.param()


@pytest.fixture(params=ALL_IMPLS, ids=_param_ids)
def seq(request):
    return request.param()

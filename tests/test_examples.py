from inspect import getmembers, ismodule
import pytest
import examples


def example_fns():
    ex = []
    for name, module in getmembers(examples, ismodule):
        ex.append(module)
    return ex


@pytest.mark.parametrize("example_fn", example_fns())
def test_example(htb_client, example_fn):
    # 2nd param is `testing` - some examples shouldn't
    # be run as part of the test suite
    example_fn.main(htb_client, True)

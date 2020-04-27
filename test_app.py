from app import show_msg


def test_show_msg():
    assert show_msg() == "hello"

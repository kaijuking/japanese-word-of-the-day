from src import app
import pytest

def test_hello_world():
    _tmp = app.get_default_post()
    assert _tmp == "Thank you for following MaikuOnline! 毎日頑張りましょう！"
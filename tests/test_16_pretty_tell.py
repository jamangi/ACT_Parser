# test_log_util.py
from log_util import pretty_tell

def test_pretty_tell():
    assert pretty_tell("Sota tells Ussoo Ku") == "**Sota** tells **Ussoo Ku**"
    assert pretty_tell("Who tells tells Haltise El Yokade") == "**Who tells** tells **Haltise El Yokade**"
    assert pretty_tell("Invalid channel format") == "Invalid channel format"

if __name__ == "__main__":
    pytest.main()

import pytest
from log_util import post_bundler

def test_post_bundler():
    # Define input strings with lengths close to 2000 characters
    input_strings = [
        "a" * 1000,
        "b" * 1000,
        "c" * 1000,
        "d" * 1000,
        "e" * 1000
    ]

    # Call the post_bundler function
    bundled_posts = post_bundler(input_strings)

    # Assert that the length of each bundled post is nearly 2000 characters or less
    for bundled_post in bundled_posts:
        assert len(bundled_post) <= 2000

    # Assert that the concatenated bundled posts are equal to the input strings concatenated with newlines
    concatenated_input = "\n".join(input_strings)
    concatenated_bundled = "\n".join(bundled_posts)
    assert concatenated_bundled == concatenated_input

    # Edge case: Empty input list should return an empty list
    assert post_bundler([]) == []


if __name__ == "__main__":
    pytest.main()

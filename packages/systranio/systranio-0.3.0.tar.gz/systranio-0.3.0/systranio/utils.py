"""
Tools
"""

def snake_to_camel_case(snake):
    """
    Converts a snake_case string to camelCase
    @see: https://codereview.stackexchange.com/a/85314
    """
    first, *rest = snake.split('_')
    return first + ''.join(word.capitalize() for word in rest)

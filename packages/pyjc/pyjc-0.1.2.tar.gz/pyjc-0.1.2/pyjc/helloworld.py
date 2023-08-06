"""
helloworld.py
==============
Contains "state-of-the-art" helloworld function (and maybe more) to prove that thing works.
"""

def helloworld():
    """return the hello world string
    >>> helloworld()
    Hello World!
    """

    return "Hello World!"


if __name__ == "__main__":
    assert(helloworld() == 'Hello World!')

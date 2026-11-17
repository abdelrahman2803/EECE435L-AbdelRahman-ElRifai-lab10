"""A small greeting application built and deployed by Jenkins."""


def greet(name):
    """Return a personalized greeting with the student's name."""
    return f"Hello, {name} from Abdel Rahman El Rifai!"


def main():
    """Print the default greeting."""
    print(greet("World"))


if __name__ == "__main__":
    main()

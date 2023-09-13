import os


if __name__ == "__main__":
    os.system("pytest --cov --cov-report term-missing --disable-warnings")

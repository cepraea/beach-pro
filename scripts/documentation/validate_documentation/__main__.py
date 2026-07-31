"""Run the documentation validator through its canonical module entrypoint."""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())

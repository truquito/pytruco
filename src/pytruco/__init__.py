"""pytruco package."""

from importlib.metadata import PackageNotFoundError, version

try:
  __version__ = version("pytruco")
except PackageNotFoundError:
  __version__ = "0.1.1"

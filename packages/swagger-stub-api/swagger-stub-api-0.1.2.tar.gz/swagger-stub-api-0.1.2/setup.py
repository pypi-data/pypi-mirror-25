from setuptools import setup

version = "0.1.2"

install_requires = [
    "Flask>=0.11",
    "python-decouple>=3.1",
    "swagger-parser>=1.0",
    "Flask-Cors>=3.0",
    "click>=6.7",
    "pyaml>=17.8",
    "requests>=2.18"]

test_requires = [
    "responses>=0.8",
    "pytest>=3.0",
    "pytest-cov>=2.2",
    "pytest-mock>=1.2",
    "tox>=2.8"]

setup(name="swagger-stub-api",
      version=version,
      description="Swagger Stub API",
      url="https://github.com/rai200890/swagger-stub-api",
      author="Raissa Ferreira",
      author_email="rai2000890@gmail.com",
      classifiers=[
          "Natural Language :: English",
          "Programming Language :: Python :: 3"],
      keywords="swagger mock api",
      install_requires=install_requires,
      test_requires=test_requires,
      platforms=["unix", "linux", "osx", "cygwin", "win32"],
      package_dir={"swagger_stub_api": "swagger_stub_api"},
      packages=["swagger_stub_api"],
      entry_points={
          "console_scripts": ["swagger-stub-api = swagger_stub_api.command:main"]})

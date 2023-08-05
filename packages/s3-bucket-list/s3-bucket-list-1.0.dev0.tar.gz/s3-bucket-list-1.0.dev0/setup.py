import os
from setuptools import find_packages, setup

requirements = [
    'Click',
    'requests',
    'progressbar2',
    'termcolor',
    'colorama',
    'watchdog',
    'mcommons',
    'dnspython'
]

buildNumber = os.getenv('CIRCLE_BUILD_NUM')

# {{BUILD_NUMBER}} is replaced by CI.
if buildNumber is None:
    buildNumber = "{{BUILD_NUMBER}}"

# {{BUILD_NUMBER}} wasn't replaced with proper build number (for instance, installation from git)
if buildNumber.startswith("{{BUILD_"):
    buildNumber = "dev"

setup(name="s3-bucket-list",
      install_requires=requirements,
      version="1.0" + buildNumber,
      description="CLI to query AWS S3 buckets through CloudWatch metrics",
      author="Moshe Immerman",
      author_email='name.surname@gmail.com',
      platforms=["any"],
      license="BSD",
      url="http://github.com/Moshe-Immerman/bucket-list",
      packages=['bucket_list'],
      entry_points={
          "console_scripts": [
              "bucket-list = bucket_list:main",
          ]
      }
      )

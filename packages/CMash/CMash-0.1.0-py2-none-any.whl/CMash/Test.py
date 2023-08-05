###########################
# Note that you now import minhash via: from CMash import MinHash as MH
###########################
import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.md'), 'r') as fid:
    long_description = fid.read()

print(HERE)
print(long_description)
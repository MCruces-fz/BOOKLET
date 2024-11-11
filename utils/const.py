"""

C O N S T A N T S

"""
import os
from os.path import join as join_path

ROOTDIR = os.path.abspath("./")
INPDIR = join_path(ROOTDIR, "input")
OUTDIR = join_path(ROOTDIR, "output")
TESTDIR = join_path(ROOTDIR, "testing")
STORE = join_path(ROOTDIR, "store")
STORAGE = join_path(ROOTDIR, "store")

FACES_PER_SHEET = 4
SHEETS_PER_BOOKLET = 4
FACES_PER_BOOKLET = FACES_PER_SHEET * SHEETS_PER_BOOKLET
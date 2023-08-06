from __future__ import unicode_literals

import os
import datetime

import time

import pytest
from dalimil import dalimil


@pytest.fixture
def datasrc(tmpdir):
    srcdir = tmpdir / "datasrc"
    srcdir.ensure_dir()

    # populate with some data
    dates = ["2010-11-01T12:22:10",
             "2010-11-01T13:22:10",
             "2010-11-01T14:22:10",
             "2010-11-02T12:22:10",
             "2010-11-02T20:22:10",
             "2010-11-02T21:22:10",
             datetime.datetime.now().isoformat()[:19],
             datetime.datetime.now().isoformat()[:19]
             ]
    pattern = "{short_dt}_{i:d}_123.xml"
    for i, dt in enumerate(dates, 1):
        dt_struct = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        dt_yearago = dt_struct
        dt_yearago.replace(year=dt_yearago.year - 1)
        dt_yearago = time.mktime(dt_yearago.timetuple())
        # fname = srcdir "/" dt[:10] + "_" + str(i) + "_123.xml"
        basename = pattern.format(short_dt=dt[:10], i=i)
        fname = srcdir / basename
        fname.write_text(fname.strpath, "utf-8")
        os.utime(fname.strpath, (dt_yearago, dt_yearago))
    return srcdir


def test_list(datasrc):
    """test list actions
    """
    org_files = list(datasrc.listdir("*"))
    with datasrc.as_cwd():
        print("pwd", os.getcwd())
        filepattern = (datasrc / "*").strpath
        args = ["-action", "list", filepattern]
        dalimil.main(args)
        # Check, that source files are still there
        for org_file in org_files:
            assert org_file.exists()
        # TODO: check somehow, that something is printed out
    return


def test_copy2zip(datasrc):
    """test copy2zip action
    """
    org_files = list(datasrc.listdir("*"))
    with datasrc.as_cwd():
        print("pwd", os.getcwd())
        filepattern = (datasrc / "*").strpath
        args = ["-action", "copy2zip", filepattern]
        dalimil.main(args)
        # check, that source files are still there
        for org_file in org_files:
            assert org_file.exists()
        # TODO: check, that expected archives are created
    return


def test_move2zip(datasrc):
    """test move2zip action
    """
    with datasrc.as_cwd():
        print("pwd", os.getcwd())
        filepattern = (datasrc / "*").strpath
        args = ["-action", "move2zip", filepattern]
        dalimil.main(args)
        # TODO: check, that source files from completed periods are removed
        # TODO: check, that source files from current time period are still
        # present
        # TODO: check, that expected archives are created
    return


@pytest.mark.skip(reason="Not implemented yet.")
def test_easy_scenario(datasrc):
    """test minimal set of parameters
    """
    print("testing")
    pass


@pytest.mark.skip(reason="Not implemented yet.")
def test_pattern_time_detection(datasrc):
    """test pattern time detction
    """
    print("testing")
    pass

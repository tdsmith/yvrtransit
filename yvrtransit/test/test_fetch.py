import datetime as dt

from yvrtransit.fetch import _dates_to_archive, _months_to_rollup


class TestFetch:
    def test_dates_to_archive(self):
        today = dt.date(2005, 5, 5)
        past = ["2005-05-04T05:05_stub"]
        present = ["2005-05-05T00:00_stub"]
        to_archive = _dates_to_archive(past+present, today)
        assert to_archive == ["2005-05-04"]

    def test_months_to_rollup(self):
        today = dt.date(2005, 1, 31)
        past = ["2004-12-31_trip.tar.xz"]
        present = ["2005-01-01_trip.tar.xz",
                   "2005-01-02_trip.tar.xz",
                   "2005-02-20_trip.tar.xz"]
        to_archive = _months_to_rollup(past+present, today)
        assert to_archive == ["2004-12"]

import datetime as dt

from yvrtransit.fetch import _dates_to_archive


class TestFetch:
    def test_dates_to_archive(self):
        today = dt.date(2005, 5, 5)
        past = ["2005-05-04T05:05_stub"]
        present = ["2005-05-05T00:00_stub"]
        to_archive = _dates_to_archive(past+present, today)
        assert to_archive == ["2005-05-04"]

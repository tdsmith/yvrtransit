import datetime
from glob import glob
import os
import tarfile
import warnings
import zipfile

import click
from dateutil.parser import parse as dtparse
from dateutil.tz import tzlocal
import requests

# (url, needs_auth)
URLS = {
    "static": ("http://ns.translink.ca/gtfs/google_transit.zip", False),
    "trip": ("https://gtfs.translink.ca/gtfsrealtime", True),
    "position": ("https://gtfs.translink.ca/gtfsposition", True),
}


def _get_api_key():
    return os.environ["TRANSLINK_API_KEY"]


@click.command()
@click.argument("feed", type=click.Choice(URLS.keys()))
@click.option("--repository", type=click.Path(exists=True), default=os.curdir,
              help="Path to data repository")
def fetch(feed, repository):
    """Fetch a feed from Translink.

    Valid feed types are [static, trip, position].
    Creates files in REPOSITORY of the form TIME_stub, where TIME is a
    ISO8601 timestamp and stub is a feed type.
    """
    now = datetime.datetime.now(tzlocal()).replace(microsecond=0)
    filename = now.isoformat() + "_" + feed
    local_target = os.path.join(repository, filename)

    url, needs_auth = URLS[feed]
    req = requests.get(
            url,
            params={"apikey": _get_api_key()} if needs_auth else {},
            timeout=60,
    )
    req.raise_for_status()

    with open(local_target, "wb") as f:
        f.write(req.content)


def _dates_to_archive(filenames, today=None):
    """Given a list of filenames, reports which dates are in the past.

    Parameters:
        filenames: A list of filenames, assumed to be in TIME_stub format,
            where TIME is a ISO8601 timestamp.
        today: The current day, as a datetime.date. Defaults to the current
            day, in the current timezone.

    Returns:
        A list of strings representing dates to archive in YYYY-MM-DD format.
        "Dates to archive" are any encountered dates before, and not including,
        the present day.
    """
    if today is None:
        today = datetime.date.today()
    seen_dates = set()
    for fn in filenames:
        try:
            basename = os.path.basename(fn)
            date = dtparse(basename.split("_")[0]).date()
        except ValueError:
            warnings.warn(f"Could not parse {fn}; ignoring.")
        seen_dates.add(date)
    past_dates = {d for d in seen_dates if d < today}
    past_date_stubs = [d.isoformat() for d in sorted(past_dates)]
    return past_date_stubs


@click.command()
@click.option("--repository", type=click.Path(exists=True), default=os.curdir,
              help="Path to data repository")
def archive(repository):
    """Makes daily .tar.xz archives for dates in the past, and makes monthly
    .zip archives for months in the past.

    (.tar.xz is used for good compression. zip is used because it supports
    random access and monthly archives are large.)

    `archive` creates separate trip and position archives.
    """
    do_archive(repository)
    do_rollup(repository)


def do_archive(repository):
    for stub in ["position", "trip"]:
        filenames = glob(os.path.join(repository, f"*_{stub}"))
        dates_to_archive = _dates_to_archive(filenames)
        for date in dates_to_archive:
            archive_filename = os.path.join(repository, f"{date}_{stub}.tar.xz")
            to_archive = glob(os.path.join(repository, f"{date}T*_{stub}"))
            to_archive.sort()
            with tarfile.open(archive_filename, mode="x:xz") as tar:
                for target in to_archive:
                    arcname = os.path.basename(target)
                    tar.add(target, arcname=arcname, recursive=False)
            for target in to_archive:
                try:
                    os.unlink(target)
                except Exception:
                    warnings.warn(f"Could not delete {target}; continuing.")


def _months_to_rollup(filenames, today=None):
    """Given a list of filenames with Y-m-d prefixes, report the set of Y-m
    prefixes that were observed which are from before the current month.

    Parameters:
        filenames: A list of filenames, assumed to be in DATE_stub format,
            where DATE is of the form YYYY-MM-dd.
        today: The current day, as a datetime.date. Defaults to the current
            day, in the current timezone.

    Returns:
        A list of strings representing dates to archive in YYYY-MM format.
        "Dates to archive" are any encountered dates before, and not including,
        the present day.
    """
    if today is None:
        today = datetime.date.today()
    first_of_month = today.replace(day=1)
    seen_dates = set()
    for fn in filenames:
        try:
            basename = os.path.basename(fn)
            date = dtparse(basename.split("_")[0]).date().replace(day=1)
        except ValueError:
            warnings.warn(f"Could not parse {fn}; ignoring.")
        seen_dates.add(date)
    past_dates = {d for d in seen_dates if d < first_of_month}
    past_date_stubs = [d.strftime("%Y-%m") for d in sorted(past_dates)]
    return past_date_stubs


def do_rollup(repository):
    for stub in ["position", "trip"]:
        filenames = glob(os.path.join(repository, f"*_{stub}.tar.xz"))
        months_to_rollup = _months_to_rollup(filenames)
        for yyyymm in months_to_rollup:
            archive_filename = os.path.join(repository, f"{yyyymm}_{stub}.zip")
            target_glob = f"{yyyymm}-[0-9][0-9]_{stub}.tar.xz"
            to_archive = glob(os.path.join(repository, target_glob))
            to_archive.sort()
            with zipfile.ZipFile(archive_filename, mode="x") as z:
                for target in to_archive:
                    arcname = os.path.basename(target)
                    z.write(target, arcname)
            for target in to_archive:
                try:
                    os.unlink(target)
                except Exception:
                    warnings.warn(f"Could not delete {target}; continuing.")

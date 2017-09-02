import datetime
import os

import click
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
@click.option("--repository", type=click.Path(exists=True), default=os.curdir)
def fetch(feed, repository):
    """Fetch a feed from Translink.

    Valid feed types are [static, trip, position]."""
    now = datetime.datetime.now(tzlocal()).replace(microsecond=0)
    filename = now.isoformat() + "_" + feed
    local_target = os.path.join(repository, filename)

    url, needs_auth = URLS[feed]
    req = requests.get(url, params={"apikey": _get_api_key()} if needs_auth else {})
    req.raise_for_status()

    with open(local_target, "wb") as f:
        f.write(req.content)

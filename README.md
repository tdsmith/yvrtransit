See archives at: https://tl.tds.xyz

crontab:

```
TRANSLINK_API_KEY=your_key
TRANSITREPO=/some/path


* * * * * yvrtransit_fetch --repository $TRANSITREPO trip
* * * * * yvrtransit_fetch --repository $TRANSITREPO position
# updated Friday 6pm; fetch Saturday AM
3 0 * * 6 yvrtransit_fetch --repository $TRANSITREPO static

# create daily .tar.xz archives
0 4 * * * yvrtransit_archive --repository $TRANSITREPO
0 5 * * * yvrtransit_advertise --repository $TRANSITREPO > $TRANSITREPO/index.html
```

Some of the data used in this product or service is provided by permission of TransLink. TransLink assumes no responsibility for the accuracy or currency of the Data used in this product or service.

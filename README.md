crontab:

```
TRANSLINK_API_KEY=your_key
TRANSITREPO=/some/path


* * * * * yvrtransit_fetch --repository $TRANSITREPO trip
* * * * * yvrtransit_fetch --repository $TRANSITREPO position
3 0 * * 6 yvrtransit_fetch --repository $TRANSITREPO static  # updated Friday 6pm; fetch Saturday AM
```

Some of the data used in this product or service is provided by permission of TransLink. TransLink assumes no responsibility for the accuracy or currency of the Data used in this product or service.

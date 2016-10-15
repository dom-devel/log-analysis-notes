# Help on constructing a tool for SEO log analysis

This is the companion code section for the [Guide to Log Analysis wit Big Query](https://www.distilled.net/resources/guide-to-log-analysis-with-big-query/).

Onwards. Our log processer needs to do two crucial things:

1. Format the logs so they can be uploaded to BigQuery (I will reference turning them to into CSV files for the purposes of this tutorial, but BigQuery accepts multiple formats.)
2. Double check which logs are Googlebot.

There are also several convenience things which are nice to do in code:

1. Accept log files whether they're zipped or unzipped.
2. Accept log files which are in an S3 bucket (often necessary if the log files are very very large.)
3. Upload the log files to BigQuery.

##How to format the logs
I wrote a python log parser, which takes a regex string and a line of a log file and outputs a pythonary dictionary with the various values. You can find it under log_parser.py.

It's by far the least terrible and most re-useable part of my code which is why I uploaded it. (I've commented it a lot for any other amateur coders that may be reading this.)

I've also got several regex strings for parsing common log formats that may come in useful:

##How to double check which logs are Googlebot?
The primary way for identifying Googlebot is using a reverse DNS lookup and then a forward DNS lookup as recommended by Google themselves.

https://support.google.com/webmasters/answer/80553?hl=en

This works fine for most scenarios, however if you're performing historical log analysis on logs which are often a year or older, then Google will have occasionally rotated the IP addresses they're using for crawling and your reverse DNS lookup will fail.

In this case we can do an ASN lookup to discover the owner of that particular IP, because Google as a large organisation will buy static IP ranges to crawl from.

In python we used the DNS module to perform the reverse and forward DNS lookups and the cymruwhois module to perform ASN lookups and discover the owner of the IP.

##How best to go about doing this?

The rough code that I have hacked together use

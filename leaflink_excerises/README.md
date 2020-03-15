How to run the program:

`python leaflink_load_to_redshift_table.py 01`

where `01` is the date paramater that corresponds to the s3 directory after the bucket

It will load all json data in that folder `01` into `load_impressions_{year}{month}{day}` redshift table where year and month is assumed to be 2020 and 02 
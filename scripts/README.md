# scripts

Miscellaneous scripts used in ISARIC ETL

## `relsub.py`: REDCap RELSUB matcher

In many REDCap datasets, patients are assigned a new ID each time they come in
for a visit. While this suffices as the visit ID, this means that we can not
identify patients across visits. REDCap databases usually have a separate RELSUB
table that contains two columns USUBJID and RSUBJID, which identify these
(visit) IDs as the same patient.

This script reads RELSUB and outputs a unique ID for each patient corresponding
to their visit ID. In practice, this is used to either replace the subject IDs
in the source dataset, or used as a parameter to adtl when parsing the source
dataset to generate unique patient identifiers that are the same across visits.

There are several identifier generation methods supported:

* `serial`: IDs start from 1 and are serially incremented
* `uuid`: IDs are [UUIDs](<https://en.wikipedia.org/wiki/Universally_unique_identifiers>

The script only requires Python and can be run as follows

```shell
python3 scripts/relsub.py <RELSUB file>
```

which will save the ID mappings to a `relsub.json` file to be used in the
parser. The output file name can be changed by passing the `-o` or `--output`
flag. The default generator is `serial`, to use UUIDs instead, pass
`--generator=uuid` to the program.

As an example, running on the CCPUK RELSUB file gives

```shell
$ python3 relsub.py CCPUK\ RELSUB.csv
relsub.py: wrote relsub.json
           11793 unique IDs across 23587 total
```

## `missing_fields.py`: lists missing fields

The majority of the parser attributes are optional, as they may not
always be present in each dataset. However, this makes it easy to miss
fields which should be mapped, as there are no associated warnings for
optional fields.

This script checks either an individual parser, or all parsers in a folder,
against the current schema to check which of the optional fields are missing.
A summary table of the percentage of schema fields present in the parser is
printed in the terminal, and a csv file showing whether each attribute individually
is present (true) or absent (false) from the parser.

This script requires Python, along with the pandas and tomli packages installable
with the provided `requirements.txt` file. It can be run as follows
```shell
python3 scripts/checkfields/missing_fields.py <PATH TO PARSER FILE>
```
which will save an output file `check_fields.csv` containing a list of all
possible attributes and whether or not they are present. All the parsers can
be tested at once by adding a `--all` flag and providing a path to the folder, rather
than a file, e.g.

```shell
python3 scripts/checkfields/missing_fields.py isaric/parsers --all
```

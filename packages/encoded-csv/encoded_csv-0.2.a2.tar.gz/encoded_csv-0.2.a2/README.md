# encoded_csv

Could that CSV file be encoded in something other than ASCII? No problem.

This package provides support for reading CSV files that use arbitrary text encodings. It is built on top of Python's standard [csv](https://docs.python.org/3/library/csv.html) and [codecs](https://docs.python.org/3.6/library/codecs.html) packages, and it uses [Daniel Blanchard's ```chardet``` universal encoding detector](https://pypi.python.org/pypi/chardet) to guess the encoding for a file, if necessary. 

Note that ```utf-8-sig``` (UTF-8 with leading [Byte Order Mark](http://unicode.org/faq/utf_bom.html#BOM)) is supported. This format is used by recent versions of Microsoft Excel when the user selects "Save As ..." and chooses the "CSV UTF-8."

## using it

There's just one function: ```get_csv()```, as follows:

```python
encoded_csv.get_csv(csv_file, skip_lines=0, encoding='', dialect='', fieldnames=[], sample_lines=100)
```

Code in the ```tests/``` directory provides usage examples. The function returns a tuple, in which the first item is a list of the field names. The second item is a list of ordered dictionaries, each containing the data read from a given line of the CSV file.

The first row (after discarding any header lines) is assumed to contain column names.

Keyword arguments:

 * ```csv_file``` -- path to CSV file to open
 * ```skip_header_lines``` -- (optional) number of lines to discard in the assumption that they constitute a file header of some sort (default is to skip no lines)
 * ```encoding``` -- (optional) specifies the encoding which is to be used for the file; [the standard python ```codecs``` module](https://docs.python.org/3.6/library/codecs.html) is used, so any of [the standard encodings](https://docs.python.org/3.6/library/codecs.html#standard-encodings) may be specified; default behavior is to attempt best guess using ```chardet```)
 * ```dialect``` -- (optional) a set of parameters specific to a particular CSV dialect; [the standard python ```csv``` module](https://docs.python.org/3/library/csv.html) is used, so [the standard, predefined ```dialect``` values or formatting parameters](https://docs.python.org/3/library/csv.html#csv-fmt-params) must be used; default behavior is to attempt best guess using ```csv.Sniffer```.
 * ```fieldnames``` -- (optional) is used to force the [csv.DictReader](https://docs.python.org/3/library/csv.html#csv.DictReader) to use a particular set of fieldnames. 
 * ```sample_lines``` -- (optional) integer used to prepare the sample given to ```csv.Sniffer()``` when attempting to detect the CSV dialect in use; default is 100 lines or the entire file, whichever is fewer.

## etc.

Bug reports and feature requests are welcome, but really I'd prefer pull requests. 

    


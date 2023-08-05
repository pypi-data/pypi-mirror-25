py_curate_json
==============

Curate:
http://www.macmillandictionary.com/us/dictionary/american/curate_2
"to select items from among a large number of possibilities for other people to consume and enjoy"

Flattens a JSON record without requiring a JSON schema or invidual element mapping.

For a file with a list of JSON records (one per line), first run the curate script to create a schema.

Then run the flatten/denormalize scipt to actually flatten the JSON according to the derived schema and output as a csv file.

ToDo: configurable column sub-name delimiter

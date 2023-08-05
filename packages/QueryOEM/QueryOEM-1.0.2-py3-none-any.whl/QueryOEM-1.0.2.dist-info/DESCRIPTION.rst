# QueryOEM
Query OEM for information about workstations, laptops, servers and others.

# How to Install
Just issue ```pip install QueryOEM```

# Supported OEM's
Only DELL is supported at this moment

# Usage
There are two diferent classes. **QueryOEM** will query a single equipment and **MultipleQueryOEM** is a wrapper
which will return a list of **QueryOEM** instances.

Check the following usage for both classes:

## Quering a single equipment
```python
import QueryOEM

my_laptop = QueryOEM.QueryOEM(PART_NUMBER="XXXXXX")
my_laptop.get_from_dell()

# Return a dictionary
print(my_laptop.dell_data)

# Return a JSON and save it into a file
fopen = open('c:/temp/my_laptop.json', 'w')
fopen.write(my_laptop.json_from_dell())
fopen.close()
```

## Quering multiple equipments
```python
import QueryOEM

assets_list = MultipleQueryOEM(['XXXXXX','YYYYYY','WWWWWW','ZZZZZZ'])
assets_list.get_from_dell()

# Loop over the queried equipments
for i in assets_list.results:
  print(i)

# Retrieve a JSON containing all equipments
JSON = assets_list.json_from_dell()
fopen = open('c:/temp/assets_list.json', 'w')
fopen.write(JSON)
fopen.close()
```


# QueryOEM
Query OEM for information about workstations, laptops, servers and others.

1.0.0 First Release, 07/04/2017
- Installable module
- Support Dell OEM
- Query single/multuple service tags
- Export to json

1.0.1 07/05/2017
- Dell: Added Send date from vendor on the response

1.0.2 12/09/2017
- Added CLI support by using python -m QueryOEM.cli


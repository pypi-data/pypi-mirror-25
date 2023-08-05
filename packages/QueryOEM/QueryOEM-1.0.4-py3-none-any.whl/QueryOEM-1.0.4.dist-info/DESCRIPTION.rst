# QueryOEM
Query OEM for information about workstations, laptops, servers and others.

# How to Install
Just issue ```pip install QueryOEM```

# Supported OEM's
Only DELL is supported at this moment

# Usage

There are two approaches. You can embbed it to your code or use it on the terminal.

## CLI usage

Use it on the terminal makes the task easier to achive

### Query assets from terminal
You can query tags using ```python3 -m QueryOEM.cli --tag output=<output> format=<format> vendor=<vendor> <servicetags>```

Arguments
- (Required) tags - Service tags, separated by space
- (Required) output - Path to file to be saved
- (Optional) format - Output format (Default is JSON - Only JSON available)
- (Optional) vendor - OEM name (Default is Dell. Only Dell available)

Example
`python  -m QueryOEM.cli --tag output=~/my_assets format=json vendor=dell A0DA0CR A1DA1CR A2DA2CR`
`python  -m QueryOEM.cli --tag output=~/my_assets A0DA0CR A1DA1CR A2DA2CR`
`python  -m QueryOEM.cli --tag output=C:/temp/my_assets A0DA0CR`

### Query assets from a text file

You can also create a tags.txt file, add 1 tag per line and query them in one single shot

Arguments
- (Required) origin - Path to file containing service tags (1 per line)
- (Required) output - Path to output file: Path to save output file
- (Optional) vendor - Vendor - Default Dell
- (Optional) format - Output format - Default JSON 

`python3 -m QueryOEM.cli --file origin=<text_file> output=<c:/temp/myfile>`

Example:

tags.txt
```
ABC1234
QWE1234
IOP4321
```

The run this code on the terminal
```python -m QueryOEM.cli --file origin=tags.txt output=c:/temp/my_assets```

## Embedded to your code

There are two diferent classes. **QueryOEM** will query a single equipment and **MultipleQueryOEM** is a wrapper
which will return a list of **QueryOEM** instances.

Check the following usage for both classes:

### Quering a single equipment
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

### Quering multiple equipments
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

1.0.3 12/09/2017
- Small changes on CLI help text

1.0.4 19/09/2017
- CLI for --tag can be used to output a JSON file instead of terminal display
- Added new arguments to --tag to fit new feature
### To Do
- Test suite


[![PyPI](https://img.shields.io/pypi/v/nine.svg)](https://pypi.python.org/pypi/libjournal/1.0) [![Github Releases (by Release)](https://img.shields.io/github/downloads/atom/atom/v1.0.0/total.svg)](https://github.com/undystopia/libjournal/archive/0.1.tar.gz)

# libjournal (1.0)

Libjournal is a free and open-source library that is currently in development. It allows you to create a digital journal. With Libjournal, you can currently add, delete, and read entries that are organized by name, date, and time. More featers are to come soon!

## Instalation

### PIP
If you are going to use PIP, then run this command
```python
$ pip3 install libjournal
```
### Manual Install
If you aren't going to use PIP, you can manually install it using [this](https://github.com/undystopia/libjournal/archive/1.0.tar.gz) link. Then run:
```python
$ python install setup.py
```

## Usage
Using libJournal is extremely simple. First, create a `JSON` file in your directory. Then write:
```python
import libjournal
```
At the top of your python file. Next you need to initialize the libJournal object. To do this, you do it like any other object:
```python
# libj can be anything you want
libj = libjournal()
```
Next you need to set the location of you `JSON` file. In order to do that, you must use the `set_JSON_location` method:
```python
# replace your 'example.json' with the directory of your JSON file
libj.set_JSON_location("example.json")
```
Finally, use the `add_entry()` method in order to add an entry. This takes in the parameters `entry_title` and `content` as it's paremters. (Note: whatever you set as the `entry_title` is what you use to delete or search your entries. Currently you cannot have entries with the same name (case doesn't matter)
```python
# replace the 'title' and the 'content' to what you want
libj.add_entry("title", "content")
```
In order to search and entry up use the `entry_read()` method. It takes one parameter, `entry_title`, which is the name of the entry (cases don't matter) you want to search up, and read
```python
# replace the 'title' with the entry name (cases don't matter)
libj.read_entry("title")
```
If you want to delete an entry, you must use the 'delete_entry()' method which takes in one parameter, `entry_title`, which is the name of the entry (cases don't matter) that you want to delete
```python
#replace teh 'title' with the entry name (cases don't matter)
libj.delete_entry("title")
```

## WIP Features
 - Searching by time
 - Searching by general time
 - More profecient syntax

That's all that's planned for now, but more may be added in the future.

## Library Authors
 - Aneesh Edara
 - Aviral Mishra

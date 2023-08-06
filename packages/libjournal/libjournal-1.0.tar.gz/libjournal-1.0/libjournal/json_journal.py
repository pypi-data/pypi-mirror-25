import json
import datetime

class libjournal():
    def __init__(self):
        self.json_location = ''

    def set_JSON_location(self, json):
        """Sets the location of the JSON used to store entries. Must be done before appending or deleting entries"""
        self.json_location = json

    def add_entry(self, entry_title, content):
        """Adds an entry given title & content as long as 'json_location' has been set"""
        entries = open(self.json_location)
        entries_str = entries.read()
        if entries_str == '':
            entries_str = "{}"
        entries_data = json.loads(entries_str)

        now = datetime.datetime.now()

        libj_date = (now.strftime("%Y-%m-%d"))
        libj_time = (now.strftime("%H:%M"))

        entries_data[entry_title.upper()] = {"Date": libj_date, "Time": libj_time, "Content": content}

        with open(self.json_location, 'w') as fp:
            json.dump(entries_data, fp)

        print("Added entry: " + entry_title)

    def delete_entry(self, entry_title):
        """Deletes and entry given the name of the entry as long as 'json_location' has been set"""
        entries = open(self.json_location)
        entries_str = entries.read()
        if entries_str == '':
            entries_str = "{}"
        entries_data = json.loads(entries_str)

        del entries_data[entry_title.upper()]

        with open(self.json_location, 'w') as fp:
            json.dump(entries_data, fp)

        print("Deleted entry: " + entry_title)

    def entry_read(self, entry_title):
        """Searchs through all stored entries to find the one named 'entry_title'. It then returns the content"""
        entries = open(self.json_location)
        entries_str = entries.read()
        if entries_str == '':
            entries_str = "{}"
        entries_data = json.loads(entries_str)

        entry_content = entries_data[entry_title.upper()]["Content"]
        return entry_content
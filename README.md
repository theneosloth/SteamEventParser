# SteamEventParser
A python class that yields the information about the events in a given steam group

#Problems

* Currently the code is very clunky using counters instead of a truly modular method.
* This could probably be circumvented by using a library like BeautifulSoup but I wanted to stick to the standard library.

#Sample Code Usage
```py
id = "ID_STRING"
event_parser = SteamEventParser(id)
for event in event_parser.iterate_events():
    # See: Sample Output
    print(event)

# Returns: {'Date': 'Tuesday 24', 'Message': 'Game Up!', 'Time': '06:22pm'}
print(event_parser.get_last_event())

# Returns a list representation of iterate_events()
print(event.get_event_list())
```

#Sample Output
```
{'Date': 'Tuesday 24', 'Message': 'Game Up!', 'Time': '06:22pm'}
{'Date': 'Sunday 22', 'Message': 'Join the chat room!', 'Time': '06:58pm'}
{'Date': 'Saturday 21', 'Message': 'Welcome to the group!', 'Time': '06:38pm'}
```

#Sample Command Line Usage
```
steam_parser.py 1003526346346
```



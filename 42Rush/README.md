# Paris-Metro-Direction-Builder
### 1 day coding challenge.

Shortest path from street A to street B for Metro users in Paris.
The program uses [Navitia](https://www.navitia.io/) API to find the closest Metro station to provided location, builds a graph from Paris Metro stations and finds the shortest path to provided destination by using BFS.
The first run can take a couple of seconds because we download all the Metro network and cache it. Once it's cached responses will be faster.

> Please note that this was a one-day coding challenge. The code is quite messy and needs to be refactored! So please do not judge strictly ^-^

# Usage

#### Special dependencies
```bash
$> pip3 install ansicolors
```
#### Run
```bash
$> python3 ratp.py <Yor location> <Destination point>
```
#### Example

![](https://github.com/katolikyan/ratp/blob/master/.media/examples.png)

> Colored output works correctly only in the `iTerm` !

---

The project have been done in collaboration with [iiskakov](https://github.com/iiskakov)

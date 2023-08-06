find
Find Examples

- Find by name or extension: `find /home/username/ -name "*.err"`
- Find file by name: `find . -name testfile.txt`
- Find all by extension: `find /home -name '*.jpg'`
- Find empty files: `find . -type f -empty`
- Find all files (ignore case) modified by user in last 7 days: `find /home -user someuser -mtime 7 -iname ".db"`
- Find with grep to find based on content: `find . -type f -exec grep "search" '{}' \; -print`

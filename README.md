# ssh-hosts
This is a simple helper for connecting as different users to different SSH servers. Only tested on Mac OS and Linux!

## Usage
The script takes in path to a CSV file as argument. This file should contain server and user information for different 
SSH servers that are used regularly. Check "hosts_example.lst" for an example.

Running the script:

 ```
   $ ./ssh_hosts.py -l /path/to/your/hosts_list
   ```
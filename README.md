Mike Basdeo 2018

# Local Server Request
In this assignment, you will re-implement the HTTP client and the HTTP remote file
manager of Assignments #1 and #2 respectively using UDP protocol. In the previous
assignments, you leverage TCP protocol for implementation to guarantee packet
transmission over unreliable network links. Because you are going to use UDP protocol that
does not guarantee the transfer, you need to insure reliability by implementing a specific
instance of the Automatic-Repeat-Request (ARQ) protocol called: Selective Repeat ARQ /
Selective Reject ARQ. Before starting on this Lab, we encourage you to review the
programming samples and the associated course materials.

### Step 1 - Run echo server
`python httpfs.py --port 8007`

### Step 2 - Run router
`.\router_x64.exe`

### Client GET - List all files
`python httpc.py get localhost`

### Client GET - Contents of foo.txt
`python httpc.py get localhost/foo`

### Client POST -  Overrite contents of file foo.txt
`python httpc.py post -d "Assignment 3" localhost/foo`


### Run echo server with debugging messages
`python httpfs.py -v -d "other" --port 8807`

### Change server data directory
`python httpfs.py -d "other" --port 8007`


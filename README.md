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


## Tasks
- [ ] Mimicking the TCP three-way handshaking technique when you in or start the
communication with the server: 1 Mark
- [ ] GET: 2.5 Marks (e.g. read the content of a file and listing files)
- [ ] POST: 2.5 Marks (e.g. create a new file)
- [ ] With drop rate only: 1.5 Marks
- [ ] With delayed only: 1.5 Marks
- [ ] With both drop and delay: 1 Mark

## Optional Tasks
- [ ] Support multiple clients at the server: 2 Marks

## Steps To Run

### Step 1 - Run echo server
`python httpfs.py --port 8007`

### Step 2 - Run router
`./router`
`./router  --drop-rate=0.2 --max-delay=10ms --seed=1`

### Client GET - List all files
`python httpc.py get localhost`

### Client GET - Contents of foo.txt
`python httpc.py get localhost/foo`

### Client POST -  Overrite contents of file foo.txt
`python httpc.py post -d "Assignment 6969" localhost/foo`


### Run echo server with debugging messages
`python httpfs.py -v -d "other" --port 8807`

### Change server data directory
`python httpfs.py -d "other" --port 8007`


### Tricksy Mac'ss
./router  --drop-rate=0.2 --max-delay=10ms --seed=1


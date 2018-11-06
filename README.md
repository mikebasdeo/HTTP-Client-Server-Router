Mike Basdeo 2018

# Local Server Request

## Run echo server
`python httpfs.py --port 8007`

## Run router
`.\router_x64.exe`

## Client GET - List all files
`httpc.py get localhost`

## Client GET - Contents of foo.txt
`httpc.py get localhost/foo`

## Client POST -  Overrite contents of file foo.txt
`python httpc.py post -d "Assignment 3" localhost/foo`


##################################
###OLD


## Run echo server with debugging messages
`python httpfs.py -v -d "other" --port 8807`

## Change server data directory
`python httpfs.py -d "other" --port 8007`

## Httpc Get Command 
### Will return a list of the current files in the data directory.
`./httpc.py get localhost`

## Httpc Get /*
### Will return the contents of the fille named * inside the data directory.
`./httpc get localhost/foo`
 
## HTTPC Post /*
`./httpc post -d "Hello World" localhost/foo`






# Web Post Request
./httpc.py post -p 8007 -d "hello_world" http://httpbin.org/post

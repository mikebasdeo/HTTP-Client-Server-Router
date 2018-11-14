# Router

You can either use the precompiled distributions for Windows, Linux or MacOS.
Or build from source code by yourself.

1. Use the binary
Run `./router --help` for the usage.

2. Compile from source
 - Install Go (1.7 or later)
 - Run `go build router.go`







Router is a logical router dispatches UDP packets between applications.
It receives UDP packets, then dispatches to the associated destination of the packet.
During the delivery the value of a peer address will be changed from 'toAddr' to 'fromAddr'.

Usage:
    router --port int --drop-rate float --max-delay duration --seed int

    --port int-number
        port number that the router is listening for the incoming packet.
        default value is 3000.

    --drop-rate float-number
        drop rate is the probability of packets will be dropped during on the way.
        use 0 to disable the drop feature.

    --max-delay duration (eg. 5ms, 4s, or 1m)
        max delay the maximum duration that any packet can be delayed.
                any packet will be subject to a delay duration between 0 and this value.
        the duration is in format 5s, 10ms. Uses 0 to route packets immediately.

    --seed int
        seed is used to initialize the random generator.
        if the same seed is provided, the random behaviors are expected to repeat.

    Example:
    router --port=3000 --drop-rate=0.2 --max-delay=10ms --seed=1
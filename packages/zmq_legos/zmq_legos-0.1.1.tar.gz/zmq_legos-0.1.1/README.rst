A collection of usefull zeromq legos. Building blocks for larger applications.

===
MPD
===

Asyncio implementation using zeromq of the [Majordomo Protocol](https://rfc.zeromq.org/spec:7/MDP/).

Currently on my laptop can serve around 4K msg/second

With a few tweeks:
 - can control eager scheduling of messages to workers (useful for messages that take unequal time)
 - READY additionally returns json dict of worker configuration

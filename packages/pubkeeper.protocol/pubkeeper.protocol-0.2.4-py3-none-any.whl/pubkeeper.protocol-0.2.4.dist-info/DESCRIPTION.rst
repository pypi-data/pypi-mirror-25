# PubKeeper Protocol
## Intro

The goal of the PubKeeper protocol is to facilitate a distributed Publisher/Subscriber model for topics of information.

## Methods
### authenticate
- **params**
 - token - JWT for Authentication

```
PubkeeperPacket(Packet.AUTHENTICATE, {
   	token: 'your_jwt'
})
```

This method _should_ be the first packet to the PubKeeper server from a client.  You provide the server a JWT which should be issued to you by the admin of the server.  The token, should, have an issuer and audience of _pubkeeper_, and the subject should be your client.  Along with those, the token will also contain an array of rights associated for this token.


### authenticated
- **params**
 - authenticated - Your authenticated status

```
PubkeeperPacket(Packet.AUTHENTICATED, {
	authenticated: Bool
})
```

In response to every **authenticate** packet, you will receieve an **authenticated** packet which alerts you to your current status with the PubKeeper server.

### brewer_register
-  **params**
 - topic - Topic you will be brewing to
 - brewer - configuration of your brewer

```
PubkeeperPacket(Packet.BREWER_REGISTER, {
	'topic': 'test.topic',
	'brewer': {
		'uuid': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
 		'hostname': 'localhost',
 		'port': 9899,
 		'protocol': 'udp'
   	}
 })
```

This method will register your **_brewer_** with the **_pubkeeper_** server for a specific topic.  The brewer configuration should be able to instruct a subscriber how to listen to your stream of data.  This method, will send a **brewer_notify** packet to all clients subscribed to this topic.

### brewer_unregister
-  **params**
 - topic - Topic you are brewing to
 - brewer - configuration of your brewer

```
PubkeeperPacket(Packet.BREWER_UNREGISTER, {
	'topic': 'test.topic',
	'brewer': {
	 	'uuid': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
		'hostname': 'localhost',
		'port': 9899,
		'protocol': 'udp'
	}
})
```

This method, an inverse of above, will instruct the server to remove your brewer from being available for consumption.  It will also send a **brewer_removed** packet to all clients subscribed to this topic, to instruct them to destory their patrons. _[Note: You may supply only a UUID string, rather than an object for the brewer to unregister only.  If you provde an obejct you will need to supply the exact same object as used when registering]_


### brewer_notify
-  **params**
 - topic - Topic of new brewer
 - brewer - Configuration of new brewer in the network

```
 	PubkeeperPacket(Packet.BREWER_NOTIFY, {
 		'topic': 'test.topic',
  		'brewer': {
 		 	'uuid': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
 			'hostname': 'localhost',
 			'port': 9899,
 			'protocol': 'udp'
   		}
 	})
```

This method is sent to the client from the server to inform them of a new brewer brewing on the network, as well as where to find them.  This packet will only be sent to clients that are subscribed to this topic, or a wild-carded topic like _test.*_.

### brewer_removed
-  **params**
 - topic - Topic of removed brewer
 - brewer - Configuration of removed brewer from network

```
 	PubkeeperPacket(Packet.BREWER_REMOVED, {
 		'topic': 'test.topic',
  		'brewer': {
 		 	'uuid': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
 			'hostname': 'localhost',
 			'port': 9899,
 			'protocol': 'udp'
   		}
 	})
```

This method will be sent out to clients whom are subscribed to this topic to inform them of a brewer who is no longer on the network.  Like above, this packet will be sent to clients listening to a wild-carded topic.

### subscribe
-  **params**
 - topic - Topic to subscribe to

```
 	PubkeeperPacket(Packet.SUBSCRIBE, {
 		'topic': 'test.topic'
 	})
```

Used to inform the server that you would like a current list of brewers for the given topic, and would like to register for updates about brewers of this specific topic.  The topic string may be of a format with wildcards.  For example, _test.*_ would susbcribe to all topics that begin with _test_.  This method will initiate the server to start sending you **brewer_notify** packets for all current brewers in the system.


### unsubscribe
-  **params**
 - topic - Topic to unsubscribe from

```
 	PubkeeperPacket(Packet.UNSUBSCRIBE, {
 		'topic': 'test.topic'
 	})
```

Used to inform the server that you would like to cancel your subscription to the given topic.  The server will not send you any other information, it is the clients liability to close all connections to brewers.

### Error
-  **params**
 - message - Error Message

```
 	PubkeeperPacket(Packet.ERROR, {
		'message': 'Failure doing something'
 	})
```

Something on the server end went wrong, and this will alert clients to the problem.  Problems can range from failure to authenticate, to issuing commands while unauthenticated.



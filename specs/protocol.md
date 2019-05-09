# EWP (Ethereum Wire Protocol)

## Messages

The message type both defines the `request` and `response` as they are identical. The `message` format is the following: 

```
EWP <version> <protocol> <compression> <encoding> <headers-length> <body-length>
<header><body>
```

A parsed message would look like this:

```python
{
    'version': 'string',
    'protocol': 'string'
    'compression': 'string',
    'encoding': 'string',
    'headers': 'bytes',
    'body': 'bytes'
}
```

### Fields

| Field | Definition | Validity |
|:------:|----------|:----:|
| `version` | Defines the EWP version number e.g. `0.1`. | `(\d+\.)(\d+)` |
| `protocol` | Defines the communication protocol. | `(RPC\|GOSSIP)` |
| `compression` | Defines the compression codec of the `header` and `body`, none can be specified. | `[a-z0-9_]+` |
| `encoding` | Defines the encoding of the `header` and `body`. | `[a-z0-9_]+` |
| `header` | Defines the header which is a `BSON` payload, it is seperately encoded and compressed. | `BSON` payload |
| `body` | Defines the body which is a `BSON` payload, it is seperately encoded and compressed. | `BSON` payload |

### Examples

example of a wire protocol message

#### RPC call example with ping
```
# Request (RPC call with a body of a RPC ping call)
EWP 0.2 RPC none json 0 25
{"id":1,"method_id":0x00}

# Response
EWP 0.2 RPC none json 0 25
{"id":1,"method_id":0x01}
```

#### RPC call with payload
```
# Request (empty headers, bson body)
EWP 0.2 RPC deflate bson 0 1234
<1234 bytes of deflate compressed binary bson body data>
# Response
EWP 0.2 RPC gzip bson 321 1234
<321 bytes of gzip compressed binary bson header data>
<1234 bytes of gzip compressed binary bson body data>

# Request (no compression, bson headers, bson body)
EWP 0.1 RPC none none 321 1234
<321 bytes of binary bson header data>
<1234 bytes of binary bson body data>
# Response
200 none 0 0\n
```

#### Gossip
```
# Request (Gossip call with a header with a message hash)
EWP 0.2 GOSSIP none json 33 0
"001322323232232932232322232327f"

# Request (Gossip call with a full block)
EWP 0.2 GOSSIP snappy bson 25 1234
<25 bytes of snappy compressed binary bson header data>
<1234 bytes of snappy compressed binary bson body data>
```


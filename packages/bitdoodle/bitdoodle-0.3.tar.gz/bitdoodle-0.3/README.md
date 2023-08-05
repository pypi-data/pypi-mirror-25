# BitDoodle!
Python Class for dealing with variable length bit doodles.

Description:

Bit Doodle is a class designed for working with variable length bit fields.  While the class can technically be used for anything, it is catered towards IPv4 and IPv6 addresses.  The main methods are join and disjoin, which will take a list of variable length fields and a list of values and join them together to a single value, or disjoin which will take a single value and a list of bit lengths, and break the original value into its multiple parts.

# EXAMPLES:

Basic useage simple example
```python
from BitDoodle import BitDoodle
format_ = [8, 8, 8, 8]
dood = BitDoodle(format_)
dood.join([10, 20, 30, 40])
IPv4Address(u'10.20.30.40')
dood.total_bit_length
32
```
Not so obvious IPv4 example

Imagine if a standard IP address was broken up into meaningful pieces.  For example the first 8 bits are a static 10, but the next 5 bits represent your datacenter, and the next 4 bits might represent the security zone, and the next 4 bits might represent the pod number, and so on.  Given a format and values to put into the fields, you can generate a meaningful IP address.
```python
format_ = [8, 5, 4, 5, 4, 6]
dood = BitDoodle(format_)
dood.join([10, 4, 0, 1, 4, 30])
IPv4Address(u'10.32.5.30')
```
Not so obvious IPv6 example

This is the same as above, but for IPv6.  If ARIN (or your RIR) gave you a /40, the first 40 bits would be static, then the next 24 bits could mean something specific to your use case, split up however you want.  Finally the last 64 are the host, which you could also break down further if you wanted.  This is more to show BitDoodle working fine with very large numbers.

```python
format_ = [40, 6, 4, 6, 4, 4, 64]
dood = BitDoodle(format_)
dood.join([0x200199aa00, 4, 0, 1, 4, 10, 255])
IPv6Address(u'2001:99aa:10:14a::ff')
```

Disjoin example

Disjoin does the opposite of join.  Given a format and an integer (in this case, represented as a binary number / IP address), return the values of each section.  So just like above, if you knew the IP address you could find out the data center, security zone, pod, etc, of each field.
```python
format_ = [8, 5, 4, 5, 4, 6]
dood = BitDoodle(format_)
dood.disjoin(0b00001010000011111111111100101101)
[10L, 1, 15, 31, 12, 45]
```

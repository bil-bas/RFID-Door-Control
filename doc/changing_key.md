# Changing Keys

Notes on how to change keys on a MiFare 1K Classic

So initial key is all F (0xFF 0xFF 0xFF 0xFF 0xFF 0xFF) which is the default
for both key A and key B. To change a key, you just need to write to the block
which coincides with the correct set of sectors - which is every 4 blocks (0
indexed). So, we will be using blocks 4 to 7. This is sector 1. The keys are
stored in Block 7, so to change the key, after authenticating you need to
write to Block 7 with the correct set of data.


To change the key, you need a new key (hexadecimal, 12 characters long). You
also need to set up the access conditions. See page 12-14 of [Mifare 1K
Datasheet](http://www.nxp.com/documents/data_sheet/MF1S50YYX.pdf). The default
ones are as below (this is a dump of Block 7 after authentication with the
default key):

```
0x000000000000ff078069ffffffffffff
```

Here you can see the initial Key A is hidden (the first 12 digits), the access
settings, which we will break down shortly, and the Key B which is identical to
Key A at present.

Byte | Bits     | Comment |
---- | -------- | ------- |
ff   | 11111111 | C2 and C1 inverted |
07   | 00000111 | C1 normal, C3 inverted |
80   | 10000000 | C3 and C2 normal |
69   | 01101001 | User Data |

This breaks out as so:

Access Bits  | Values | Comment |
------------ | ------ | ------- |
C1 C2 C3 (3) | 0 0 1  | Transport Config - Key A read/write all |
C1 C2 C3 (2) | 0 0 0  | Transport Config - Key A|B works for all |
C1 C2 C3 (1) | 0 0 0  | Transport Config - Key A|B works for all |
C1 C2 C3 (0) | 0 0 0  | Transport Config - Key A|B works for all |

As Key B is in a readable format, it does not get used for Auth so can be used
for User data. otherwise it is unused and will not authenticate this Sector.

From this, we will probably be leaving this the same so that key A works for
all. No point making it more difficult anyway.

So, now we can actually modify the Key A by authenticating using it, then
writing to Block 7 with the new code, and the same Access Bits. Then we can
authenticate with it and read cards again!

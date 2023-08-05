# AioPhue

A port of [Phue](https://github.com/studioimaginaire/phue) to AsyncIO using 
AioHTTP to communicate with the bridge.

## Examples

AioPhue's API is similar to the one of the original library, but uses 
coroutines where possible / necessary.

```python 
from aiophue import AioBridge

b = await AioBridge.get_bridge("BRIDGE IP")
lights = await b.get_light_objects()
for light in lights:
    if await light.is_reachable():
        await light.turn_on()
```
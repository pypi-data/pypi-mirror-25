import logging

from .light import AioLight

_LOGGER = logging.getLogger(__name__)


class AioGroup(AioLight):
    def __init__(self, bridge, light_id):
        super().__init__(bridge, light_id)
        self.group_id = None

    @classmethod
    async def get_group(cls, bridge, group_id):
        group = cls(bridge, None)
        del group.light_id

        try:
            group.group_id = int(group_id)
        except:
            name = group_id
            groups = await bridge.get_group()
            for idnumber, info in groups.items():
                if info['name'] == name:
                    group.group_id = int(idnumber)
                    break
            else:
                raise LookupError("Could not find a group by {}"
                                  .format(group_id))

        return group

    async def _get(self, *args, **kwargs):
        resp = await self.bridge.get_group(self.group_id, *args, **kwargs)

        return resp

    async def _set(self, *args, **kwargs):
        if self.transitiontime is not None:
            kwargs['transitiontime'] = self.transitiontime
            _LOGGER.debug("Setting with transitiontime {} = {} s".format(
                self.transitiontime, float(self.transitiontime) / 10
            ))

            if (args[0] == "on" and args[1] is False) or (
                    kwargs.get("on", True) is False):
                self._reset_bri_after_on = True

        resp = await self.bridge.get_group(self.group_id, *args, **kwargs)

        return resp

    async def set_name(self, name):
        old_name = await self.get_name()
        self._name = name
        await self._set("name", self._name)
        _LOGGER.debug("Renaming light group from {} to {}"
                      .format(old_name, self._name))

        await self._set("name", self._name)

    async def get_lights(self):
        lights = await self._get("lights")
        return [AioLight(self.bridge, int(l)) for l in lights]

    async def set_lights(self, value):
        _LOGGER.debug("Setting lights in group {} to {}"
                      .format(self.group_id, str(value)))

        await self._set("lights", value)


class AioAllLights(AioGroup):
    @classmethod
    async def get_all(cls, bridge):
        from .bridge import AioBridge

        if bridge is None:
            bridge = AioBridge()

        group = AioGroup(bridge, 0)

        return group
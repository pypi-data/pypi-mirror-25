import logging

import phue

_LOGGER = logging.getLogger(__name__)


class AioLight(phue.Light):
    @property
    def name(self):
        return self._name or "anonymous"

    async def _get(self, *args, **kwargs):
        light = await self.bridge.get_light(self.light_id, *args, **kwargs)

        return light

    async def _set(self, *args, **kwargs):
        if self.transitiontime is not None:
            kwargs['transitiontime'] = self.transitiontime
            _LOGGER.debug("Setting with transitiontime = {} ds {} s"
                          .format(self.transitiontime,
                                  float(self.transitiontime) / 10))

            if (args[0] == "on" and args[1] is False) or (
                        kwargs.get("on", True) is False):
                self._reset_bri_after_on = True

        resp = await self.bridge.set_light(self.light_id, *args, **kwargs)

        return resp

    async def get_name(self):
        self._name = await self._get("name")

        return self._name

    async def set_name(self, name):
        old_name = await self.get_name()
        self._name = name
        await self._set("name", self._name)
        _LOGGER.debug("Renaming light from {} to {}".format(old_name,
                                                            self._name))

        self.bridge.lights_by_name[self._name] = self
        del self.bridge.lights_by_name[old_name]

    async def is_on(self):
        self._on = await self._get("on")

        return self._on

    async def turn_on(self):
        if self._on is False:
            if self._reset_bri_after_on:
                _LOGGER.warning(
                    "Light was turned off with transitionstime specified, "
                    "brightness needs to be reset now")
                self.brightness = self._brightness
                self._reset_bri_after_on = False

        self._on = True
        await self._set("on", self._on)

    async def turn_off(self):
        if self._on:
            self._reset_bri_after_on = self.transitiontime is not None
            if self._reset_bri_after_on:
                _LOGGER.warning(
                    "Turned off light with transitiontime specified, "
                    "brightness will be reset on power on")

        self._on = False
        await self._set("on", self._on)

    async def get_colormode(self):
        self._colormode = await self._get("colormode")

        return self._colormode

    async def get_brightness(self):
        self._brightness = await self._get("bri")

        return self._brightness

    async def set_brightness(self, value):
        self._brightness = value
        await self._set("bri", self._brightness)

    async def get_hue(self):
        self._hue = await self._get("hue")

        return self._hue

    async def set_hue(self, value):
        self._hue = int(value)
        await self._set("hue", value)

    async def get_saturation(self):
        self._saturation = await self._get("sat")

        return self._saturation

    async def set_saturation(self, value):
        self._saturation = value
        await self._set("sat", self._saturation)

    async def get_xy(self):
        self._xy = await self._get("xy")

        return self._xy

    async def set_xy(self, value):
        self._xy = value
        await self._set("xy", self._xy)

    async def get_colortemp(self):
        self._colortemp = await self._get("ct")

        return self._colortemp

    async def set_colortemp(self, value):
        if value < 154:
            _LOGGER.warning("154 mireds is coolest allowed color temp")
            value = 154
        elif value > 500:
            _LOGGER.warning("500 mireds is warmest allowed color temp")
            value = 500

        self._colortemp = value
        await self._set("ct", self._colortemp)

    async def get_colortemp_k(self):
        ct = await self.get_colortemp()

        return int(round(1e6 / ct))

    async def set_colortemp_k(self, value):
        if value > 6500:
            _LOGGER.warning("6500 K is warmest allowed color temp")
            value = 6500
        elif value < 2000:
            _LOGGER.warning("2000 K is coolest allowed color temp")
            value = 2000

        colortemp_mireds = int(round(1e6 / value))
        _LOGGER.debug("{} k is {} mireds".format(value, colortemp_mireds))
        await self.set_colortemp(colortemp_mireds)

    async def get_effect(self):
        self._effect = await self._get("effect")

        return self._effect

    async def set_effect(self, value):
        self._effect = value
        await self._set("effect", self._effect)

    async def get_alert(self):
        self._alert = await self._get("alert")

        return self._alert

    async def set_alert(self, value):
        if value is None:
            value = "none"

        self._alert = value
        await self._set("alert", self._alert)

    async def is_reachable(self):
        self._reachable = await self._get("reachable")

        return self._reachable

    async def get_type(self):
        self._type = await self._get("type")

        return self._type

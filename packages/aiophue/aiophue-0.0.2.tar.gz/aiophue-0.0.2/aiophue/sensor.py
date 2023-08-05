import logging

import phue

_LOGGER = logging.getLogger(__name__)


class AioDict(object):
    def __init__(self):
        self._data = {}

    async def set(self, key, value):
        self._data[key] = value

    async def get(self, key, default=None):
        if key in self._data:
            return self._data[key]
        else:
            return default

    async def delete(self, key):
        del self._data

    async def clear(self):
        return self._data.clear()

    async def update(self, **kwargs):
        return self._data.update(**kwargs)


class AioSensorState(AioDict):
    def __init__(self, bridge, sensor_id):
        super().__init__()
        
        self._bridge = bridge
        self._sensor_id = sensor_id

    async def set(self, key, value):
        super(AioSensorState, self).set(key, value)
        await self._bridge.set_sensor_sate(self._sensor_id, self)


class AioSensorConfig(AioDict):
    def __init__(self, bridge, sensor_id):
        super().__init__()
        self._bridge = bridge
        self._sensor_id = sensor_id

    async def set(self, key, value):
        super(AioSensorConfig, self).set(key, value)
        await self._bridge.set_sensor_config(self._sensor_id, self)


class AioSensor(phue.Sensor):
    def __init__(self, bridge, sensor_id):
        super().__init__(bridge, sensor_id)

        self._state = AioSensorState(bridge, sensor_id)

    async def _get(self, *args, **kwargs):
        resp = await self.bridge.get_sensor(self.sensor_id, *args, **kwargs)

        return resp

    async def _set(self, *args, **kwargs):
        resp = await self.bridge.set_sensor(self.sensor_id, *args, **kwargs)

        return resp

    async def get_name(self):
        self._name = await self._get("name")

        return self._name

    async def set_name(self, value):
        old_name = self._name
        self._name = value
        await self._set("name", self._name)

        _LOGGER.debug("Renaming sensor from {} to {}".format(old_name, value))

    async def get_modelid(self):
        self._modelid = await self._get("modelid")

        return self._modelid

    async def get_swversion(self):
        self._swversion = await self._get("swversion")

        return self._swversion

    async def get_type(self):
        self._type = await self._get("type")

        return self._type

    async def get_uniqueid(self):
        self._uniqueid = await self._get("uniqueid")

        return self._uniqueid

    async def get_manufacturername(self):
        self._manufacturername = await self._get("manufacturername")

        return self._manufacturername

    async def get_state(self):
        data = await self._get("state")

        await self._state.clear()
        await self._state.update(**data)

        return self._state

    async def set_sate(self, data):
        await self._state.clear()
        await self._state.update(**data)

    async def get_config(self):
        data = await self._get("config")
        self._config.clear()
        self._config.update(**data)

    async def should_recycle(self):
        self._recycle = await self._get("manufacturername")

        return self._manufacturername


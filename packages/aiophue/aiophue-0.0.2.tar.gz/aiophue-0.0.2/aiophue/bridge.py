import asyncio
import json
import os
import logging
import platform

import aiohttp
import phue

from .group import AioGroup
from .light import AioLight

_LOGGER = logging.getLogger(__name__)


class AioBridge(object):
    def __init__(self, ip=None, username=None, config_file_path=None,
                 loop: asyncio.AbstractEventLoop = None):
        if config_file_path is not None:
            self.config_file_path = config_file_path
        elif os.getenv(phue.USER_HOME) is not None and os.access(
                os.getenv(phue.USER_HOME), os.W_OK):
            self.config_file_path = os.path.join(os.getenv(phue.USER_HOME),
                                                 '.python_hue')
        elif 'iPad' in platform.machine() or 'iPhone' in platform.machine() \
                or 'iPad' in platform.machine():
            self.config_file_path = os.path.join(os.getenv(phue.USER_HOME),
                                                 'Documents', '.python_hue')
        else:
            self.config_file_path = os.path.join(os.getcwd(), '.python_hue')

        self.ip = ip
        self.username = username
        self.lights_by_id = {}
        self.lights_by_name = {}
        self.sensors_by_id = {}
        self.sensors_by_name = {}
        self._name = None

        self.loop = loop or asyncio.get_event_loop()

    @classmethod
    async def get_bridge(cls, ip: str = None, username: str = None,
                         config_file_path: str = None):
        bridge = cls(ip=ip, username=username,
                     config_file_path=config_file_path)
        await bridge.connect()

        return bridge

    async def get_name(self):
        path = "/api/{}/config".format(self.username)
        data = {'name': self._name}
        response = await self.request(address=path, data=data)
        if response.get("name", False):
            self._name = response.get("name")
        else:
            raise ValueError

        return self._name

    async def set_name(self, name):
        self._name = name
        path = "/api/{}/config".format(self.username)
        data = {'name': self._name}
        await self.request('PUT', address=path, data=data)

    async def request(self, mode='GET', address=None, data=None):
        address = "http://{}{}".format(self.ip, address)
        if data is None:
            _LOGGER.debug("Calling {} without data".format(address))
        else:
            _LOGGER.debug("Calling {} with {}".format(address, str(data)))
        async with aiohttp.ClientSession(conn_timeout=10) as session:
            resp = await session.request(mode, address, json=data)

        decoded_response = await resp.json()

        return decoded_response

    async def get_ip_address(self, set_result=False):
        response = await self.request(address='www.meethue.com/api/nupnp')

        ip = response[0].get("internalipaddress", None)
        if ip is not None:
            if set_result:
                self.ip = ip
                _LOGGER.debug("IP address is now {}".format(self.ip))
        else:
            ip = False

        return ip

    async def register_app(self):
        data = {'devicetype': "aiophue"}
        response = await self.request("POST", "/api", data)
        for line in response:
            for status, payload in line.items():
                if status == "success":
                    # TODO: Async file operation
                    with open(self.config_file_path, 'w') as f:
                        _LOGGER.info("Writing configuration file to {}".format(
                            self.config_file_path))
                        f.write(json.dumps({self.ip: payload}))
                    await self.connect()

                if status == "error":
                    error_type = payload['type']
                    if error_type == 101:
                        raise phue.PhueRegistrationException(
                            error_type, payload['description'])
                    else:
                        raise phue.PhueException(
                            error_type, payload['description'])

    async def connect(self):
        _LOGGER.info("Attempting to connect to the bridge...")
        if self.ip is not None and self.username is not None:
            _LOGGER.info("Using IP: {}".format(self.ip))
            _LOGGER.info("Using username: {}".format(self.username))
        else:
            try:
                # TODO: Async file operation
                with open(self.config_file_path) as f:
                    config = json.loads(f.read())
                    if self.ip is None:
                        self.ip = list(config.keys())[0]
                        _LOGGER.debug("Using IP from config: {}"
                                      .format(self.ip))
                    else:
                        _LOGGER.debug("Using IP: {}".format(self.ip))

                    if self.username is None:
                        self.username = config[self.ip]['username']
                        _LOGGER.debug("Using username from config: {}"
                                      .format(self.username))
                    else:
                        _LOGGER.debug("Using username: {}"
                                      .format(self.username))
            except Exception:
                _LOGGER.info("Error opening {}, will attempt bridge "
                             "registration".format(self.config_file_path))
                await self.register_app()

    async def get_api(self):
        path = "/api/{}".format(self.username)
        response = await self.request(address=path)

        return response

    # Lights

    async def set_light(self, light_id, parameter, value=None,
                        transitiontime=None):
        if isinstance(parameter, dict):
            data = parameter
        else:
            data = {parameter: value}

        if transitiontime is not None:
            data['transitiontime'] = int(round(transitiontime))

        light_ids = light_id
        if isinstance(light_id, int) or phue.is_string(light_id):
            light_ids = [light_id, ]

        result = []
        for light in light_ids:
            _LOGGER.debug(str(data))
            if parameter == "name":
                path = "/api/{}/lights/{}".format(self.username, str(light_id))
                resp = await self.request("PUT", address=path, data=data)

                result.append(resp)
            else:
                if phue.is_string(light):
                    converted_light = await self.get_light_id_by_name(light)
                else:
                    converted_light = light

                    path = "/api/{}/lights/{}/state" \
                        .format(self.username, str(converted_light))
                    resp = await self.request("PUT", address=path, data=data)
                    result.append(resp)

            if "error" in list(result[-1][0].keys()):
                _LOGGER.warning("ERROR: {} for light {}".format(
                    result[-1][0]['error']['description'], light
                ))

            _LOGGER.debug(result)

            return result

    async def get_light(self, light_id=None, parameter=None):
        if phue.is_string(light_id):
            light_id = await self.get_light_id_by_name(light_id)

        if light_id is None:
            path = "/api/{}/lights/".format(self.username)
            response = await self.request(address=path)

            return response
        path = "/api/{}/lights/{}".format(self.username, str(light_id))
        state = await self.request(address=path)
        if parameter is None:
            return state

        if parameter in ["name", "type", "uniqueid", "swversion"]:
            return state[parameter]
        else:
            try:
                return state['state'][parameter]
            except KeyError as e:
                raise KeyError("Not a valid key, parameter {} is not "
                               "associated with light {}"
                               .format(parameter, light_id))

    async def get_light_id_by_name(self, name):
        lights = await self.get_light()
        for light_id in lights:
            if name == lights[lights]['name']:
                return light_id

        return False

    async def get_light_objects(self, mode='list'):
        if self.lights_by_id == {}:
            path = "/api/{}/lights/".format(self.username)
            resp = await self.request(address=path)
            for light_id in resp:
                light = AioLight(self, int(light_id))
                name = await light.get_name()

                self.lights_by_id[int(light_id)] = light
                self.lights_by_name[name] = light

        if mode == "id":
            return self.lights_by_id
        elif mode == "name":
            return self.lights_by_name
        elif mode == "list":
            return [self.lights_by_id[_id]
                    for _id
                    in sorted(self.lights_by_id)]

    # Groups
    async def get_groups(self):
        groups = await self.get_group()

        return [AioGroup(self, int(group_id))
                for group_id in groups.keys()]

    async def get_group(self, group_id=None, parameter=None):
        if phue.is_string(group_id):
            group_id = await self.get_group_id_by_name(name)
        if group_id is False:
            _LOGGER.error("Group name {} does not exist".format(group_id))

        if group_id is None:
            path = "/api/{}/groups/".format(self.username)
            resp = await self.request(address=path)
        else:
            path = "/api/{}/groups/{}".format(self.username, str(group_id))
            resp = await self.request(address=path)
            if parameter == "name" or parameter == "lights":
                resp = resp[parameter]
            else:
                resp = resp['action'][parameter]

        return resp

    async def set_group(self, group_id, parameter, value=None,
                        transitiontime=None):
        if isinstance(parameter, dict):
            data = parameter
        elif parameter == "lights" and (isinstance(value, (list, int))):
            if isinstance(value, int):
                value = [value, ]
            data = {parameter: [str(v) for v in value]}
        else:
            data = {parameter: value}

        if transitiontime is not None:
            data['transitiontime'] = int(round(transitiontime))

        group_ids = group_id
        if isinstance(group_id, int) or phue.is_string(group_id):
            group_ids = [group_id, ]

        result = []
        for group in group_ids:
            _LOGGER.debug(str(data))
            if phue.is_string(group):
                converted_group = await self.get_group_id_by_name(group)
            else:
                converted_group = group

            if converted_group is False:
                _LOGGER.error("Group name {} does not exist"
                              .format(converted_group))

                return
            if parameter == "name" or parameter == "lights":
                path = "/api/{}/groups/{}".format(self.username,
                                                  str(converted_group))
                resp = await self.request("PUT", address=path, data=data)
            else:
                path = "/api/{}/groups/{}/action".format(self.username,
                                                         str(converted_group))
                resp = await self.request("PUT", address=path, data=data)
            result.append(resp)

        if "error" in list(result[-1][0].keys()):
            _LOGGER.warning("ERROR: {} for group {}"
                            .format(result[-1][0]['error']['description'],
                                    group_id))
        _LOGGER.debug(result)

        return result

    async def create_group(self, name, lights=None):
        data = {
            'lights': [str(light) for light in lights],
            'name': name
        }
        path = "/api/{}/groups/".format(self.username)
        resp = await self.request("POST", address=path, data=data)

        return data

    async def delete_group(self, group_id):
        path = "/api/{}/groups/{}".format(self.username, group_id)
        resp = await self.request("DELETE", address=path)

    # Sensors

    async def get_sensor(self, sensor_id=None, parameter=None):
        if phue.is_string(sensor_id):
            sensor_id = await self.get_sensor_id_by_name(sensor_id)

        if sensor_id is None:
            path = "/api/{}/sensors".format(self.username)
            resp = await self.request(address=path)

            return resp

        path = "/api/{}/sensors/{}".format(self.username, str(sensor_id))
        data = await self.request(address=path)

        if isinstance(data, list):
            _LOGGER.debug(
                "Unable to read sensor wiht ID {}: {}".format(sensor_id,
                                                              repr(data)))
            return

        if parameter is None:
            return data

        return data[parameter]

    async def set_sensor(self, sensor_id, parameter, value=None):
        if isinstance(parameter, dict):
            data = parameter
        else:
            data = {parameter: value}

        result = None
        _LOGGER.debug(str(data))
        path = "/api/{}/sensors/{}".format(self.username, str(sensor_id))
        result = await self.request("PUT", address=path, data=data)

        if "error" in list(result[0].keys()):
            _LOGGER.warning("ERROR: {0} for sensor {1}".format(
                result[0]['error']['description'], sensor_id))
        _LOGGER.debug(result)

        return result

    async def set_sensor_state(self, sensor_id, parameter, value=None):
        await self.set_sensor_content(sensor_id, parameter, value, "state")

    async def set_sensor_config(self, sensor_id, parameter, value=None):
        await self.set_sensor_content(sensor_id, parameter, value, "config")

    async def set_sensor_content(self, sensor_id, parameter, value=None,
                                 structure="state"):
        if structure != "state" and structure != "config":
            raise ValueError(
                "set_sensor_content expects structure 'state' or 'config'.")

        if isinstance(parameter, dict):
            data = parameter.copy()
        else:
            data = {parameter: value}

        if "lastupdated" in data:
            del data['lastupdated']

        result = None
        _LOGGER.debug(str(data))
        path = "/api/{}/sensors/{}/{}".format(self.username, str(sensor_id),
                                              structure)
        result = await self.request("PUT", path, data)

        if "error" in list(result[0].keys()):
            _LOGGER.warning("ERROR: {} for sensor {}".format(
                result[0]['error']['description'], sensor_id))
        _LOGGER.debug(result)

        return result

    async def delete_sensor(self, sensor_id):
        try:
            name = await self.sensors_by_id[sensor_id].get_name()
            del self.sensors_by_name[name]
            del self.sensors_by_id[sensor_id]

            path = "/api/{}/sensors/{}".format(self.username, str(sensor_id))
            resp = await self.request("DELETE", path)

            return resp
        except Exception:
            _LOGGER.warning(
                "Unable to delete non existent sensor with ID {}".format(
                    sensor_id))

    # Scenes
    async def get_scenes(self):
        scenes = await self.get_scene()

        return [phue.Scene(k, **v) for k, v in scenes.items()]

    async def get_scene(self):
        path = "/api/{}/scenes".format(self.username)
        resp = await self.request(address=path)

        return resp

    async def activate_scene(self, group_id, scene_id):
        path = "/api/{}/groups/{}/action".format(self.username, str(group_id))
        resp = await self.request("PUT", path, {'scene': scene_id})

    async def run_scene(self, group_name, scene_name):
        groups = await self.get_groups()
        groups = [g for g in groups if await g.get_name() == group_name]
        if len(groups) != 1:
            raise ValueError(
                "More than 1 group with name {}".format(group_name))
        group = groups[0]

        scenes = await self.get_scenes()
        scenes = [s for s in scenes if await s.name == group_name]
        if len(scenes) == 0:
            raise ValueError("No scene found with name {}".format(scene_name))

        if len(scenes) == 1:
            await self.activate_scene(group.group_id, scenes[0].scene_id)

        lights = await group.get_lights()
        group_lights = sorted([l.light_id for l in lights])
        for scene in scenes:
            if group_lights == scene.lights:
                await self.activate_scene(group.group_id, scene.scene_id)
                return

        _LOGGER.warning(
            "Did not find a scene {} that shared lights with {}".format(
                scene_name, group_name))

    # Schedules
    async def get_schedule(self, schedule_id=None, parameter=None):
        if schedule_id is None:
            path = "/api/{}/schedules".format(self.username)
        else:
            path = "/api/{}/schedules/{}".format(self.username,
                                                 str(schedule_id))
        resp = await self.request(address=path)

        return resp

    async def create_schedule(self, name, time, light_id, data,
                              description=' '):
        schedule = {
            'name': name,
            'localtime': time,
            'description': description,
            'command':
                {
                    'method': 'PUT',
                    'address': "/api/{}/lights/{}/state"
                        .format(self.username, str(light_id)),
                    'body': data
                }
        }
        path = "/api/{}/schedules".format(self.username)
        resp = await self.request("POST", path)

        return resp

    async def set_schedule_attributes(self, schedule_id, attributes):
        path = "/api/{}/schedules/{}".format(self.username, str(schedule_id))
        resp = await self.request("PUT", path, data=attributes)

    async def create_group_schedule(self, name, time, group_id, data,
                                    description=' '):
        schedule = {
            'name': name,
            'localtime': time,
            'description': description,
            'command':
                {
                    'method': 'PUT',
                    'address': "/api/{}/groups/{}/action"
                        .format(self.username, str(group_id)),
                    'body': data
                }
        }
        path = "/api/{}/schedules".format(self.username)
        resp = await self.request("POST", path, schedule)

        return resp

    async def delete_schedule(self, schedule_id):
        path = "/api/{}/schedules/{}".format(self.username, schedule_id)
        resp = await self.request("DELETE", path)

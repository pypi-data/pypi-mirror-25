import asyncio
import logging
from typing import List, Union, Set, Dict

import yaml
from aiolifxc.aiolifx import Lights, Light, Color, DeviceOffline

from robotica.outputs import Output
from robotica.types import Action

logger = logging.getLogger(__name__)


class LifxOutput(Output):
    def __init__(self, loop: asyncio.AbstractEventLoop, config: Dict) -> None:
        self._loop = loop
        self._config = config
        self._disabled = self._config['disabled']
        self._lights = Lights(loop=self._loop)
        self._locations = self._config.get('locations', {}) or {}

    def start(self) -> None:
        if not self._disabled:
            logger.debug("LIFX enabled.")
            self._task = self._lights.start_discover()

    def stop(self) -> None:
        if not self._disabled:
            self._task.cancel()

    def _get_labels_for_locations(self, locations: Set[str]) -> Set[str]:
        labels = set()  # type: Set[str]
        if self._disabled:
            return set()
        for location in locations:
            labels = labels | set(self._locations.get(location, []))
        return labels

    def is_action_required_for_locations(self, locations: Set[str], action: Action) -> bool:
        labels = self._get_labels_for_locations(locations)
        if len(labels) == 0:
            return False

        if 'lights' in action:
            return True

        return False

    async def execute(self, locations: Set[str], action: Action) -> None:
        if 'lights' in action:
            lights = action['lights']

            lights_action = lights['action']
            if lights_action == "flash":
                await self.flash(locations=locations)
            elif lights_action == "wake_up":
                await self.wake_up(locations=locations)
            elif lights_action == "turn_off":
                await self.turn_off(locations=locations)
            else:
                logger.error("Unknown action '%s'.", action)

    def _get_lights_from_locations(self, locations: Set[str]) -> Lights:
        labels = self._get_labels_for_locations(locations)
        lights = self._lights.get_by_lists(labels=list(labels))  # type: Lights
        return lights

    async def wake_up(self, locations: Set[str]) -> None:
        async def single_device(device: Light) -> None:
            try:
                power = await device.get_power()
                if not power:
                    await device.set_color(
                        Color(hue=0, saturation=0, brightness=0, kelvin=2500))
                await device.set_power(True)
                await device.set_color(
                    Color(hue=0, saturation=0, brightness=100, kelvin=2500),
                    duration=60000)
            except DeviceOffline:
                logger.error("Light is offline %s.", device)

        lights = self._get_lights_from_locations(locations)
        logger.info("Lifx wakeup for lights %s.", lights)
        await lights.do_for_every_device(Light, single_device)

    async def flash(self, locations: Set[str]) -> None:
        lights = self._get_lights_from_locations(locations)
        logger.info("Lifx flash for lights %s.", lights)
        await lights.set_waveform(
            color=Color(hue=0, saturation=100, brightness=100, kelvin=3500),
            transient=1,
            period=1000,
            cycles=2,
            duty_cycle=0,
            waveform=0,
        )

    async def turn_off(self, locations: Set[str]) -> None:
        lights = self._get_lights_from_locations(locations)
        logger.info("Lifx flash for lights %s.", lights)
        await lights.set_light_power(False)

"""
KMP Pellet Heater Controller

Tested against KMP Mysinge v0.43, but should work with all KMP pellet heaters with the same control unit.
"""

from . import constants
from html import unescape
from http.client import HTTPConnection, HTTPException
from ipaddress import IPv4Address, IPv6Address
from json import loads as json_loads
from time import sleep

class KMPHeater:
    def __init__(self, host: IPv4Address | IPv6Address) -> None:
        self.host = host

    def _doit(self, action: int) -> int:
        """
        Calls the heater's "doit" fuctions to perform an action.

        Parameters
        ----------
        action : int
            The action code of the action to be perfomed. See `kmp.constants`.

        Returns
        -------
        int
            The response status code of the HTTP request. Should be 200 for OK.
        """
        connection = HTTPConnection(str(self.host), 80, timeout=10)
        connection.request("GET", f"/doit?todo={str(action)}")
        response = connection.getresponse()
        connection.close()
        return response.status
        
    def readData(self, page = constants.STATUS):
        connection = HTTPConnection(str(self.host), 80, timeout=10)
        connection.request("GET", page)
        response = connection.getresponse()
        
        # print(f"Status: {response.status} and reason: {response.reason}\n")
        if response.status != 200:
            raise HTTPException()
        data = response.read().decode("utf-8")
        data = unescape(str(data))
        data = json_loads(data)

        connection.close()
        return data

    def get_targetTemp(self) -> int:
        """
        Returns the target room temperature in °C
        """
        return int(self.readData()["tStop"])
    
    def power_toggle(self):
        """
        Toggles the power of the heater.
        """
        self._doit(constants.START_STOP)

    def temperature_down(self):
        """
        Lowers the target room temperature in °C by 1.
        """
        self._doit(constants.TEMP_DOWN)

    def temperature_up(self):
        """
        Raises the target room temperature in °C by 1.
        """
        self._doit(constants.TEMP_UP)

    def set_temperature(self, newTargetTemp: int):
        """
        Sets the target room temperature for the heater.

        Parameters
        ----------
        newTargetTemp : int
            The new target room temperature in °C
        """
        while (newTargetTemp != self.get_targetTemp()):
            if newTargetTemp < self.get_targetTemp():
                self.temperature_down()
            else:
                self.temperature_up()
            sleep(0.250)    # 0.250 seems to work, 0.200 overshoots the target
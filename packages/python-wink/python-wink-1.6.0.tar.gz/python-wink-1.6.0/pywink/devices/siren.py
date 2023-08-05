from pywink.devices.base import WinkDevice


class WinkSiren(WinkDevice):
    """
    Represents a Wink Siren.
    """

    def state(self):
        return self._last_reading.get('powered', False)

    def mode(self):
        return self._last_reading.get('mode', None)

    def auto_shutoff(self):
        return self._last_reading.get('auto_shutoff', None)

    def set_mode(self, mode):
        """
        :param mode:  a str, one of [siren_only, strobe_only, siren_and_strobe]
        :return: nothing
        """
        values = {
            "desired_state": {
                "mode": mode
            }
        }
        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)

    def set_auto_shutoff(self, timer):
        """
        :param time: an int, one of [None (never), 30, 60, 120]
        :return: nothing
        """
        values = {
            "desired_state": {
                "auto_shutoff": timer
            }
        }
        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)

    def update_state(self):
        """
        Update state with latest info from Wink API.
        """
        response = self.api_interface.get_device_state(self)
        return self._update_state_from_response(response)

    def set_state(self, state):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        values = {"desired_state": {"powered": state}}
        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)

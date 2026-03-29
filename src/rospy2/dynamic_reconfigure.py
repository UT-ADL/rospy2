"""
Compatibility shim for dynamic_reconfigure on ROS 2.

Provides a Server class that mirrors the ROS 1 dynamic_reconfigure.server.Server
interface using the native ROS 2 parameter callback mechanism.

The Config class argument is accepted but ignored -- on ROS 2, parameters are
already declared via rospy2.get_param() and managed by the native parameter system.
The callback receives an attribute-access config object and a dummy level=0,
matching the ROS 1 signature: callback(config, level) -> config.
"""

from rcl_interfaces.msg import SetParametersResult


class _Config:
    """Attribute-access wrapper over a dict of parameter values."""
    def __init__(self, params_dict):
        self.__dict__.update(params_dict)

    def __getattr__(self, name):
        raise AttributeError("Config has no parameter '%s'" % name)


class Server:
    def __init__(self, config_type, callback):
        import rospy2
        self._callback = callback
        self._node = rospy2._node

        # Initial call with current values (matches ROS 1 behavior)
        current = self._get_current_params()
        config = _Config(current)
        self._callback(config, 0)

        # Register for future changes
        self._node.add_on_set_parameters_callback(self._on_params_changed)

    def _get_current_params(self):
        params = {}
        for name, param in self._node._parameters.items():
            if param.value is not None:
                params[name] = param.value
        return params

    def _on_params_changed(self, params):
        current = self._get_current_params()
        # Apply incoming changes
        for p in params:
            current[p.name] = p.value
        config = _Config(current)
        self._callback(config, 0)
        return SetParametersResult(successful=True)


# Expose as dynamic_reconfigure.server.Server
class _ServerModule:
    Server = Server

server = _ServerModule()

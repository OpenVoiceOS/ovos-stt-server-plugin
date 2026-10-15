# Licensed under the Apache License, Version 2.0
"""Every declared entry point must load the object it names.

`ovos-stt-plugin-server.config` named `OVOSHTTPServerSTTConfig`, which this
package did not define. The metadata carries a name whether or not the
attribute exists, so nothing caught it: `opm.stt.config` was empty in practice,
and `get_stt_module_configs("ovos-stt-plugin-server")` raised
`AttributeError: 'NoneType' object has no attribute 'items'`, because OPM calls
`.items()` on whatever the entry point loads.

These rows read the installed distribution's own metadata rather than a list
written here, so an entry point added later is covered the day it is added.
"""
import importlib.metadata as md

import pytest

DISTRIBUTION = "ovos-stt-plugin-server"

# The base each group promises. A `.config` group promises a mapping instead,
# which is why it is absent here and checked separately below.
EXPECTED_BASES = {
    "opm.stt": "STT",
    "opm.transformer.audio": "AudioLanguageDetector",
}


def _declared():
    """Return (group, name, value) for every entry point this package ships."""
    eps = md.distribution(DISTRIBUTION).entry_points
    return [(ep.group, ep.name, ep.value) for ep in eps]


def _entry_point(group, name):
    return next(e for e in md.distribution(DISTRIBUTION).entry_points
                if e.group == group and e.name == name)


def test_the_package_declares_entry_points():
    """A guard on the guard: an empty list would pass every row below."""
    assert len(_declared()) == 3, _declared()


@pytest.mark.parametrize("group,name,value", _declared())
def test_entry_point_loads(group, name, value):
    """Loading must not raise, whatever the group promises."""
    _entry_point(group, name).load()


@pytest.mark.parametrize("group,name,value", _declared())
def test_entry_point_is_what_its_group_promises(group, name, value):
    """A name can load and still be the wrong kind of object.

    A class group must give a subclass of its base, so the audio entry point
    cannot quietly be pointed at the STT class. A `.config` group must give a
    mapping, because OPM calls `.items()` on it.
    """
    obj = _entry_point(group, name).load()
    if group.endswith(".config"):
        assert hasattr(obj, "items"), \
            f"{name} loaded {obj!r}, which OPM cannot call .items() on"
        return
    bases = [b.__name__ for b in obj.__mro__]
    assert EXPECTED_BASES[group] in bases, \
        f"{name} is a {bases[0]}, which is not a {EXPECTED_BASES[group]}"


def test_opm_lists_the_config_group():
    """OPM's own loader, not importlib: the group must not be empty."""
    from ovos_plugin_manager.utils import PluginConfigTypes, find_plugins
    assert "ovos-stt-plugin-server.config" in find_plugins(PluginConfigTypes.STT)


def test_opm_can_read_this_plugin_s_configs():
    """The call that raised. It must answer a mapping, empty or not."""
    from ovos_plugin_manager.stt import get_stt_module_configs
    assert get_stt_module_configs("ovos-stt-plugin-server") == {}

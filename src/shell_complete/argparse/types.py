# -*- coding=utf-8 -*-
r"""
https://salsa.debian.org/debian/bash-completion/blob/master/bash_completion
"""
from .code import ShellCode


__all__ = [
    'associate', 'new_pseudo_type',
    'path', 'file', 'directory',
    'mac_address', 'ip_address', 'ipv4_address', 'ipv6_address',
    'network_interface',
    'uid', 'gid',
    'service',
    'user_group', 'user_at_host', 'known_hosts',
]


def associate(completer, to=None):
    r"""
    association decorator

    @associate(types.directory)
    def dir(value: str) -> pathlib.Path:
        return pathlib.Path(value)

    dir = associate(types.directory, to=pathlib.Path)
    """
    if hasattr(completer, '__completer__'):
        completer = completer.__completer__

    def decorator(fn):
        fn.__completion__ = completer
        return fn

    if to:
        return decorator(to)
    else:
        return decorator


def new_pseudo_type(completer: ShellCode, fn=None):
    r"""
    creates a new association

    pass_through_type = new_association(ShellCode("<shell-code>"))
    integer_type = new_association(Recommended(1, 2, 3), int)
    """
    if fn is None:
        fn = lambda v: v  # noqa
    fn.__completer__ = completer
    return fn


path = new_pseudo_type(ShellCode('_filedir'))
file = new_pseudo_type(ShellCode('_filedir'))
directory = new_pseudo_type(ShellCode('_filedir -d'))

mac_address = new_pseudo_type(ShellCode('_mac_addresses'))
ip_address = new_pseudo_type(ShellCode('_ip_addresses -a'))
ipv4_address = new_pseudo_type(ShellCode('_ip_addresses -4'))
ipv6_address = new_pseudo_type(ShellCode('_ip_addresses -6'))

network_interface = new_pseudo_type(ShellCode('_available_interfaces'))
inet_services = new_pseudo_type(ShellCode('_xinetd_services'))

uid = new_pseudo_type(ShellCode('_uids'))
gid = new_pseudo_type(ShellCode('_gids'))

service = new_pseudo_type(ShellCode('_services'))

user_group = new_pseudo_type(ShellCode('_usergroup -u'))  # user:group
user_at_host = new_pseudo_type(ShellCode('_user_at_host'))  # user@host
known_hosts = new_pseudo_type(ShellCode('_known_hosts_real -a "$cur"'))

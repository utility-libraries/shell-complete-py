# -*- coding=utf-8 -*-
r"""
https://salsa.debian.org/debian/bash-completion/blob/master/bash_completion
"""


__all__ = [
    'associate', 'new_association',
    'path', 'file', 'directory',
    'mac_address', 'ip_address', 'ipv4_address', 'ipv6_address',
    'network_interface',
    'uid', 'gid',
    'service',
    'user_group', 'user_at_host', 'known_hosts',
]


def associate(completion: str):
    r"""
    association decorator

    @associate(types.directory)
    def dir(value: str) -> pathlib.Path:
        return pathlib.Path(value)
    """
    if hasattr(completion, '__completion__'):
        completion = completion.__completion__

    def decorator(fn):
        fn.__completion__ = getattr(completion, '__completion__', completion)
        return fn

    return decorator


def new_association(completion: str):
    r"""
    creates a new association

    new_type = new_association("<shell-code>")
    """
    fn = lambda v: v  # noqa
    fn.__completion__ = getattr(completion, '__completion__', completion)
    return fn


path = new_association('_filedir')
file = new_association('_filedir')
directory = new_association('_filedir -d')

mac_address = new_association('_mac_addresses')
ip_address = new_association('_ip_addresses -a')
ipv4_address = new_association('_ip_addresses -4')
ipv6_address = new_association('_ip_addresses -6')

network_interface = new_association('_available_interfaces')
inet_services = new_association('_xinetd_services')

uid = new_association('_uids')
gid = new_association('_gids')

service = new_association('_services')

user_group = new_association('_usergroup -u')  # user:group
user_at_host = new_association('_user_at_host')  # user@host
known_hosts = new_association('_known_hosts_real -a "$cur"')

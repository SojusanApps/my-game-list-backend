from _typeshed import Incomplete

PORT_SPEC: Incomplete

def add_port_mapping(port_bindings: Incomplete, internal_port: Incomplete, external: Incomplete) -> None: ...
def add_port(port_bindings: Incomplete, internal_port_range: Incomplete, external_range: Incomplete) -> None: ...
def build_port_bindings(ports: Incomplete) -> Incomplete: ...
def port_range(
    start: Incomplete, end: Incomplete, proto: Incomplete, randomly_available_port: bool = ...
) -> Incomplete: ...
def split_port(port: Incomplete) -> Incomplete: ...

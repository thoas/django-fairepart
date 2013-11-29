def get_backends():
    from ..settings import BACKENDS
    from ..utils import load_class

    backends = {}

    for backend_path in BACKENDS:
        backend = load_class(backend_path)
        backends[backend.name] = backend

    return backends

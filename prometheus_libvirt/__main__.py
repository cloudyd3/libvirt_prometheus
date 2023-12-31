import asyncio
import logging
import threading
from wsgiref.simple_server import make_server


import libvirt
from prometheus_client import (
    REGISTRY,
    GC_COLLECTOR,
    PROCESS_COLLECTOR,
    PLATFORM_COLLECTOR,
    make_wsgi_app,
)

from prometheus_libvirt.domain_worker import DomainWorker
from prometheus_libvirt.storage_pool_worker import StoragePoolWorker
from . import prometheus_desc


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)

REGISTRY.unregister(GC_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(PROCESS_COLLECTOR)

conn = libvirt.open("qemu:///system")
hypervisor_version_num = conn.getVersion()
hypervisor_version = "%s.%s.%s" % (
    int(hypervisor_version_num / 1000000 % 1000),
    int(hypervisor_version_num / 1000 % 1000),
    int(hypervisor_version_num % 1000),
)
libvirtd_version_num = conn.getLibVersion()
libvirtd_version = "%s.%s.%s" % (
    int(libvirtd_version_num / 1000000 % 1000),
    int(libvirtd_version_num / 1000 % 1000),
    int(libvirtd_version_num % 1000),
)
lib_version_num = libvirt.getVersion()
lib_version = "%s.%s.%s" % (
    int(lib_version_num / 1000000 % 1000),
    int(lib_version_num / 1000 % 1000),
    int(lib_version_num % 1000),
)

prometheus_desc.libvirt_versions_info.labels(
    hypervisor=hypervisor_version,
    libvirtd=libvirtd_version,
    libvirt_lib=lib_version,
)


def run_server():
    app = make_wsgi_app(registry=REGISTRY, disable_compression=True)
    httpd = make_server("0.0.0.0", 8000, app)
    t = threading.Thread(target=httpd.serve_forever)
    t.daemon = True
    t.start()


if __name__ == "__main__":
    run_server()
    domain_worker = DomainWorker(conn=conn)
    storage_pool_worker = StoragePoolWorker(conn=conn)
    loop = asyncio.get_event_loop()
    loop.create_task(domain_worker.run())
    loop.create_task(storage_pool_worker.run())
    loop.run_forever()

import asyncio
import logging
import threading
from wsgiref.simple_server import make_server

from flask import Flask, Response, request

from keystoneauth1 import session, exceptions
from keystoneclient.v3 import client

import libvirt
from prometheus_client import (
    REGISTRY,
    GC_COLLECTOR,
    PROCESS_COLLECTOR,
    PLATFORM_COLLECTOR,
    generate_latest,
)

from prometheus_libvirt.domain_worker import DomainWorker
from prometheus_libvirt.storage_pool_worker import StoragePoolWorker
from . import prometheus_desc, conf


CONF = conf.CONF()
CONF.load_from_file()

auth = CONF.authenticate()

sess = session.Session(auth=auth)
keystone = client.Client(session=sess)

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

app = Flask(__name__)

@app.route("/metrics", methods=['GET'])
def return_metrics():
    token = request.headers.get("X-Auth-Token")
    if not token:
        return Response(status=401, response="Authentication required")
    try:
        keystone.tokens.validate(token)
    except exceptions.http.NotFound as e:
        return Response(status=404, response=e.response.text)
    response = Response(response=generate_latest(REGISTRY), status=200, mimetype="application/openmetrics-text")
    return response


def run_server():
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

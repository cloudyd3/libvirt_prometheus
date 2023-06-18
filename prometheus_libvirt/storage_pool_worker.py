import asyncio
import logging

import libvirt

from prometheus_libvirt import prometheus_desc


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)

class StoragePoolWorker:
    def __init__(
            self,
            conn: libvirt.virConnect,
    ):
        self.conn = conn

    async def run(self):
        while True:
            pool_list = self.conn.listAllStoragePools(0)
            workers = [self.storage_pool_worker(pool) for pool in pool_list]
            await asyncio.gather(*workers, return_exceptions=False)
            await asyncio.sleep(5)

    async def storage_pool_worker(self, pool: libvirt.virStoragePool):
        pool_name = pool.name()
        pool_info = pool.info()
        pool_uuid = pool.UUIDString()
        prometheus_desc.libvirt_storage_pool_metadata.labels(
            pool_name=pool_name,
            pool_uuid=pool_uuid
        )
        prometheus_desc.libvirt_storage_pool_state.labels(
            pool_name=pool_name
        ).set(int(pool_info[0]))
        prometheus_desc.libvirt_storage_pool_capacity.labels(
            pool_name=pool_name
        ).set(int(pool_info[1]))
        prometheus_desc.libvirt_storage_pool_allocation.labels(
            pool_name=pool_name
        ).set(int(pool_info[2]))
        prometheus_desc.libvirt_storage_pool_available.labels(
            pool_name=pool_name
        ).set(int(pool_info[3]))

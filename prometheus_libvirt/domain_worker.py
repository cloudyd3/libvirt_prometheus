import asyncio
import time

import defusedxml.ElementTree as ET
import libvirt
import xmltodict

from prometheus_libvirt import prometheus_desc

# noinspection PyProtectedMember
class DomainWorker:
    __slots__ = "conn"

    def __init__(
        self,
        conn: libvirt.virConnect,
    ):
        self.conn = conn

    async def run(self):
        while True:
            domain_list = await asyncio.to_thread(self.conn.listAllDomains, 0)
            workers = [self.worker(domain) for domain in domain_list]
            await asyncio.gather(*workers, return_exceptions=True)

    async def worker(self, domain: libvirt.virDomain):
        domain_name = domain.name()
        domain_info = domain.info()
        prometheus_desc.libvirt_domain_metadata.labels(
            domain=domain_name,
            uuid=domain.UUIDString(),
        )
        prometheus_desc.libvirt_domain_state.labels(domain=domain_name).set(
            domain_info[0]
        )
        prometheus_desc.libvirt_domain_vcpus.labels(domain=domain_name).set(
            domain_info[3]
        )
        dom_xml = xmltodict.parse(domain.XMLDesc(0))
        if "nova:instance" in dom_xml["domain"]["metadata"]:
            nova_meta = dom_xml["domain"]["metadata"]["nova:instance"]
            nova_owner = nova_meta["nova:owner"]
            prometheus_desc.libvirt_domain_nova_metadata.labels(
                domain=domain.name(),
                uuid=domain.UUIDString(),
                instance_name=nova_meta["nova:name"],
                flavor=nova_meta["nova:flavor"]["@name"],
                user_name=nova_owner["nova:user"]["#text"],
                user_uuid=nova_owner["nova:user"]["@uuid"],
                project_name=nova_owner["nova:project"]["#text"],
                project_uuid=nova_owner["nova:project"]["@uuid"],
            )
        domain_coroutines = [
            self.cpu_helper(domain),
            self.mem_helper(domain),
            self.io_helper(domain),
            self.block_dev_helper(domain),
        ]
        await asyncio.gather(*domain_coroutines, return_exceptions=True)

    async def cpu_helper(self, domain: libvirt.virDomain):
        cpu_time_abs = 0
        cpu_system_time_abs = 0
        cpu_user_time_abs = 0
        if domain.isActive():
            cpu_info = domain.getCPUStats(True)
            cpu_time_abs = cpu_info[0]["cpu_time"]
            cpu_system_time_abs = cpu_info[0]["system_time"]
            cpu_user_time_abs = cpu_info[0]["user_time"]
        prometheus_desc.libvirt_domain_cpu_time.labels(domain=domain.name())._value.set(
            float(cpu_time_abs / 1000 / 1000 / 1000)
        )
        prometheus_desc.libvirt_domain_cpu_user_time.labels(
            domain=domain.name()
        )._value.set(float(cpu_user_time_abs / 1000 / 1000 / 1000))
        prometheus_desc.libvirt_domain_cpu_system_time.labels(
            domain=domain.name()
        )._value.set(float(cpu_system_time_abs / 1000 / 1000 / 1000))

    # noinspection PyProtectedMember
    async def mem_helper(self, domain: libvirt.virDomain):
        domain_name = domain.name()
        domain_info = domain.info()
        info = {}
        if domain.isActive():
            try:
                info = domain.memoryStats()
            except libvirt.libvirtError:
                pass
        prometheus_desc.libvirt_domain_max_memory_bytes.labels(domain=domain_name).set(
            domain_info[1] * 1024
        )
        prometheus_desc.libvirt_domain_mem_stat_usage_bytes.labels(
            domain=domain_name
        ).set(domain_info[2] * 1024)
        prometheus_desc.libvirt_domain_mem_stat_actual_balloon_bytes.labels(
            domain=domain_name
        ).set(int(info.get("actual", 0) * 1024))
        prometheus_desc.libvirt_domain_mem_stat_swap_in_bytes.labels(
            domain=domain_name
        )._value.set(int(info.get("swap_in", 0) * 1024))
        prometheus_desc.libvirt_domain_mem_stat_swap_out_bytes.labels(
            domain=domain_name
        )._value.set(int(info.get("swap_out", 0) * 1024))
        prometheus_desc.libvirt_domain_mem_stat_major_fault.labels(
            domain=domain_name
        )._value.set(info.get("major_fault", 0))
        prometheus_desc.libvirt_domain_mem_stat_minor_fault.labels(
            domain=domain_name
        )._value.set(info.get("minor_fault", 0))
        prometheus_desc.libvirt_domain_mem_stat_unused_bytes.labels(
            domain=domain_name
        ).set(int(info.get("unused", 0)))
        prometheus_desc.libvirt_domain_mem_stat_available_bytes.labels(
            domain=domain_name
        ).set(int(info.get("available", 0) * 1024))
        prometheus_desc.libvirt_domain_mem_stat_usable_bytes.labels(
            domain=domain_name
        ).set(int(info.get("usable", 0) * 1024))
        prometheus_desc.libvirt_domain_mem_stat_disk_caches_bytes.labels(
            domain=domain_name
        ).set(int(info.get("disk_caches", 0) * 1024))
        prometheus_desc.libvirt_domain_mem_stat_hugetlb_pgalloc.labels(
            domain=domain_name
        )._value.set(info.get("hugetlb_pgalloc", 0))
        prometheus_desc.libvirt_domain_mem_stat_hugetlb_pgfail.labels(
            domain=domain_name
        )._value.set(info.get("hugetlb_pgfail", 0))
        prometheus_desc.libvirt_domain_mem_stat_rss.labels(domain=domain_name).set(
            int(info.get("rss", 0) * 1024)
        )

    async def io_helper(self, domain: libvirt.virDomain):
        domain_name = domain.name()
        domain_xml = ET.fromstring(domain.XMLDesc(0))
        for interface in domain_xml.iter("interface"):
            stats = domain.interfaceStats(interface.find("target").attrib.get("dev"))
            dev_mac = interface.find("mac").attrib.get("address")
            prometheus_desc.libvirt_domain_io_rx_bytes.labels(
                domain=domain_name, dev_mac=dev_mac
            )._value.set(int(stats[0]))
            prometheus_desc.libvirt_domain_io_rx_packets.labels(
                domain=domain_name, dev_mac=dev_mac
            )._value.set(int(stats[1]))
            prometheus_desc.libvirt_domain_io_rx_errors.labels(
                domain=domain_name, dev_mac=dev_mac
            )._value.set(int(stats[2]))
            prometheus_desc.libvirt_domain_io_rx_drops.labels(
                domain=domain_name, dev_mac=dev_mac
            )._value.set(int(stats[3]))
            prometheus_desc.libvirt_domain_io_tx_bytes.labels(
                domain=domain_name, dev_mac=dev_mac
            )._value.set(int(stats[4]))
            prometheus_desc.libvirt_domain_io_tx_packets.labels(
                domain=domain_name, dev_mac=dev_mac
            )._value.set(int(stats[5]))
            prometheus_desc.libvirt_domain_io_tx_errors.labels(
                domain=domain_name, dev_mac=dev_mac
            )._value.set(int(stats[6]))
            prometheus_desc.libvirt_domain_io_tx_drops.labels(
                domain=domain_name, dev_mac=dev_mac
            )._value.set(int(stats[7]))

    async def block_dev_helper(self, domain: libvirt.virDomain):
        domain_name = domain.name()
        domain_xml = ET.fromstring(domain.XMLDesc(0))
        for disk in domain_xml.iter("disk"):
            stats_flagged = {}
            target_dev = disk.find("target").attrib.get("dev")
            if domain.isActive():
                try:
                    stats_flagged = domain.blockStatsFlags(target_dev)
                except libvirt.libvirtError:
                    pass
            prometheus_desc.libvirt_domain_block_dev_metadata.labels(
                domain=domain_name,
                disk_type=disk.attrib.get("type"),
                target_dev=disk.find("target").attrib.get("dev"),
                target_bus=disk.find("target").attrib.get("bus"),
                source_file=disk.find("source").attrib.get("file"),
                driver_name=disk.find("driver").attrib.get("name"),
                driver_type=disk.find("driver").attrib.get("type"),
                driver_discard=disk.find("driver").attrib.get("discard"),
            )
            prometheus_desc.libvirt_domain_block_dev_read_bytes.labels(
                domain=domain_name,
                target_dev=target_dev,
            )._value.set(stats_flagged.get("rd_bytes", 0))
            prometheus_desc.libvirt_domain_block_dev_read_operations.labels(
                domain=domain_name,
                target_dev=target_dev,
            )._value.set(stats_flagged.get("rd_operations", 0))
            prometheus_desc.libvirt_domain_block_dev_read_total_seconds.labels(
                domain=domain_name,
                target_dev=target_dev,
            )._value.set(
                float(stats_flagged.get("rd_total_times", 0) / 1000 / 1000 / 1000)
            )
            prometheus_desc.libvirt_domain_block_dev_write_bytes.labels(
                domain=domain_name,
                target_dev=target_dev,
            )._value.set(stats_flagged.get("wr_bytes", 0))
            prometheus_desc.libvirt_domain_block_dev_write_operations.labels(
                domain=domain_name,
                target_dev=target_dev,
            )._value.set(stats_flagged.get("wr_operations", 0))
            prometheus_desc.libvirt_domain_block_dev_write_total_seconds.labels(
                domain=domain_name,
                target_dev=target_dev,
            )._value.set(
                float(stats_flagged.get("wr_total_times", 0) / 1000 / 1000 / 1000)
            )
            prometheus_desc.libvirt_domain_block_dev_flush_operations.labels(
                domain=domain_name,
                target_dev=target_dev,
            )._value.set(stats_flagged.get("flush_operations", 0))
            prometheus_desc.libvirt_domain_block_dev_flush_total_seconds.labels(
                domain=domain_name,
                target_dev=target_dev,
            )._value.set(
                float(stats_flagged.get("flush_total_times", 0) / 1000 / 1000 / 1000)
            )

from prometheus_client import Gauge, Info, Counter

####
# General information
####

libvirt_versions_info = Info(
    namespace="libvirt",
    name="versions_info",
    documentation="Libvirt version information",
    labelnames=["hypervisor", "libvirtd", "libvirt_lib"],
)

####
# Storage pool
####

libvirt_storage_pool_metadata = Info(
    namespace="libvirt",
    subsystem="storage_pool",
    name="metadata",
    documentation="Libvirt storage pool information",
    labelnames=["pool_name", "pool_uuid"],
)

libvirt_storage_pool_state = Gauge(
    namespace="libvirt",
    subsystem="storage_pool",
    name="state",
    documentation="Storage pool state information",
    labelnames=["pool_name"],
)

libvirt_storage_pool_capacity = Gauge(
    namespace="libvirt",
    subsystem="storage_pool",
    name="capacity",
    documentation="Pool capacity, in bytes",
    unit="bytes",
    labelnames=["pool_name"],
)

libvirt_storage_pool_allocation = Gauge(
    namespace="libvirt",
    subsystem="storage_pool",
    name="allocation",
    documentation="Pool allocation, in bytes",
    unit="bytes",
    labelnames=["pool_name"],
)

libvirt_storage_pool_available = Gauge(
    namespace="libvirt",
    subsystem="storage_pool",
    name="available",
    documentation="Pool available space, in bytes",
    unit="bytes",
    labelnames=["pool_name"],
)

####
# Domain Info
####

libvirt_domain_metadata = Info(
    namespace="libvirt",
    subsystem="domain",
    name="metadata",
    documentation="Domain metadata",
    labelnames=[
        "domain",
        "uuid",
    ],
)

libvirt_domain_nova_metadata = Info(
    namespace="libvirt",
    subsystem="domain",
    name="nova_metadata",
    documentation="Openstack Nova metadata",
    labelnames=[
        "domain",
        "uuid",
        "instance_name",
        "flavor",
        "user_name",
        "user_uuid",
        "project_name",
        "project_uuid",
    ],
)

libvirt_domain_max_memory_bytes = Gauge(
    namespace="libvirt",
    subsystem="domain_info",
    name="max_memory_bytes",
    documentation="Maximum allowed memory of the domain, in bytes.",
    labelnames=["domain"],
    unit="bytes",
)

libvirt_domain_mem_stat_usage_bytes = Gauge(
    namespace="libvirt",
    subsystem="domain_info",
    name="memory_usage_bytes",
    documentation="Memory usage of the domain, in bytes.",
    labelnames=["domain"],
    unit="bytes",
)

libvirt_domain_vcpus = Gauge(
    namespace="libvirt",
    subsystem="domain_info",
    name="vcpus",
    documentation="Number of virtual CPUs on the domain.",
    labelnames=["domain"],
)

libvirt_domain_cpu_time = Counter(
    namespace="libvirt",
    subsystem="domain_info",
    name="cpu_time_seconds_total",
    documentation="Amount of CPU time used by the domain, in seconds.",
    labelnames=["domain"],
    unit="seconds",
)

libvirt_domain_cpu_user_time = Counter(
    namespace="libvirt",
    subsystem="domain_info",
    name="cpu_time_user_seconds_total",
    documentation="Amount of CPU time used by the domain by the user, in seconds.",
    labelnames=["domain"],
    unit="seconds",
)

libvirt_domain_cpu_system_time = Counter(
    namespace="libvirt",
    subsystem="domain_info",
    name="cpu_time_system_seconds_total",
    documentation="Amount of CPU time used by the domain by the system, in seconds.",
    labelnames=["domain"],
    unit="seconds",
)


libvirt_domain_state = Gauge(
    namespace="libvirt",
    subsystem="domain",
    name="state",
    documentation="Virtual domain state. 0: no state, 1: the domain is running, 2: the domain is blocked on resource,"
    + " 3: the domain is paused by user, 4: the domain is being shut down, 5: the domain is shut off,"
    + "6: the domain is crashed, 7: the domain is suspended by guest power management",
    labelnames=["domain"],
)

####
# block device
####

libvirt_domain_block_dev_metadata = Info(
    namespace="libvirt",
    subsystem="domain_block_dev",
    name="metadata_info",
    documentation="Block device metadata info. Device name, source file, serial.",
    labelnames=[
        "domain",
        "disk_type",
        "target_dev",
        "target_bus",
        "source_file",
        "driver_name",
        "driver_type",
        "driver_discard",
    ],
)

libvirt_domain_block_dev_read_bytes = Counter(
    namespace="libvirt",
    subsystem="domain_block_dev",
    name="read_bytes_total",
    documentation="number of bytes read from a block device.",
    labelnames=["domain", "target_dev"],
    unit="bytes",
)

libvirt_domain_block_dev_read_operations = Counter(
    namespace="libvirt",
    subsystem="domain_block_dev",
    name="read_operations_total",
    documentation="Number of read operations from a block device.",
    labelnames=["domain", "target_dev"],
)

libvirt_domain_block_dev_read_total_seconds = Counter(
    namespace="libvirt",
    subsystem="domain_block_dev",
    name="read_seconds_total",
    documentation="Total duration of reads from a block device, in seconds.",
    labelnames=["domain", "target_dev"],
    unit="seconds",
)

libvirt_domain_block_dev_write_bytes = Counter(
    namespace="libvirt",
    subsystem="domain_block_dev",
    name="write_bytes_total",
    documentation="Number of bytes written to a block device.",
    labelnames=["domain", "target_dev"],
    unit="bytes",
)

libvirt_domain_block_dev_write_operations = Counter(
    namespace="libvirt",
    subsystem="domain_block_dev",
    name="write_operations_total",
    documentation="Number of write operations to a block device.",
    labelnames=["domain", "target_dev"],
)

libvirt_domain_block_dev_write_total_seconds = Counter(
    namespace="libvirt",
    subsystem="domain_block_dev",
    name="write_seconds_total",
    documentation="Total duration of writes on a block device, in seconds",
    labelnames=["domain", "target_dev"],
    unit="seconds",
)

libvirt_domain_block_dev_flush_operations = Counter(
    namespace="libvirt",
    subsystem="domain_block_dev",
    name="flush_operations_total",
    documentation="Number of flush operations from a block device.",
    labelnames=["domain", "target_dev"],
)

libvirt_domain_block_dev_flush_total_seconds = Counter(
    namespace="libvirt",
    subsystem="domain_block_dev",
    name="flush_seconds_total",
    documentation="Total duration of flushes to a block device, in seconds.",
    labelnames=["domain", "target_dev"],
    unit="seconds",
)

###
# Domain Memory
###

libvirt_domain_mem_stat_actual_balloon_bytes = Gauge(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="actual_balloon_bytes",
    documentation="Actual balloon size, in bytes.",
    labelnames=["domain"],
    unit="bytes",
)

libvirt_domain_mem_stat_swap_in_bytes = Counter(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="swap_in_bytes_total",
    documentation="The amount of data read from swap space, in bytes.",
    labelnames=["domain"],
    unit="bytes",
)

libvirt_domain_mem_stat_swap_out_bytes = Counter(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="swap_out_bytes_total",
    documentation="The amount of memory written out to swap space, in bytes.",
    labelnames=["domain"],
    unit="bytes",
)

libvirt_domain_mem_stat_major_fault = Counter(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="major_faults_total",
    documentation="The number of page faults where disk IO was required.",
    labelnames=["domain"],
)

libvirt_domain_mem_stat_minor_fault = Counter(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="minor_faults_total",
    documentation="The number of other page faults.",
    labelnames=["domain"],
)

libvirt_domain_mem_stat_unused_bytes = Gauge(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="unused_bytes_total",
    documentation="The amount of memory left unused by the system, in bytes.",
    labelnames=["domain"],
    unit="bytes",
)

libvirt_domain_mem_stat_available_bytes = Gauge(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="available_bytes",
    documentation="The amount of usable memory as seen by the domain, in bytes.",
    labelnames=["domain"],
    unit="bytes",
)

libvirt_domain_mem_stat_usable_bytes = Gauge(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="usable_bytes",
    documentation="The amount of memory which can be reclaimed by balloon without causing host swapping (in KiB), in bytes.",
    labelnames=["domain"],
    unit="bytes",
)

libvirt_domain_mem_stat_disk_caches_bytes = Gauge(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="disk_caches_bytes_total",
    documentation="The amount of memory that can be reclaimed without additional I/O, typically disk caches, in bytes.",
    labelnames=["domain"],
    unit="bytes",
)

libvirt_domain_mem_stat_hugetlb_pgalloc = Counter(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="hugetlb_pgalloc_total",
    documentation="The number of successful huge page allocations initiated from within the domain.",
    labelnames=["domain"],
)

libvirt_domain_mem_stat_hugetlb_pgfail = Counter(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="hugetlb_pgfail_total",
    documentation="The number of failed huge page allocations initiated from within the domain.",
    labelnames=["domain"],
)

libvirt_domain_mem_stat_rss = Gauge(
    namespace="libvirt",
    subsystem="domain_mem_stat",
    name="rss_bytes",
    documentation="Resident Set Size of the running domain's process, in bytes.",
    labelnames=["domain"],
)

####
# Domain Network Interfaces
####

libvirt_domain_io_rx_bytes = Counter(
    namespace="libvirt",
    subsystem="domain_interface",
    name="receive_bytes_total",
    documentation="Number of bytes received on a network interface, in bytes.",
    unit="bytes",
    labelnames=["domain", "dev_mac"],
)

libvirt_domain_io_rx_packets = Counter(
    namespace="libvirt",
    subsystem="domain_interface",
    name="receive_packets_total",
    documentation="Number of packets received on a network interface.",
    labelnames=["domain", "dev_mac"],
)

libvirt_domain_io_rx_errors = Counter(
    namespace="libvirt",
    subsystem="domain_interface",
    name="receive_errors_total",
    documentation="Number of packet receive errors on a network interface.",
    labelnames=["domain", "dev_mac"],
)

libvirt_domain_io_rx_drops = Counter(
    namespace="libvirt",
    subsystem="domain_interface",
    name="receive_drops_total",
    documentation="Number of packet receive drops on a network interface.",
    labelnames=["domain", "dev_mac"],
)

libvirt_domain_io_tx_bytes = Counter(
    namespace="libvirt",
    subsystem="domain_interface",
    name="transmit_bytes_total",
    documentation="NNumber of bytes transmitted on a network interface, in bytes.",
    unit="bytes",
    labelnames=["domain", "dev_mac"],
)

libvirt_domain_io_tx_packets = Counter(
    namespace="libvirt",
    subsystem="domain_interface",
    name="transmit_packets_total",
    documentation="Number of packets transmitted on a network interface.",
    labelnames=["domain", "dev_mac"],
)

libvirt_domain_io_tx_errors = Counter(
    namespace="libvirt",
    subsystem="domain_interface",
    name="transmit_errors_total",
    documentation="Number of packet transmit errors on a network interface.",
    labelnames=["domain", "dev_mac"],
)

libvirt_domain_io_tx_drops = Counter(
    namespace="libvirt",
    subsystem="domain_interface",
    name="transmit_drops_total",
    documentation="Number of packet transmit drops on a network interface.",
    labelnames=["domain", "dev_mac"],
)

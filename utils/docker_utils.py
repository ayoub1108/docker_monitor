import docker
import psutil

def get_container_stats(container_id):
    """Fetch CPU, memory, and I/O stats for a container."""
    client = docker.from_env()
    container = client.containers.get(container_id)
    stats = container.stats(stream=False)

    cpu_percent = calculate_cpu_percent(stats)
    memory_usage = stats['memory_stats']['usage'] / 1024 / 1024  # Convert to MB
    network_io = stats['networks']['eth0']['rx_bytes']  # Example for network I/O
    block_io = stats['blkio_stats']['io_service_bytes'][0]['value']  # Example for block I/O

    return {
        'cpu_percent': cpu_percent,
        'memory_usage': memory_usage,
        'network_io': network_io,
        'block_io': block_io
    }

def calculate_cpu_percent(stats):
    """Calculate CPU usage percentage."""
    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    if system_delta > 0:
        return (cpu_delta / system_delta) * 100
    return 0

import docker
import psutil
import time
from blessed import Terminal
from utils.docker_utils import get_container_stats
from utils.animation_utils import display_animation

term = Terminal()

def display_container_info(container):
    """Display detailed information about a Docker container."""
    print(term.clear)
    print(term.bold(f"Container ID: {container.id}"))
    print(term.bold(f"Name: {container.name}"))
    print(term.bold(f"Status: {container.status}"))
    print(term.bold(f"Image: {container.image.tags[0] if container.image.tags else 'None'}"))
    print(term.bold(f"CPU Usage: {get_container_stats(container.id)['cpu_percent']}%"))
    print(term.bold(f"Memory Usage: {get_container_stats(container.id)['memory_usage']} MB"))
    print(term.bold(f"Network I/O: {get_container_stats(container.id)['network_io']}"))
    print(term.bold(f"Block I/O: {get_container_stats(container.id)['block_io']}"))

def main():
    client = docker.from_env()
    containers = client.containers.list()

    print(term.clear)
    print(term.bold("Docker Container Monitor"))
    print(term.bold("========================\n"))

    for idx, container in enumerate(containers):
        print(f"{idx + 1}. {container.name}")

    choice = int(input("\nSelect a container to monitor (1-{}): ".format(len(containers)))) - 1
    selected_container = containers[choice]

    while True:
        display_container_info(selected_container)
        display_animation()
        time.sleep(1)

if __name__ == "__main__":
    main()

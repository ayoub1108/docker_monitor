# docker_monitor
tool that helps you to get all informations about a container running 
Creating a tool that provides detailed information about Docker containers with a cool animation and an interactive interface is a great idea! Below is a step-by-step guide to help you build this tool in Linux. I'll also provide a basic structure for the project directory and some code snippets to get you started.

---

### **Project Structure**
Here’s how your project directory could look:

```
docker-monitor/
├── README.md
├── requirements.txt
├── monitor.py
├── animations/
│   └── (animation files, e.g., ASCII art or spinners)
├── utils/
│   ├── docker_utils.py
│   └── animation_utils.py
└── tests/
    └── test_docker_utils.py
```

---

### **Steps to Build the Tool**

1. **Set Up the Environment**
   - Ensure you have Python 3.x installed.
   - Install Docker on your Linux machine.
   - Install the required Python libraries:
     ```bash
     pip install docker psutil blessed
     ```
     - `docker`: Python library to interact with Docker.
     - `psutil`: To monitor CPU, memory, and other system resources.
     - `blessed`: For creating an interactive terminal interface.

2. **Create the Main Script (`monitor.py`)**
   This script will be the entry point for your tool. It will fetch Docker container details and display them in an interactive and animated way.

   ```python
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
   ```

3. **Create Utility Functions (`docker_utils.py`)**
   This file will contain helper functions to fetch Docker container stats.

   ```python
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
   ```

4. **Add Animations (`animation_utils.py`)**
   Create fun animations using ASCII art or spinners.

   ```python
   import time
   from blessed import Terminal

   term = Terminal()

   def display_animation():
       """Display a cool animation."""
       frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
       for frame in frames:
           print(term.move_xy(0, term.height - 1) + term.bold(frame), end="", flush=True)
           time.sleep(0.1)
   ```

5. **Add a `requirements.txt` File**
   List all dependencies for the project.

   ```
   docker
   psutil
   blessed
   ```

6. **Push to GitHub**
   - Initialize a Git repository:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     ```
   - Create a new repository on GitHub and push your code:
     ```bash
     git remote add origin https://github.com/your-username/docker-monitor.git
     git branch -M main
     git push -u origin main
     ```

---

### **Features to Add Later**
- Add more detailed stats (e.g., disk usage, network bandwidth).
- Support for multiple containers in a single view.
- Add color-coded alerts for high CPU/memory usage.
- Create a Docker image for the tool itself.

---

### **Running the Tool**
1. Clone the repository:
   ```bash
   git clone https://github.com/ayoub1108/docker_monitor
   cd docker-monitor
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the tool:
   ```bash
   python monitor.py
   ```


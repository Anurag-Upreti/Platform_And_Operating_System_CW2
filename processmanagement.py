import psutil

def list_processes():
    print("List of currently running processes:")
    print("------------------------------------")
    print("PID    | Name                | Priority | Memory Usage")
    print("------------------------------------")
    for process in psutil.process_iter(attrs=['pid', 'name', 'nice', 'memory_info']):
        try:
            process_info = process.info
            pid = str(process_info['pid'])
            name = str(process_info['name'])
            priority = str(process_info['nice'])
            memory_usage = str(process_info['memory_info'].rss // (1024 * 1024))  # Convert to MB
            
            print(f"{pid:6} | {name:20} | {priority:8} | {memory_usage:12} MB")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def process_menu():
    while True:
        print("\nProcess Management Menu:")
        print("1. List Processes")
        print("2. View Process Details")
        print("3. Change Process Priority")
        print("4. Terminate Process")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            list_processes()
        elif choice == "2":
            pid = input("Enter the PID of the process you want to view details for: ")
            view_process_details(pid)
        elif choice == "3":
            pid = input("Enter the PID of the process you want to change priority for: ")
            new_priority = input("Enter the new priority value (niceness): ")
            change_process_priority(pid, new_priority)
        elif choice == "4":
            pid = input("Enter the PID of the process you want to terminate: ")
            terminate_process(pid)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def view_process_details(pid):
    try:
        process = psutil.Process(int(pid))
        print("\nProcess Details:")
        print("----------------")
        print(f"PID: {process.pid}")
        print(f"Name: {process.name()}")
        print(f"Status: {process.status()}")
        print(f"Priority (niceness): {process.nice()}")
        print(f"Memory Usage: {process.memory_info().rss // (1024 * 1024)} MB")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        print(f"Process with PID {pid} not found.")

def change_process_priority(pid, new_priority):
    try:
        process = psutil.Process(int(pid))
        process.nice(int(new_priority))
        print(f"Priority of process {pid} changed to {new_priority}.")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        print(f"Process with PID {pid} not found.")
    except ValueError:
        print("Invalid priority value. Please enter an integer.")

def terminate_process(pid):
    try:
        process = psutil.Process(int(pid))
        process.terminate()
        print(f"Process {pid} terminated.")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        print(f"Process with PID {pid} not found.")

if __name__ == "__main__":
    process_menu()

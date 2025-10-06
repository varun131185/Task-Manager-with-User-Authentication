import os
import csv

"""
This class is dedicate for Task Manager that allows users to manage their tasks. 
users can create, view, update, and delete their tasks. Each user’s tasks 
should be stored separately, 
and only the authenticated user can access their tasks.
"""


class UserTaskManger:

    # Constructor method: initializes new objects of the class UserTasks
    def __init__(self, username):
        self.username = username  # Instance variable
        self.tasks = []  # Instance variable - list of tasks
        self.TASK_FILE = 'tasks.csv'  # Instance variable

    # ------------------ Load Tasks ------------------ #
    def load_tasks(self):
        file_path = "users_tasks/" + self.username + "_" + self.TASK_FILE
        if os.path.exists(file_path):
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                self.tasks = [row for row in reader]
                # Convert task ID to int
                for task in self.tasks:
                    task['Task_ID'] = int(task['Task_ID'])
        else:
            self.tasks = []

    # ------------------ get Next Task ID ------------------ #
    def _get_next_task_id(self):
        if not self.tasks:
            return 1
        else:
            return max(int(task['Task_ID']) for task in self.tasks) + 1

    # ------------------ add New Task  ------------------ #
    def add_task(self):
        description = input("Enter task description: ").strip()
        if not description:
            print("Task description cannot be empty.")
            return
        task_id = self._get_next_task_id()
        # creating task as dictionary
        task = {
            'Task_ID': task_id,
            'Status': "Pending",
            'description': description
        }

        # adding task as dictionary in tasks list
        self.tasks.append(task)
        self._save_all_tasks()
        print(f"Task added successfully! (ID: {task_id})\n")

    # ------------------Private method Save Tasks  ------------------ #
    def _save_all_tasks(self):
        file_path = "users_tasks/" + self.username + "_" + self.TASK_FILE
        directory_path = "users_tasks/"
        os.makedirs(directory_path, exist_ok=True)
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Task_ID', 'Status', 'description'])
            writer.writeheader()
            writer.writerows(self.tasks)
            file.close()

    # ------------------ View User's Tasks  ------------------ #
    def view_tasks(self):
        if not self.tasks:
            print("No tasks found for User : {username} \n")
        else:
            print(f"\n-------- Tasks for {self.username} -------")
            for task in self.tasks:
                # Perform operations with the dictionary, knowing all keys exist
                print(f"Task_ID: {task['Task_ID']} | Status: {task['Status']} | Description: {task['description']}")
            print(f"\n--------------------------------------------")

    # ------------------ Mark User's Tasks as Completed ------------------ #
    def mark_task_completed(self):
        if not self.tasks:
            print("No tasks to mark as completed.\n")
            return
        self.view_tasks()
        # taking user input for task Id as valid integer value
        found_flag = False
        while True:
            try:
                task_id = int(input("Enter the task ID to mark as completed: "))
                for task in self.tasks:
                    if task.get("Task_ID") == task_id:
                        task['Status'] = "Completed"
                        found_flag = True
                        break
                break
            except ValueError:
                print("Invalid Task Id! Please enter a number.")
        if found_flag:
            self._save_all_tasks()
            print(f"Task ID  {task_id} marked as completed.\n")
        else:
            print(f"Task ID {task_id} not found.\n")

    # ------------------ Delete Task  ------------------ #
    def delete_task(self):
        if not self.tasks:
            print("No tasks to delete.\n")
            return
        self.view_tasks()
        # taking user input for task Id as valid integer value
        found_flag = False
        while True:
            try:
                task_id = int(input("Enter the task ID to delete:  ").strip())
                for task in self.tasks:
                    if task.get("Task_ID") == task_id:
                        self.tasks.remove(task)
                        found_flag = True
                        break
                break
            except ValueError:
                print("Invalid Task Id! Please enter a number.")
        if found_flag:
            self._save_all_tasks()
            print(f"Task ID  {task_id} deleted successfully.\n")
        else:
            print(f"Task ID {task_id} not found.\n")


    # ------------------ Interactive task menu ------------------ #
    def interactive_task_menu(self):
        self.load_tasks()
        while True:
            print("\n==== Task Manager Options: ====")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Mark Task as Completed")
            print("4. Delete Task")
            print("5. Logout")
            task_choice = input("Choose an option (1-3): ").strip()
            if task_choice == '1':
                self.add_task()
            elif task_choice == '2':
                self.view_tasks()
            elif task_choice == '3':
                self.mark_task_completed()
            elif task_choice == '4':
                self.delete_task()
            elif task_choice == '5':
                print("Logging out...\n")
                break
            else:
                print("Invalid option. Try again and Please choose between 1 and 5.\n")

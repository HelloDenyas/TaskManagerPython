import json


TASKS_FILE = "tasks.json"


def load_tasks():
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError):
        print("Could not load tasks. Starting with an empty task list.")
        return []


def save_tasks(tasks):
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError:
        print("Could not save tasks.")


def display_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return

    for task in tasks:
        status = "x" if task["completed"] else " "
        print(f'[{status}] {task["id"]} - {task["title"]} - {task["priority"]}')


def get_next_id(tasks):
    highest_id = 0

    for task in tasks:
        if task["id"] > highest_id:
            highest_id = task["id"]

    return highest_id + 1


def add_task(tasks):
    title = input("Title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return None

    print("1 - Low")
    print("2 - Medium")
    print("3 - High")

    while True:
        priority_choice = input("Priority: ").strip()

        if priority_choice == "1":
            priority = "Low"
            break
        elif priority_choice == "2":
            priority = "Medium"
            break
        elif priority_choice == "3":
            priority = "High"
            break
        else:
            print("Please choose 1, 2, or 3.")

    task = {
        "id": get_next_id(tasks),
        "title": title,
        "completed": False,
        "priority": priority,
    }

    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")
    return task


def complete_task(tasks):
    try:
        task_id = int(input("Task ID to complete: "))
    except ValueError:
        print("Please enter a valid number.")
        return False

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print("Task completed.")
            return True

    print("Task not found.")
    return False


def delete_task(tasks):
    try:
        task_id = int(input("Task ID to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return False

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print("Task deleted.")
            return True

    print("Task not found.")
    return False


def search_tasks(tasks):
    search_text = input("Search text: ").strip().lower()
    matching_tasks = []

    for task in tasks:
        if search_text in task["title"].lower():
            matching_tasks.append(task)

    if not matching_tasks:
        print("No tasks found.")
    else:
        display_tasks(matching_tasks)

    return matching_tasks


def filter_tasks(tasks):
    print("1 - All")
    print("2 - Active")
    print("3 - Completed")
    choice = input("Choose: ").strip()
    matching_tasks = []

    if choice == "1":
        matching_tasks = tasks.copy()
    elif choice == "2":
        for task in tasks:
            if not task["completed"]:
                matching_tasks.append(task)
    elif choice == "3":
        for task in tasks:
            if task["completed"]:
                matching_tasks.append(task)
    else:
        print("Invalid choice.")
        return matching_tasks

    if not matching_tasks:
        print("No tasks found.")
    else:
        display_tasks(matching_tasks)

    return matching_tasks


def display_menu(tasks):
    print("\n==============================")
    print("         TASK MANAGER")
    print("===============================")
    print("\nTASKS\n")
    display_tasks(tasks)
    print("\n------------------------------")
    print("1 - Add task")
    print("2 - Complete task")
    print("3 - Delete task")
    print("4 - Search tasks")
    print("5 - Filter tasks")
    print("0 - Exit")
    print("-------------------------------")


def main():
    tasks = load_tasks()

    while True:
        display_menu(tasks)
        choice = input("Choose: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            complete_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            search_tasks(tasks)
        elif choice == "5":
            filter_tasks(tasks)
        elif choice == "0":
            print("end")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

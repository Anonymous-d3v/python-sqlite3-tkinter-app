import sqlite3


conn = sqlite3.connect('Databases/my_database.db')
c = conn.cursor()


# Creating a table called 'tasks'

#c.execute("DROP TABLE IF EXISTS tasks")

c.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK(status IN('Pending','In Progress', 'Completed')) DEFAULT 'Pending'
)
""")
#status = input("enter status: ").title()
#c.execute("CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)")
#c.execute("EXPLAIN QUERY PLAN SELECT * FROM tasks WHERE status = ?", (status,))
#print('New table created successfully')

conn.commit()

# Using different functions to add, delete, update and search the table

def add_task(task, status="Pending"):
# Function adds one task at a time...
    conn = sqlite3.connect('Databases/my_database.db')
    c = conn.cursor()
    if not task.strip():
        return "Task came cannot be empty"

    if status not in ['Pending', 'Completed']:
        return "Status must be either 'Pending' or 'Completed'"


    try:
        c.execute("SELECT * FROM tasks WHERE task = ?", (task,))
        existing_task = c.fetchone()

        if existing_task:
            return f"⚠️ Task '{task}' already exists!"
        else:
            c.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, status))

        conn.commit()

        return f"Task '{task}' added successfully"

    except sqlite3.IntegrityError as e:
        return f"Failed to add task: {e}"

    finally:
        conn.close()


def add_multi_tasks(task_list):
# Function adds multiple tasks by taking in a list...
    conn = sqlite3.connect('Databases/my_database.db')
    c = conn.cursor()
    c.executemany("INSERT INTO tasks (task) VALUES (?)", [(task,) for task in task_list])

    conn.commit()
    conn.close()
    return 'Tasks have been added successfully'


def get_all_tasks():
    conn = sqlite3.connect('Databases/my_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    all_tasks = c.fetchall()
    result = []

    if all_tasks:
        result.append("\n📌 Your To-Do List:")
        for task in all_tasks:
            task_id, description, status = task
            result.append(f"{task_id}. {description} - Status: {status}")
    else:
        result.append("\nNo tasks found!")

    conn.close()
    return "\n".join(result)


def get_by_id(task_id):
    conn = sqlite3.connect('Databases/my_database.db')
    c = conn.cursor()
# Function takes ID (usually a number) and displays its task...
    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()

    conn.close()

    if task:
        return f"\n 🔍 Task Found: {task[0]}. {task[1]} - Status: {task[2]}"
    else:
        return f"\n No task found with ID {task_id}"


def status_update(task_id, new_status="In Progress"):
    conn = sqlite3.connect('Databases/my_database.db')
    c = conn.cursor()
# Function takes task ID to be updates the status to 'Completed'...
    c.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()
    return f"Task {task_id} marked as {new_status}"


def delete_task(task_id):
    conn = sqlite3.connect('Databases/my_database.db')
    c = conn.cursor()
# Function takes task ID and deletes tasks if it exists...
    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()

    if task:
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return f"Task with ID '{task_id}' has been deleted."
    else:
        return 'Task not found!'


def manual_update_status(task_id, status):
    conn = sqlite3.connect('Databases/my_database.db')
    c = conn.cursor()
# Function manually updates statuses to 'Completed' or reverting back to 'Pending'
    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()

    if task:
        c.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        conn.commit()
        conn.close()
        return f"Status of task '{task_id}' has been updated to '{status}'"
    else:
        return 'Task not found!'


def general_search_status(user_input):
    conn = sqlite3.connect('Databases/my_database.db')
    c = conn.cursor()
# Function takes input (str or int) and searches by status, keyword or task ID
    if isinstance(user_input, str):
        user_input = user_input.strip().title()

        if user_input in ["Completed", "Pending", 'In Progress']:
            c.execute("SELECT * FROM tasks WHERE status = ?", (user_input,))
            fetched = c.fetchall()

            if fetched:
                for fetch in fetched:
                    return f"{fetch[0]}. {fetch[1]} - Status: {fetch[2]}"
            else:
                return f"There aren't any '{user_input}' tasks"

        else:
            c.execute("SELECT * FROM tasks WHERE task LIKE ?", (f"%{user_input}%",))
            results = c.fetchall()

            if results:
                for fetch in results:
                    return f"{fetch[0]}. {fetch[1]} - Status: {fetch[2]}"
            else:
                return "No matching tasks found."

    elif isinstance(user_input, int):
        c.execute("SELECT * FROM tasks WHERE id = ?", (user_input,))
        task = c.fetchone()
        conn.close()

        if task:
            return f"\n 🔍 Task Found: {task[0]}. {task[1]} - Status: {task[2]}"
        else:
            return f"\n No task found with ID {user_input}"

    else:
        return "⚠️ Invalid input"





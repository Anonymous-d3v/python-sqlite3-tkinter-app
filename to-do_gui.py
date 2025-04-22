from tkinter import *
import to_do_db


root = Tk()
root.title('To-Do List App')
root.iconbitmap('files/python.ico')
#root.geometry("600x600")


# Display Functions: Functions get their commands from the database file
def submit_add_task():
    update_display(text=to_do_db.add_task(add_task.get()))
    add_task.delete(0, END)


def submit_task_id():
    try:
        task_id = int(task_by_id.get())
    except ValueError:
        update_display(text="Please enter a valid task ID")
        return

    update_display(text=to_do_db.get_by_id(task_id))
    task_by_id.delete(0, END)


def submit_task_delete():
    try:
        task_id = int(task_delete.get())
    except ValueError:
        update_display(text="Please enter a valid task ID")
        return

    update_display(to_do_db.delete_task(task_id))
    task_delete.delete(0, END)


def submit_completed():
    try:
        task_id = int(completed_task.get())
    except ValueError:
        update_display("Please enter a valid task ID")
        return
    update_display(to_do_db.status_update(task_id))
    completed_task.delete(0, END)



def submit_ssearch():
    update_display(to_do_db.general_search_status(smart_search.get()))
    smart_search.delete(0, END)


query_box = Text(root, height=10, width=50)
query_box.grid(row=19, column=0, columnspan=4, padx=20, pady=10)
query_box.config(state=DISABLED)


status_update_id = Entry(root)
status_update_id.grid(row=21, column=0)

status_var = StringVar()
status_var.set("Pending")  # default
status_dropdown = OptionMenu(root, status_var, "Pending", "In Progress", "Completed")
status_dropdown.grid(row=21, column=1)


def update_display(text):
    # A general display box to give user feedback
    query_box.config(state=NORMAL)
    query_box.delete("1.0", END)
    query_box.insert(END, text)
    query_box.config(state=DISABLED)


def update_status_manually():
    try:
        task_id = int(status_update_id.get())
    except ValueError:
        update_display("Please enter a valid task ID")
        return

    new_status = status_var.get()
    update_display(to_do_db.status_update(task_id, new_status))
    status_update_id.delete(0, END)


def submit_display():
    update_display(to_do_db.get_all_tasks())


# UI design section: create and align the widgets, buttons and labels
add_task = Entry(root, width=30)
add_task.grid(row=1, column=0, padx=20)
sbmt_btn_add = Button(root, text='Submit', command=submit_add_task)
sbmt_btn_add.grid(row=1, column=1, padx=20)


get_all_tasks_btn = Button(root, text="Display all tasks", command=submit_display)
get_all_tasks_btn.grid(row=18, column=0, columnspan=4, padx=10, pady=25)


status_btn = Button(root, text="Update Status", command=update_status_manually)
status_btn.grid(row=21, column=2)


task_by_id = Entry(root, width=30)
task_by_id.grid(row=5, column=0, padx=20)
sbmt_btn_task_id = Button(root, text='Submit', command=submit_task_id)
sbmt_btn_task_id.grid(row=5, column=1, padx=20)


task_delete = Entry(root, width=30)
task_delete.grid(row=7, column=0, padx=20)
sbmt_btn_task_delete = Button(root, text='Submit', command=submit_task_delete)
sbmt_btn_task_delete.grid(row=7, column=1, padx=20)


completed_task = Entry(root, width=30)
completed_task.grid(row=9, column=0, padx=20)
sbmt_btn_complete = Button(root, text='Submit', command=submit_completed)
sbmt_btn_complete.grid(row=9, column=1, padx=20)


smart_search = Entry(root, width=30)
smart_search.grid(row=11, column=0, padx=20)
sbmt_btn_ssearch = Button(root, text='Submit', command=submit_ssearch)
sbmt_btn_ssearch.grid(row=11, column=1, padx=20)


add_task_label = Label(root, text="Add task")
add_task_label.grid(row=0)

task_by_id_label = Label(root, text="Search for task with ID")
task_by_id_label.grid(row=4)

task_delete_label = Label(root, text="Delete task")
task_delete_label.grid(row=6)

completed_task_label = Label(root, text="Enter Completed task ID")
completed_task_label.grid(row=8)

smart_search_label = Label(root, text="Smart Search Task")
smart_search_label.grid(row=10)


root.mainloop()
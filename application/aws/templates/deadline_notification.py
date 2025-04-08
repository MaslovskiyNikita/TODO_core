def deadline_template_data(task):
    template_data = {
        "task_title": task.title,
        "time_left": "1 час",
        "description": task.description,
        "project_title": task.project.title,
    }

    return template_data

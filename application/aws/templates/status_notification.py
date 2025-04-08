def status_template(project_name, project_owner):
    template_data = {
        "title": project_name,
        "description": project_name,
        "project_title": project_owner,
    }
    return template_data

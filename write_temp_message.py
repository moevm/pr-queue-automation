from scrtip_parsing_pr import ParseDataGit
from jinja2 import Environment, FileSystemLoader


data = ParseDataGit(token='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', repo_name='test_repo')
data.set_path_to_temp_message("templates/script_templates/temp_for_lb.txt")
path_to_temp_message = data.get_path_to_temp_message()

name_status_list_of_dict = []
students = data.get_status_to_proctering()

for student in students:
    buffer_dict = {}
    name = ' '.join(student.split('_')[:-1])
    status = students[student]
    if status == 'passed':
        buffer_dict['name'] = name
        buffer_dict['status'] = status
        name_status_list_of_dict.append(buffer_dict)

environment = Environment(loader=FileSystemLoader("templates/script_templates"))

results_filename = "templates/result_templates/students_results.txt"
name_of_file = path_to_temp_message.split('/')[-1]
results_template = environment.get_template(name_of_file)

context = {
    "students": name_status_list_of_dict,
}
with open(results_filename, mode="w", encoding="utf-8") as results:
    results.write(results_template.render(context))
    print(f"... wrote {results_filename}")
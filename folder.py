import os
import html
from tkinter import Tk, filedialog

def generate_html(file_list, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<title>File List</title>\n')
        f.write('<style>\n')
        f.write('body { font-family: Arial, sans-serif; margin: 20px; }\n')
        f.write('table { width: 100%; border-collapse: collapse; }\n')
        f.write('th, td { border: 1px solid #ddd; padding: 8px; }\n')
        f.write('th { background-color: #f4f4f4; }\n')
        f.write('</style>\n')
        f.write('</head>\n')
        f.write('<body>\n')
        f.write('<h1>File List</h1>\n')
        f.write('<table>\n')
        f.write('<tr><th>Name</th><th>Type</th><th>Size (Bytes)</th></tr>\n')
        for item in file_list:
            name = html.escape(item['name'])
            type_ = html.escape(item['type'])
            size = item.get('size', 'N/A')
            f.write(f'<tr><td>{name}</td><td>{type_}</td><td>{size}</td></tr>\n')
        f.write('</table>\n')
        f.write('</body>\n')
        f.write('</html>\n')

def list_files_and_folders(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for name in dirs:
            file_list.append({'name': name, 'type': 'Folder'})
        for name in files:
            path = os.path.join(root, name)
            size = os.path.getsize(path)
            file_list.append({'name': name, 'type': 'File', 'size': size})
    return file_list

root = Tk()
root.withdraw()
selected_folder = filedialog.askdirectory(title="Select a folder")
if selected_folder:
    output_file = os.path.join(os.path.expanduser("~"), "file_list.html")
    file_list = list_files_and_folders(selected_folder)
    generate_html(file_list, output_file)
    os.startfile(output_file)
else:
    print("No folder selected.")

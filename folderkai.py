import os
import html
from tkinter import Tk, filedialog
import webbrowser
import tempfile  # TEMP

def generate_html(file_list, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<title>File List</title>\n')
        f.write('<style>\n')
        f.write('body { font-family: Arial, sans-serif; margin: 20px; }\n')
        f.write('table { width: 100%; border-collapse: collapse; }\n')
        f.write('th, td { border: 1px solid #ddd; padding: 8px; }\n')
        f.write('th { background-color: #f4f4f4; cursor: pointer; }\n')
        f.write('</style>\n')
        f.write('<script>\n')
        f.write('function sortTable(n) {\n')
        f.write('  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;\n')
        f.write('  table = document.getElementById("fileTable");\n')
        f.write('  switching = true;\n')
        f.write('  dir = "asc";\n')
        f.write('  while (switching) {\n')
        f.write('    switching = false;\n')
        f.write('    rows = table.rows;\n')
        f.write('    for (i = 1; i < (rows.length - 1); i++) {\n')
        f.write('      shouldSwitch = false;\n')
        f.write('      x = rows[i].getElementsByTagName("TD")[n];\n')
        f.write('      y = rows[i + 1].getElementsByTagName("TD")[n];\n')
        f.write('      if (dir == "asc") {\n')
        f.write('        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {\n')
        f.write('          shouldSwitch = true;\n')
        f.write('          break;\n')
        f.write('        }\n')
        f.write('      } else if (dir == "desc") {\n')
        f.write('        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {\n')
        f.write('          shouldSwitch = true;\n')
        f.write('          break;\n')
        f.write('        }\n')
        f.write('      }\n')
        f.write('    }\n')
        f.write('    if (shouldSwitch) {\n')
        f.write('      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);\n')
        f.write('      switching = true;\n')
        f.write('      switchcount ++;\n')
        f.write('    } else {\n')
        f.write('      if (switchcount == 0 && dir == "asc") {\n')
        f.write('        dir = "desc";\n')
        f.write('        switching = true;\n')
        f.write('      }\n')
        f.write('    }\n')
        f.write('  }\n')
        f.write('}\n')
        f.write('</script>\n')
        f.write('</head>\n')
        f.write('<body>\n')
        f.write('<h1>File List</h1>\n')
        f.write('<table id="fileTable">\n')
        f.write('<tr><th onclick="sortTable(0)">Name</th><th onclick="sortTable(1)">Type</th><th onclick="sortTable(2)">Size (Bytes)</th></tr>\n')
        for item in file_list:
            name = html.escape(item['name'])
            type_ = html.escape(item['type'])
            size = item.get('size', 'N/A')
            f.write(f'<tr><td>{name}</td><td>{type_}</td><td>{size}</td></tr>\n')
        f.write('</table>\n')
        f.write('</body>\n')
        f.write('</html>\n')

def calculate_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def list_files_and_folders(folder_path, exclude_types=None):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for name in dirs:
            dir_path = os.path.join(root, name)
            size = calculate_folder_size(dir_path)
            if exclude_types and 'Folder' in exclude_types:
                continue
            file_list.append({'name': name, 'type': 'Folder', 'size': size})
        for name in files:
            file_ext = os.path.splitext(name)[1].lower()
            if exclude_types and file_ext in exclude_types:
                continue
            path = os.path.join(root, name)
            size = os.path.getsize(path)
            file_list.append({'name': name, 'type': 'File', 'size': size})
    return file_list

def open_html(output_file):
    webbrowser.open('file://' + os.path.realpath(output_file))

root = Tk()
root.withdraw()
selected_folder = filedialog.askdirectory(title="Select a folder")
if selected_folder:
    temp_dir = tempfile.gettempdir()
    output_file = os.path.join(temp_dir, "file_list.html")
    
    exclude_types = []
    file_list = list_files_and_folders(selected_folder, exclude_types=exclude_types)
    generate_html(file_list, output_file)
    open_html(output_file)
else:
    print("No folder selected.")

import os
import yaml
import glob
import copy
import jinja2    


folder_configuration = "configuration"
folder_configuration = os.path.join(os.path.dirname(__file__), folder_configuration)
file_configuration = os.path.join(folder_configuration, "configuration.yaml")
#import templates
with open(file_configuration, 'r') as stream:
    try:
        configuration = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:   
        print(exc)



def main(**kwargs):
    overwrite = kwargs.get("overwrite", False)
    import concurrent.futures
    workers  = 4
    if overwrite:
        workers = 1
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in range(workers):
            executor.submit(main_thread, **kwargs)

def main_thread(**kwargs):

    test_for_inkscape()
    
    
    folder = kwargs.get("folder", f"os.path.dirname(__file__)/parts")
    folder = folder.replace("\\","/")
    
    kwargs["file_template_list"] = configuration
    print(f"oomlout_oomp_utility_readme_generation for folder: {folder}")
    create_recursive(**kwargs)
    
def create_recursive(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    folder_template_absolute = kwargs.get("folder_template_absolute", "")
    kwargs["folder_template_absolute"] = folder_template_absolute
    filter = kwargs.get("filter", "")
    for item in os.listdir(folder):
        if filter in item:
            item_absolute = os.path.join(folder, item)
            if os.path.isdir(item_absolute):
                #if working.yaml exists in the folder
                if os.path.exists(os.path.join(item_absolute, "working.yaml")):
                    kwargs["directory"] = item_absolute
                    create(**kwargs)

def create(**kwargs):
    directory = kwargs.get("directory", os.getcwd())    
    kwargs["directory"] = directory
    file_template_list = kwargs.get("file_template_list", configuration)
    kwargs["file_template_list"] = file_template_list
    generate(**kwargs)
    

def generate(**kwargs):
    import os
    directory = kwargs.get("directory",os.getcwd())   
    overwrite = kwargs.get("overwrite", False) 
    files = os.listdir(directory)
    for file in files:
        if file.endswith(".svg"):
            file_input = os.path.join(directory, file)
            file_output = file_input.replace(".svg", ".png")
            if overwrite or not os.path.exists(file_output):
                #if running on windows
                if os.name == 'nt':
                    string_exec = f"inkscape --export-type=png --export-filename={file_output} {file_input}"
                else:
                    #use the older 0.92 version of the export command
                    #string_exec = f"echo -e '{file_input}\nexport pdf {file_output}\nquit' | inkscape --shell"
                    string_exec = ""
                #print(string_exec)
                print(f"Converting {file_input} to {file_output}")
                os.system(string_exec)
            else:
                print(f"Skipping {file_input} to {file_output}")
            
            
            pass

def test_for_inkscape():
    import subprocess
    string_exec = f"inkscape --version"
    #store the output to a string
    try:
        subprocess.check_output(string_exec, shell=True)
    except:
        string_exec = f"sudo apt-get update"
        os.system(string_exec)
        string_exec = f"sudo apt-get install -y inkscape"
        os.system(string_exec)
        #test again
        string_exec = f"inkscape --version"
        try:
            output = subprocess.check_output(string_exec, shell=True)
        except:        
            print("inkscape not found, please install inkscape and add to path")
            exit()
    pass


if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    kwargs["folder"] = folder
    overwrite = False
    kwargs["overwrite"] = overwrite
    #run main using 4 threads
    
    
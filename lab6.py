

import xml.etree.ElementTree as ET
import logging
import os

class FileNotFound(Exception):
    pass

class FileCorrupted(Exception):
    pass

logging.basicConfig(filename = 'my_errors.log', level = logging.ERROR)

def logged(exception_cls, mode):
    """
    :param exception_cls: Exception
    :param mode: way to open file
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_cls as e:
                if mode == "console":
                    print(f"Decorator {e}")
                elif mode == "file":
                    logging.error(e)
                raise e
        return wrapper
    return decorator

class File:
    @logged(FileNotFound, mode = "console")
    def __init__(self, directory, name):
        self.full_path = os.path.join(directory, name)

        if not os.path.exists(directory):
            raise FileNotFound("Файл не знайдено")
        self.tree = ET.parse(self.full_path)
        self.root = self.tree.getroot()
        
        self.directory = directory
        self.name = name     
    
    @logged(FileCorrupted, mode = "console")
    def read_file(self):
        try:
            return ET.tostring(self.root, encoding="unicode")
        except Exception as e:
            raise FileCorrupted(f"Файл {self.name} пошкоджено, не вдалося прочитати. {e}")

    @logged(FileCorrupted, mode = "file") 
    def edit_data(self, text, tag):
        """
        Docstring for edit_data
         :param self: Description
        :param content: Description
        """
        try:
            self.root = ET.Element(tag)
            self.root.text = str(text)
            self.tree = ET.ElementTree(self.root)
            self.tree.write(self.full_path, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            raise FileCorrupted(f"Файл {self.name} пошкоджено, не вдалося змінити. {e}")
        
    @logged(FileCorrupted, mode="file")
    def append_data(self, text, tag):
        """
        Docstring for append_data
        :param self: append data to file
        :param content: content that you want to append
        """
        try:
            new_element = ET.SubElement(self.root, tag)
            new_element.text = str(text)
            self.root[:] = sorted(self.root, key = lambda stud: (stud.tag, stud.text if stud.text else ""))
            self.tree.write(self.full_path, encoding="utf-8", xml_declaration=True)
                
        except Exception as e:
            raise FileCorrupted(f"Файл {self.name} пошкоджено, не вдалося дописати. {e}")


if __name__ == "__main__":
    try:
        file3 = File("C:/Users/Admin/Desktop/labs/lab6", "labfile.xml")
        print(file3.read_file())
        print('\n\n')
        new_data = "<users><user>Student</user></users>"
        file3.edit_data("Student list", "UniversityList")
        print(file3.read_file())

        append_data = "\n<status>Active</status>"

        print('\n\n')
        file3.append_data(append_data, "Student")
        file3.append_data("Zenoviy", "Student")
        file3.append_data("Andriy", "Student")
        file3.append_data("Fndriy", "Student")
        print(file3.read_file())
    
    except Exception as e:
        print(f"Помилка {e}")
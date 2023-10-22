    # def set_final_path():
    #     if self.var_destination_same_as_source.get():
    #         if self.var_create_hap_folder_at_source.get():
    #             # Identify the base directory 
    #             base_path = os.path.dirname(file_path)
    #             while os.path.basename(base_path) != self.parent_folder and base_path:
    #                 base_path = os.path.dirname(base_path)
    #             final_path = os.path.join(base_path, "HAP")

    #         else:
    #             final_path = os.path.join(os.path.dirname(file_path), file_name)

    #     return final_path


    # print(set_final_path())
    # input()

# import os
# # files = ["C:/First/Second/Third/TestFile.png", "C:/First/Second/Third/Fourth/TestFile.png"]
# files = [r"C:\Users\Desktop\First\samples",
#          r"C:\Users\Desktop\First\100kPeople_422.mov",
#          r"C:\Users\Desktop\First\100kPeople_422_HAP.mov",
#          r"C:\Users\Desktop\First\samples\100kPeople_422.mov",
#          r"C:\Users\Desktop\First\samples\100kPeople_NotchLC.mov",
#          r"C:\Users\Desktop\Second\sub",
#          r"C:\Users\Desktop\Second\TCBLogo_White.png",
#          r"C:\Users\Desktop\Second\test.png",
#          r"C:\Users\Desktop\Second\sub\sub sub",
#          r"C:\Users\Desktop\Second\sub\TCBLogo_White.png",
#          r"C:\Users\Desktop\Second\sub\sub sub\TCBLogo_White - Copy.png"]


# def common_parent_folder(paths):
#     """Return the highest common parent folder from a list of paths."""
#     common_prefix = os.path.commonprefix(paths)
#     return os.path.dirname(common_prefix)

# def relative_to_common(file, common_path):
#     """Get the relative path from common path to the file."""
#     return os.path.relpath(file, common_path)


# parent_folder = common_parent_folder(files)
# insert_folder = os.path.join(parent_folder, "INSERT")

# for file in files:
#     relative_path = relative_to_common(file, parent_folder)
#     final_path = os.path.join(insert_folder, relative_path)
#     print(final_path)


import os
import re

files = ["C:/First//TestFile_V215.png", "C:/First/Second/TestFile_v1.png","C:/First/Second/NoVersion.png"]

for file in files:
    file = os.path.basename(file)
    file = os.path.splitext(file)[0]
    if file.lower().find("_v") > 0:
        file_prefix = file[:file.lower().rfind("_v")]
        file_version = file[file.lower().rfind("_v"):]
        file = file_prefix + "_HAP" + file_version
    else:

        file = file + "_HAP"
    print(file)
    

# for file in files:
#     file = os.path.basename(file)
#     file = os.path.splitext(file)[0]
    
#     # Remove _v or _V and anything that follows
#     file_prefix = re.sub(r'_v\d*', '', file, flags=re.IGNORECASE)
    
#     print(file_prefix)
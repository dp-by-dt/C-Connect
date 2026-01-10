import os


def delete_profile_picture_file(pic_url):
    if not pic_url:
        return

    # If stored locally
    file_path = pic_url.replace("/static/", "static/") #------ TO DO: If change in storage, this might want to be modified
    if os.path.exists(file_path):
        os.remove(file_path)

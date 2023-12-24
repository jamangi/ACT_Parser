import psutil

def is_file_in_use(file_path):
    for process in psutil.process_iter(['pid', 'open_files']):
        try:
            open_files = process.info['open_files']
            if any(file_path == file_info.path for file_info in open_files):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
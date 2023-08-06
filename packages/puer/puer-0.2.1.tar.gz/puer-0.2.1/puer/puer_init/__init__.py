import os


def create_folder(path, name):
    os.chdir(path)
    os.mkdir(name)


def main():
    cwd = os.getcwd()
    print("Current directory:", cwd)
    create_folder(cwd, "apps")
    print("Apps folder created")
    apps_dir = os.path.join(cwd, "apps")
    create_folder(apps_dir, "base")
    print("Base app folder created")
    with open(os.path.join(cwd, "manage.py"), "a+") as manage_file:
        manage_file.write(
            """
            #!/usr/bin/env python3
            from puer.manager import Manager
            
            
            if __name__ == "__main__":
                args = Manager.parse_args()
                Manager(args)
            """
        )

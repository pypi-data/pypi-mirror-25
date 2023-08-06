import os


def create_folder(path, name):
    os.chdir(path)
    os.mkdir(name)


def main():
    cwd = os.getcwd()
    create_folder(cwd, "apps")
    apps_dir = os.path.join(cwd, "apps")
    create_folder(apps_dir, "base")
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

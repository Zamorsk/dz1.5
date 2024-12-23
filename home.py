import os
import sys
import tarfile
#4 19 so sdvigom
class Home:
    def __init__(self, tar_file):
        self.tar_file = tar_file
        self.cwd = "/"
        self.fs = {}
        self.mount()

    def mount(self):
        try:
            with tarfile.open(self.tar_file, 'r') as f:
                for file in f.getnames():
                    self.fs[file] = None
        except FileNotFoundError:
            print(f"File {self.tar_file} not found.")
            sys.exit(1)

    def ls(self):
        for file in self.fs:
            if file.startswith(self.cwd.strip("/")) and len(file) != len(self.cwd.strip("/")):
                print(file)

    def cd(self, args):
        if not args:
            self.cwd = "/"
            return
        self.cwd = os.path.join(self.cwd, args)

    def exit(self):
        sys.exit(0)

    def find(self, args):
        for file in self.fs:
            if args in file:
                print(file)

    def rev(self, args):
        with tarfile.open(self.tar_file, 'r') as f:
            for tar_file_name in f.getnames():
                if args == tar_file_name:
                    info = f.getmember(tar_file_name)
                    t = f.extractfile(info).read()
                    s = t.decode()
                    print(s[::-1])

    def clear(self):
        os.system("clear")

    def parse_command(self, command):
        cmd, *args = command.split()
        if hasattr(self, cmd):
            getattr(self, cmd)(*args)

    def run(self):
        while True:
            try:
                command = input(f"{self.cwd}% ").strip()
                if not command:
                    continue
                self.parse_command(command)
            except KeyboardInterrupt:
                print()
                continue

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python home.py <tar_file>")
        sys.exit(1)
    tar_file = sys.argv[1]
    shell = Home(tar_file)
    shell.run()
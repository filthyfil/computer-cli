class Linter():
    unsafe_bash_dict = ["~", ," / ", "..", "mv", "cp", "rm", "chmod", "chown", "chgrp", "ln", "mkdir", "rmdir", "mkfs", "mount", "umount", "dd", "parted", "fdisk", "sfdisk", "sgdisk", "cfdisk"]
    unsafe_write_dict = [" os", " subprocess"]
    unsafe_filepath_dict = ["~", ".."]

    def lint_bash(self, command):
        for unsafe in self.unsafe_bash_dict:
            if command.find(unsafe) != -1:
                return False
        return True

    def lint_write(self, command):
        for unsafe in self.unsafe_write_dict:
            if command.find(unsafe) != -1:
                return False
        return True

    def lint_filepath(self, command):
        for unsafe in self.unsafe_filepath_dict:
            if command.find(unsafe) != -1:
                return False
        return True

    def check_python(self, command):
        if "python" in command:
            return True
        return False

linter = Linter()
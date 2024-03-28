from tkinter import messagebox
import subprocess


class Utils:
    @staticmethod
    def validate_positive_integer(input_value):
        if input_value == '':
            return False
        try:
            value = int(input_value)
            if value > 0:
                return True
            else:
                return False
        except ValueError:
            return False


class MessageUtils:
    @staticmethod
    def show_message(title, message):
        messagebox.showinfo(title, message)

    @staticmethod
    def show_error(title, message):
        messagebox.showerror(title, message)


class FileUtils:
    @staticmethod
    def open_file(file_name, event=None):
        """Open a file with the default application."""
        try:
            subprocess.check_call(f'start {file_name}', shell=True)
        except subprocess.CalledProcessError:
            print(f"Failed to open file: {file_name}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

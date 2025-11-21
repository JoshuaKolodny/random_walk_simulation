from tkinter import messagebox
import subprocess


class Utils:
    @staticmethod
    def validate_positive_integer(input_value: str) -> bool:
        """
        Validates if the input value is a positive integer.

        Args:
            input_value (str): The input value to validate.

        Returns:
            bool: True if the input value is a positive integer, False otherwise.
        """
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
    def show_message(title: str, message: str) -> None:
        """
        Displays an informational message box with the given title and message.

        Args:
            title (str): The title of the message box.
            message (str): The message to display.
        """
        messagebox.showinfo(title, message)

    @staticmethod
    def show_error(title: str, message: str) -> None:
        """
        Displays an error message box with the given title and message.

        Args:
            title (str): The title of the message box.
            message (str): The message to display.
        """
        messagebox.showerror(title, message)


class FileUtils:
    @staticmethod
    def open_file(file_name: str, event=None) -> None:
        """
        Opens a file with the default application.

        Args:
            file_name (str): The name of the file to open.
            event: Optional; Default is None. Not currently used.

        Raises:
            subprocess.CalledProcessError: If the subprocess call to open the file fails.
            Exception: For any other exceptions that may occur.
        """
        try:
            subprocess.check_call(f'start {file_name}', shell=True)
        except subprocess.CalledProcessError:
            print(f"Failed to open file: {file_name}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
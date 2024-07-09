import os


def error_message_detail(error, error_detail):
    # extracting filename and line number where the error occured
    _, _, exc_tb = error_detail.exec_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    # creating error message
    error_message = f"Error ocuured python script name [{file_name}] line number [{exc_tb.tb_lineno}] error message [{str(error)}]"

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self) -> str:
        # overriding string representation to return detailed error message
        return self.error_message

from flask import flash

class FlashMessages:
    @staticmethod
    def flash_success(msg):
        flash(msg, "success")

    @staticmethod
    def flash_error(msg):
        flash(msg, "danger")

    @staticmethod
    def flash_warning(msg):
        flash(msg, "warning")

    @staticmethod
    def flash_info(msg):
        flash(msg, "info")
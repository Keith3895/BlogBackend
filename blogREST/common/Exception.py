class ValidationException(Exception):
    def __init__(self, message='Validation error', error_field_name='unknown_field'):
        super().__init__()
        self.error_field_name = error_field_name
        self.message = message

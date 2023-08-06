# Define your microservice logic in this file.


class MicroService:
    """
    This class defines your custom AI logic. Fill in each method
    below to create your microservice.
    """
    def __init__(self):
        """
        Declare your class variables here.
        eg: self.trained_model = None
        """
        self.use_custom_validation = False

    def validate_input(self, input_data, input_headers):
        """
        This method can be used to add custom validation logic for your
        microservice. By default inputschema.json is parsed and used
        to validate your microservice. Set 'self.use_custom_validation'
        to True if you want this method called on every request.

        Throw an exception on bad input or bad headers to signal
        an invalid request. This method will be called before self.run.
        """
        pass

    def load(self):
        """
        This method is called only once by the application handler.
        Use this method to set class variables required by 'run'.
        """
        pass

    def run(self, input_data):
        """
        This method is run every time a request hits the microservice.
        Make sure this method is fast!
        """
        return input_data

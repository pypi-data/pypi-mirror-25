def upload_failed(func):
    """ Prints upload failed message. """

    def function_wrapper(*args):
        print('='*70)
        print("[\033[91m ERROR \033[0m] Upload failed!")
        print('='*70)

        return func(*args)
    return function_wrapper

class ProjectNotSetError(Exception):

    @upload_failed
    def __init__(self):
        msg = "Project not set!"
        super().__init__(msg)

class SuiteNotSetError(Exception):

    @upload_failed
    def __init__(self):
        msg = "Test suite not set!"
        super().__init__(msg)

class RunNotSetError(Exception):

    @upload_failed
    def __init__(self):
        msg = "Test run not set!"
        super().__init__(msg)

class ProjectNotFoundError(Exception):

    @upload_failed
    def __init__(self, value):
        msg = " Project '{}' was not found in TestRail!".format(value)
        super().__init__(msg)

class SuiteNotFoundError(Exception):

    @upload_failed
    def __init__(self, value, project_id):

        msg = "Test suite '{}' not found for project {} in TestRail!".format(value, project_id)
        super().__init__(msg)

class RunNotFoundError(Exception):

    @upload_failed
    def __init__(self, value, project_id):

        msg = "Test run '{}' not found for project {} in TestRail!".format(value, project_id)
        super().__init__(msg)

class MilestoneNotFoundError(Exception):

    @upload_failed
    def __init__(self, value, project_id):

        msg = "Milestone '{}' not found for project {} in TestRail!".format(value, project_id)
        super().__init__(msg)

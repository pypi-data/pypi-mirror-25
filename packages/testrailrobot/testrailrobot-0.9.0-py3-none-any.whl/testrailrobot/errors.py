class NotFoundError(Exception):

    def __init__(self):

        if self.value:
            super().__init__(self.msg_not_found)
        else:
            super().__init__(self.msg_not_set)

class ProjectNotFoundError(NotFoundError):

    def __init__(self, value = None):
        self.value = value
        self.msg_not_found = "Project '{}' was not found in TestRail!".format(value)
        self.msg_not_set = 'Project must be set.'

        super().__init__()

class SuiteNotFoundError(NotFoundError):

    def __init__(self, value = None, project_id = None):
        self.value = value
        self.msg_not_found = "Test suite '{}' was not found for project {} in TestRail!".format(value, project_id)
        self.msg_not_set = 'Test suite must be set.'

        super().__init__()

class RunNotFoundError(NotFoundError):

    def __init__(self, value = None, project_id = None):
        self.value = value
        self.msg_not_found = "Test run '{}' was not found for project {} in TestRail!".format(value, project_id)
        self.msg_not_set = 'Test run must be set.'

        super().__init__()

class MilestoneNotFoundError(NotFoundError):

    def __init__(self, value = None, project_id = None):
        self.value = value
        self.msg_not_found = "Milestone '{}' was not found for project {} in TestRail!".format(value, project_id)
        self.msg_not_set = 'Milesotne must be set.'

        super().__init__()

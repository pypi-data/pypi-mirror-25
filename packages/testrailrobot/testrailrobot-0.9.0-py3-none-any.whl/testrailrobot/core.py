#!/usr/bin/env python
# Version: 0.9.0
# Author: Tanel Torn
# Python version: 3.6
#
import os
import sys
import traceback
import time
import logging
from copy import deepcopy
import xml.etree.ElementTree as ET
from testrailrobot.api import APIClient, APIError
from testrailrobot.errors import *

#
# Decorator functions
#

def update_progress(message):
    """ Decorator for printing progress to terminal.

    Args:
        message (str): Message to be printed
    """
    def print_progress_decorator(func):
        def function_wrapper(*args):
            TestRail.print_progress(0, message)
            func(*args)
            TestRail.print_progress(100, message)
        return function_wrapper
    return print_progress_decorator

def print_header(status, error_flag, message):
    """ Decorator for printing script's status to terminal.

    Args:
        message (str): Message to be printed
    """
    def print_header_decorator(func):
        def function_wrapper(*args):
            if error_flag:
                TestRail.print_status(status, 91, message)
            else:
                TestRail.print_status(status, 92, message)
            func(*args)
        return function_wrapper
    return print_header_decorator

def project_must_be_set(func):
    """ Raises an error if the project is not set.

    Raises:
        ProjectNotSetError
    """
    def function_wrapper(*args):
        if args[0].project is None:
            TestRail.print_status('ERROR', 91, 'Project not set.')
            raise ProjectNotFoundError()
        return func(*args)
    return function_wrapper

def suite_must_be_set(func):
    """ Raises an error if the test suite is not set.

    Raises:
        SuiteNotSetError
    """
    def function_wrapper(*args):
        if args[0].suite is None:
            TestRail.print_status('ERROR', 91, 'Test suite not set.')
            raise SuiteNotFoundError()
        return func(*args)
    return function_wrapper

def run_must_be_set(func):
    """ Raises an error if the test run is not set.

    Raises:
        RunNotSetError
    """
    def function_wrapper(*args):
        if args[0].run is None:
            TestRail.print_status('ERROR', 91, 'Test run not set.')
            raise RunNotSetError()
        return func(*args)
    return function_wrapper


class TestRail:
    """ A class for connecting to TestRail and to publish Robot results. """

    def __init__(self, server, user, password):

        # connection details
        self.server = server
        self.user = user
        self.password = password

        # parsed results
        self.results = []

        # statistics
        self.cases_updated = 0
        self.cases_inserted = 0
        self.results_added = 0

        # default options
        self.options = {

            # set this to False if you do not want to insert new cases
            # to TestRail from Robot results and only want to upload test
            # results to existing cases
            "insert_new_cases": True,

            # set this to False if you do not want to update test step
            # information of existing TestRail cases and only want to upload
            # test results
            "update_existing_cases": True,

            # set this to False if you do not want to add new tests to a
            # existing TestRail run (when run is set) and only want to upload
            # results for tests already in the run
            "add_cases_to_existing_run": True,

            # specifies the ID of the TestRail template to be used when
            # inserting a new test case. default values in TestRail:
            # 1 - Test Case (Text)
            # 2 - Test Case (Steps)
            "default_case_template_id": 2,

            # specifies the ID of the TestRail case type to be used when
            # inserting a new test case. default values in TestRail:
            # 1 - acceptance
            # 2 - accessibility
            # 3 - automated
            # ...
            # 12 - usability
            "default_case_type_id": 3,

            # name of the new test run
            "new_test_run_name": "Robot - {}".format(time.strftime("%d/%m/%Y %H:%M")),

            # name of the tests section where new cases will be inserted
            "section_name": "Kategoriseerimata",

            # name of the field in TestRail that specifies if results can be
            # uploaded to a given test
            "custom_is_autotest_field_name": "custom_autotest",
        }

        # set logging
        self._set_logging()

        # connect to TestRail
        self._connect()

        self._TestRail__project = None
        self._TestRail__suite = None
        self._TestRail__run = None
        self._TestRail__milestone = None

    @staticmethod
    def print_progress(progress, message):
        """ Prints the script's progress to terminal.

        E.g.
        connecting to testrail...                100%

        Args:
            progress (numeric): Progress of the current task
            message (str): Message of current task to be printed
        """
        print("{0: <40} {1: >3}%".format(message, round(progress)), sep='', end='\r')

    @staticmethod
    def print_status(status, code, message):
        """ Print script's status to terminal.

        E.g.
        ======================================================================
        [ ERROR ] Project not found.
        ======================================================================

        Args:
            status (string): Status of the script (e.g. 'ERROR')
            code (int):      Code of the color in which the status will be displayed:
                             91 - red
                             92 - green
            message (str):   Message to be printed
        """
        print('='*70)
        print("[\033[{}m {} \033[0m] {}".format(code, status, message))
        print('='*70)

    #
    # Public methods
    #

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, values):
        """ Sets the given options.

        Input values will be added to default options. Duplicate entries will
        not be added, default values will be overwritten.

        Args:
            values (dict): A dict containing option/value pairs
        Raises:
            Exception: Raises an Exception if the input parameter is not a
                       Python dict.
        """
        try:
            if isinstance(values, dict):
                if hasattr(self, 'options'):
                    for k, v in values.items():
                        self.__options[k] = v
                        self.logger.info("Set new value for option '{}': {}".format(k, v))
                else:
                    self.__options = values
            else:
                raise Exception('Options must be specified as Python dict.')
        except Exception as e:
            self._log_and_raise(e)


    # get/set project

    @property
    def project(self):
        return self.__project

    @project.setter
    @update_progress('setting project...')
    def project(self, value):
        """ Specifies the project in TestRail to use.

        All cases and results will be uploaded to the specified project. The
        first test suite of the project will automatically be set. This will be
        the suite 'Master' for a project that uses a single repository for all
        test cases. Also, the test run and milestone will be unset.

        Args:
            value (int/str): ID or name of the project in TestRail
        Raises:
            ProjectNotFoundError: Raises an exception if the project is not
                                  found in TestRail.
        """
        try:
            self.logger.info('Trying to set project: {}'.format(value))

            project = self._get_testrail_project(value)
            if not project:
                raise ProjectNotFoundError(value)

            self.__project = project
            self.logger.info("Project set to: {} ('{}')".format(self.project['id'], self.project['name']))

            self.suite = {}

            self._TestRail__run = None
            self._TestRail__milestone = None

        except Exception as e:
            self._log_and_raise(e)


    # get/set suite

    @property
    def suite(self):
        return self.__suite

    @suite.setter
    @project_must_be_set
    @update_progress('setting test suite...')
    def suite(self, value):
        """ Specifies the test suite in TestRail to use.

        All cases will be uploaded to the specified suite.

        Args:
            value (int/str): ID or name of the suite in TestRail
        Raises:
            SuiteNotFoundError: Raises an exception if the suite is not found
                                in TestRail.
        """
        try:
            self.logger.info('Trying to set test suite: {}'.format(value))

            suite = self._get_testrail_suite(value, self.project.get('id'))
            if not suite:
                raise SuiteNotFoundError(value, self.project.get('id'))

            self.__suite = suite
            self.logger.info("Test suite set to: {} ('{}')".format(self.suite['id'], self.suite['name']))

        except Exception as e:
            self._log_and_raise(e)


    # get/set run

    @property
    def run(self):
        return self.__run

    @run.setter
    @project_must_be_set
    @update_progress('setting test run...')
    def run(self, value):
        """ Specifies the test run in TestRail to use.

        All test results will be uploaded to the specified run. If the run's
        suite does not match the set suite, the suite will be set according to
        the test run.

        Args:
            value (int/str): ID or name of the run in TestRail
        Raises:
            RunNotFoundError: Raises an exception if the run is not found in
                              TestRail.
        """
        try:
            self.logger.info('Trying to set test run: {}'.format(value))

            run = self._get_testrail_run(value, self.project.get('id'))
            if not run:
                raise RunNotFoundError(value, self.project.get('id'))

            self.__run = run
            self.logger.info("Test run set to: {} ('{}')".format(self.run['id'], self.run['name']))

            if self.suite.get('id') != run['suite_id']:
                self.suite = run['suite_id']

        except Exception as e:
            self._log_and_raise(e)


    # get/set milestone

    @property
    def milestone(self):
        return self.__milestone

    @milestone.setter
    @project_must_be_set
    @update_progress('setting milestone...')
    def milestone(self, value):
        """ Specifies the milestone in TestRail to use.

        All test results will be uploaded under the specified milestone.

        Args:
            value (int/str): ID or name of the run in TestRail
        Raises:
            MilestoneNotFoundError: Raises an exception if the milestone is not
                                    found in TestRail.
        """
        try:
            self.logger.info('Trying to set milestone: {}'.format(value))

            milestone = self._get_testrail_milestone(value, self.project.get('id'))
            if not milestone:
                raise MilestoneNotFoundError(value, self.project.get('id'))

            self.__milestone = milestone
            self.logger.info("Milestone set to: {} ('{}')".format(self.milestone['id'], self.milestone['name']))

        except Exception as e:
            self._log_and_raise(e)



    # parse results

    @update_progress('parsing results...')
    def parse_results(self, path):
        """ Parses the Robot Framework's test results.

        Robot Framework's results will be converted to the correct format for
        uploading them to TestRail.

        Args: path (str): Path to the XML file containing Robot test results.
        """
        try:
            self.logger.info('Trying to parse Robot results...')

            rr = RobotResults(path)

            if rr.errors:
                raise Exception(rr.errors[0])

            for i, r in enumerate(rr.results):
                result = self._parse_result(r)
                self.results.append(result)

                TestRail.print_progress((i + 1) / len(rr.results) * 100, "parsing results...")
            else:
                self.logger.info("Successfully parsed {} Robot result(s).".format(i + 1))

        except Exception as e:
            self._log_and_raise(e)


    # upload results

    @project_must_be_set
    @suite_must_be_set
    def upload_results(self):
        """ Uploads results from Robot Framework to TestRail.

        Depending on the set options, this method will also:
        - Insert new cases to TestRail (if option 'insert_new_cases' is set to True)
        - Update existing cases in TestRail (if option 'update_existing_cases' is set to False)
        - Insert new run to TestRail (if test run is not set)
        - Update an existing run in TestRail (if test run is set)
        - Add cases to existing run (if test run is not set and option 'add_cases_to_existing_run' is set to True)
        """
        try:
            self.cases_updated = 0
            self.cases_inserted = 0

            if not self.results:
                TestRail.print_status('DONE', 92, 'Nothing to upload.')
                self.logger.info("No results to upload.")
                return

            self._prepare_data_for_upload()

            if (self.options.get('update_existing_cases')):
                self._update_cases()

            if (self.options.get('insert_new_cases')):
                self._insert_cases()

            if self.run is not None:
                self._update_existing_run()
            else:
                self._create_new_run(self.options.get('new_test_run_name'))

            self._post_results_to_testrail()

            self._log_statistics()
            self._print_statistics()

        except Exception as e:
            self._log_and_raise(e)

    #
    # Private methods
    #

    @update_progress('connecting to testrail...')
    def _connect(self):
        """ Establishes a connection to the TestRail instance. """

        try:
            self.logger.info('Trying to connect to TestRail instance: {}'.format(self.server))

            self.client = APIClient(self.server)
            self.client.user = self.user
            self.client.password = self.password

            # shorthand methods for sending GET and POST requests
            self.get = self.client.send_get
            self.post = self.client.send_post

            # set testrail user
            self.testrail_user = self.get('get_user_by_email&email=' + self.client.user)

            self.logger.info('Connected to TestRail instance: {}'.format(self.server))

        except Exception as e:
            self._log_and_raise(e)


    def _get_testrail_project(self, value):
        """ Retrieves a project from TestRail.

        If the 'value' parameter is empty, the first project will be returned.

        Args:
            value (int/str): ID or name of the project in TestRail
        Returns:
            A dict containing project data if the project is in TestRail,
            False otherwise
        """
        self.logger.debug('Trying to retrieve project from TestRail: {}'.format(value))
        projects = self.get('get_projects&is_completed=0')

        if projects:
            if value:
                key = 'id' if isinstance(value, int) else 'name'
                matching_projects = [p for p in projects if p.get(key) == value]
            else:
                matching_projects = projects

            if matching_projects:
                self.logger.debug('Retrieved project: {}'.format(matching_projects[0]))
                return matching_projects[0]

        return False

    def _get_testrail_suite(self, value, project_id):
        """ Retrieves a test suite from TestRail.

        If the 'value' parameter is empty, the first suite will be returned for
        the given project (suite 'Master' for a project with single repository).

        Args:
            value (int/str): ID or name of the test suite in TestRail
            project_id (int): ID of the project in TestRail for which the
                              test suites will be retrieved
        Returns:
            A dict containing test suite data if the suite is in TestRail,
            False otherwise
        """
        self.logger.debug('Trying to retrieve test suite from TestRail: {}'.format(value))
        suites = self.get('get_suites/{}'.format(project_id))

        if suites:
            if value:
                key = 'id' if isinstance(value, int) else 'name'
                matching_suites = [s for s in suites if s.get(key) == value]
            else:
                matching_suites = suites

            if matching_suites:
                self.logger.debug('Retrieved test suite: {}'.format(matching_suites[0]))
                return matching_suites[0]

        return False

    def _get_testrail_run(self, value, project_id):
        """ Retrieves a test run from TestRail.

        If the 'value' parameter is empty, the latest run will be returned for
        the given project.

        Args:
            value (int/str): ID or name of the test run in TestRail
            project_id (int): ID of the project in TestRail for which the
                              test runs will be retrieved
        Returns:
            A dict containing test run data if the run is in TestRail, False
            otherwise
        """
        self.logger.debug('Trying to retrieve test run from TestRail: {}'.format(value))
        runs = self.get('get_runs/{}&is_completed=0'.format(project_id))

        if runs:
            if value:
                key = 'id' if isinstance(value, int) else 'name'
                matching_runs = [r for r in runs if r.get(key) == value]
            else:
                matching_runs = runs

            if matching_runs:
                self.logger.debug('Retrieved test run: {}'.format(matching_runs[0]))
                return matching_runs[0]

        return False

    def _get_testrail_milestone(self, value, project_id):
        """ Retrieves a milestone from TestRail.

        If the 'value' parameter is empty, the next uncompleted milestone will
        be returned for the given project.

        Args:
            value (int/str): ID or name of the milestone in TestRail
            project_id (int): ID of the project in TestRail for which the
                              test runs will be retrieved
        Returns:
            A dict containing test run data if the run is in TestRail, False
            otherwise
        """
        self.logger.debug('Trying to retrieve milestone from TestRail: {}'.format(value))
        milestones = self.get('get_milestones/{}&is_completed=0'.format(project_id))

        if milestones:
            if value:
                key = 'id' if isinstance(value, int) else 'name'
                matching_milestones = [m for m in milestones if m.get(key) == value]
            else:
                matching_milestones = milestones

            if matching_milestones:
                self.logger.debug('Retrieved milestone: {}'.format(matching_milestones[0]))
                return matching_milestones[0]

        return False


    @project_must_be_set
    @suite_must_be_set
    def _get_testrail_tests(self):
        """ Retrieves automated tests from TestRail.

        Retrieves results for the given project and suite.

        Returns:
            A list of automated tests in TestRail
        """
        self.logger.debug('Trying to retrieve automated tests for project: {} and suite: {}'.format(self.project.get('id'), self.suite.get('id')))

        request_str = "get_cases/{}&suite_id={}".format(self.project.get('id'), self.suite.get('id'))
        tests = self.get(request_str)

        tests = [t for t in tests if t.get(self.options.get('custom_is_autotest_field_name'))]

        self.logger.debug('Retrieved tests: {}'.format(tests))
        return tests

    def _get_testrail_test_by_name(self, name, testrail_tests = None):
        """ Retrieves a test from TestRail with a given name.

        If the second argument testrail_tests is specified, the test will be
        searched from that list, otherwise a request will be made to TestRail
        to retrieve the tests in TestRail.

        Args:
            name (str): Name of the test
            testrail_tests (list): List of TestRail tests, optional
        Returns:
            A dict containing TestRail test data if test is in TestRail, False
            otherwise
        """
        self.logger.debug('Trying to retrieve test from TestRail by name: {}'.format(name))

        if not testrail_tests:
            testrail_tests = self._get_testrail_tests()

        matching_testrail_tests = [t for t in testrail_tests if t.get('title') == name]

        if matching_testrail_tests:
            self.logger.debug('Retrieved test: {}'.format(matching_testrail_tests[0]))
            return matching_testrail_tests[0]

        return False

    def _get_testrail_status_id(self, status):
        """ Returns a TestRail status id for a given status.

        Args:
            status (str): Status string
        """
        self.logger.debug('Trying to retrieve status ID for status: {}'.format(status))
        if (status.lower() in ['pass', 'passed', 'ok']):
            self.logger.debug('Retrieved status ID: 1')
            return 1
        elif (status.lower() in ['fail', 'failed', 'nok', 'not ok']):
            self.logger.debug('Retrieved status ID: 5')
            return 5

        self.logger.warning('Could not find status ID for status: {}'.format(status))
        return False


    def _prepare_data_for_upload(self):
        """ Prepares test results to be ready for upload. """

        # using another variable here, because some tests might be excluded
        # from the original list of results to be uploaded. this will keep
        # the original list of results unchanged and allows it to be used
        # to upload results to another run or suite with different options
        self.results_to_upload = deepcopy(self.results)

        self._add_data_from_testrail()

    def _add_data_from_testrail(self):
        """ Adds TestRail data to the results.

        If a test is already in TestRail, ID, type ID and template ID of the
        case will be added to corresponding test result.
        """
        testrail_tests = self._get_testrail_tests()

        for r in self.results_to_upload:
            matching_testrail_test = self._get_testrail_test_by_name(r['title'], testrail_tests)

            if matching_testrail_test:
                r['id'] = matching_testrail_test.get('id')
                r['template_id'] = matching_testrail_test.get('template_id')
                r['type_id'] = matching_testrail_test.get('type_id')
            else:
                r['id'] = None
                r['template_id'] = self.options.get('default_case_template_id')
                r['type_id'] = self.options.get('default_case_type_id')
            r['case_id'] = r['id']

    def _parse_steps_as_text(self, steps):
        """ Parses steps as text (single field).

        Args:
            steps: Robot steps to be parsed
        Returns:
            A dict containing step data
        """

        parsed_steps = ''

        for i, s in enumerate(steps):
            content = s.get('name')
            if s.get('arguments'):
                content += " | {}".format(' | '.join(s['arguments']))

            parsed_steps += "{}. {}\n".format(i + 1, content)

        return parsed_steps

    def _parse_steps_as_separated(self, steps):
        """ Parses steps as separated fields.

        Args:
            steps: Robot steps to be parsed
        Returns:
            A dict containing step data
        """

        parsed_steps = []

        for s in steps:
            content = s.get('name')
            if s.get('arguments'):
                content += " | {}".format(' | '.join(s['arguments']))
            actual = s.get('message')
            status_id = self._get_testrail_status_id(s.get('status'))

            parsed_steps.append({
                'content': content,
                'actual': actual,
                'status_id': status_id,
            })

        return parsed_steps

    def _parse_result(self, robot_result):
        """ Parses a robot result and adds it to the list of results.

        Args:
            robot_result (dict): A dict containing Robot test result
        Returns:
            A dict containing parsed result
        """
        self.logger.debug('Trying to parse result: {}'.format(robot_result))

        result = {}

        result['title'] = robot_result.get('title')
        result['status'] = robot_result.get('status')
        result['comment'] = robot_result.get('message')
        result[self.options['custom_is_autotest_field_name']] = True
        result['status_id'] = self._get_testrail_status_id(robot_result.get('status'))

        result['custom_steps'] = self._parse_steps_as_text(robot_result.get('steps'))
        result['custom_steps_separated'] = self._parse_steps_as_separated(robot_result.get('steps'))

        # TestRail API uses different fields for adding steps and step results:
        # 'custom_steps_separated' - for adding steps
        # 'custom_step_results' - for adding step results
        result['custom_step_results'] = result['custom_steps_separated']

        self.logger.debug('Result parsed.')

        return result


    @project_must_be_set
    @suite_must_be_set
    def _get_section(self):
        """ Retrieves the test case section for automated tests in TestRail.

        If the section is not found, a new section will be created with the
        name specified with the option 'section_name'.

        Return:
            A dict containing the data of the test case section for automated
            tests.
        """
        self.logger.debug('Trying to retrieve test section for automated tests from TestRail...')

        request_str = "get_sections/{}&suite_id={}".format(self.project.get('id'), self.suite.get('id'))
        sections = self.get(request_str)

        section_name = self.options.get('section_name') if self.options.get('section_name') else 'Kategoriseerimata'
        matching_sections = [s for s in sections if s.get('name') == section_name]

        if matching_sections:
            section = matching_sections[0]
            self.logger.debug('Retrieved section: {}'.format(section))
        else:
            section = self._create_section(section_name)

        return section

    @project_must_be_set
    @suite_must_be_set
    def _create_section(self, name):
        """ Creates a new section for automated tests in TestRail.

        Args:
            name (str): Name of the section to be created
        Return:
            A dict containing the data of the test case section for automated
            tests.
        """
        self.logger.info('Trying to create new section for automated tests in TestRail: {}'.format(name))

        section = self.post("add_section/{}".format(self.project.get('id')), {
            "name": name,
            "suite_id": self.suite.get('id')
        })

        self.logger.info("Created a new section: {} ('{}')".format(section.get('id'), section.get('name')))
        return section

    @project_must_be_set
    @suite_must_be_set
    @update_progress('adding new test run...')
    def _create_new_run(self, name):
        """ Creates a new test run.

        Test cases from the list of results will be added to the new run.

        Args:
            name (str): Name of the test run to be created
        """
        self.logger.info('Trying to create a new test run in TestRail: '.format(name))

        run = self.post(
            "add_run/{}".format(self.project.get('id')),
            {
                'suite_id': self.suite.get('id'),
                'name': name,
                'milestone_id': self.milestone.get('id') if self.milestone else None,
                'assignedto_id': self.testrail_user.get('id'),
                'include_all': False,
                'case_ids': [c.get('case_id') for c in self.results_to_upload]
            }
        )
        self.logger.info("Created a new test run: {} ('{}')".format(run.get('id'), run.get('name')))

        self.run = run.get('id')

        return run

    @run_must_be_set
    @update_progress('update existing test run...')
    def _update_existing_run(self):
        """ Updates an existing run.

        If the option 'add_cases_to_existing_run' is set to True, cases not
        already in the run will be added to the run from the list of results.
        If the option is set to False, cases not in the run will be discarded.
        """
        self.logger.info('Trying to update existing test run in TestRail: '.format(self.run.get('id')))
        tests_in_run = self.get('get_tests/{}'.format(self.run.get('id')))

        if (self.options.get('add_cases_to_existing_run')):
            self.logger.info('Trying to add cases to test run: {}'.format(self.run.get('id')))

            run_cases = [t.get('case_id') for t in tests_in_run]

            cases_to_add = [c for c in self.results_to_upload if c.get('id') not in run_cases]
            if cases_to_add:
                for i, c in enumerate(cases_to_add):
                    tests_in_run.append(c)

                run = self.post("update_run/{}".format(self.run.get('id')), {
                    "case_ids": [c.get('case_id') for c in tests_in_run if c.get('case_id') is not None]
                })
                self.logger.debug('Added cases: {}'.format(cases_to_add))
                self.logger.info("Added {} test case(s) to run: {}".format(len(cases_to_add), self.run.get('id')))
            else:
                self.logger.info('All cases already in test run.')

        else:
            self.logger.debug('Excluding cases not in test run: {}'.format(self.run.get('id')))
            self.results_to_upload = [r for r in self.results_to_upload for t in tests_in_run if t['case_id'] == r['id']]

            if not self.results_to_upload:
                print("{0: <80}".format("No results to upload."))
                self.logger.warning("No results to upload.")
                return

    @update_progress('inserting new cases...')
    def _insert_cases(self):
        """ Inserts new test cases to TestRail.

        All cases not already in TestRail will be added under the section
        specified with the option 'section_name'.
        """
        self.logger.info('Trying to insert new cases in TestRail...')

        cases_to_insert = [r for r in self.results_to_upload if r.get('id') is None]
        section = self._get_section()

        if cases_to_insert:
            for i, c in enumerate(cases_to_insert):
                t = self.post('add_case/{}'.format(section['id']), c)
                self.cases_inserted += 1

                # update results list with TestRail ID's
                for r in [r for r in self.results_to_upload if r['title'] == t['title']]:
                    r['id'] = t['id']       # API uses id to upload the case
                    r['case_id'] = t['id']  # API uses case_id to upload the result

                self.logger.debug("Inserted new case: {} ('{}')".format(t['id'], t['title']))
                TestRail.print_progress((i + 1) / len(cases_to_insert) * 100, "inserting new cases...")
            else:
                self.logger.info("Inserted {} new test case(s).".format(i + 1))
        else:
            self.logger.info('No new cases to insert.')

    @update_progress('updating existing cases...')
    def _update_cases(self):
        """ Updates test step information of test cases in TestRail. """

        self.logger.info('Trying to update existing cases in TestRail...')

        cases_to_update = [r for r in self.results_to_upload if r.get('id') is not None]

        if cases_to_update:
            for i, c in enumerate(cases_to_update):
                self.post('update_case/{}'.format(c['id']), c)
                self.cases_updated += 1

                self.logger.debug("Updated case: {}".format(c['id']))
                TestRail.print_progress((i + 1) / len(cases_to_update) * 100, "updating existing cases...")
            else:
                self.logger.info("Updated {} existing case(s) in TestRail.".format(i + 1))
        else:
            self.logger.info('No cases to update.')

    @run_must_be_set
    @update_progress('uploading results...')
    def _post_results_to_testrail(self):
        """ Posts results to TestRail. """

        self.logger.info('Trying to post results to TestRail...')

        results_to_post = [c for c in self.results_to_upload if c.get('case_id') is not None]

        if results_to_post:
            self.post(
                "add_results_for_cases/{}".format(self.run['id']), {
                    "results": results_to_post
                })
            self.logger.info("Posted {} result(s).".format(len(results_to_post)))
        else:
            self.logger.warning('No results to post.')


    def _set_logging(self):
        """ Sets logging. """

        # set handler
        handler = logging.FileHandler('testrailrobot.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        # instantiate logger object
        self.logger = logging.getLogger()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        # clear the log file
        open('testrailrobot.log', 'w').close()

    @project_must_be_set
    @suite_must_be_set
    @run_must_be_set
    def _log_statistics(self):
        """ Logs statistics of the results uploaded. """

        log_message = "Results successfully uploaded to TestRail!"
        log_message += " Project: {} ('{}')".format(self.project.get('id'), self.project.get('name'))
        log_message += ", test suite: {} ('{}')".format(self.suite.get('id'), self.suite.get('name'))
        log_message += ", test run: {} ('{}')".format(self.run.get('id'), self.run.get('name'))
        log_message += ", results added: {}".format(len(self.results_to_upload))
        log_message += ", cases inserted: {}".format(self.cases_inserted)
        log_message += ", cases updated: {}.".format(self.cases_updated)
        self.logger.info(log_message)

    @project_must_be_set
    @suite_must_be_set
    @run_must_be_set
    def _print_statistics(self):
        """ Prints statistics of the uploaded results to terminal. """

        print('='*70)
        print("[\033[92m DONE \033[0m] Results successfully uploaded to TestRail!")
        print('='*70)
        print("{0: <13}{1} ('{2}')".format("Project:", self.project.get('id'), self.project.get('name')))
        print("{0: <13}{1} ('{2}')".format("Test suite:", self.suite.get('id'), self.suite.get('name')))
        print("{0: <13}{1} ('{2}')".format("Test run:", self.run.get('id'), self.run.get('name')))
        print('='*70)
        print("{0: <17}{1}".format("Results added:", len(self.results_to_upload)))
        print("{0: <17}{1}".format("Cases inserted:", self.cases_inserted))
        print("{0: <17}{1}".format("Cases updated:", self.cases_updated))
        print('='*70)
        print("Log file:", os.path.abspath("TestRail.log"))

    @print_header('ERROR', 1, 'Upload failed!')
    def _log_and_raise(self, e):
        """ Logs and raises the error. """

        self.logger.exception(str(e))
        raise


class RobotResults:
    """ A class for test results from Robot Framework. """

    def __init__(self, path):
        self.errors = []
        self.results = []

        self._get_results_from_xml(path)

    @property
    def _has_errors(self):
        """ Checks if there are any errors in the Robot results.

        <errors> tag should be empty if there are no errors. """

        self.output_errors = self.output.find('.//errors')

        return self.output_errors is not None and len(self.output_errors) > 0

    def _get_errors(self):
        """ Finds all <msg> tags from the XML file and stores the messages to a
            list. """

        msgs = self.output_errors.findall('msg')
        if (msgs):
            for e in msgs:
                self.errors.append(e.text)
        else:
            self.errors.append("Errors found in the XML file containing test results.")

    def _get_results_from_xml(self, path):
        """ Parses Robot Framework test results from a given XML file.

        For each test, the following fields will be used from XML file:
        * title (str)
        * status (str)
        * message (str)
        * steps (list)

        Example:
        >>> rr = RobotResults('output.xml')
        >>> rr.results
        >>> [
               {
                  'title':'Test Case 1',
                  'status':'FAIL',
                  'message':"Step 2 failed",
                  'steps':[
                     {
                        'name':'Step 1',
                        'status':'PASS',
                        'arguments':[]
                     },
                     {
                        'name':'Step 2',
                        'status':'FAIL',
                        'arguments':['Arg 1', 'Arg 2'],
            			'message':"Step 2 failed"
                     }
                  ]
               }
            ]

        Args:
            path (str): Path to the XML file containing results from
                        Robot Framework.
        Returns:
            List of Robot Framework results.
        """
        try:
            self.output = ET.parse(path)

            if self._has_errors:
                self._get_errors()
                return

            xml_results = self.output.findall('.//test')

            for xmlt in xml_results:
                test = {}
                test['title'] = xmlt.attrib['name']
                test['status'] = xmlt.find('status').attrib['status']
                test['message'] = xmlt.find('status').text
                test['steps'] = []

                for kw in xmlt.findall('kw'):
                    step = {}
                    step['name'] = kw.attrib['name']
                    step['status'] = kw.find('status').attrib['status']
                    step['arguments'] = []
                    for arg in kw.findall('arguments/arg'):
                        step['arguments'].append(arg.text)

                    msg = kw.find(".//msg[@level='FAIL']")
                    if msg is not None:
                        step['message'] = msg.text

                    test['steps'].append(step)

                self.results.append(test)

        except Exception as e:
            self.errors.append('Error parsing XML file: {}'.format(traceback.format_exc()))
            return

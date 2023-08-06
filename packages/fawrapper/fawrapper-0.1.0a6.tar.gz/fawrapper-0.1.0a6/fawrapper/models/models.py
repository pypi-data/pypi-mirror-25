#!/usr/bin/env python3
"""
Models of all resources on the api.
"""
from datetime import datetime
from fawrapper.models.base import ListResource, InstanceResource
from fawrapper.utils import format_time_to_iso, read_token, persist_token

class Change(InstanceResource):

    path = '/changes/'

    def _set_attributes(self, params):
        self.status = params.get('status')
        self.changed_by = params.get('changedBy')
        self.entity_class = params.get('entityClass')
        self.url = params.get('url')
        self.entity = params.get('entity')
        self.actions = params.get('actions')
        self.id = params.get('id')

    def pull_details(self):
        pass


class Changes(ListResource):
    """
    Class for changes instance resource on the api
    Gets changes after a token, which is saved to disk
    for use on the next request.
    Token will be saved to the users home directory.
    """
    instance = Change
    since_token = None

    def list(self, since_token=None):
        if not since_token:
            try:
                since_token = read_token()
            except FileNotFoundError:
                return list()
            finally:
                persist_token(self.get_current_token())
        self.since_token = since_token
        return super().list()


    def _get_all_pages(self, filters=None):
        page = self.requester.get(
            f'/changes/{self.since_token}/'
        )
        yield page['items']

    def get_current_token(self):
        return self.requester.get('/changes/token')['sinceToken']


class Task(InstanceResource):
    """
    Class for Task instance resource on the api
    glAccount mandatory name uuid markupType taxable
    markupValue customFields estDuration unitPrice unitCost
    description
    """
    path = '/task/'

    def _set_attributes(self, params):
        self.uuid = params.get('uuid')
        self.gl_account = params.get('glAccount')
        self.name = params.get('name')
        self.markup_type = params.get('markupType')
        self.taxable = params.get('taxable')
        self.markup_value = params.get('markupValue')
        self.custom_fields = params.get('customFields')
        self.est_duration = params.get('estDuration')
        self.unit_price = params.get('unitPrice')
        self.unit_cost = params.get('unitCost')
        self.description = params.get('description')


class Tasks(ListResource):
    instance = Task


class ItemInTask(InstanceResource):
    """Class for item in job object"""

    def _set_attributes(self, params):
        self.unit_cost = params.get('unitCost')
        self.unit_price = params.get('unitPrice')
        self.uuid = params.get('uuid')
        self.quantity = params.get('quantity')
        self.custom_fields = params.get('customFields')
        self._item = params.get('item')

    @property
    def item(self):
        item = Item(self.requester, **self._item)
        item.pull_details()
        return item


class TaskInJob(InstanceResource):
    """Class for task in job object"""

    def __init__(self, requester,  **params):
        self.job_uuid = params['job_uuid']
        self.path = f'/job/{self.job_uuid}/task/'
        super().__init__(requester, **params)

    def _set_attributes(self, params):
        self.attachments = params.get('attachments')
        self.done = params.get('done')
        self.unit_price = params.get('unitPrice')
        self.uuid = params.get('uuid')
        self.note = params.get('note')
        self.asset = params.get('asset')
        self.custom_fields = params.get('customFields')
        self.unit_cost = params.get('unitCost')
        self._task = params.get('task')
        self._items = params.get('items')

    @property
    def items(self):
        items_in_task_list = list()
        for item_dict in self._items:
            item_in_task = ItemInTask(self.requester, **item_dict)
            items_in_task_list.append(item_in_task)
        return items_in_task_list

    @property
    def task(self):
        task = Task(self.requester, **self._task)
        task.pull_details()
        return task


class Job(InstanceResource):
    """
    Class for Job instance resource on the api.

    Attributes from API:
    tasks description revenue signature jobId invoice jobLead
    scheduledOn labor pre_signature customer estDuration uuid
    createdOn crew state contact asset completedOn customFields
    location

    """
    path = '/job/'

    def _set_attributes(self, params):
        self.uuid = params.get('uuid')
        self.scheduled_on = params.get('scheduledOn')
        self.description = params.get('description')
        self.location = params.get('location')
        self.contact = params.get('contact')
        self.est_duration = params.get('estDuration')
        self.asset = params.get('asset')
        self.crew = params.get('crew')
        self.custom_fields = params.get('customFields')
        self.labor = params.get('labor')
        self.started_on = params.get('startedOn')
        self.revenue = params.get('revenue')
        self.signature = params.get('signature')
        self.job_id = params.get('jobId')
        self.invoice = params.get('invoice')
        self.pre_signature = params.get('pre_signature')
        self.customer = params.get('customer')
        self.created_on = params.get('createdOn')
        self.completed_on = params.get('completedOn')
        self._state = params.get('state')
        self._job_lead = params.get('jobLead')
        self._tasks = params.get('tasks')
        self._items_used = list()

    @property
    def items_used(self):
        for task in self.tasks:
            for item in task.items:
                self._items_used.append(item.item)
        return self._items_used

    @property
    def state(self):
        return self._state[0]

    @property
    def job_lead(self):
        if isinstance(self._job_lead, User):
            return self._job_lead
        else:
            user = User(self.requester, **self._job_lead)
            user.pull_details()
            self._job_lead = user
            return self._job_lead

    @job_lead.setter
    def job_lead(self, user):
        self._job_lead = user
        data = {"jobLead": {"uuid": user.uuid}}
        self.post(data)

    @property
    def tasks(self):
        tasks_list = list()
        for task_dict in self._tasks:
            task_dict.update({'job_uuid': self.uuid})
            task_instance = TaskInJob(self.requester, **task_dict)
            task_instance.pull_details()
            tasks_list.append(task_instance)
        return tasks_list


class Jobs(ListResource):
    """
    Class for Jobs list resource on the api
    """
    instance = Job
    valid_filters = ['start', 'end', 'sortedBy',
                     'location', 'jobLead', 'state']

    def list(self,filters=None):
        """
        Listing jobs will require a 'start' and 'end' value
        to be included in the filters.

        Query Parameters:
            start – starting date (required)
            end – end date (required)
            sortedBy – Available sorting criteria:
                scheduledOn, jobLead , location and state
            location – filtered by location
            jobLead – filtered by jobLead
            state – filtered by state

        """
        if not filters:
            return super().list()
        if 'pageSize' not in filters:
            filters['pageSize'] = 200
        filters = self._validate_filters(filters)
        return super().list(filters=filters)

    def _validate_filters(self, filters=None):
        filters = super()._validate_filters(filters)
        if 'start' not in filters:
            filters['start'] = format_time_to_iso(2000, 1, 1)
        if 'end' not in filters:
            end = datetime(2060, 1, 1)
            filters['end'] = format_time_to_iso(
                end.year, end.month, end.day, end.hour, end.minute)
        return filters


class User(InstanceResource):
    """
    Class for User instance resource
    """
    path = '/user/'

    def _set_attributes(self, params):
        self.uuid = params.get('uuid')
        self.email = params.get('email')
        self.password = params.get('password')
        self.first_name = params.get('firstName')
        self.last_name = params.get('lastName')
        self.phone_number = params.get('phone')
        self.locale = params.get('locale')
        self.timezone = params.get('timezone')
        self.platform = params.get('platform')
        self.role = params.get('role')
        self.archived = params.get('archived')
        self.custom_fields = params.get('customFields')
        self.address = params.get('address')


class Users(ListResource):
    """
    Class used for listing users from api
    """
    instance = User
    valid_filters = ['firstName']


class Item(InstanceResource):
    """
    Class for item instance resource
    """
    path = '/item/'
    valid_filters = [
        'sortedBy', 'name', 'partNumber', 'taxable', 'glAccount'
    ]

    def _set_attributes(self, params):
        self.uuid = params.get('uuid')
        self.name = params.get('name')
        self.part_number = params.get('partNumber')
        self.description = params.get('description')
        self.gl_account = params.get('glAccount')
        self.markup_type = params.get('markupType')
        self.markup_value = params.get('markupValue')
        self.taxable = params.get('taxable')
        self.track_on_van = params.get('trackOnVan')
        self.unit_cost = params.get('unitCost')
        self.unit_price = params.get('unitPrice')
        self.custom_fields = params.get('customFields')


class Items(ListResource):
    """
    Class used for listing item objects on api
    """
    instance = Item


class Customer(InstanceResource):
    path = '/customer/'
    valid_filters = ['sortedBy', 'firstName', 'lastName',
                      'email', 'phone', 'customer']


class Contact(InstanceResource):
    path = '/contact/'
    valid_filters = ['sortedBy', 'firstName', 'lastName',
                      'email', 'phone', 'customer']


class Location(InstanceResource):
    path = '/location/'
    valid_filters = ['sortedBy', 'name', 'streetName', 'locality',
                      'region', 'postcode', 'country', 'isBilling',
                      'type', 'customer']




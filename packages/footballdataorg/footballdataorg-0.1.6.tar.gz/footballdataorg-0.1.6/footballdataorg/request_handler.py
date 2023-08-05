"""
This module contains the RequestHandler which encapsulates the requests
to the football-data.org api.
"""
from footballdataorg.exceptions import APIErrorException, IncorrectParametersException, IncorrectFilterException
from footballdataorg.service import SERVICE_DEFINITION
import requests
import logging

class RequestHandler(object):
    """ The RequestHandler encapsulates the requests to the football-data.org api."""

    BASE_URL = SERVICE_DEFINITION['url']
    LIVE_URL = 'http://soccer-cli.appspot.com/'

    def __init__(self, headers):
        self.logger = logging.getLogger(__name__)
        self.headers = headers
        if headers:
            self.logger.info('Initializing Request Handler with the following headers:')
            for header in headers:
                self.logger.info(f'{header}: {headers[header]}')
        else:
            self.logger.info('Initializing Request Handler without headers')

    def get_json(self, main, main_id=None, sub=None, filters=None):
        return self._get(self._get_url(main, main_id=main_id, sub=sub, filters=filters)).json()

    def _get(self, url):
        """Handles api.football-data.org requests"""
        self.logger.info(f'Sending request: {RequestHandler.BASE_URL+url}')
        req = requests.get(RequestHandler.BASE_URL+url, headers=self.headers)
        self.logger.info(f'Request returned with status code {req.status_code}')

        if req.status_code == requests.codes.ok:
            return req

        if req.status_code == requests.codes.bad:
            raise APIErrorException('Invalid request. Check parameters.', req.status_code)

        if req.status_code == requests.codes.forbidden:
            raise APIErrorException('This resource is restricted', req.status_code)

        if req.status_code == requests.codes.not_found:
            raise APIErrorException('This resource does not exist. Check parameters', req.status_code)

        if req.status_code == requests.codes.too_many_requests:
            raise APIErrorException('You have exceeded your allowed requests per minute/day', req.status_code)

    def _get_url(self, main, main_id=None, sub=None, filters=None):
        self.logger.debug('Creating URL')
        self.logger.debug(f'Main Resource: {main}')
        self.logger.debug(f'Main ID: {main_id}')
        self.logger.debug(f'Subresource: {sub}')
        self.logger.debug(f'Filters: {filters}')

        url = ''
        if main in SERVICE_DEFINITION['resources']:
            resource = SERVICE_DEFINITION['resources'][main]
            url = url + '/' + main

            if main_id == None:
                if resource['standalone'] == False and filters is None:
                    raise IncorrectParametersException(f'Resource {main} can not be used without an id or filter', main, main_id, sub, filters)

                if sub is not None:
                    raise IncorrectParametersException(f'Sub resources can only be used if an ID is present', main, main_id, sub, filters)
                
                if filters is not None and 'filters' in resource:
                    url = self._add_filters(url, resource, filters)

            else:
                url = url + '/' + str(main_id)

                if sub is not None:
                    if sub in resource['subresources']:
                        subresource = resource['subresources'][sub]
                        url = url + '/' + sub
                        if filters is not None and 'filters' in subresource:
                            url = self._add_filters(url, subresource, filters)

                    else:
                        raise IncorrectParametersException(f'The subresource {sub} is not valid for resource {main}', main, main_id, sub, filters)
                else:
                    if filters is not None and 'filters' in resource:
                        url = self._add_filters(url, resource, filters, withId=True)
        else:
            raise IncorrectParametersException(f'Main resource {main} does not exist', main, main_id, sub, filters)

        self.logger.debug(f'Final URL: {RequestHandler.BASE_URL+url}')
        return url

    def _add_filters(self, url, resource, filters, withId=False):
        bFirstFilter = True
        if filters is not None:
            for filter in filters:
                if filter['name'] in resource['filters']:
                    if 'withId' in resource['filters'][filter['name']]:
                        if resource['filters'][filter['name']]['withId'] != withId:
                            raise IncorrectFilterException(f'Wrong use of filter {filter["name"]}. Please check if ID needs to be present.', resource['name'], filter['name'], filter['value'])

                    match = resource['filters'][filter['name']]['re'].match(filter['value'])
                    if match is None:
                        raise IncorrectFilterException(f'Incorrect value for filter {filter["name"]}', resource['name'], filter['name'], filter['value'])
                    else:
                        if bFirstFilter:
                            url = url + '?' + filter['name'] + "=" + filter['value']
                            bFirstFilter = False
                        else:
                            url = url + '&' + filter['name'] + "=" + filter['value']
                else:
                    raise IncorrectFilterException(f'Invalid filter {filter["name"]}', resource['name'], filter['name'], filter['value'])
        return url
import requests
import datetime


class Client:
    """Client for RSpace API v1.

    Most methods return a dictionary with fields described in the API documentation. The documentation can be found at
    https://community.researchspace.com/public/apiDocs (or your own instance's /public/apiDocs).

    For authentication, an API key must be provided. It can be found by logging in and navigating to 'My Profile' page.
    """
    class ConnectionError(Exception):
        pass

    class AuthenticationError(Exception):
        pass

    class NoSuchLinkRel(Exception):
        pass

    API_VERSION = 'v1'

    def __init__(self, rspace_url, api_key):
        """
        Initializes RSpace client.
        :param rspace_url: RSpace server URL (for example, https://community.researchspace.com)
        :param api_key: RSpace API key of a user can be found on 'My Profile' page
        """
        self.rspace_url = rspace_url
        self.api_key = api_key

    def _get_api_url(self):
        """
        Returns an API server URL.
        :return: string URL
        """
        return '%s/api/%s' % (self.rspace_url, Client.API_VERSION)

    def _get_headers(self, content_type='application/json'):
        return {
            'apiKey': self.api_key,
            'Accept': content_type
        }

    @staticmethod
    def _handle_response(response):
        # Check whether response includes UNAUTHORIZED response code
        if response.status_code == 401:
            raise Client.AuthenticationError(response.json()['message'])

        if str(response.status_code)[0] != '2':
            if 'application/json' in response.headers['Content-Type']:
                print(response.status_code, response.text)
                error = response.json()['message'] or next(iter(response.json()['errors'] or []), None)
            else:
                error = 'Error code: {}, error message: {}'.format(response.status_code, response.text)
            return ValueError(error)

        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def retrieve_api_results(self, url, params=None, content_type='application/json', request_type='GET'):
        """
        Makes the requested API call and returns either an exception or a parsed JSON response as a dictionary.
        Authentication header is automatically added. In most cases, a specialised method can be used instead.
        :param url: URL to retrieve
        :param request_type: 'GET', 'POST', 'PUT'
        :param params: arguments to be added to the API request
        :param content_type: content type
        :return: parsed JSON response as a dictionary
        """
        headers = self._get_headers(content_type)
        try:
            if request_type == 'GET':
                response = requests.get(url, params=params, headers=headers)
            elif request_type == 'PUT' or request_type == 'POST':
                response = requests.request(request_type, url, json=params, headers=headers)
            else:
                raise ValueError('Expected GET / PUT / POST request type, received {} instead' % request_type)

            return self._handle_response(response)
        except requests.exceptions.ConnectionError as e:
            raise Client.ConnectionError(e)

    @staticmethod
    def _get_links(response):
        """
        Finds links part of the response. Most responses contain links section with URLs that might be useful to query
        for further information.
        :param response: response from the API server
        :return: links section of the response
        """
        try:
            return response['_links']
        except KeyError:
            raise Client.NoSuchLinkRel('There are no links!')

    def get_link_contents(self, response, link_rel):
        """
        Finds a link with rel attribute equal to link_rel and retrieves its contents.
        :param response: response from the API server
        :param link_rel: rel attribute value to look for
        :return: parsed response from the found URL
        """
        return self.retrieve_api_results(self.get_link(response, link_rel))

    def get_link(self, response, link_rel):
        """
        Finds a link with rel attribute equal to link_rel.
        :param response: response from the API server.
        :param link_rel: rel attribute value to look for
        :return: string URL
        """
        for link in self._get_links(response):
            if link['rel'] == link_rel:
                return link['link']
        raise Client.NoSuchLinkRel('Requested link rel "%s", available rel(s): %s' %
                                   (link_rel, ', '.join([x['rel'] for x in self._get_links(response)])))

    def download_link_to_file(self, url, filename):
        """
        Downloads a file from the API server.
        :param url: URL of the file to be downloaded
        :param filename: file path to save the file to
        """
        headers = {
            'apiKey': self.api_key,
            'Accept': 'application/octet-stream'
        }
        with open(filename, 'wb') as fd:
            for chunk in requests.get(url, headers=headers).iter_content(chunk_size=128):
                fd.write(chunk)

    @staticmethod
    def link_exists(response, link_rel):
        """
        Checks whether there is a link with rel attribute equal to link_rel in the links section of the response.
        :param response: response from the API server
        :param link_rel: rel attribute value to look for
        :return: True, iff the link exists
        """
        return link_rel in [x['rel'] for x in Client._get_links(response)]

    # Documents methods
    def get_documents(self, query=None, order_by='lastModified desc', page_number=0, page_size=20):
        """
        The Documents endpoint returns a paginated list of summary information about Documents in the RSpace workspace.
        These can be individual documents or notebook entries. More information on
        https://community.researchspace.com/public/apiDocs (or your own instance's /public/apiDocs).
        :param (optional) query: Global search for a term, works identically to the simple "All' search in RSpace
        Workspace.
        :param order_by: Sort order for documents.
        :param page_number: For paginated results, this is the number of the page requested, 0 based.
        :param page_size: The maximum number of items to retrieve.
        :return: parsed response as a dictionary
        """
        params = {
            'orderBy': order_by,
            'pageSize': page_size,
            'pageNumber': page_number
        }
        if query is not None:
            params['query'] = query

        return self.retrieve_api_results(self._get_api_url() + '/documents', params)

    def get_documents_advanced_query(self, advanced_query, order_by='lastModified desc', page_number=0, page_size=20):
        """
        The Documents endpoint returns a paginated list of summary information about Documents in the RSpace workspace.
        These can be individual documents or notebook entries. More information on
        https://community.researchspace.com/public/apiDocs (or your own instance's /public/apiDocs).
        :param advanced_query: JSON representation of a search query. This can be built using AdvancedQueryBuilder.
        :param order_by: Sort order for documents.
        :param page_number: For paginated results, this is the number of the page requested, 0 based.
        :param page_size: The maximum number of items to retrieve.
        :return: parsed response as a dictionary
        """
        params = {
            'advancedQuery': advanced_query,
            'orderBy': order_by,
            'pageSize': page_size,
            'pageNumber': page_number
        }
        return self.retrieve_api_results(self._get_api_url() + '/documents', params)

    def get_document(self, doc_id):
        """
        Gets information about a document. More information on
        https://community.researchspace.com/public/apiDocs (or your own instance's /public/apiDocs).
        :param doc_id: numeric document ID (the same as Global ID, but just the numeric part)
        :return: a dictionary that includes: document metadata, field content, metadata about media items belonging to
        this document, links to download the content of media files
        """
        return self.retrieve_api_results(self._get_api_url() + '/documents/' + str(doc_id))

    def get_document_csv(self, doc_id):
        """
        Gets information about a document. More information on
        https://community.researchspace.com/public/apiDocs (or your own instance's /public/apiDocs).
        :param doc_id: numeric document ID (the same as Global ID, but just the numeric part)
        :return: CSV that includes: document metadata, field content, metadata about media items belonging to
        this document, links to download the content of media files
        """
        return self.retrieve_api_results(self._get_api_url() + '/documents/' + str(doc_id), content_type='text/csv')

    def create_document(self, name=None, tags=None, form_id=None, fields=None):
        """
        Creates a new document in user’s Api Inbox folder. More information on
        https://community.researchspace.com/public/apiDocs (or your own instance's /public/apiDocs).
        :param name: name of the document (can be omitted)
        :param tags: list of tags (['tag1', 'tag2']) or comma separated string of tags ('tag1,tag2')
        :param form_id: numeric form ID (the same as Global ID, but just the numeric part)
        :param fields: list of fields (dictionaries of (optionally) ids and contents). For example,
        [{'content': 'some example text'}] or [{'id': 123, 'content': 'some example text'}].
        :return:
        """
        data = {}

        if name is not None:
            data['name'] = name

        if tags is not None:
            if type(tags) == list:
                tags = ','.join(tags)
            data['tags'] = tags

        if form_id is not None:
            try:
                data['form'] = {"id": int(form_id)}
            except ValueError:
                raise ValueError('Excepted a numeric form ID, received {}'.format(form_id))

        if fields is not None and len(fields) > 0:
            data['fields'] = fields

        return self.retrieve_api_results(self._get_api_url() + '/documents', request_type='POST', params=data)

    def update_document(self, document_id, name=None, tags=None, form_id=None, fields=None):
        data = {}

        if name is not None:
            data['name'] = name

        if tags is not None:
            if type(tags) == list:
                tags = ','.join(tags)
            data['tags'] = tags

        if form_id is not None:
            try:
                data['form'] = {"id": int(form_id)}
            except ValueError:
                raise ValueError('Excepted a numeric form ID, received {}'.format(form_id))

        if fields is not None and len(fields) > 0:
            data['fields'] = fields

        return self.retrieve_api_results(self._get_api_url() + '/documents/' + str(int(document_id)),
                                         request_type='PUT', params=data)

    # File methods

    def get_files(self, page_number=0, page_size=20, order_by="lastModified desc", media_type="image"):
        """
        Lists media items - i.e. content shown in the Gallery in RSpace web application. Note that this does not include
        files linked from external file systems or 3rd party providers. More information on
        https://community.researchspace.com/public/apiDocs (or your own instance's /public/apiDocs).
        :param page_number: For paginated results, this is the number of the page requested, 0 based.
        :param page_size: The maximum number of items to retrieve.
        :param order_by: Sort order for documents.
        :param media_type: can be 'image', 'av' (audio or video), 'document' (any other file)
        :return: parsed response as a dictionary
        """
        params = {
            'pageNumber': page_number,
            'pageSize': page_size,
            'orderBy': order_by,
            'mediaType': media_type
        }
        return self.retrieve_api_results(self._get_api_url() + '/files', params)

    def get_file_info(self, file_id):
        """
        Gets metadata of a single file by its id. More information on
        https://community.researchspace.com/public/apiDocs (or your own instance's /public/apiDocs).
        :param file_id: numeric document ID (the same as Global ID, but just the numeric part)
        :return: parsed response as a dictionary
        """
        return self.retrieve_api_results(self._get_api_url() + '/files/' + str(file_id))

    def download_file(self, file_id, filename):
        """
        Downloads file contents. More information on
        https://community.researchspace.com/public/apiDocs (or your own instance's /public/apiDocs).
        :param file_id: numeric document ID (the same as Global ID, but just the numeric part)
        :param filename: file path to save the file to
        """
        return self.download_link_to_file(self._get_api_url() + '/files/' + str(file_id) + '/file', filename)

    def upload_file(self, file, folder_id=None, caption=None):
        data = {}

        if folder_id is not None:
            try:
                data['folderId'] = int(folder_id)
            except ValueError:
                raise ValueError('Excepted a numeric folder ID, received {}'.format(folder_id))

        if caption is not None:
            data['caption'] = caption

        response = requests.post(self._get_api_url() + '/files', files={"file": file}, data=data,
                                 headers=self._get_headers())
        return self._handle_response(response)

    # Activity methods
    def get_activity(self, page_number=0, page_size=100, order_by=None, date_from=None, date_to=None, actions=None,
                     domains=None, global_id=None, users=None):
        """
        Returns all activity for a particular document. More information on
        https://community.researchspace.com/public/apiDocs (or your own instance's /public/apiDocs).
        :param page_number: for paginated results, this is the number of the page requested, 0 based.
        :param page_size: the maximum number of items to retrieve.
        :param order_by: sort order for activities.
        :param date_from: yyyy-mm-dd string or datetime.date object. The earliest date to retrieve activity from.
        :param date_to: yyyy-mm-dd string or datetime.date object. The latest date to retrieve activity from.
        :param actions: a comma separated string or list of strings. Actions to restrict the query.
        :param domains: a comma separated string or list of strings. Domains to restrict the query.
        :param global_id: the global ID of a resource, e.g. SD12345
        :param users: a comma separated string or list of strings. Users to restrict the query.
        :return:
        """
        params = {
            'pageNumber': page_number,
            'pageSize': page_size
        }

        if order_by is not None:
            params['orderBy'] = order_by

        if date_from is not None:
            if type(date_from) == datetime.date:
                params['dateFrom'] = date_from.isoformat()
            elif type(date_from) == str:
                params['dateFrom'] = date_from
            else:
                raise TypeError('Unexpected date_from type {}'.format(str(type(date_from))))

        if date_to is not None:
            if type(date_to) == datetime.date:
                params['dateTo'] = date_to.isoformat()
            elif type(date_to) == str:
                params['dateTo'] = date_to
            else:
                raise TypeError('Unexpected date_from type {}'.format(str(type(date_to))))

        if actions is not None:
            if type(actions) == list:
                params['actions'] = ','.join(actions)
            elif type(actions) == str:
                params['actions'] = actions
            else:
                raise TypeError('Unexpected actions type {}'.format(str(type(actions))))

        if domains is not None:
            if type(domains) == list:
                params['domains'] = ','.join(domains)
            elif type(domains) == str:
                params['domains'] = domains
            else:
                raise TypeError('Unexpected domains type {}'.format(str(type(domains))))

        if global_id is not None:
            params['oid'] = str(global_id)

        if users is not None:
            if type(users) == list:
                params['users'] = ','.join(users)
            elif type(users) == str:
                params['users'] = users
            else:
                raise TypeError('Unexpected users type {}'.format(str(type(users))))

        return self.retrieve_api_results(self._get_api_url() + '/activity', params=params)


    # Miscellaneous methods
    def get_status(self):
        """
        Simple API call to check that API service is available. Throws an AuthenticationError if authentication fails.
        More information on https://community.researchspace.com/public/apiDocs (or your own instance's /public/apiDocs).
        :return: parsed response as a dictionary (most important field is 'message' which is supposed to be 'OK')
        """
        return self.retrieve_api_results(self._get_api_url() + '/status')

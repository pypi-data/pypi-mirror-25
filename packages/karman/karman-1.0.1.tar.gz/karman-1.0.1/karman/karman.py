import requests


class Karman:
    caching_enabled = False
    logging_enabled = False

    def __init__(self, base_url=None):
        self.base_url = base_url or 'http://localhost:8000/'

    def _log(self, log_message):
        if self.logging_enabled:
            print(log_message)

    def _request(self, method: str, user: str, functionality_group_id: str) -> dict:
        r = requests.get('{}api/v1/{}/{}/{}/'.format(
            self.base_url, method, user, functionality_group_id
        ))
        request_json = r.json()
        self._log(request_json)

        request_json['karman_elapsed_time'] = r.elapsed.total_seconds()
        return request_json

    def can_i_use(self, user: str, functionality_group_id: str) -> bool:
        response_json = self._request('caniuse', user, functionality_group_id)
        return response_json.get('enabled')

    def which(self, user: str, functionality_group_id: str, return_statistics=False):
        response_json = self._request('which', user, functionality_group_id)

        if return_statistics:
            return response_json.get('functionality'), response_json.get('karman_elapsed_time')
        return response_json.get('functionality')

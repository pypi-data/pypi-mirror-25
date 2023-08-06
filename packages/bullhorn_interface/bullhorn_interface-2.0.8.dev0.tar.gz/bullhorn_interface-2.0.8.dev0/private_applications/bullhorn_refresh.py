from bullhorn_interface.api import LiveInterface, StoredInterface, tokenbox
from mylittlehelpers import time_elapsed
import datetime
import moment
import time
import fire


def do_stuff(num_calls=100, version=0):
    start = time.time()
    independent = True if version == 0 else False
    for i in range(num_calls):
        if i == 0 and independent:
            print(version, i, time_elapsed(start),
                  interface.api_call(command="search", entity="Candidate", select_fields=["id", "firstName"],
                                     query=f"firstName:John-Paul AND lastName:Jorissen", independent=independent)['data'][0]["firstName"])
        else:
            print(version, i, time_elapsed(start),
                  interface.api_call(command="search", entity="Candidate", select_fields=["id", "firstName"],
                                     query=f"firstName:John-Paul AND lastName:Jorissen", independent=independent)['data'][0]["firstName"])


def do_stuff2(num_calls=100, version=0):
    start = time.time()
    for i in range(num_calls):
        if i == 0:
            interface.login()
            interface.get_api_token()
        print(version, i, time_elapsed(start),
              interface.api_call(command="search", entity="Candidate", select_fields=["id", "firstName"],
                                 query=f"firstName:John-Paul AND lastName:Jorissen")['data'][0])


def grabnpis_comment(num_calls=100, version=0):
    start = time.time()
    independent = False if version else True
    candidate_id = 425086
    comments = 'NEWWW comment.'
    body = {"comments": comments}
    for i in range(num_calls):
        response = interface.api_call(command="entity", entity="Candidate", entity_id=f'{candidate_id}',
                                      select_fields="id, firstName, comments", method="GET")["data"]["comments"]
        args = (version, i, time_elapsed(start), response)
        print(*args)
        response = interface.api_call(command="entity", entity="Candidate", entity_id=f'{candidate_id}', body=body,
                                      select_fields="id, firstName, comments", method="UPDATE")["data"]["comments"]
        args = (version, i, time_elapsed(start), response)
        print(*args)


if __name__ == '__main__':
  fire.Fire(update_comment)
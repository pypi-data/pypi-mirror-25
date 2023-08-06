import json

from eu.softfire.nfv.utils.ob_utils import OBClient

if __name__ == '__main__':
    ob_client = OBClient()

    for project in json.loads(ob_client.list_projects()):
        print(project.get('name'))
        client = OBClient(project_name=project.get('name'))
        vim_instances = client.list_vim_instances()
        for vim in vim_instances:
            print("\t - %s" % vim.get("name"))
        print("Total: %d" % len(vim_instances))
        print("")
        print("")

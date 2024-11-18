#!/usr/bin/env python3

import json
import os
import urllib3


GIT_API_URL = 'https://api.github.com'
TOKEN = 'ghp_Tok3nEx4mp1e'

REMOTE_REPO_NAME = 'origin'

REPOS_LIST = {
    ('/orgs/FirstOrg',  1, 'C:/projects/first',  False),
    ('/orgs/SecondOrg', 1, 'C:/projects/second', False),
}


def process_one_link(link, page, repo_root_dir, mirror):
    full_link = GIT_API_URL + link + '/repos?per_page=100&page=' + str(page)
    print('\n\nGet repos list: ' + full_link)
    try:
        http = urllib3.PoolManager()
        header = {"authorization": "Bearer %s" % TOKEN}
        response = http.request('GET', full_link, headers=header)
        response.close()
        data = response.data.decode('utf-8')
        repos = json.loads(data)
        repos_count = len(repos)
        print('Repos loaded: %d' % repos_count)
        i = 0
        for repo in repos:
            i += 1
            repo_url = repo['html_url']
            repo_name = repo['name']
            print('\n(%d из %d) Processing %s ...' % (i, repos_count, repo_url))
            project_path = repo_root_dir + '/' + repo_name
            if not os.path.exists(project_path):
                print(project_path + ' not exists -> Clone:')
                if mirror:
                    os.system('git clone --mirror --origin %s %s %s' % (REMOTE_REPO_NAME, repo_url, project_path))
                else:
                    os.system('git clone --origin %s %s %s' % (REMOTE_REPO_NAME, repo_url, project_path))
            else:
                if mirror:
                    print(project_path + ' already exists (mirror) -> Fetch:')
                else:
                    print(project_path + ' already exists -> Fetch:')
                os.system('git -C %s fetch --all --tags' % project_path)
    except Exception as e:
        print('API error: %s' % full_link)
        print(e)


if __name__ == '__main__':
    for (link, page, repo_root_dir, mirror) in REPOS_LIST:
        process_one_link(link, page, repo_root_dir, mirror)

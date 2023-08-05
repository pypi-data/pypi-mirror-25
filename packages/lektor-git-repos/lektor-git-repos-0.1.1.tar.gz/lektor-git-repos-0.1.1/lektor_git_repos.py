# -*- coding: utf-8 -*-
import os
import requests
from lektor.pluginsystem import Plugin

def errormsg(name, values, given):
    return 'get_github_repos: `{name}` not one of: {values}. Got: {given}'.format(
        name=name,
        values=', '.join(values),
        given=given
    )

class GithubReposPlugin(Plugin):
    name = u'GitHub Repos'
    description = u'Fetches your GitHub repos for display in Lektor templates'

    def on_process_template_context(self, context, **extra):
        context['get_github_repos'] = self.get_github_repos
        context['get_top_github_repos'] = self.get_top_github_repos

    def get_github_repos(self, visibility = 'all', sort = 'full_name', direction = None, **params):
        visibility_values = ['all', 'public', 'private']
        if visibility not in visibility_values:
            raise ValueError(errormsg('visibility', visibility_values, visibility))

        sort_values = ['full_name', 'created', 'updated', 'pushed']
        if sort not in sort_values:
            raise ValueError('sort', sort_values, sort)

        direction_values = ['all', 'public', 'private']
        if direction not in direction_values:
            raise ValueError(errormsg('direction', direction_values, direction))

        if direction is None:
            if sort == 'full_name':
                direction = 'asc'
            else:
                direction = 'desc'

        config = self.get_config()
        github_token = os.getenv('LEKTOR_GITHUB_TOKEN') or config.get('git-repos.github_token')

        params.setdefault('per_page', 100)
        params.setdefault('visibility', visibility)
        params.setdefault('sort', sort)
        params.setdefault('direction', direction)
        resp = requests.get(
            'https://api.github.com/user/repos',
            headers={'Authorization': 'token ' + github_token},
            params=params,
        )
        return resp.json()

    def get_top_github_repos(self, **params):
        count = params.pop('count', None)
        repos = self.get_github_repos(**params)
        return sorted(
            repos,
            key=lambda repo: repo['stargazers_count'],
            reverse=True,
        )[:count]


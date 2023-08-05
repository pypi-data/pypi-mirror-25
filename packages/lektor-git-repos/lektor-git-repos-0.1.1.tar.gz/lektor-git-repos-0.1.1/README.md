# lektor-github-pages

[![pipeline status](https://gitlab.com/Forkbombco/lektor-git-repos/badges/master/pipeline.svg)](https://gitlab.com/Forkbombco/lektor-git-repos/commits/master)

Fetches your GitHub repos for display in Lektor templates
Gitlab is planned soon

[Demo](https://forkbomb.co/projects/lektor-git-repos)

## Enabling the plugin

To enable the plugin add this to your project file:

```
[packages]
lektor-github-repos = 0.1.1
```

## Generate a personal access token

If you're only accessing public repos, the GitHub API allows you
to only make 60 unauthenticated requests per hour. But that goes up
to 5,000 requests per hour with authentication and it's not that hard to do:

Go to 

GitHub: https://github.com/settings/tokens/new 
GitLab: https://gitlab.com/profile/personal_access_tokens

and generate a token. You can untick all scopes to get public access.

## Create the config file

Create `configs/github-repos.ini` with the following content:

```
[git-repos]
github_token = <your personal access token>
gitlab_token = <your personal access token>
```

But those are not secure. You dont want to give out your personal access tokens.
You can also (preferred) add an OS environment variable with the following code:

```bash
LEKTOR_GITHUB_TOKEN="githubtoken"
LEKTOR_GITLAB_TOKEN="gitlabtoken"
```

And the plugin will use those over the config file values.

## Use in your templates

The plugin adds `get_git_repos()` and `get_top_githrepos()` (stars) to the template
context. Both accept the same parameters as with the user repos API call
(https://developer.github.com/v3/repos/#list-your-repositories).
`get_top_git_repos` also sorts repos by stargazers and accepts an additional
param `count`.

### Get latest pushed repositories

```
<ul>
{% for repo in get_github_repos(sort="pushed") %}
  <li>
    <strong>{{ repo.name }}</strong>
    {{ repo.description }}
  </li>
{% endfor %}
</ul>
```

### Get 10 latest updated repositories sorted by stargazers

```
<ul>
{% for repo in get_top_github_repos(type="owner", sort="updated", count=10) %}
  <li>
    [{{ repo.stargazers_count }} stars]
    <strong>{{ repo.name }}</strong>
    {{ repo.description }}
  </li>
{% endfor %}
</ul>
```

## In action

* [My homepage](https://forkbomb.co/projects)

## Forked
Originally forked from https://marksteve.com/lektor-github-repos

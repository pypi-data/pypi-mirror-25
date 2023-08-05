# HUD.ai Python Client

[![Build Status][ci-badge]][ci-url]
[![PyPI][pypi-badge]][pypi-url]
[![PyPI][python-versions-badge]][pypi-url]
[![License][license-badge]]()

The HUD.ai Python Client provides an easy to use wrapper to interact with the
HUD.ai API in python applications.

You must first acquire a HUD.ai secret key before you can use this module.

## Installation

`pip install hudai`

## Usage

```python
from hudai import Client as HudAiClient

hud_ai = HudAiClient(
    client_id='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    client_secret='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
)

hud_ai.companies.list()

hud_ai.articles.fetch('17787d76-4198-4775-a49a-b3581c37a482')
```

### Parameters

| Parameter | Usage | Example |
|-----------|-------|---------|
| `client_id`*    | Registered Client ID | `'46ef9d9b-89a9-4fd2-84cf-af6de31f2618'` |
| `client_secret` | Registered Client Secret | `'59170c3e-e2c9-4244-92d8-c3595d4af325'` |
| `base_url`      | Specify an alternate server to request resources from | `'https://stage.api.hud.ai/v1'` |
| `auth_url`      | Specify an alternate server to request auth tokens from | `'https://stage.accounts.hud.ai'` |
| `redirect_uri`  | Path to redirect auth requests to (required for `#get_authorize_uri`) | `'https://app.example.com/oauth/callbacks/hud-ai'` |

### Client Auth Flow

In order to access HUD.ai data on a user's behalf, they must authorize you to do
so. This requires 3 steps.

First, send them to the authorization URL

```python
from flask import Flask, redirect, url_for
from hudai import Client as HudAiClient

app = Flask(__name__)

hud_ai = HudAiClient(
    client_id='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    client_secret='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    redirect_uri='https://app.example.com/oauth/callbacks/hud-ai'
)

@app.route('/oauth/authorize/hud-ai')
def hud_ai_authorization():
    return redirect(hud_ai.get_authorize_uri(), code=302)
```

Now the user will be presented with a dialog screen where they can accept or
deny your request. The auth server will redirect back to your app in either
case.

Finally, parse the response and get the code and attach it to the client. The
code will be exchanged before the next request is made.

```python
@app.route('/oauth/callbacks/hud-ai')
def hud_ai_callback():
    code = request.args.get('code')
    hud_ai.set_auth_code(code)
```

### `client.get_authorize_uri()`

**NOTE:** This method requires `redirect_uri`

Returns a URL to direct users to to authorize your application to act on their
behalf. You will need to handle the redirect that includes the `code`

### `client.set_auth_code(code)`

Store the code for future exchange for an auth token

### `client.refresh_tokens()`

Attempts to ensure that the client has valid auth tokens.

* Refreshes known expired tokens
* Exchanges auth `code`s for access tokens
* Exchanges client ID/secret for app access tokens

## Resources

> **DOCUMENTATION NOTES**
>
> - `*` and bolded `Type` indicates required param
> - Params indicated with `?` are optional keyword params
> - `Date` types are automatically converted to/from standard `DateTime` objects
> - All `list` resources are paginated to 50/request, with `page` being 0-indexed (e.g. `page=3` will get you the fourth page)

### Article

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`               | String         | Resource ID **Cannot be edited** |
| `authors`          | list\<String\> | List of author names |
| `image_url`        | String         | Image published in the article's metadata |
| `importance_score` | Number         | `hudai-importance-scorer` output |
| `link_hash`        | String         | MD5 hash of the `link_url` **Cannot be edited** |
| `link_url`*        | **String**     | Where the article was originally published (e.g. `https://www.nytimes.com/2017/08/01/world/middleeast/mosul-isis-survivors-rights.html`) |
| `published_at`     | Date           | Original publishing date |
| `raw_data_url`*    | **String**     | Location of raw feed content (e.g. JSON/HTML), this is typically an S3 location (e.g. `s3://raw-storage/2017/08/01/raw-article.json`) |
| `source_url`*      | **String**     | URL of the publication source (e.g. `https://newsapi.org/v1/articles?source=the-wall-street-journal`) |
| `text`             | String         | Plaintext format of the article body |
| `title`*           | **String**     | Title article was published as |
| `article_type`*    | **String**     | `rss` \| `newsApi` \| `facebook` \| `twitter` |

#### `client.articles.list(article_type?, importance_score_min?, key_term?, link_hash?, page?, published_after?, published_before?)`

Example:

```python
last_week = datetime.datetime.now() - datetime.timedelta(days=7)

client.articles.list(article_type='rss', published_after=last_week)
```

#### `client.articles.create(**params)`

Takes all of the model attributes as keyword params (except `link_hash`)

#### `client.articles.fetch(id)`

#### `client.articles.update(id, **params)`

Takes all of the model attributes as keyword params (except `link_hash`)

#### `client.articles.delete(id)`

#### `client.articles.key_terms(id)`

Returns a list of key terms (`String`) associated with the article

### ArticleHighlights

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`          | String     | Resource ID **Cannot be edited** |
| `article_id`* | **String** | Article being highlighted |
| `body`*       | **String** | Phrases that should be highlighted |
| `user_id`*    | **String** | User the highlights apply to |

#### `client.article_highlights.list(article_id?, link_hash?, user_id?, page?)`

**NOTE:** `link_hash` is MD5 hash of the article URL

#### `client.article_highlights.create(**params)`

Takes all of the model attributes as keyword params

#### `client.article_highlights.fetch(id)`

#### `client.article_highlights.update(id, **params)`

Takes all of the model attributes as keyword params

#### `client.article_highlights.delete(id)`

### ArticleKeyTerm

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`          | String     | Resource ID **Cannot be edited** |
| `article_id`* | **String** | Article identifier |
| `term`*       | **String** | Key term in article |

#### `client.article_key_terms.list(article_id, page?)`

#### `client.article_key_terms.create(article_id, term)`

#### `client.article_key_terms.fetch(article_id, term)`

#### `client.article_key_terms.delete(article_id, term)`

### ArticleTag

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`          | String     | Resource ID **Cannot be edited** |
| `article_id`* | **String** | Article identifier |
| `tag`*        | **String** | Category that the article falls into |

#### `client.article_tags.list(article_id, page?)`

#### `client.article_tags.create(article_id, tag)`

#### `client.article_tags.fetch(article_id, tag)`

#### `client.article_tags.delete(article_id, tag)`

### Company

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`     | String     | Resource ID **Cannot be edited** |
| `name`*  | **String** | Primary company name (others can be associated as key terms) |
| `ticker` | String     | Stock ticker (e.g. `"NASDAQ:TWTR"`) |

#### `client.companies.list(name?, ticker?, key_term?, page?)`

#### `client.companies.create(**params)`

Takes all of the model attributes as keyword params

#### `client.companies.fetch(id)`

#### `client.companies.update(id, **params)`

Takes all of the model attributes as keyword params

#### `client.companies.delete(id)`

#### `client.companies.domains(id)`

Lists all `Domain`s (hostnames) associated with the company

#### `client.companies.key_terms(id)`

Lists all `KeyTerm`s associated with the company

### CompanyKeyTerm

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`          | String     | Resource ID **Cannot be edited** |
| `company_id`* | **String** | Associated company |
| `term`*       | **String** | Term (can be word or phrase) to find in articles |

#### `client.company_key_terms.list(company_id?, page?)`

#### `client.company_key_terms.create(**params)`

Takes all of the model attributes as keyword params

#### `client.company_key_terms.fetch(id)`

#### `client.company_key_terms.delete(id)`

### Domain

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`          | String     | Resource ID **Cannot be edited** |
| `company_id`* | **String** | Associated company |
| `hostname`*   | **String** | FQDN e.g. `api.hud.ai` |

#### `client.domains.list(company_id?, hostname?, page?)`

#### `client.domains.create(**params)`

Takes all of the model attributes as keyword params

#### `client.domains.fetch(id)`

#### `client.domains.update(id, **params)`

Takes all of the model attributes as keyword params

#### `client.domains.delete(id)`

### KeyTerm

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `term`* | **String** | Term (can be word or phrase) to find in articles |

#### `client.key_terms.list(page?)`

#### `client.key_terms.create(**params)`

Takes all of the model attributes as keyword params

#### `client.key_terms.fetch(term)`

#### `client.key_terms.delete(term)`

### Person

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`        | String     | Resource ID **Cannot be edited** |
| `name`*     | **String** | Full name |
| `title`*    | **String** | Professional title (e.g. `'Partner, Foundry.ai'`) |
| `image_url` | String     | URL for a picture of the person |

#### `client.people.list(name?, title?, term?, page?)`

#### `client.people.create(**params)`

Takes all of the model attributes as keyword params

#### `client.people.fetch(person_id)`

#### `client.people.update(person_id, **params)`

Takes all of the model attributes as keyword params

#### `client.people.delete(person_id)`

#### `client.people.quotes(pseron_id, page?)`

Convenience method

### PersonKeyTerm

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`         | String     | Resource ID **Cannot be edited** |
| `person_id`* | **String** | Related entity ID |
| `term`*      | **String** | Term (can be word or phrase) to find in articles |

#### `client.person_key_terms.list(person_id, page?)`

#### `client.person_key_terms.create(**params)`

Takes all of the model attributes as keyword params

#### `client.person_key_terms.fetch(person_id, term)`

#### `client.person_key_terms.delete(person_id, term)`

### PersonQuote

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`          | String     | Resource ID **Cannot be edited** |
| `article_id`* | **String** | Related entity ID |
| `term`*       | **String** | Term (can be word or phrase) to find in articles |
| `text`*       | **String** | Section of the article containing the quote (e.g. surrounding paragraph) |

#### `client.person_quotes.list(person_id, article_id?, term?, page?)`

#### `client.person_quotes.create(**params)`

Takes all of the model attributes as keyword params

#### `client.person_quotes.fetch(person_id, quote_id)`

#### `client.person_quotes.update(person_id, quote_id)`

Takes all of the model attributes as keyword params

#### `client.person_quotes.delete(person_id, quote_id)`

### RelevantArticle

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`                   | String     | Resource ID **Cannot be edited** |
| `article_id`*          | **String** | Scored article |
| `user_id`*             | **String** | User the score applies to |
| `score`*               | **Float**  | Score between 0 and 1 |
| `scored_at`*           | **Date**   | When the scoring was performed |
| `article_published_at` | Date       | When scored article was published |

#### `client.relevant_articles.list(article_id?, user_id?, scored_above?, scored_below?, scored_before?, scored_after?, published_before?, published_after?, page?)`

#### `client.relevant_articles.create(**params)`

Takes all of the model attributes as keyword params.

**NOTE:** Multiple RelevantArticles *cannot* be created with the same `user_id`
and `article_id`

#### `client.relevant_articles.fetch(id)`

#### `client.relevant_articles.update(id, **params)`

Only the `score` and `scored_at` and `article_published_at` can be updated.

#### `client.relevant_articles.delete(id)`

### SystemEvent

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`       | String         | Resource ID **Cannot be edited** |
| `name`*    | **String**     | Event identifier e.g. `article.processed` |
| `payload`* | **Dictionary** | Event payload e.g. `{'location': 's3://my-bucket/file-path', type:'rss'}` |

#### `client.system_events.list(page?)`

#### `client.system_events.create(**params)`

Takes all of the model attributes as keyword params

#### `client.system_events.fetch(id)`

### SystemTask

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`           | String     | Resource ID **Cannot be edited** |
| `task_id`*     | **String** | Task identifier (typically from `celery`) |
| `attempts`     | Number     | How many times has this job been started |
| `completed_at` | Date       | When the job finished (irregardless of success) |
| `started_at`   | Date       | Last time that the job was attempted |

#### `client.system_tasks.list(completed?, started_after?, started_before?, task_id?, page?)`

#### `client.system_tasks.create(**params)`

Takes all of the model attributes as keyword params

#### `client.system_tasks.fetch(id)`

#### `client.system_tasks.fetch_by_task_id(task_id)`

#### `client.system_tasks.update(id, **params)`

Takes all of the model attributes as keyword params

#### `client.system_tasks.mark_complete(id, completed_at?)`

When `completed_at` is omitted, it will default to now.

#### `client.system_tasks.delete(id)`

### TextCorpus

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`        | String     | Resource ID **Cannot be edited** |
| `body`*     | **String** | Text blob to use for relevance matching |
| `type`*     | **String** | Text origin e.g. `email` or `email` |
| `user_id`*  | **String** | User the corpus is used to identify articles for |

#### `client.text_corpora.list(corpus_type?, user_id?, page?)`

#### `client.text_corpora.create(user_id?, corpus_type?, body?)`

#### `client.text_corpora.fetch(id)`

#### `client.text_corpora.update(id, user_id?, corpus_type?, body?)`

#### `client.text_corpora.delete(id)`

### User

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`        | String     | Resource ID **Cannot be edited** |
| `email`*    | **String** | Primary email address for updates/notifications |
| `name`*     | **String** | User's full name (used in emails and other communications) |
| `time_zone` | String     | [tz database][tz-database-link] time zone used to determine when to send notifications (defaults to `America/New_York`) |

#### `client.users.list(email?, digest_subscription_day?, digest_subscription_hour?, name?, key_term?, company_id?, page?)`

#### `client.users.create(**params)`

Takes all of the model attributes as keyword params

#### `client.users.fetch(id)`

#### `client.users.update(id, **params)`

Takes all of the model attributes as keyword params

#### `client.users.delete(id)`

### UserCompany

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`          | String     | Resource ID **Cannot be edited** |
| `company_id`* | **String** | Associated company |
| `user_id`*    | **String** | Associated user |

#### `client.user_companies.list(user_id, page?)`

#### `client.user_companies.create(user_id, company_id)`

#### `client.user_companies.fetch(user_id, company_id)`

#### `client.user_companies.delete(user_id, company_id)`

### UserDigestSubscription

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`           | String     | Resource ID **Cannot be edited** |
| `day_of_week`* | **String** | `sunday` \| `monday` \| `tuesday` \| `wednesday` \| `thursday` \| `friday` \| `saturday` |
| `iso_hour`*    | **String** | 24-hour hour e.g. `08` = 8am, `17` = 5pm |
| `user_id`*     | **String** | Associated user |

#### `client.user_digest_subscriptions.list(user_id, day_of_week?, iso_hour?, page?)`

#### `client.user_digest_subscriptions.create(user_id, **params)`

Takes all of the model attributes as keyword params

#### `client.user_digest_subscriptions.fetch(user_id, digest_id)`

#### `client.user_digest_subscriptions.delete(user_id, digest_id)`

### UserKeyTerm

| Attribute | Type | Description |
| --------- | ---- | ----------- |
| `id`       | String     | Resource ID **Cannot be edited** |
| `term`*    | **String** | Term (can be word or phrase) to find in articles |
| `user_id`* | **String** | Associated user |

#### `client.user_key_terms.list(user_id, page?)`

#### `client.user_key_terms.create(user_id, term)`

#### `client.user_key_terms.fetch(user_id, term)`

#### `client.user_key_terms.delete(user_id, term)`

## Deployment

Deploys occur automatically via Travis-CI on tagged commits that build
successfully. Should you need to manually build the project, follow these steps:

```bash
# Install twine to prevent your password from being set in plaintext
pip install twine
# Build the package
python setup.py sdist
# Upload via twine
twine upload dist/hudai-NEW_VERSION_HERE.tar.gz
```

[ci-badge]: https://travis-ci.org/FoundryAI/hud-ai-python.svg?branch=master
[ci-url]: https://travis-ci.org/FoundryAI/hud-ai-python
[pypi-badge]: https://img.shields.io/pypi/v/hudai.svg
[pypi-url]: https://pypi.python.org/pypi/hudai
[python-versions-badge]: https://img.shields.io/pypi/pyversions/hudai.svg
[license-badge]: https://img.shields.io/pypi/l/hudai.svg
[tz-database-link]: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

# Omni SDK 

**Unofficial  SDK for [Omni Analytics](https://omni.co/)**

## Getting Started

### Install

#### pip

`pip install git+https://github.com/tillable/omni-sdk.git`

#### poetry

`poetry add git+https://github.com/tillable/omni-sdk.git`

## Configuration

The following environment variables can be set to automatically configure classes so that kwargs do not need to be pass on creation.

| Env Var                | Description                                                                                 | Example                                                           |
|------------------------|---------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| OMNI_ORGANIZATION_NAME | Name of your Omni organization. Can be found in Admin -> Settings -> General in the Omni UI | acme                                                              |
| OMNI_EMBED_SECRET      | Secret key for created dashboard embed urls. Can be found in Admin -> Embed -> Admin.       | vglUd1WblfyBSdBSMPj0KrxZcNUEZ1CC                                  |
| OMNI_API_KEY           | API key for authenticating requests to the REST API. Can be generated in Admin -> API Keys. | omni_osk_r0dvvwTfLkOC1QP6eomT65yOIWtjfDsU5gZpvKNdKWxHSrDJPT1RAUyV |


## Usage

### Create a dashboard embed URL
The SDK provides a convenience class for generating the url to embed dashboards in external pages and signing it.
For more information on the options see the [Omni Docs](https://docs.omni.co/docs/embed/private-embedding#embed-url-customization-options).

```python
from omni import OmniDashboardEmbedder

# kwargs are not required if environment variables have been configured.
embedder = OmniDashboardEmbedder(organization_name="acme", embed_secret="vglUd1WblfyBSdBSMPj0KrxZcNUEZ1CC")

url = embedder.build_url(
    content_path="/dashboards/da24491e",
    external_id="1",
    name="Somebody",
    custom_theme={
        "dashboard-background": "#00FF00",
        "dashboard-tile-background": "#00FF00",
    },
    entity="Acme",
    filter_search_params={"state": "GA"},
    link_access=True,
    prefers_dark=OmniDashboardEmbedder.PrefersDark.yes,
    theme=OmniDashboardEmbedder.Theme.dawn,
    user_attributes={"country": "USA"},
)
```

### Refresh a model
Refreshes a model to reflect the latest structures (schemas, views, fields) from the data source. This will remove any 
structures that are no longer present in the source, but will not remove anything created by users.

```python
from omni import OmniApiClient

# kwargs are not required if environment variables have been configured.
client = OmniApiClient(organization_name="acme", api_token="omni_osk_r0dvvwTfLkOC1QP6eomT65yOIWtjfDsU5gZpvKNdKWxHSrDJPT1RAUyV")

client.refresh_model("f0970eb8-785a-460b-9ced-cf603e160558")
```



 

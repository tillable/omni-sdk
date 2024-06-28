from urllib.parse import urlparse, parse_qs, urlencode, quote

import pytest
import requests

from omni import OmniDashboardEmbedder


@pytest.fixture
def embedder():
    return OmniDashboardEmbedder(
        organization_name="acme", embed_secret="17cb84c1ed4f4a94b091d7f752278344"
    )


@pytest.fixture(autouse=True)
def patch_uuid(monkeypatch):
    monkeypatch.setattr("uuid.UUID.hex", "365f7003aa5b4f3586d9b81b4a5d9f69")


class TestUnit:
    def test_basic_url(self, embedder):
        url = embedder.build_url(
            content_path="/dashboards/da24491e",
            external_id="1",
            name="Somebody",
        )
        assert (
            url == "https://acme.embed-omniapp.co/embed/login?"
            "contentPath=%2Fdashboards%2Fda24491e"
            "&externalId=1"
            "&name=Somebody"
            "&nonce=365f7003aa5b4f3586d9b81b4a5d9f69"
            "&signature=TjqD3emJJshOglYXfV5z-W9SV1nB0pW82zTl6ki4zrg%3D"
        )

    def test_kitchen_sink(self, embedder):
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
        assert url == (
            "https://acme.embed-omniapp.co/embed/login?"
            "contentPath=%2Fdashboards%2Fda24491e"
            "&externalId=1"
            "&name=Somebody"
            "&nonce=365f7003aa5b4f3586d9b81b4a5d9f69"
            "&customTheme=%7B%22dashboard-background%22%3A%22%2300FF00%22%2C%22dashboard-tile-background%22%3A%22%2300FF00%22%7D"
            "&entity=Acme"
            "&filterSearchParam=state%3DGA"
            "&linkAccess=__omni_link_access_open"
            "&prefersDark=true"
            "&theme=dawn"
            "&userAttributes=%7B%22country%22%3A%22USA%22%7D"
            "&signature=Pig9HZhUBuwIeTDZuV0_8cUsmrbJl8oPjB3eOji4XLw%3D"
        )

    def test_link_access(self, embedder):
        url = embedder.build_url(
            content_path="/dashboards/da24491e",
            external_id="1",
            name="Somebody",
            link_access=True,
        )
        assert (
            url == "https://acme.embed-omniapp.co/embed/login?"
            "contentPath=%2Fdashboards%2Fda24491e"
            "&externalId=1"
            "&name=Somebody"
            "&nonce=365f7003aa5b4f3586d9b81b4a5d9f69"
            "&linkAccess=__omni_link_access_open"
            "&signature=x58o-XDqvwuIxWFlsc8GtYN8ZU9oIKVUpV28l8jDdKw%3D"
        )
        url = embedder.build_url(
            content_path="/dashboards/da24491e",
            external_id="1",
            name="Somebody",
            link_access=["abcd1234", "efgh5678"],
        )
        assert (
            url == "https://acme.embed-omniapp.co/embed/login?"
            "contentPath=%2Fdashboards%2Fda24491e"
            "&externalId=1"
            "&name=Somebody"
            "&nonce=365f7003aa5b4f3586d9b81b4a5d9f69"
            "&linkAccess=abcd1234%2Cefgh5678"
            "&signature=c__6ZtGxus4P13Ax1csUDOr0Pglkve2EQItkfJQkfls%3D"
        )

    def test_filter_search_params(self, embedder):
        str_url = embedder.build_url(
            content_path="/dashboards/da24491e",
            external_id="1",
            name="Somebody",
            filter_search_params="state=GA&county=Fulton",
        )
        dict_url = embedder.build_url(
            content_path="/dashboards/da24491e",
            external_id="1",
            name="Somebody",
            filter_search_params={"state": "GA", "county": "Fulton"},
        )
        assert (
            str_url == dict_url == "https://acme.embed-omniapp.co/embed/login?"
            "contentPath=%2Fdashboards%2Fda24491e"
            "&externalId=1"
            "&name=Somebody"
            "&nonce=365f7003aa5b4f3586d9b81b4a5d9f69"
            "&filterSearchParam=state%3DGA%26county%3DFulton"
            "&signature=WsZAvf0R5rhC5-Np6hR2Rkmb0XrMntHt0qESmwrZR2o%3D"
        )

        empty_dict_url = embedder.build_url(
            content_path="/dashboards/da24491e",
            external_id="1",
            name="Somebody",
            filter_search_params={},
        )
        assert (
            empty_dict_url == "https://acme.embed-omniapp.co/embed/login?"
            "contentPath=%2Fdashboards%2Fda24491e"
            "&externalId=1"
            "&name=Somebody"
            "&nonce=365f7003aa5b4f3586d9b81b4a5d9f69"
            "&signature=TjqD3emJJshOglYXfV5z-W9SV1nB0pW82zTl6ki4zrg%3D"
        )

    def test_missing_organization_name(self):
        with pytest.raises(ValueError):
            OmniDashboardEmbedder(embed_secret="super_secret")

    def test_missing_embed_secret(self):
        with pytest.raises(ValueError):
            OmniDashboardEmbedder(organization_name="acme")

    def test_env_configuration(self, monkeypatch):
        monkeypatch.setenv("OMNI_ORGANIZATION_NAME", "acme")
        monkeypatch.setenv("OMNI_EMBED_SECRET", "super_secret")
        OmniDashboardEmbedder()


class TestIntegration:
    @staticmethod
    def get_url_params(url: str) -> dict:
        parsed_url = urlparse(url)
        return {
            param: quote(values_list[0])
            for param, values_list in parse_qs(parsed_url.query).items()
        }

    @pytest.mark.skip(
        "Currently working with Omni to understand why this test is not passing."
    )
    def test_kitchen_sink(self, embedder):
        generated_url = embedder.build_url(
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

        params = self.get_url_params(generated_url)
        generated_signature = params.pop("signature")
        params["secret"] = embedder.embed_secret

        # Do some string manipulation to create url for Omni signature verification endpoint.
        expected_url = requests.post(
            "https://acme.embed-omniapp.co/embed/sso/generate-url", json=params
        ).json()["url"]
        assert generated_signature == self.get_url_params(expected_url)["signature"]

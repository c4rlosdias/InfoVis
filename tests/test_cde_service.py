import importlib.util
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).parents[1] / "modules" / "cde" / "service.py"
SPEC = importlib.util.spec_from_file_location("infovis_cde_service", MODULE_PATH)
cde = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cde)


class Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def response(data):
    return Response(json.dumps(data).encode("utf-8"))


class TestCDEClient(unittest.TestCase):
    def test_authentication_uses_published_contract(self):
        captured = {}

        def fake_urlopen(request, timeout):
            captured["url"] = request.full_url
            captured["body"] = json.loads(request.data)
            return response({
                "status": "success",
                "data": {"access": "jwt", "refresh": "refresh"},
            })

        with patch.object(cde, "urlopen", fake_urlopen):
            client = cde.CDEClient("http://example.test:8080")
            client.authenticate("client", "secret")
        self.assertEqual(captured, {
            "url": "http://example.test:8080/auth/token",
            "body": {"client_id": "client", "client_secret": "secret"},
        })
        self.assertTrue(client.authenticated)

    def test_unwrapped_response_is_still_supported(self):
        with patch.object(cde, "urlopen", lambda request, timeout: response({"access": "jwt"})):
            client = cde.CDEClient("http://example.test")
            client.authenticate("client", "secret")
        self.assertEqual(client.access_token, "jwt")

    def test_pagination_follows_same_host(self):
        pages = iter([
            {"results": [{"name": "A"}], "next": "http://example.test/api/v1/projects?offset=1"},
            {"results": [{"name": "B"}], "next": None},
        ])
        with patch.object(cde, "urlopen", lambda request, timeout: response(next(pages))):
            client = cde.CDEClient("http://example.test")
            names = [item["name"] for item in client.list_projects()]
        self.assertEqual(names, ["A", "B"])

    def test_list_projects_accepts_wrapped_direct_list(self):
        payload = {"status": "success", "data": [{"name": "Project A"}]}
        with patch.object(cde, "urlopen", lambda request, timeout: response(payload)):
            client = cde.CDEClient("http://example.test")
            projects = client.list_projects()
        self.assertEqual(projects, [{"name": "Project A"}])

    def test_ifc_submissions_and_exports_use_distinct_endpoints(self):
        client = cde.CDEClient("http://example.test")
        with patch.object(client, "_all_pages", return_value=[]) as all_pages:
            client.list_ifc_files("asset-1")
            client.list_exports("asset-1")
        self.assertEqual(all_pages.call_args_list[0].args[0], "/api/v1/assets/asset-1/ifc-files")
        self.assertEqual(all_pages.call_args_list[1].args[0], "/api/v1/assets/asset-1/exports")

    def test_get_export_uses_specific_export_endpoint(self):
        client = cde.CDEClient("http://example.test")
        with patch.object(client, "_request_json", return_value={"id": "run-1"}) as request_json:
            client.get_export("asset-1", "run-1")
        request_json.assert_called_once_with(
            "GET", "/api/v1/assets/asset-1/exports/run-1"
        )

    def test_download_accepts_server_selected_binary_media_type(self):
        import tempfile
        client = cde.CDEClient("http://example.test")
        captured = {}

        def fake_request(method, path, **kwargs):
            captured.update(method=method, path=path, accept=kwargs.get("accept"))
            return Response(b"ISO-10303-21;")

        with tempfile.TemporaryDirectory() as directory, patch.object(client, "_request", fake_request):
            client.download_export("asset-1", "run-1", directory, "modelo.ifc")
        self.assertEqual(captured, {
            "method": "GET",
            "path": "/api/v1/assets/asset-1/exports/run-1/download",
            "accept": "*/*",
        })

    def test_create_export_uses_asset_export_endpoint(self):
        client = cde.CDEClient("http://example.test")
        with patch.object(
            client, "_request_json", return_value={"id": "run-1", "status": "queued"}
        ) as request_json:
            client.create_export("asset-1")
        request_json.assert_called_once_with(
            "POST",
            "/api/v1/assets/asset-1/exports",
            payload={"force": False},
        )

    def test_get_ifc_file_uses_selected_ifc_global_id(self):
        client = cde.CDEClient("http://example.test")
        with patch.object(client, "_request_json", return_value={"id": "ifc-global-1"}) as request_json:
            client.get_ifc_file("asset-1", "ifc-global-1")
        request_json.assert_called_once_with(
            "GET", "/api/v1/assets/asset-1/ifc-files/ifc-global-1"
        )

    def test_generate_export_polls_the_created_export(self):
        client = cde.CDEClient("http://example.test")
        progress = []
        callback = progress.append
        with patch.object(client, "get_ifc_file", return_value={"id": "ifc-global-1"}) as get_ifc_file, patch.object(
            client, "create_export", return_value={"id": "run-1", "status": "queued"}
        ) as create_export, patch.object(
            client,
            "wait_for_export",
            return_value={"id": "run-1", "status": "succeeded"},
        ) as wait_for_export:
            result = client.generate_export_and_wait("asset-1", "ifc-global-1", callback)
        self.assertEqual(result["status"], "succeeded")
        self.assertEqual(progress, ["queued"])
        get_ifc_file.assert_called_once_with("asset-1", "ifc-global-1")
        create_export.assert_called_once_with("asset-1")
        wait_for_export.assert_called_once_with(
            "asset-1", "run-1", progress=callback
        )

    def test_rejects_invalid_base_url(self):
        with self.assertRaises(cde.CDEError):
            cde.CDEClient("not-a-url")


if __name__ == "__main__":
    unittest.main()

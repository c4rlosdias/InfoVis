"""HTTP client for the CERTI CDE API, without Blender dependencies."""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen


class CDEError(RuntimeError):
    """A user-facing CDE request error."""


def _safe_filename(value: str) -> str:
    name = Path(value or "model.ifc").name
    name = re.sub(r"[^A-Za-z0-9._ -]+", "_", name).strip(" .")
    if not name.lower().endswith(".ifc"):
        name += ".ifc"
    return name or "model.ifc"


class CDEClient:
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = (base_url or "").strip().rstrip("/") + "/"
        self.timeout = timeout
        self.access_token = ""
        self.refresh_token = ""
        parsed = urlparse(self.base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise CDEError("The CDE URL must start with http:// or https://.")

    @property
    def authenticated(self) -> bool:
        return bool(self.access_token)

    def logout(self) -> None:
        self.access_token = ""
        self.refresh_token = ""

    def _url(self, path: str) -> str:
        return urljoin(self.base_url, path.lstrip("/"))

    def _request(self, method: str, path: str, *, params=None, payload=None, accept="application/json"):
        url = self._url(path)
        if params:
            url += ("&" if "?" in url else "?") + urlencode(params)
        headers = {"Accept": accept}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        body = None
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(url, data=body, headers=headers, method=method)
        try:
            return urlopen(request, timeout=self.timeout)
        except HTTPError as error:
            detail = ""
            try:
                raw = error.read().decode("utf-8", errors="replace")
                data = json.loads(raw)
                if isinstance(data, dict):
                    detail = data.get("detail") or data.get("message") or data
                else:
                    detail = data
                if isinstance(detail, (dict, list)):
                    detail = json.dumps(detail, ensure_ascii=False)
            except Exception:
                detail = getattr(error, "reason", "") or ""
            if error.code == 401:
                self.logout()
                raise CDEError(
                    "Invalid credentials or expired JWT session. Check your credentials and connect again."
                ) from error
            request_path = urlparse(url).path
            raise CDEError(
                f"CDE returned HTTP {error.code} for {method} {request_path}"
                f"{f': {detail}' if detail else ''}"
            ) from error
        except (URLError, TimeoutError, OSError) as error:
            raise CDEError(f"Could not connect to the CDE: {getattr(error, 'reason', error)}") from error

    def _request_json(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        with self._request(method, path, **kwargs) as response:
            try:
                decoded = json.loads(response.read().decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise CDEError("The CDE returned an invalid JSON response.") from error
        # The live API wraps successful payloads as {"data": ...}, although
        # the OpenAPI schemas describe the inner object. The official Postman
        # collection confirms this for JWT at response.data.access.
        if isinstance(decoded, dict) and isinstance(decoded.get("data"), (dict, list)):
            return decoded["data"]
        return decoded

    def authenticate(self, client_id: str, client_secret: str) -> None:
        if not client_id.strip() or not client_secret:
            raise CDEError("Enter the Client ID and Client Secret.")
        data = self._request_json("POST", "/auth/token", payload={
            "client_id": client_id.strip(), "client_secret": client_secret,
        })
        access = data.get("access") or data.get("access_token")
        if not access:
            raise CDEError("The CDE did not return an access token.")
        self.access_token = access
        self.refresh_token = data.get("refresh") or data.get("refresh_token") or ""

    def _all_pages(self, path: str, *, limit: int = 100) -> list[dict[str, Any]]:
        results, next_path, pages = [], path, 0
        while next_path and pages < 100:
            data = self._request_json("GET", next_path, params={"limit": limit} if pages == 0 else None)
            if isinstance(data, list):
                page_results = data
                next_url = None
            elif isinstance(data, dict):
                page_results = data.get("results", [])
                next_url = data.get("next")
            else:
                raise CDEError("The CDE returned an unexpected pagination format.")
            if not isinstance(page_results, list):
                raise CDEError("The CDE returned a list in an unexpected format.")
            results.extend(item for item in page_results if isinstance(item, dict))
            if next_url:
                current_host, next_host = urlparse(self.base_url).netloc, urlparse(next_url).netloc
                if next_host and next_host != current_host:
                    raise CDEError("The CDE returned a pagination link for a different server.")
            next_path = next_url
            pages += 1
        if next_path:
            raise CDEError("The request exceeded the 100-page limit.")
        return results

    def list_projects(self):
        return self._all_pages("/api/v1/projects")

    def list_assets(self, project_global_id: str):
        return self._all_pages(f"/api/v1/projects/{project_global_id}/assets")

    def list_ifc_files(self, asset_global_id: str):
        return self._all_pages(f"/api/v1/assets/{asset_global_id}/ifc-files")

    def get_ifc_file(self, asset_global_id: str, ifc_global_id: str):
        return self._request_json(
            "GET", f"/api/v1/assets/{asset_global_id}/ifc-files/{ifc_global_id}"
        )

    def list_exports(self, asset_global_id: str):
        return self._all_pages(f"/api/v1/assets/{asset_global_id}/exports")

    def get_export(self, asset_global_id: str, export_id: str):
        return self._request_json(
            "GET", f"/api/v1/assets/{asset_global_id}/exports/{export_id}"
        )

    def create_export(self, asset_global_id: str):
        payload = {"force": False}
        return self._request_json("POST", f"/api/v1/assets/{asset_global_id}/exports", payload=payload)

    def wait_for_export(self, asset_global_id: str, export_id: str, *, poll_interval=1.0,
                        max_wait=600.0, progress: Callable[[str], None] | None = None):
        deadline = time.monotonic() + max_wait
        while time.monotonic() < deadline:
            data = self.get_export(asset_global_id, export_id)
            status = data.get("status", "")
            if progress:
                progress(status)
            if status == "succeeded":
                return data
            if status == "failed":
                message = data.get("error_message") or data.get("error_code") or "unknown error"
                raise CDEError(f"IFC generation failed: {message}")
            time.sleep(poll_interval)
        raise CDEError("IFC generation timed out after 10 minutes.")

    def generate_export_and_wait(
        self,
        asset_global_id: str,
        ifc_global_id: str,
        progress: Callable[[str], None] | None = None,
    ) -> dict[str, Any]:
        ifc_global_id = str(ifc_global_id or "").strip()
        if not ifc_global_id:
            raise CDEError("Select an IFC submission before generating an export.")
        # Validate that the selected IFC belongs to the asset and is still
        # available before requesting the asset export described by the API.
        self.get_ifc_file(asset_global_id, ifc_global_id)
        export = self.create_export(asset_global_id)
        export_id = str(export.get("id") or "")
        if not export_id:
            raise CDEError("The CDE did not return an IFC export ID.")
        status = str(export.get("status") or "queued")
        if progress:
            progress(status)
        if status == "succeeded":
            return export
        return self.wait_for_export(asset_global_id, export_id, progress=progress)

    def download_export(self, asset_global_id: str, export_id: str,
                        destination_dir: str, filename: str) -> str:
        directory = Path(destination_dir).resolve()
        directory.mkdir(parents=True, exist_ok=True)
        target = (directory / _safe_filename(filename)).resolve()
        if directory != target.parent:
            raise CDEError("The CDE returned an invalid IFC filename.")
        partial = target.with_suffix(target.suffix + ".part")
        try:
            with self._request("GET", f"/api/v1/assets/{asset_global_id}/exports/{export_id}/download",
                               # The live API rejects the media types advertised
                               # by its own OpenAPI schema with HTTP 406. A wildcard
                               # lets the download view choose its binary renderer.
                               accept="*/*") as response, partial.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
            os.replace(partial, target)
        except Exception:
            try:
                partial.unlink(missing_ok=True)
            except OSError:
                pass
            raise
        return str(target)

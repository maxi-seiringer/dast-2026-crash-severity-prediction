"""
dbrepo client helper
Provides a small wrapper to fetch DBRepo views as pandas DataFrames.
"""
from typing import List, Optional, Tuple
import os
import requests
import pandas as pd


class DBRepoError(Exception):
    pass


class DBRepoClient:
    def __init__(self, api_base: Optional[str] = None, db_id: Optional[str] = None,
                 auth: Optional[Tuple[str, str]] = None, timeout: int = 30):
        self.api_base = api_base or os.getenv("DBREPO_API_BASE")
        self.db_id = db_id or os.getenv("DBREPO_DB_ID")
        self.auth = auth or (os.getenv("DBREPO_USER"), os.getenv("DBREPO_PASSWORD"))
        self.timeout = timeout
        if not self.api_base or not self.db_id:
            raise DBRepoError("DBRepo API base URL and DB ID must be provided via args or env vars")

    def _request(self, path: str, params: dict = None) -> requests.Response:
        url = f"{self.api_base.rstrip('/')}/{path.lstrip('/')}"
        try:
            resp = requests.get(url, params=params, auth=self.auth, timeout=self.timeout)
        except requests.RequestException as e:
            raise DBRepoError(f"Connection error while requesting {url}: {e}") from e
        if resp.status_code != 200:
            raise DBRepoError(f"Unexpected response {resp.status_code} from {url}: {resp.text}")
        return resp

    def list_views(self) -> List[str]:
        # Attempt to list subsets/views for the database
        path = f"database/{self.db_id}/subset"
        resp = self._request(path)
        j = resp.json()
        # Try to extract names from the returned structure
        if isinstance(j, dict) and "data" in j and isinstance(j["data"], list):
            return [s.get("id") or s.get("name") or s.get("slug") for s in j["data"] if isinstance(s, dict)]
        raise DBRepoError("Unexpected JSON structure when listing views")

    def get_view(self, view_name: str) -> pd.DataFrame:
        path = f"database/{self.db_id}/subset/{view_name}"
        resp = self._request(path)
        j = resp.json()
        if not isinstance(j, dict) or "data" not in j:
            raise DBRepoError(f"View {view_name} returned unexpected JSON: {j}")
        data = j["data"]
        try:
            df = pd.DataFrame(data)
        except Exception as e:
            raise DBRepoError(f"Failed to convert view {view_name} to DataFrame: {e}") from e
        return df

    def find_first_existing_view(self, candidates: List[str]) -> Optional[str]:
        for c in candidates:
            try:
                self.get_view(c)
                return c
            except DBRepoError:
                continue
        return None

    def create_subset(self, name: str, query: str, persist: bool = True) -> dict:
        """Create/persist a subset (view) on the DBRepo instance.

        Returns the JSON response as dict on success.
        """
        url = f"{self.api_base.rstrip('/')}/database/{self.db_id}/subset"
        payload = {
            "name": name,
            "query": query,
            "type": "query",
            "is_persisted": bool(persist),
        }
        try:
            resp = requests.post(url, json=payload, auth=self.auth, timeout=self.timeout)
        except requests.RequestException as e:
            raise DBRepoError(f"Connection error while creating subset {name}: {e}") from e
        if resp.status_code not in (200, 201):
            raise DBRepoError(f"Failed to create subset {name}: {resp.status_code} {resp.text}")
        try:
            return resp.json()
        except Exception:
            return {"status_code": resp.status_code, "text": resp.text}

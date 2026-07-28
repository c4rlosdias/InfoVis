import requests

from .ifc_session import get_model


class CDE_Api:  
    def __init__(self, endpoint="", token="", timeout=15):
        self.endpoint = (endpoint or "").rstrip("/")
        self.token = token or ""
        self.timeout = timeout

    @classmethod
    def from_blender_context(cls, context, timeout=15):
        endpoint = ""
        token = ""
        try:
            package_name = __package__.split(".data", 1)[0]
            addon = context.preferences.addons.get(package_name)
            preferences = addon.preferences if addon else None
            if preferences:
                endpoint = getattr(preferences, "cde_url", "") or ""
                token = getattr(preferences, "cde_token", "") or ""
        except Exception:
            pass
        return cls(endpoint=endpoint, token=token, timeout=timeout)

    def _headers(self):
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request_json(self, method, path, params=None):
        if not self.endpoint:
            return None
        url = f"{self.endpoint}/{path.lstrip('/')}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._headers(),
                params=params,
                timeout=self.timeout,
            )
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            return None
        return None
    
    def get_projects(self, element):
        return self._request_json("GET", "/projects")
    
    def get_contracts(self, element):
        contracts = []
           
        model = get_model()
        entity = model.by_id(element.id)
        assignment = entity.HasAssignments
        if assignment:
            for rel in assignment:
                if rel.is_a("IfcRelAssignsToControl"):
                    contract = rel.RelatingControl                   
                    if contract.is_a("IfcProjectOrder"):
                        contract_data = {
                            "id"          : contract.GlobalId,
                            "name"        : contract.Name,
                            "description" : contract.Description,
                        }
                        contracts.append(contract_data)
        return contracts


    def get_inventory(self, element):
        inventory = [
            {
                "id": "in1",
                "name": "Inventory-001",
                "objects": [
                    {
                        "id" : "AC-001",
                        "name" : "AC-001"
                    },
                    {
                        "id" : "AC-002",
                        "name" : "AC-002"
                    }
                ]
            },
            {
                "id": "in2",
                "name": "Inventory-002",
                "objects": [
                    {
                        "id" : "AC-003",
                        "name" : "AC-003"
                    },
                    {
                        "id" : "AC-004",
                        "name" : "AC-004"
                    }
                ]
            }
        ]


        return inventory

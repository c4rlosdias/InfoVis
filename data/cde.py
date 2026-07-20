import requests
import bonsai.tool as tool


class CDE_Api:  
    def __init__(self, endpoint):
        self.endpoint = endpoint
    
    def get_projects(self, element):
        response = requests.get(f'{self.endpoint}/projects')
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def get_contracts(self, element):
        contracts = []
           
        model = tool.Ifc.get()
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

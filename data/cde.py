import requests


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
        contracts = [
            {
                "id": "ct1",
                "name": "Contracto-001",
                "objects": [
                    {
                        "id" : "TR-001",
                        "name" : "Trench-001",
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
                        "id" : "TR-002",
                        "name" : "Trench-002",
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
            },
            {
                "id": "ct2",
                "name": "Contracto-002",
                "objects": [
                    {
                        "id" : "TR-003",
                        "name" : "Trench-003",
                        "objects": [
                            {
                                "id" : "AC-005",
                                "name" : "AC-005"
                            },
                            {
                                "id" : "AC-006",
                                "name" : "AC-006"
                            }
                        ]
                    },
                    {
                        "id" : "TR-004",
                        "name" : "Trench-004",
                        "objects": [
                            {
                                "id" : "AC-007",
                                "name" : "AC-007"
                            },
                            {
                                "id" : "AC-008",
                                "name" : "AC-008"
                            }
                        ]
                    }

                ]
            }
        ]

        return contracts


    def get_inventory(self):
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

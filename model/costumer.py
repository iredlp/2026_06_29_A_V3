from dataclasses import dataclass, field
from typing import Optional, Set

@dataclass
class Customer:
    CustomerId: int
    FirstName: str
    LastName: str
    Company: str
    Address: str
    City: str
    State: str
    Country: str
    PostalCode: str
    Phone: str
    Fax: str
    Email: str
    SupportRepId: int


    #fatturato_tot: list = field(default_factory=list)
    fatturato_tot: float = 0.0
    artisti: set = field(default_factory=set)
   # playlist: set = field(default_factory=set)

    def __hash__(self):
        return hash(self.CustomerId)

    def __eq__(self, other):
        if isinstance(other, Customer):
            return self.CustomerId == other.CustomerId
        return False

    def __repr__(self):
        return f"{self.FirstName} {self.LastName} ({self.CustomerId })" #if self.date_of_birth is not None else 'N/D'})"
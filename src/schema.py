from pydantic import BaseModel, Field
from typing import List, Optional

class EmissionMetric(BaseModel):
    scope_1: Optional[float] = Field(None, description="Direct GHG emissions in metric tonnes of CO2 equivalent.")
    scope_2: Optional[float] = Field(None, description="Indirect GHG emissions from purchased electricity.")
    scope_3: Optional[float] = Field(None, description="Other indirect GHG emissions.")
    unit: str = Field("Metric Tonnes CO2e", description="Unit of measurement.")

class WasteManagement(BaseModel):
    total_waste_generated: Optional[float] = Field(None, description="Total waste generated in metric tonnes.")
    recycled_percentage: Optional[float] = Field(None, description="Percentage of waste recycled or re-used.")
    hazardous_waste: Optional[float] = Field(None, description="Total hazardous waste generated.")

class WaterConsumption(BaseModel):
    total_water_consumed: Optional[float] = Field(None, description="Total water consumption in kilolitres.")
    water_intensity: Optional[float] = Field(None, description="Water consumption per rupee of turnover.")

class Principle6Schema(BaseModel):
    """
    Schema for BRSR Principle 6: Details of Environmental Responsibilities.
    """
    emissions: EmissionMetric = Field(default_factory=EmissionMetric)
    waste: WasteManagement = Field(default_factory=WasteManagement)
    water: WaterConsumption = Field(default_factory=WaterConsumption)
    
    # Generic "Other" for anything else Principle 6 related that doesn't fit high-level buckets
    other_initiatives: List[str] = Field(default_factory=list, description="List of other environmental initiatives described.")

    class Config:
        json_schema_extra = {
            "example": {
                "emissions": {"scope_1": 120.5, "scope_2": 500.0},
                "waste": {"total_waste_generated": 50.0},
                "water": {"total_water_consumed": 1000.0}
            }
        }

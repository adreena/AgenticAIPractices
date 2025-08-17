from pydantic import BaseModel
import datetime
from mock_api import Interest

class Traveler(BaseModel):
    name: str
    age: int
    interests: list[Interest]

class VacationInfo(BaseModel):
    travelers: list[Traveler]
    destination: str
    date_of_arrival: datetime.date
    date_of_departure: datetime.date
    budget: int

class Weather(BaseModel):
    temperature: float
    temperature_unit: str
    condition: str


class Activity(BaseModel):
    activity_id: str
    name: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    location: str
    description: str
    price: int
    related_interests: list[Interest]


class ActivityRecommendation(BaseModel):
    activity: Activity
    reasons_for_recommendation: list[str]


class ItineraryDay(BaseModel):
    date: datetime.date
    weather: Weather
    activity_recommendations: list[ActivityRecommendation]


class TravelPlan(BaseModel):
    city: str
    start_date: datetime.date
    end_date: datetime.date
    total_cost: int
    itinerary_days: list[ItineraryDay]
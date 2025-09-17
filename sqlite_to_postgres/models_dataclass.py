from dataclasses import dataclass


@dataclass
class Film:
    title: str
    description: str
    rating: float


@dataclass
class Genre:
    name: str
    description: str | None = None


@dataclass
class Person:
    full_name: str

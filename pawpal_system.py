"""Logic layer for the PawPal pet care app."""

from dataclasses import dataclass


class Owner:
    """Represents a pet owner."""

    def __init__(self, name="", address="", amount_of_pets=0):
        self.name = name
        self.address = address
        self.amount_of_pets = amount_of_pets
        self.pets = []

    def add_pet(self, pet):
        pass

    def update_owner_info(self, name, address):
        pass

    def get_pet_count(self):
        pass


@dataclass
class Pet:
    """Represents a pet receiving care."""

    type_of_pet: str = ""
    name_of_pet: str = ""
    breed_of_pet: str = ""
    age_of_pet: int = 0

    def update_pet_info(self, type_of_pet, name_of_pet, breed_of_pet, age_of_pet):
        pass

    def get_pet_details(self):
        pass


@dataclass
class Task:
    """Represents pet care tasks selected by the owner."""

    shower_pet: bool = False
    cut_pet_nails: bool = False
    cut_pet_hair: bool = False
    give_vitamin_booster: bool = False

    def select_task(self, task_name):
        pass

    def remove_task(self, task_name):
        pass

    def get_selected_tasks(self):
        pass


class Scheduler:
    """Schedules pet care appointments."""

    def __init__(self, selected_day="", selected_time=""):
        self.open_days = "Monday - Friday"
        self.open_hours = "10:00 a.m. - 4:30 p.m."
        self.selected_day = selected_day
        self.selected_time = selected_time

    def show_available_days(self):
        pass

    def show_available_times(self):
        pass

    def fill_out_pet_information(self, owner, pet):
        pass

    def submit_schedule(self):
        pass

    def show_confirmation_message(self):
        pass

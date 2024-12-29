import os
from django.contrib.auth.models import User

from company.models import Company


def run():
    # Read user credentials from environment variables
    username = os.getenv("DUMMY_USER_NAME")
    password = os.getenv("DUMMY_USER_PASSWORD")
    email = os.getenv("DUMMY_USER_EMAIL")

    # Create user if it doesn't exist
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.email = email
        user.save()
        print(f"Dummy user '{username}' created successfully.")
    else:
        print(f"Dummy user '{username}' already exists.")

    # Create Company records owned by the user
    companies = [
        {
            "company_name": "Tech Innovations",
            "description": "A company focused on innovative tech solutions.",
            "number_of_employees": 50,
        },
        {
            "company_name": "Eco Ventures",
            "description": "Promoting sustainable and eco-friendly projects.",
            "number_of_employees": 30,
        },
        {
            "company_name": "Health First",
            "description": "Healthcare services and products company.",
            "number_of_employees": 100,
        },
        {
            "company_name": "FinTech Hub",
            "description": "A leader in financial technology solutions.",
            "number_of_employees": 75,
        },
    ]

    for company_data in companies:
        company, created = Company.objects.get_or_create(
            owner=user,
            company_name=company_data["company_name"],
            defaults={
                "description": company_data["description"],
                "number_of_employees": company_data["number_of_employees"],
            },
        )
        if created:
            print(f"Company '{company.company_name}' created.")
        else:
            print(f"Company '{company.company_name}' already exists.")

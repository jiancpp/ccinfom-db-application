from app import create_app
from app.models import db, Section
from app.utils import generate_seats_for_section  # import your function

app = create_app()
app.app_context().push()  # needed to use db outside request

# Fetch all sections
sections = Section.query.all()

for section in sections:
    generate_seats_for_section(
        venue_id=section.Venue_ID,
        section_id=section.Section_ID,
        section_capacity=section.Max_Capacity  # or whatever your column is
    )
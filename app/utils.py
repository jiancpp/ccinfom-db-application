import string
from app.models import db, Seat

def get_row_label(i):
    row_labels = string.ascii_uppercase
    label = ""
    while i >= 0:
        label = row_labels[i % 26] + label
        i = i // 26 - 1
    return label

def generate_seats_for_section(venue_id, section_id, section_capacity):
    # Default seats per row
    seats = []
    seats_per_row = 45
    rows_needed = (section_capacity + seats_per_row - 1) // seats_per_row
    row_labels = string.ascii_uppercase  # A to Z

    for i in range(rows_needed):
        row = get_row_label(i)

        start_number = 1
        end_number = seats_per_row
        if (i + 1) * seats_per_row > section_capacity:
            end_number = section_capacity - i * seats_per_row  # Remainder

        for seat_number in range(start_number, end_number + 1):
            seat = Seat(
                Venue_ID = venue_id,
                Section_ID = section_id,
                Seat_Row = row,
                Seat_Number = seat_number
            )

            seats.append(seat)

    db.session.bulk_save_objects(seats)
    db.session.commit()
    print(f"Added {len(seats)} seats to section {section_id} in venue {venue_id}")

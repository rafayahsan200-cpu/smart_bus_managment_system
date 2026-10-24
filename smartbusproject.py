
# ============================================
# SMART BUS TICKET BOOKING & RESERVATION SYSTEM
# ============================================

routes = [
    {
        "route_id": "R101",
        "departure_city": "Karachi",
        "destination_city": "Hyderabad",
        "departure_time": "08:00 AM",
        "ticket_price": 1200,
        "total_seats": 40,
        "available_seats": 40
    },
    {
        "route_id": "R102",
        "departure_city": "Karachi",
        "destination_city": "Sukkur",
        "departure_time": "09:30 AM",
        "ticket_price": 2000,
        "total_seats": 36,
        "available_seats": 36
    },
    {
        "route_id": "R103",
        "departure_city": "Hyderabad",
        "destination_city": "Mirpur Khas",
        "departure_time": "11:00 AM",
        "ticket_price": 800,
        "total_seats": 32,
        "available_seats": 32
    },
    {
        "route_id": "R104",
        "departure_city": "Karachi",
        "destination_city": "Lahore",
        "departure_time": "07:00 PM",
        "ticket_price": 5000,
        "total_seats": 45,
        "available_seats": 45
    },
    {
        "route_id": "R105",
        "departure_city": "Sukkur",
        "destination_city": "Hyderabad",
        "departure_time": "02:00 PM",
        "ticket_price": 1500,
        "total_seats": 30,
        "available_seats": 30
    }
]

bookings = []
issued_booking_ids = set()
next_booking_number = 1001


# ============================================
# OPTION 1: VIEW AVAILABLE BUS ROUTES
# ============================================

def view_routes():
    print("\n" + "=" * 90)
    print("                    AVAILABLE BUS ROUTES")
    print("=" * 90)

    if len(routes) == 0:
        print("Sorry! No bus routes are available.")
        return

    print(
        f"{'Route ID':<10}"
        f"{'From':<17}"
        f"{'Destination':<18}"
        f"{'Departure':<15}"
        f"{'Fare (Rs.)':<14}"
        f"{'Seats':<12}"
    )

    print("-" * 90)

    for route in routes:
        print(
            f"{route['route_id']:<10}"
            f"{route['departure_city']:<17}"
            f"{route['destination_city']:<18}"
            f"{route['departure_time']:<15}"
            f"{route['ticket_price']:<14}"
            f"{route['available_seats']}/{route['total_seats']}"
        )

    print("-" * 90)
    print("Total Routes Available:", len(routes))
    print("All fares are in Pakistani Rupees (Rs.).")
    print("=" * 90)


# ============================================
# OPTION 2: SEARCH FOR A ROUTE
# ============================================

def search_route():
    search = input(
        "Enter Route ID or City Name: "
    ).strip().lower()

    if not search:
        print("Please enter a route ID or city name.")
        return

    found = False

    for route in routes:
        if (
            search == route["route_id"].lower()
            or search == route["departure_city"].lower()
            or search == route["destination_city"].lower()
        ):
            print("\nRoute Found!")
            print("-" * 40)
            print("Route ID:", route["route_id"])
            print(
                "Journey:",
                route["departure_city"],
                "->",
                route["destination_city"]
            )
            print("Departure:", route["departure_time"])
            print("Ticket Price: Rs.", route["ticket_price"])
            print(
                "Available Seats:",
                route["available_seats"],
                "/",
                route["total_seats"]
            )
            found = True

    if not found:
        print("No matching route found.")


# ============================================
# OPTION 3: BOOK A TICKET
# ============================================

def book_ticket():
    global next_booking_number

    name = input("Enter Passenger Name: ").strip()

    if not name:
        print("Passenger name cannot be empty.")
        return

    try:
        age = int(input("Enter Passenger Age: "))
        seats = int(input("Enter Number of Seats: "))
    except ValueError:
        print("Age and number of seats must be whole numbers.")
        return

    if age <= 0:
        print("Age must be greater than zero.")
        return

    if seats <= 0:
        print("Number of seats must be greater than zero.")
        return

    route_id = input(
        "Enter Route ID (e.g. R101): "
    ).strip().upper()

    selected_route = None

    for route in routes:
        if route["route_id"] == route_id:
            selected_route = route
            break

    if selected_route is None:
        print("Invalid Route ID.")
        return

    if seats > selected_route["available_seats"]:
        print("Sorry! Not enough seats are available.")
        print("Available Seats:", selected_route["available_seats"])
        return

    booking_id = "B" + str(next_booking_number)

    while booking_id in issued_booking_ids:
        next_booking_number += 1
        booking_id = "B" + str(next_booking_number)

    total_fare = selected_route["ticket_price"] * seats

    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route_id,
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed"
    }

    bookings.append(booking)
    issued_booking_ids.add(booking_id)

    selected_route["available_seats"] -= seats
    next_booking_number += 1

    print("\n" + "=" * 40)
    print("          BOOKING CONFIRMED!")
    print("=" * 40)
    print("Booking ID:", booking_id)
    print("Passenger Name:", name)
    print("Passenger Age:", age)
    print("Route ID:", route_id)
    print("Seats Booked:", seats)
    print("Total Fare: Rs.", total_fare)
    print("=" * 40)


# ============================================
# OPTION 4: VIEW BOOKINGS
# ============================================

def view_bookings():
    if not bookings:
        print("No bookings found.")
        return

    print("\n========== ALL BOOKINGS ==========")

    for booking in bookings:
        print("-" * 40)
        print("Booking ID:", booking["booking_id"])
        print("Passenger:", booking["passenger_name"])
        print("Age:", booking["passenger_age"])
        print("Route ID:", booking["route_id"])
        print("Seats:", booking["seats"])
        print("Total Fare: Rs.", booking["total_fare"])
        print("Status:", booking["status"])


# ============================================
# OPTION 5: CANCEL A BOOKING
# ============================================

def cancel_booking():
    booking_id = input(
        "Enter Booking ID to Cancel: "
    ).strip().upper()

    if not booking_id:
        print("Please enter a Booking ID.")
        return

    for booking in bookings:
        if booking["booking_id"] == booking_id:

            if booking["status"] == "Cancelled":
                print("This booking is already cancelled.")
                return

            for route in routes:
                if route["route_id"] == booking["route_id"]:
                    route["available_seats"] += booking["seats"]
                    break

            booking["status"] = "Cancelled"

            print("Booking cancelled successfully.")
            print("Booking ID:", booking_id)
            print("Seats restored:", booking["seats"])
            return

    print("Booking ID not found.")


# ============================================
# OPTION 6: VIEW SEAT AVAILABILITY
# ============================================

def view_availability():
    print("\n========== SEAT AVAILABILITY ==========")

    for route in routes:
        available = route["available_seats"]

        if available == 0:
            status = "Fully Booked"
        elif available == route["total_seats"]:
            status = "Available"
        else:
            status = "Partially Booked"

        print("-" * 40)
        print("Route ID:", route["route_id"])
        print(
            "Journey:",
            route["departure_city"],
            "->",
            route["destination_city"]
        )
        print(
            "Seats:",
            available,
            "/",
            route["total_seats"]
        )
        print("Status:", status)


# ============================================
# OPTION 7: GENERATE BOOKING REPORT
# ============================================

def booking_report():
    confirmed = 0
    cancelled = 0
    reserved_seats = 0
    revenue = 0

    for booking in bookings:
        if booking["status"] == "Confirmed":
            confirmed += 1
            reserved_seats += booking["seats"]
            revenue += booking["total_fare"]
        else:
            cancelled += 1

    full_routes = 0

    for route in routes:
        if route["available_seats"] == 0:
            full_routes += 1

    print("\n========== BOOKING REPORT ==========")
    print("Total Bookings:", len(bookings))
    print("Confirmed Bookings:", confirmed)
    print("Cancelled Bookings:", cancelled)
    print("Reserved Seats:", reserved_seats)
    print("Confirmed Revenue: Rs.", revenue)
    print("Fully Booked Routes:", full_routes)


# ============================================
# OPTION 8: VIEW ROUTE SCHEDULE
# ============================================

def route_schedule():
    print("\n========== BUS ROUTE SCHEDULE ==========")

    for route in routes:
        print("-" * 45)
        print("Route ID:", route["route_id"])
        print("Departure City:", route["departure_city"])
        print("Destination City:", route["destination_city"])
        print("Departure Time:", route["departure_time"])


# ============================================
# MAIN MENU
# ============================================

def main():
    while True:
        print("\n")
        print("=" * 45)
        print("   SMART BUS TICKET BOOKING SYSTEM")
        print("=" * 45)
        print("1. View Available Routes")
        print("2. Search for a Route")
        print("3. Book a Ticket")
        print("4. View Bookings")
        print("5. Cancel a Booking")
        print("6. View Seat Availability")
        print("7. Generate Booking Report")
        print("8. View Route Schedule")
        print("9. Exit")
        print("=" * 45)

        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            view_routes()

        elif choice == "2":
            search_route()

        elif choice == "3":
            book_ticket()

        elif choice == "4":
            view_bookings()

        elif choice == "5":
            cancel_booking()

        elif choice == "6":
            view_availability()

        elif choice == "7":
            booking_report()

        elif choice == "8":
            route_schedule()

        elif choice == "9":
            print("Thank you for using Smart Bus System!")
            break

        else:
            print("Invalid choice! Please enter a number from 1 to 9.")


# ============================================
# START PROGRAM
# ============================================

if __name__ == "__main__":
    main()
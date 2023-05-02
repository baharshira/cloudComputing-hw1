from datetime import datetime, timedelta
from flask import Flask, request
import app as app


class Ticket:
    app = Flask(__name__)

    def __init__(self, plate, parkingLot, ticketId, entryTime):
        self.plate = plate
        self.parkingLot = parkingLot
        self.ticketId = ticketId
        self.entryTime = entryTime

    # initialize a global list to store created tickets
    tickets = []
    # initialize a global variable to keep track of the last assigned ticket ID
    last_ticket_id = 0

    # example Flask route for handling POST requests to /entry
    @app.route('/entry', methods=['POST'])
    def create_ticket(self):
        global last_ticket_id

        # extract the plate and parkingLot values from the request parameters
        plate = request.args.get('plate')
        parking_lot = request.args.get('parkingLot')

        # save the current time as the entry time for the ticket
        entry_time = datetime.now().isoformat()

        # generate a unique ticket ID based on the last assigned ticket ID
        ticket_id = last_ticket_id + 1
        last_ticket_id = ticket_id

        # create a new ticket object with the provided data and entry time
        ticket = Ticket(plate, parking_lot, ticket_id, entry_time)

        # save the ticket to the global list
        Ticket.tickets.append(ticket)

        # return a success response
        return {'status': 'success', 'ticket': ticket.__dict__}

    @app.route('/exit', methods=['POST'])
    def exit_parking(self):
        # extract the ticket ID from the request parameters
        ticket_id = int(request.args.get('ticketId'))

        # find the corresponding ticket object in the list of tickets
        for ticket in Ticket.tickets:
            if ticket.ticketId == ticket_id:
                # calculate the parking time based on the difference between the entry time and the current time
                entry_time = datetime.fromisoformat(ticket.entryTime)
                exit_time = datetime.now()
                parking_time = exit_time - entry_time
                parking_hours = parking_time.total_seconds() / 3600

                # calculate the charge based on the parking time
                charge = round(parking_hours * 10, 2)

                # remove the ticket from the list of tickets
                Ticket.tickets.remove(ticket)

                # return the license plate, parking time, parking lot ID, and charge as a response
                return {
                    'status': 'success',
                    'plate': ticket.plate,
                    'parkingTime': str(parking_time),
                    'parkingLot': ticket.parkingLot,
                    'charge': charge
                }

        # if the ticket ID was not found, return an error response
        return {'status': 'error', 'message': 'Ticket ID not found'}

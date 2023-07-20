from flask_restful import Resource, fields, marshal_with, reqparse, marshal, output_json
from .database import db
from .models import *
from .validation import *
import requests
from datetime import datetime


# marshaling for venue
show={
    "show_id":fields.Integer
}

venue={
    "venue_id":fields.Integer,
    "venue_name":fields.String,
    "venue_place":fields.String,
    "venue_capacity": fields.Integer,
    "venue_location": fields.String,
    "shows":fields.List(fields.Nested(show))
}

update_venue_parser = reqparse.RequestParser()
update_venue_parser.add_argument("venue_name", type=str)
update_venue_parser.add_argument("venue_place", type=str)
update_venue_parser.add_argument("venue_capacity", type=int)
update_venue_parser.add_argument("venue_location", type=str)

create_venue_parser = reqparse.RequestParser()
create_venue_parser.add_argument("venue_name", type=str)
create_venue_parser.add_argument("venue_place", type=str)
create_venue_parser.add_argument("venue_capacity", type=int)
create_venue_parser.add_argument("venue_location", type=str)

class venueApi(Resource):
    @marshal_with(venue)#completed and ready for share
    def get(self):
        try:
            venues=Venue.query.all()
            if venues:
                marsha_venue=[marshal(ven, venue) for ven in venues]
                return marsha_venue
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e))
        
    @marshal_with(venue) 
    def put(self, venue_id):
        args=update_venue_parser.parse_args()
        venue_name=args.get("venue_name", None)
        venue_place=args.get("venue_place", None)
        venue_capacity=args.get("venue_capacity", None)
        venue_location=args.get("venue_location", None)
        if venue_id is None:
            raise NotFoundError(status_code=400)
        elif venue_name is None:
            NotFoundError(status_code=400)
        elif venue_place is None:
            NotFoundError(status_code=400)
        elif venue_capacity is None:
            NotFoundError(status_code=400)
        elif venue_location is None:
            NotFoundError(status_code=400)
        else:
            venue = Venue.query.filter_by(venue_id=int(venue_id)).first()
            try:
                venue.venue_name=venue_name
                venue.venue_place=venue_place
                venue.venue_location=venue_location
                venue.venue_capacity=venue_capacity
                db.session.commit()
                return venue
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))    
    def delete(self, venue_id):
        if venue_id is None:
            raise NotFoundError(status_code=400)            
        else:
            ids=Venue.query.with_entities(Venue.venue_id).all()
            vids=[i[0] for i in ids]
            if venue_id in vids:
                try:
                    venue = Venue.query.filter_by(venue_id=venue_id).first()
                    for show in venue.shows:
                        db.session.delete(show)
                        db.session.commit()
                    db.session.delete(venue)
                    db.session.commit()
                    return output_json(data={"message":"successfully deleted"}, code=200)
                except requests.exceptions.RequestException as e:
                    db.session.rollback()
                    raise NetworkError(status_code=405, message="Error: {}".format(e))
            else:
                raise NotFoundError(status_code=404)    
    @marshal_with(venue)
    def post(self):
        args=create_venue_parser.parse_args()
        venue_name=args.get("venue_name", None)
        venue_place=args.get("venue_place", None)
        venue_capacity=args.get("venue_capacity", None)
        venue_location=args.get("venue_location", None)

        if venue_name is None:
            raise NotFoundError(status_code=400)
        elif venue_place is None:
            raise NotFoundError(status_code=400)
        elif venue_capacity is None:
            raise NotFoundError(status_code=400)
        elif venue_location is None:
            raise NotFoundError(status_code=400)
        else:
            try:
                venue=Venue(venue_name=venue_name, venue_place=venue_place, venue_capacity=venue_capacity, venue_location=venue_location)
                db.session.add(venue)
                db.session.commit()
                return venue
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))    

shows= {
    "show_id": fields.Integer,
    "show_name":fields.String,
    "show_rating":fields.Float,
    "show_tag": fields.String,
    "show_price": fields.Float,
    "no_seats": fields.Integer,
    "show_stime":fields.String,
    "show_etime":fields.String
}

update_show_parser = reqparse.RequestParser()
update_show_parser.add_argument("show_name", type=str)
update_show_parser.add_argument("show_rating", type=float)
update_show_parser.add_argument("show_tag", type=str)
update_show_parser.add_argument("show_price", type=float)
update_show_parser.add_argument("no_seats", type=int)
update_show_parser.add_argument("show_stime", type=str)
update_show_parser.add_argument("show_etime", type=str)

create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument("show_name", type=str)
create_show_parser.add_argument("show_rating", type=float)
create_show_parser.add_argument("show_tag", type=str)
create_show_parser.add_argument("show_price", type=float)
create_show_parser.add_argument("no_seats", type=int)
create_show_parser.add_argument("show_stime", type=str)
create_show_parser.add_argument("show_etime", type=str)

class showApi(Resource):
    @marshal_with(shows)
    def get(self):
        try:
            shows1=Show.query.all()
            if shows1:
                marsha_show=[marshal(sh, shows) for sh in shows1]
                return marsha_show
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e) )
    @marshal_with(shows)
    def put(self, show_id):
        args=update_show_parser.parse_args()
        show_name=args.get("show_name", None)
        show_rating=args.get("show_rating", None)
        show_tag=args.get("show_tag", None)
        show_price=args.get("show_price", None)
        no_seats=args.get("no_seats", None)
        show_stime=args.get("show_stime", None)
        show_etime=args.get("show_etime", None)
        if show_id is None:
            raise NotFoundError(status_code=400)
        elif show_name is None:
            NotFoundError(status_code=400)
        elif show_rating is None:
            NotFoundError(status_code=400)
        elif show_tag is None:
            NotFoundError(status_code=400)
        elif show_price is None:
            NotFoundError(status_code=400)
        elif no_seats is None:
            NotFoundError(status_code=400)
        elif show_stime is None:
            NotFoundError(status_code=400)
        elif show_etime is None:
            NotFoundError(status_code=400)
        else:
            try:
                date_format="%H:%M"
                show=Show.query.filter_by(show_id=show_id).first()
                show.show_name=show_name
                show.show_rating=show_rating
                show.show_tag=show_tag
                show.show_price=show_price
                show.no_seats=no_seats
                show.show_stime=datetime.strptime(show_stime, date_format)
                show.show_etime=datetime.strptime(show_etime, date_format)
                db.session.commit()
                return show
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))
            
    def delete(self, show_id):
        if show_id is None:
            raise NotFoundError(status_code=400)            
        else:
            ids=Show.query.with_entities(Show.show_id).all()
            vids=[i[0] for i in ids]
            if show_id in vids:
                try:
                    show = Show.query.filter_by(show_id=show_id).first()
                    db.session.delete(show)
                    db.session.commit()
                    return output_json(data={"message":"successfully deleted"}, code=200)
                except requests.exceptions.RequestException as e:
                    db.session.rollback()
                    raise NetworkError(status_code=405, message="Error: {}".format(e))
            else:
                raise NotFoundError(status_code=404)
    @marshal_with(shows)
    def post(self):
        args=update_show_parser.parse_args()
        show_name=args.get("show_name", None)
        show_rating=args.get("show_rating", None)
        show_tag=args.get("show_tag", None)
        show_price=args.get("show_price", None)
        no_seats=args.get("no_seats", None)
        show_stime=args.get("show_stime", None)
        show_etime=args.get("show_etime", None)

        if show_name is None:
            NotFoundError(status_code=400)
        elif show_rating is None:
            NotFoundError(status_code=400)
        elif show_tag is None:
            NotFoundError(status_code=400)
        elif show_price is None:
            NotFoundError(status_code=400)
        elif no_seats is None:
            NotFoundError(status_code=400)
        elif show_stime is None:
            NotFoundError(status_code=400)
        elif show_etime is None:
            NotFoundError(status_code=400)
        else:
            try:
                date_format="%H:%M"
                sstime=datetime.strptime(show_stime, date_format)
                setime=datetime.strptime(show_etime, date_format)
                show=Show(show_name=show_name, show_tag=show_tag, show_price=show_price, no_seats=int(no_seats), show_stime=sstime, show_etime=setime)
                db.session.add(show)
                db.session.commit()
                return show
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))

ticket={
    "ticket_id":fields.Integer
}
user_output={
    "user_id": fields.String,
    "user_name":fields.String,
    "user_mobile":fields.String,
    "user_pass":fields.String,
    "tickets":fields.List(fields.Nested(ticket))
}

user_update_parse=reqparse.RequestParser()
user_update_parse.add_argument("user_name", type=str)
user_update_parse.add_argument("user_mobile", type=str)
user_update_parse.add_argument("user_pass", type=str)

user_create_parse=reqparse.RequestParser()
user_create_parse.add_argument("user_id", type=str)
user_create_parse.add_argument("user_name", type=str)
user_create_parse.add_argument("user_mobile", type=str)
user_create_parse.add_argument("user_pass", type=str)
# cannot update tickets in the user!!
class userApi(Resource):
    @marshal_with(user_output)
    def get(self, user_id):
        try:
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                return user
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e) )
    @marshal_with(user_output)   
    def put(self, user_id):
        args=user_update_parse.parse_args()
        user_name=args.get("user_name")
        user_mobile=args.get("user_mobile")
        user_pass=args.get("user_pass")
        if user_id is None:
            raise NotFoundError(status_code=400)
        elif user_name is None:
            raise NotFoundError(status_code=400)
        elif user_mobile is None:
            raise NotFoundError(status_code=400)
        elif user_pass is None:
            raise NotFoundError(status_code=400)
        else:
            id=User.query.with_entities(User.user_id).all()
            ids=[i[0] for i in id]
            if user_id in ids:
                try:
                    user=User.query.filter_by(user_id=user_id).first()
                    user.user_name=user_name
                    user.user_mobile=user_mobile
                    user.user_pass=user_pass
                    db.session.commit()
                    return user
                except requests.exceptions.RequestException as e:
                    db.session.rollback()
                    raise NetworkError(status_code=405, message="Error: {}".format(e))
            else:
                raise NotFoundError(status_code=404)
    def delete(self, user_id):
        if user_id is None:
            raise NotFoundError(status_code=400)
        else:
            id=User.query.with_entities(User.user_id).all()
            ids=[i[0] for i in id]
            if user_id in ids:
                try:
                    user=User.query.filter_by(user_id=user_id).first()
                    db.session.delete(user)
                    db.session.commit()
                    return output_json(data={"message":"successfully deleted"}, code=200)
                except requests.exceptions.RequestException as e:
                    db.session.rollback()
                    raise NetworkError(status_code=405, message="Error: {}".format(e))
            else:
                raise NotFoundError(status_code=404)
    @marshal_with(user_output)
    def post(self):
        args=user_create_parse.parse_args()
        user_id=args.get("user_id")
        user_name=args.get("user_name")
        user_mobile=args.get("user_mobile")
        user_pass=args.get("user_pass")
        if user_name is None:
            raise NotFoundError(status_code=400)
        elif user_mobile is None:
            raise NotFoundError(status_code=400)
        elif user_pass is None:
            raise NotFoundError(status_code=400)
        else:
            try:
                user = User(user_id=user_id, user_name=user_name, user_mobile=user_mobile, user_pass=user_pass)
                db.session.add(user)
                db.session.commit()
                return user
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))

admin_output={
    "emp_id": fields.String,
    "emp_name":fields.String,
    "emp_mobile":fields.String,
    "emp_pass":fields.String
}
admin_update_parse=reqparse.RequestParser()
admin_update_parse.add_argument("emp_name", type=str)
admin_update_parse.add_argument("emp_mobile", type=str)
admin_update_parse.add_argument("emp_pass", type=str)

admin_create_parse=reqparse.RequestParser()
admin_create_parse.add_argument("emp_id", type=str)
admin_create_parse.add_argument("emp_name", type=str)
admin_create_parse.add_argument("emp_mobile", type=str)
admin_create_parse.add_argument("emp_pass", type=str)
class adminApi(Resource):
    @marshal_with(admin_output)
    def get(self, emp_id):
        try:
            admin = Admin.query.filter_by(emp_id=emp_id).first()
            if admin:
                return admin
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e) )
    @marshal_with(admin_output)   
    def put(self, emp_id):
        args=admin_update_parse.parse_args()
        emp_name=args.get("emp_name")
        emp_mobile=args.get("emp_mobile")
        emp_pass=args.get("emp_pass")
        if emp_id is None:
            raise NotFoundError(status_code=400)
        elif emp_name is None:
            raise NotFoundError(status_code=400)
        elif emp_mobile is None:
            raise NotFoundError(status_code=400)
        elif emp_pass is None:
            raise NotFoundError(status_code=400)
        else:
            id=Admin.query.with_entities(Admin.emp_id).all()
            ids=[i[0] for i in id]
            if emp_id in ids:
                try:
                    admin=Admin.query.filter_by(emp_id=emp_id).first()
                    admin.emp_name=emp_name
                    admin.emp_mobile=emp_mobile
                    admin.emp_pass=emp_pass
                    db.session.commit()
                    return admin
                except requests.exceptions.RequestException as e:
                    db.session.rollback()
                    raise NetworkError(status_code=405, message="Error: {}".format(e))
            else:
                raise NotFoundError(status_code=404)
    def delete(self, emp_id):
        if emp_id is None:
            raise NotFoundError(status_code=400)
        else:
            id=Admin.query.with_entities(Admin.emp_id).all()
            ids=[i[0] for i in id]
            if emp_id in ids:
                try:
                    emp=Admin.query.filter_by(emp_id=emp_id).first()
                    db.session.delete(emp)
                    db.session.commit()
                    return output_json(data={"message":"successfully deleted"}, code=200)
                except requests.exceptions.RequestException as e:
                    db.session.rollback()
                    raise NetworkError(status_code=405, message="Error: {}".format(e))
            else:
                raise NotFoundError(status_code=404)
    @marshal_with(admin_output)
    def post(self):
        args=admin_create_parse.parse_args()
        emp_id=args.get("emp_id")
        emp_name=args.get("emp_name")
        emp_mobile=args.get("emp_mobile")
        emp_pass=args.get("emp_pass")
        if emp_name is None:
            raise NotFoundError(status_code=400)
        elif emp_mobile is None:
            raise NotFoundError(status_code=400)
        elif emp_pass is None:
            raise NotFoundError(status_code=400)
        else:
            try:
                admin = Admin(emp_id=emp_id, emp_name=emp_name, emp_mobile=emp_mobile, emp_pass=emp_pass)
                db.session.add(admin)
                db.session.commit()
                return admin
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))

ticket_output={
    "ticket_id":fields.Integer,
    "venue_id":fields.Integer,
    "show_id":fields.Integer,
    "no_seats":fields.Integer
}
class ticketApi(Resource):
    @marshal_with(ticket_output)
    def get(self):
        try:
            tickets=Ticket.query.all()
            if tickets:
                marshal_ticket=[marshal(t, ticket_output) for t in tickets]
                return marshal_ticket
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e) )
    @marshal_with(ticket_output)
    def get(self, ticket_id):
        try:
            if ticket_id:
                return Ticket.query.filter_by(ticket_id=ticket_id).first()
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e) )

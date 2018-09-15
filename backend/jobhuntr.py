from flask import request, Blueprint, Response
from mongoengine import *
from bson.objectid import ObjectId
import json

bp = Blueprint("jobhuntr", __name__, url_prefix="/jobhuntr")

connect("jobs")

@bp.route("/opportunities", methods=["GET", "POST", "DELETE"])
def opportunity():
    if request.method == "GET":
        username = request.args.get("username")
        opportunities = Opportunity.objects(applicant=username)
        processes = [{ 'id': str(opportunity.id), 'company': opportunity.company, 'position': opportunity.position, 'processes': [{ "date": process.date, "document": process.document.fetch().get_dict_representation(), "type": process.document_type } for process in opportunity.processes]} for opportunity in opportunities]
        return json.dumps(processes)

    elif request.method == "POST":
        request_json = request.get_json()
        applicant = request_json["applicant"]
        company = request_json["company"]
        position = request_json["position"]
       
        error = None
        if not applicant:
            error = "applicant must be defined"
        elif not company:
            error = "company must be defined"
        elif not position:
            error = "position must be defined"

        if error is None:
            # create opportunity
            opportunity = Opportunity(applicant=applicant, company=company, position=position)
            opportunity.save()

            return 'successfully created opportunity'

        return Response(error, 500)

    elif request.method == "DELETE":
        request_json = request.get_json()
        opportunity_id = request_json["id"]

        error = None
        if not opportunity_id:
            error = "opportunity id must be defined"

        if error is None:
            # query Opportunity and delete all associated processes
            opportunity = Opportunity.objects.get(pk=opportunity_id)
            for process in opportunity.processes:
                process.document.fetch().delete()
            opportunity.delete()
            return "opportunity and all processes have been deleted"

        return Request(error, 500)

    return 'you can only create, delete, and query opportunities'


@bp.route("/applications", methods=["POST"])
def apply():
    if request.method == "POST":
        request_json = request.get_json()
        date = request_json["date"]
        opportunity_id = request_json["opportunity_id"]
        status = request_json["status"]

        error = None
        if not date:
            error = "date is required"
        elif not opportunity_id:
            error = "opportunity id is required"
        elif not status:
            error = "status is required"

        if error is None:
            # create application
            application = Application(status=status)
            application.save() 
            # create new process
            opportunity = Opportunity.objects.get(pk=opportunity_id)
            process = Process(date=date, document_type="application", document=application, parent = opportunity)
            opportunity.processes.append(process)
            opportunity.save()

            # update application parent
            application.parent = opportunity
            application.save()
            
            return 'successfully created application'
        return Response(error, 500)

    else:
        return "you can only create applications at this time."

class Application(Document):
    parent = GenericLazyReferenceField()
    status = StringField(required=True)

    def __str__(self):
        return str({"id": self.id, "status": self.status})

    def get_dict_representation(self):
        return {'id': str(self.id), 'status': self.status}


class Process(EmbeddedDocument):
    date = StringField(required=True)
    document = GenericLazyReferenceField(required=True)
    document_type = StringField(required=True)
    parent = GenericLazyReferenceField()

class Opportunity(Document):
    applicant = StringField(required=True)
    company = StringField(required=True)
    description = StringField()
    position = StringField(required=True)
    processes = EmbeddedDocumentListField(document_type=Process)

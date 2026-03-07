from models import db, Part
class PartRepository:
    @staticmethod
    def get_all():
        return Part.query.all()

    @staticmethod
    def get_by_id(part_id):
        return Part.query.get(part_id)

    @staticmethod
    def get_by_part_no(part_no):
        return Part.query.filter_by(PartNo=part_no).first()

    @staticmethod
    def create(part_no, part_desc):
        part = Part(PartNo=part_no, PartDesc=part_desc)
        db.session.add(part)
        db.session.commit()
        return part

    @staticmethod
    def update(part_id, part_no, part_desc):
        part = Part.query.get(part_id)
        if part:
            part.PartNo = part_no
            part.PartDesc = part_desc
            db.session.commit()
        return part

    @staticmethod
    def delete(part_id):
        part = Part.query.get(part_id)
        if part:
            db.session.delete(part)
            db.session.commit()
            return True
        return False

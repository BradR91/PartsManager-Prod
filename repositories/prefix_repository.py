from models import db, PartPrefix
class PrefixRepository:
    @staticmethod
    def get_by_part_id(part_id):
        return PartPrefix.query.filter_by(PartID=part_id).all()

    @staticmethod
    def create(part_id, prefix):
        part_prefix = PartPrefix(PartID=part_id, Prefix=prefix)
        db.session.add(part_prefix)
        db.session.commit()
        return part_prefix

    @staticmethod
    def delete(prefix_id):
        prefix = PartPrefix.query.get(prefix_id)
        if prefix:
            db.session.delete(prefix)
            db.session.commit()
            return True
        return False

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'tblRoles'
    
    ID = db.Column(db.Integer, primary_key=True)
    RoleDesc = db.Column(db.String(50), nullable=False)
    
    users = db.relationship('User', backref='role', lazy=True)


class User(db.Model):
    __tablename__ = 'tblUsers'
    
    ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False, unique=True)
    Password = db.Column(db.String(50), nullable=False)
    RoleID = db.Column(db.Integer, db.ForeignKey('tblRoles.ID'), nullable=False)


class Part(db.Model):
    __tablename__ = 'tblParts'
    
    ID = db.Column(db.Integer, primary_key=True)
    PartNo = db.Column(db.String(50), nullable=False, unique=True)
    PartDesc = db.Column(db.String(200), nullable=False)
    
    prefixes = db.relationship('PartPrefix', backref='part', lazy=True, cascade='all, delete-orphan')


class PartPrefix(db.Model):
    __tablename__ = 'tblPartPrefix'
    
    ID = db.Column(db.Integer, primary_key=True)
    PartID = db.Column(db.Integer, db.ForeignKey('tblParts.ID'), nullable=False)
    Prefix = db.Column(db.String(50), nullable=False)

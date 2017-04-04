from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class Unit(db.Model):
    table = db.Column(db. String(), primary_key=True)
    field = db.Column(db.String(), primary_key=True)
    unit = db.Column(db.String())


class Simulation(db.Model):
    timestamp = db.Column(db.DateTime(timezone=False),
                          primary_key=True)  # datetime object
    globalSolar = db.Column(db.String())
    PVPowerOutput = db.Column(db.Float())  # solar power produced kw
    ACPrimaryLoad = db.Column(db.Float())  # total power consumed kw
    ACPrimaryLoadServed = db.Column(db.Float())
    gridPowerPrice = db.Column(db.Float())
    gridSellbackRate = db.Column(db.Float())
    gridPurchases = db.Column(db.Float())
    gridSales = db.Column(db.Float())
    totalElectricalLoadServed = db.Column(db.Float())
    renewablePresentation = db.Column(db.Float())
    excessElectricalProduction = db.Column(db.Float())
    unmetElectricalLoad = db.Column(db.Float())
    totalRenewablePowerOutput = db.Column(db.Float())
    inverterPowerInput = db.Column(db.Float())
    inverterPowerOutput = db.Column(db.Float())
    ACRequiredOperatingCapacity = db.Column(db.Float())
    DCRequiredOperatingCapacity = db.Column(db.Float())
    ACOperatingCapacity = db.Column(db.Float())
    DCOperatingCapacity = db.Column(db.Float())

    def getRange(start, end, aggregate):
        query = db.select([
            func.max(Simulation.timestamp).label('timestamp'),
            func.sum(Simulation.PVPowerOutput).label('PVPowerOutput'),
            func.sum(Simulation.ACPrimaryLoad).label('ACPrimaryLoad')])
            .where(Simulation.timestamp >= start)\
                .where(Simulation.timestamp <= end)\

        if aggregate == 'hourly':
            # do nothing
            query = query.group_by(Simulation.timestamp)
        elif aggregate == 'daily':
            # group by date
            query = query.group_by(func.date(Simulation.timestamp))
        elif aggregate == 'monthly':
            # group by month
            query = query.group_by(func.date_part(
                'month', Simulation.timestamp))
        else:
            raise ValueError('invalid aggregation')
        return [dict(r) for r in db.session.execute(query).fetchall()]

    def getAverage(start, end):
        query = db.select([
            func.avg(Simulation.PVPowerOutput).label('PVPowerOutputAverage'),
            func.avg(Simulation.ACPrimaryLoad).label('ACPrimaryLoadAverage')
        ]).where(Simulation.timestamp >= start)\
            .where(Simulation.timestamp <= end)
        return dict(db.session.execute(query).fetchone())

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def getSockets(homeId):
        query = db.select([SmartSocket.id, SmartSocket.name])\
            .where(SmartSocket.homeId == homeId)
        return [dict(s) for s in db.session.execute(query).fetchall()]

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Circuit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    homeId = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)

    def getPowerLogs(circuitId):
        query = db.select([PowerConsumption.timestamp, PowerConsumption.power])\
            .where(PowerConsumption.circuitId == circuitId)
        return [dict(l) for l in db.session.execute(query).fetchall()]

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'homeId': self.homeId,
        }


class PowerConsumption(db.Model):
    timestamp = db.Column(db.DateTime(timezone=False),
                          primary_key=True)  # datetime object
    circuitId = db.Column(db.Integer, db.ForeignKey(
        'circuit.id'), nullable=False, primary_key=True)
    power = db.Column(db.Float(), nullable=False)

    def serialize(self):
        return {
            'timestamp': self.timestamp,
            'circuitId': self.circuitId,
            'power': self.power,
        }


class QuestSimulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=False))      # datetime obj
    apartmentNo = db.Column(db.Integer, nullable=False)
    load = db.Column(db.Float)

    def serialize(self):
        return {
            'id': self.id,
            'datetime': self.datetime,
            'apartmentNo': self.apartmentNo,
            'load': self.load
        }


class UnitCost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=False))
    cost = db.Column(db.Float)

    def serialize(self):
        return {
            'id': self.id,
            'datetime': self.datetime,
            'cost': self.cost
        }

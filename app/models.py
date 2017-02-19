from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class Unit(db.Model):
    table = db.Column(db. String(), primary_key=True)
    field = db.Column(db.String(), primary_key=True)
    unit = db.Column(db.String())

class Simulation(db.Model):
    timestamp = db.Column(db.DateTime(timezone=False), primary_key=True) # datetime object
    globalSolar = db.Column(db.String())
    PVPowerOutput = db.Column(db.Float()) # solar power produced kw
    ACPrimaryLoad = db.Column(db.Float()) # total power consumed kw
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
                func.max(Simulation.timestamp), 
                func.sum(Simulation.PVPowerOutput),
                func.sum(Simulation.ACPrimaryLoad)\
            ])\
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
            query = query.group_by(func.date_part('month', Simulation.timestamp))
        else:
            raise ValueError('invalid aggregation')
        return db.session.execute(query).fetchall()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

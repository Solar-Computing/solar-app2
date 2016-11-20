from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Simulation(db.Model):
    date = db.Column(db.DateTime(), primary_key=True) # datetime object
    globalSolar = db.Column(db.String())
    PVPowerOutput = db.Column(db.Float())
    ACPrimaryLoad = db.Column(db.Float())
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

import csv
from app import models
import inspect

class Simulation():
    files = ["migration/2016-homeresults.csv"]

    columns_to_headers = {
        'timestamp'                     :   'End Time',
        'globalSolar'                   :   'Global Solar',
        'PVPowerOutput'                 :   'PV Power Output',
        'ACPrimaryLoad'                 :   'AC Primary Load',
        'ACPrimaryLoadServed'           :   'AC Primary Load Served',
        'gridPowerPrice'                :   'Grid Power Price',
        'gridSellbackRate'              :   'Grid Sellback Rate',
        'gridPurchases'                 :   'Grid Purchases',
        'gridSales'                     :   'Grid Sales',
        'totalElectricalLoadServed'     :   'Total Electrical Load Served',
        'renewablePresentation'         :   'Renewable Penetration',
        'excessElectricalProduction'    :   'Excess Electrical Production',
        'unmetElectricalLoad'           :   'Unmet Electrical Load',
        'totalRenewablePowerOutput'     :   'Total Renewable Power Output',
        'inverterPowerInput'            :   'Inverter Power Input',
        'inverterPowerOutput'           :   'Inverter Power Output',
        'ACRequiredOperatingCapacity'   :   'AC Required Operating Capacity',
        'DCRequiredOperatingCapacity'   :   'DC Required Operating Capacity',
        'ACOperatingCapacity'           :   'AC Operating Capacity',
        'DCOperatingCapacity'           :   'DC Operating Capacity',
    }

def csv_to_table(migration_class, model_class):
    for sim_name in migration_class.files:
        with open(sim_name, 'r') as f:
            # Skip the units row
            next(f)

            reader = csv.DictReader(f)

            for row in reader:
                filtered = {}
                for col, head in migration_class.columns_to_headers.items():
                    filtered[col] = row[head]

                s = models.Simulation(**filtered)



def migrate_homeresults():
    csv_to_table(Simulation, models.Simulation)

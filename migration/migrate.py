import csv
from app import models
import inspect

class Simulation():
    files = ["2016-homeresults.csv"]
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
        'renewablePresentation'         :   'Renewable Presentation',
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

def get_indices(columns, headers, columns_to_headers):
    indices = {}

    for col in columns:
        idx = headers.index(columns_to_headers[col])
        if (idx < 0):
            return None

        indices[col] = idx

    return indices

def csv_to_table(migration_class, model_class):
    # Grab columns from Simulation DB model using reflection
    columns = inspect.getmembers(model_class, lambda a: not inspect.isroutine(a))
    columns = [name for (name, _) in columns if not(name.startswith('__') and name.endswith('__'))]

    for sim_name in migration_class.files:
        with open(sim_name, 'r') as f:
            # Skip the units row
            next(f)

            reader = csv.DictReader(f)

            # Find the indices for all of the relevant columns
            # headers = next(reader)
            # indices = get_indices(columns, headers, Simulation.columns_to_headers)
            # if indices is None:
            #     print("Unrecognized header format for {}.".format(sim_name))
            #     continue

            for row in reader:
                s = models.Simulation()
                for col in columns:
                    setattr(s, col, row[migration_class.columns_to_headers[col]])


csv_to_db(Simulation, models.Simulation)

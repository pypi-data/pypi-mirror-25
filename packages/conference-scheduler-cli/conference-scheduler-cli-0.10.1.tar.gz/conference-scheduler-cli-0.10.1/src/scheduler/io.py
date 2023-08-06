import csv
import pickle
from pathlib import Path
from pprint import pformat

import daiquiri
from conference_scheduler import converter
from ruamel.yaml import YAML
from slugify import slugify

logger = daiquiri.getLogger(__name__)
yaml = YAML(typ='safe')
yaml.default_flow_style = False


def import_yaml(input_folder):
    """Import all yaml files in the given folder into a single resources
    dict"""
    yaml_resources = {}
    yaml_files = [
        path for path in input_folder.iterdir()
        if path.suffix == '.yml']
    for path in yaml_files:
        with path.open('r') as file:
            yaml_resources[path.stem] = yaml.load(file)
    logger.debug(f'\nreources:\n{pformat(yaml_resources)}')
    return yaml_resources


def import_proposals(resources, input_folder):
    """Import the proposals data from a .csv file"""
    proposals = []
    with Path(input_folder, 'proposals.csv').open('r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            event_type = row['session_type']
            proposals.append({
                'title': row['title'],
                'duration': int(row['duration']),
                'demand': float(row.get('demand', 0)),
                'person': slugify(row['name']),
                'name': row['name'],
                'tags': [row['tag']] if row['tag'] != '' else [],
                'subtitle': row['subtitle'],
                'description': row['description'],
                'event_type': event_type})
    logger.debug(f'\nreources:\n{pformat(proposals)}')
    return proposals


def import_solution(solution_folder):
    """Import a previously computed schedule from a .csv file"""
    csv_file = Path(solution_folder, 'schedule.csv')
    logger.info(f'Importing schedule from {csv_file}')
    solution = []
    with Path(csv_file).open('r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            solution.append((
                int(row['event_index']),
                int(row['slot_index'])))
        logger.debug(f'\nreources:\n{pformat(solution)}')
    return solution


def import_schedule_definition(solution_folder):
    """Import previously pickled schedule"""
    pickle_file = Path(solution_folder, 'scheduler.pickle')
    logger.info(
        f'Importing resources, events, slots and schedule from {pickle_file}')
    with pickle_file.open('rb') as f:
        bundle = pickle.load(f)
    return bundle


def pickle_solution_and_definition(
    resources, events, slots, allocations, solution, solution_folder
):
    """Store the computed solution, the resources dict and the associated
    events and slots lists in pickle format"""
    pickle_file = Path(solution_folder, 'scheduler.pickle')
    logger.info(
        f'Pickling resources, events, slots and schedule to {pickle_file}')
    bundle = {
        'resources': resources,
        'events': events,
        'slots': slots,
        'allocations': allocations,
        'solution': solution
    }
    with pickle_file.open('wb') as f:
        pickle.dump(bundle, f, pickle.HIGHEST_PROTOCOL)


def export_schedule(solution, events, slots, solution_folder):
    """Write a human readable .csv file of the computed solution"""
    csv_file = Path(solution_folder, 'schedule.csv')
    logger.info(f'Exporting schedule to {csv_file}')

    schedule = converter.solution_to_schedule(solution, events, slots)
    scheduled_items = [
        {
            'event_index': events.index(item.event),
            'event': f'{item.event.name}',
            'slot_index': slots.index(item.slot),
            'slot': f'{item.slot.starts_at} {item.slot.venue}'
        }
        for item in schedule
    ]
    with csv_file.open('w', newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=['event_index', 'event', 'slot_index', 'slot'])
        writer.writeheader()
        for item in scheduled_items:
            writer.writerow(item)


def export_solution_and_definition(
    resources, events, slots, allocations, solution, solution_folder
):
    solution_folder.mkdir(exist_ok=True)
    pickle_solution_and_definition(
        resources, events, slots, allocations, solution, solution_folder)
    export_schedule(solution, events, slots, solution_folder)

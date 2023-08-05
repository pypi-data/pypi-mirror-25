"""Procedures to define the Command Line Interface (cli)"""
from pathlib import Path

import click
from conference_scheduler.scheduler import event_schedule_difference
from conference_scheduler.converter import solution_to_schedule
from conference_scheduler.validator import (
    is_valid_solution, solution_violations)
import daiquiri

import scheduler.calculate as calc
from scheduler.decorators import timed
import scheduler.define as defn
from scheduler import convert, io, logging, session

logger = daiquiri.getLogger(__name__)


def events_and_slots(resources):
    slots = defn.slots(resources)
    events = defn.events(resources)
    unavailability = defn.unavailability(resources, slots)
    clashes = defn.clashes(resources)
    unsuitability = defn.unsuitability(resources, slots)

    defn.add_unavailability_to_events(events, slots, unavailability)
    defn.add_clashes_to_events(events, clashes)
    defn.add_unsuitability_to_events(events, slots, unsuitability)
    return events, slots


@click.version_option(message='%(prog)s %(version)s :: UK Python Association')
@click.group()
@click.option(
    '--verbosity', '-v', default='info',
    type=click.Choice(['critical', 'error', 'warning', 'info', 'debug']),
    help='Logging verbosity')
def scheduler(verbosity):
    pass


@scheduler.command()
@click.option(
    '--verbosity', '-v', default='info',
    type=click.Choice(['critical', 'error', 'warning', 'info', 'debug']),
    help='Logging verbosity')
@click.option(
    '--algorithm', '-a', default='pulp_cbc_cmd',
    type=click.Choice(
        ['pulp_cbc_cmd', 'glpk', 'hill_climber', 'simulated_annealing']),
    help='Solver algorithm')
@click.option(
    '--objective', '-o', default=None,
    type=click.Choice(['efficiency', 'equity', 'consistency']),
    help='Objective Function')
@click.option('--diff/--no-diff', default=False, help='Show schedule diff')
@click.option(
    '--input_dir', '-i', default=None, help='Directory for input files')
@click.option(
    '--solution_dir', '-s', default=None, help='Directory for solution files')
@click.option(
    '--build_dir', '-b', default=None, help='Directory for output yaml files')
@timed
def build(
    verbosity, algorithm, objective, diff, input_dir, solution_dir, build_dir
):
    logging.setup(verbosity)
    if input_dir:
        session.folders['input'] = Path(input_dir)

    if solution_dir:
        session.folders['solution'] = Path(solution_dir)

    if build_dir:
        session.folders['build'] = Path(build_dir)

    resources = defn.resources()
    events, slots = events_and_slots(resources)

    kwargs = {}
    if objective == 'consistency' or diff:
        original_solution = io.import_solution(session.folders['solution'])
        revised_solution = [
            item for item in original_solution
            if item[0] < len(events)]
        original_schedule = solution_to_schedule(
            revised_solution, events, slots)

    if objective == 'consistency':
        diff = True
        kwargs['original_schedule'] = original_schedule

    solution = calc.solution(events, slots, algorithm, objective, **kwargs)

    if diff:
        schedule = solution_to_schedule(solution, events, slots)
        event_diff = event_schedule_difference(original_schedule, schedule)
        logger.debug(f'\nevent_diff:')
        for item in event_diff:
            logger.debug(f'{item.event.name} has moved from {item.old_slot.venue} at {item.old_slot.starts_at} to {item.new_slot.venue} at {item.new_slot.starts_at}')

    if solution is not None:
        allocations = defn.allocations(resources)
        defn.add_allocations(events, slots, solution, allocations)
        logger.debug(convert.schedule_to_text(solution, events, slots))
        io.export_solution_and_definition(
            resources, events, slots, solution, session.folders['solution'])
        io.build_output(
            resources, events, slots, solution, session.folders['build'])


@scheduler.command()
@click.option(
    '--verbosity', '-v', default='info',
    type=click.Choice(['critical', 'error', 'warning', 'info', 'debug']),
    help='Logging verbosity')
@click.option(
    '--input_dir', '-i', default=None, help='Directory for input files')
@click.option(
    '--solution_dir', '-s', default=None, help='Directory for solution files')
@click.option(
    '--reload/--no-reload', default=False, help='Reload YAML definition')
@timed
def validate(verbosity, input_dir, solution_dir, reload):
    logging.setup(verbosity)
    if solution_dir:
        session.folders['solution'] = Path(solution_dir)

    solution = io.import_solution(session.folders['solution'])

    if reload:
        resources = defn.resources()
        events, slots = events_and_slots(resources)
        original_solution = io.import_solution(session.folders['solution'])
        solution = [
            item for item in original_solution
            if item[0] < len(events)]
    else:
        solution = io.import_solution(session.folders['solution'])
        definition = io.import_schedule_definition(session.folders['solution'])
        events = definition['events']
        slots = definition['slots']

    logger.info('Validating schedule...')
    if is_valid_solution(solution, events, slots):
        logger.info('Imported solution is valid')
    else:
        for v in solution_violations(
                solution, definition['events'], definition['slots']):
            logger.error(v)


@scheduler.command()
@click.option(
    '--verbosity', '-v', default='info',
    type=click.Choice(['critical', 'error', 'warning', 'info', 'debug']),
    help='Logging verbosity')
@click.option(
    '--solution_dir', '-s', default=None, help='Directory for solution files')
@click.option(
    '--build_dir', '-b', default=None, help='Directory for output yaml files')
@timed
def rebuild(verbosity, solution_dir, build_dir):
    logging.setup(verbosity)
    if solution_dir:
        session.folders['solution'] = Path(solution_dir)

    if build_dir:
        session.folders['build'] = Path(build_dir)

    solution = io.import_solution(session.folders['solution'])
    definition = io.import_schedule_definition(session.folders['solution'])
    logger.info('Validating schedule...')
    if is_valid_solution(solution, definition['events'], definition['slots']):
        logger.info('Imported solution is valid')
        io.build_output(
            definition['resources'], definition['events'],
            definition['slots'], solution, session.folders['build'])
    else:
        for v in solution_violations(
                solution, definition['events'], definition['slots']):
            logger.error(v)

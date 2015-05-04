#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Common abbreviations to help reduce the text message length.
# Todo: Should probably move these to collections to preserve ordering
ABBREVIATIONS = {
    'minutes': 'min',
    'seconds': 'sec',
    'meters': 'm',
    'Chest-to-Bar': 'CTB',
    'Chest to Bar': 'CTB',
    'Pull-Ups': 'PU',
    'Pull Ups': 'PU',
    'as many rounds and reps as possible': 'AMRAP',
    'as many rounds as possible': 'AMRAP',
    'as many reps as possible': 'AMRAP',
    'back squat': 'BS',
    'hang squat clean': 'HSC',
    'hang clean': 'HC',
    'clean and jerk': 'C&J',
    'every minute on the minute': 'EMOM',
    'front squat': 'FS',
    'hand stand push up': 'HSPU',
    'knees to elbow': 'KTE',
    'muscle ups': 'MU',
    'overhead squat': 'OHS',
    'power clean': 'PC',
    'push press': 'PP',
    'push-press': 'PP',
    'push jerk': 'PJ',
    'power snatch': 'PSN',
    'squat clean': 'SC',
    'sumo deadlift high pull': 'SDHP',
    'toes to bar': 'TTB',
    'push-ups': 'PU',
    'snatch': 'SN',
    'squat': 'SQ',
    'kettlebell': 'KB',
    'clean': 'CLN',
    'deadlift': 'DL',
    ' one': ' 1',
    ' two': ' 2',
    ' three': ' 3',
    ' four': ' 4',
    ' five': ' 5',
    'rounds for time of': 'RFT',
    'rounds for time': 'RFT',
    'alternating': 'alt',
    'sit-ups': 'SU',
    'Sit-Ups': 'SU',
    'Double-Unders': 'DU',
    }

# This is ugly. I should do this better.
# Todo: Actually learn about encoding.
SPECIAL_CHARS = {
    '’': "'",
    '‘': "'",
    '“': '"',
    '”': '"',
    '…': '...',
    '\xc2\xa0' : ' ',
    }

# Possible headers
# Todo: Should probably move these to collections to preserve ordering
HEADERS = {
    'Open Workout:': 'Experienced Workout:',
    'Experienced Level:': 'Open Level:',
    'Experienced/Open': None,
    'Workout:': None,
    }

# List of positive reinforcement salutations
SALUTATIONS = [
    'Nice work!',
    'Boom!',
    'Not too shabby!'
    ]

# List of available commands
COMMANDS = {
    '1': ['Subscribe','Receive the daily workout every morning.'],
    '2': ['Stop','Quit receiving the daily workout every morning.'],
    '3': ['WOD','Get today\'s workout.'],
    '4': ['+ [result]','Log your result from today\'s workout. e.g. "+ 4 rounds"'],
    '5': ['[activity]: [result]','Log a PR for a movement or activity. e.g. "Clean 1RM: 135lbs"'],
    '6': ['? [activity]','Search your PRs for an activity or movement. e.g. "Clean 1RM"'],
    '7': ['Tip: [your feedback]','Give feedback on how to make the app better.'],
    }

# List of reserved words
RESERVED_WORDS = [
    'subscribe',
    'stop',
    'wod',
    ]

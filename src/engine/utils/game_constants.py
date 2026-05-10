from __future__ import annotations

from engine.comps.color_enums import PlayerColor, TrainColor


INITIAL_TRAIN_CARDS = 4
INITIAL_DESTINATION_TICKETS = 3

PLAYER_COLORS = (
    PlayerColor.RED,
    PlayerColor.BLUE,
    PlayerColor.GREEN,
    PlayerColor.YELLOW,
    PlayerColor.BLACK,
)

TRAIN_CARD_COUNTS = {
    TrainColor.RED: 12,
    TrainColor.BLUE: 12,
    TrainColor.GREEN: 12,
    TrainColor.YELLOW: 12,
    TrainColor.BLACK: 12,
    TrainColor.WHITE: 12,
    TrainColor.ORANGE: 12,
    TrainColor.PINK: 12,
    TrainColor.WILD: 14,
}

CITY_NAMES = (
    "Regent's Park",
    "King's Cross",
    "Brick Lane",
    "Baker Street",
    "British Museum",
    "The Charterhouse",
    "St Paul's",
    "Tower of London",
    "Piccadilly Circus",
    "Covent Garden",
    "Trafalgar Square",
    "Waterloo",
    "Globe Theatre",
    "Elephant & Castle",
    "Hyde Park",
    "Buckingham Palace",
    "Big Ben",
)

ROUTE_DATA = (
    ("Regent's Park", "Baker Street", TrainColor.BLUE, 2),
    ("Regent's Park", "King's Cross", TrainColor.GREEN, 5),
    ("Regent's Park", "British Museum", TrainColor.YELLOW, 4),
    ("King's Cross", "The Charterhouse", TrainColor.WHITE, 4),
    ("King's Cross", "British Museum", TrainColor.BLACK, 2),
    ("Baker Street", "British Museum", TrainColor.RED, 4),
    ("Baker Street", "Piccadilly Circus", TrainColor.WHITE, 4),
    ("Baker Street", "Hyde Park", TrainColor.BLACK, 4),
    ("British Museum", "The Charterhouse", TrainColor.BLUE, 5),
    ("British Museum", "Piccadilly Circus", TrainColor.WHITE, 2),
    ("British Museum", "Covent Garden", TrainColor.RED, 1),
    ("The Charterhouse", "Brick Lane", TrainColor.GREEN, 4),
    ("The Charterhouse", "St Paul's", TrainColor.WHITE, 1),
    ("Brick Lane", "Tower of London", TrainColor.BLUE, 4),
    ("St Paul's", "Tower of London", TrainColor.ORANGE, 4),
    ("St Paul's", "Tower of London", TrainColor.PINK, 4),
    ("Covent Garden", "St Paul's", TrainColor.GRAY, 4),
    ("Covent Garden", "St Paul's", TrainColor.RED, 4),
    ("Covent Garden", "Trafalgar Square", TrainColor.BLACK, 2),
    ("Covent Garden", "Trafalgar Square", TrainColor.PINK, 2),
    ("Piccadilly Circus", "Covent Garden", TrainColor.GREEN, 2),
    ("Piccadilly Circus", "Covent Garden", TrainColor.YELLOW, 2),
    ("Piccadilly Circus", "Trafalgar Square", TrainColor.BLUE, 2),
    ("Piccadilly Circus", "Trafalgar Square", TrainColor.ORANGE, 2),
    ("Piccadilly Circus", "Hyde Park", TrainColor.WHITE, 2),
    ("Piccadilly Circus", "Buckingham Palace", TrainColor.PINK, 3),
    ("Hyde Park", "Buckingham Palace", TrainColor.ORANGE, 2),
    ("Hyde Park", "Buckingham Palace", TrainColor.YELLOW, 2),
    ("Buckingham Palace", "Trafalgar Square", TrainColor.WHITE, 3),
    ("Buckingham Palace", "Big Ben", TrainColor.GREEN, 3),
    ("Buckingham Palace", "Waterloo", TrainColor.GRAY, 4),
    ("Trafalgar Square", "Big Ben", TrainColor.RED, 2),
    ("Trafalgar Square", "Waterloo", TrainColor.GRAY, 3),
    ("Big Ben", "Waterloo", TrainColor.ORANGE, 3),
    ("Big Ben", "Elephant & Castle", TrainColor.YELLOW, 4),
    ("Waterloo", "Globe Theatre", TrainColor.PINK, 3),
    ("Globe Theatre", "St Paul's", TrainColor.WHITE, 2),
    ("Globe Theatre", "Elephant & Castle", TrainColor.GRAY, 3),
    ("Tower of London", "Globe Theatre", TrainColor.WHITE, 2),
    ("Tower of London", "Elephant & Castle", TrainColor.BLACK, 4),
)

DESTINATION_TICKET_DATA = (
    ("Regent's Park", "Big Ben", 5),
    ("Regent's Park", "Elephant & Castle", 7),
    ("King's Cross", "Buckingham Palace", 5),
    ("King's Cross", "Tower of London", 5),
    ("Brick Lane", "Hyde Park", 8),
    ("Brick Lane", "Buckingham Palace", 8),
    ("Baker Street", "Tower of London", 6),
    ("Baker Street", "Globe Theatre", 6),
    ("British Museum", "Elephant & Castle", 6),
    ("The Charterhouse", "Hyde Park", 7),
    ("The Charterhouse", "Big Ben", 4),
    ("St Paul's", "Hyde Park", 6),
    ("Tower of London", "Buckingham Palace", 6),
    ("Piccadilly Circus", "Brick Lane", 7),
    ("Piccadilly Circus", "Elephant & Castle", 5),
    ("Covent Garden", "King's Cross", 4),
    ("Waterloo", "Baker Street", 5),
    ("Waterloo", "Brick Lane", 6),
    ("Globe Theatre", "Regent's Park", 7),
    ("Hyde Park", "St Paul's", 6),
)
# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 29/02/2021
### Added
`utils.parse_delta`: Parsing time differences to deltas.

### Fixed
Using `timedelta` and `datetime` instead of raw strings.

## [0.1.0] - 28/02/2021
### Added

- `Endgame` class.
- Flag submission for `Endgame`s, `Challenge`s and `Machine`s.

### Development

- Reduced test times by removing extraneous logins.
- Added a mock API for testing sensitive functionality like flag submission.

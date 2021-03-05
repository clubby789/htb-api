# Changelog

All notable changes to this project will be documented in this file.

## [0.4.1] 05/03/2021
### Fixed
- Ratelimited challenge downloads to 1 per 30 seconds

## [0.4.0] 05/03/2021
### Added
- Added the ability to download challenges (with a download available)

## [0.3.1] 03/03/2021
### Fixed
- Handle the API returning invalid search results

## [0.3.0] 01/03/2021
### Added
- The ability to spawn and kill challenge Docker instances.

### Development
- Dynamically set the port used by the mock API to prevent random conflicts.

## [0.2.1] 01/03/2021
### Added
- More informative error messages

### Fixed
- A bug where incorrect refresh tokens were loaded, meaning expired access tokens could not be refreshed.

### Development
- 100% test coverage!

## [0.2.0] 01/03/2021
### Added
- Retrieving authors of a challenge
- Fortresses, and submitting flags for them
- Search feature

### Fixed
- Indexed new classes in documentation
- Use consistent names for attributes between Challenges and Machines

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

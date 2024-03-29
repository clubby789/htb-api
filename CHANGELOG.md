# Changelog

All notable changes to this project will be documented in this file.

## [0.5.6] 07/03/222
### Added
- A more comprehensive `Content` object to retrieve a user's created content
- The ability to reset machines
- Exceptions to handle problems during VPN switches
### Fixed
- Made the return value more consistent with Release Arena

## [0.5.5] 27/02/222
### Added
- App tokens, allowing use of the API without credentials/OTP
- Retrieving your 'to-do list' of machines
### Development
- Improved test coverage

## [0.5.4] 21/02/222
### Fixed
- Improved loading speed of machine IPs
### Development
- Bumped dependency versions

## [0.5.3] 13/02/2022
### Added
- Add the 'remember me' option for long-lasting refresh tokens
### Fixed
- Correctly handle a failure to refresh authentication

## [0.5.2] 22/11/2021
### Fixed
- Use the correct API endpoint for retrieving the current VPN server

## [0.5.1] 27/10/2021
### Fixed
- Move to the new 'hackthebox.com' domain

## [0.5.0] 26/10/2021
### Added
- Caching mechanism ([docs](https://pyhackthebox.readthedocs.io/en/latest/htb.html))
- Automatic prompting for details
### Fixed
- Handling some unusual API responses

## [0.4.4] 24/10/2021
### Added
- Added the ability to spawn machines (both release arena and not)
- Added retrieving a machine's IP

## [0.4.3] 24/10/2021
### Fixed
- The API can return improperly padded base64 tokens. Manually pad them for some internal logic.

## [0.4.2] 23/10/2021
### Added
- Added the ability to list VPN servers
- Added the ability to switch between and download VPN packs

### Development
- Fully mock the API for unit testing

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

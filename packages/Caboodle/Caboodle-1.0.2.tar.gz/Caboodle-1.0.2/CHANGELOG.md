# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [1.0.2]
### Fixed
- An inconsistency with a utility function where it did not always return a JPG

## [1.0.1]
### Fixed
- A bug with a utility function with images containing an alpha channel

## 1.0.0
### Changed
- Usability of module (see alpha and beta version)

## 1.0.0-B3 - Update d3cryp7 Agent
### Changed
- d3cryp7 library to reflect the new version
- d3cryp7 Agent to use the new features

## 1.0.0-B2 - Fix reCAPTCHA Challenge
### Fixed
- Algorithm for reCAPTCHA Challenge

## 1.0.0-B1 - Solve Media Agents
### Added
- Solve Media Video challenge
- Solve Media Embed challenge
- Solve Media Reveal challenge
- Challenge utility functions
- pyscreenshot dependency

## 1.0.0-A3 - d3cryp7 Agent
### Added
- d3cryp7 agent

## 1.0.0-A2 - New Agents and Challenges
### Added
- ruCAPTCHA agent
- reCAPTCHA challenge

## 1.0.0-A1 - Redesign
### Added
- Challenges
- Agents

### Changed
- Solving algorithm

### Removed
- Support for web browsers other than Firefox
- Local solving with Tesseract

## [0.2.0] - CAPTCHA Solving
### Added
- Automatic or manual CAPTCHA solving

## [0.2.0-RC6] - Solve Media Bar
### Added
- Supports Solve Media bar CAPTCHAs

## [0.2.0-RC5] - Solve Media Video
### Added
- Supports Solve Media video CAPTCHAs

## [0.2.0-RC4] - Solve Media Reveal
### Added
- Supports Solve Media reveal CAPTCHAs

## [0.2.0-RC3] - Base64 Encoding
### Changed
- Solving functions use base64 encoded images

## [0.2.0-RC2] - reCAPTCHA Solving
### Added
- Supports reCAPTCHA

## [0.2.0-RC1] - CAPTCHA Solving
### Added
- `Solve` module with support for OCR, online and manual solving
- Supports Solve Media

## [0.1.3] - Action Chains
### Added
- Function `action()`

## [0.1.2] - Proxies
### Added
- Optional parameter `proxy` for connecting through a proxy

## [0.1.1] - Handle timeout
### Added
- Function `get(url)`

## [0.1.0] - Selenium
### Added
- Web module
- Browser class
- Example in README

[1.0.2]: https://bitbucket.org/bkvaluemeal/caboodle/issues/7/get_image_src-should-return-a-jpg
[1.0.1]: https://bitbucket.org/bkvaluemeal/caboodle/issues/6/get_element_image-does-not-handle-images
[0.2.0]: https://bitbucket.org/bkvaluemeal/caboodle/issues/5/captcha-solving
[0.2.0-RC6]: https://bitbucket.org/bkvaluemeal/caboodle/issues/5/captcha-solving
[0.2.0-RC5]: https://bitbucket.org/bkvaluemeal/caboodle/issues/5/captcha-solving
[0.2.0-RC4]: https://bitbucket.org/bkvaluemeal/caboodle/issues/5/captcha-solving
[0.2.0-RC3]: https://bitbucket.org/bkvaluemeal/caboodle/issues/5/captcha-solving
[0.2.0-RC2]: https://bitbucket.org/bkvaluemeal/caboodle/issues/5/captcha-solving
[0.2.0-RC1]: https://bitbucket.org/bkvaluemeal/caboodle/issues/5/captcha-solving
[0.1.3]: https://bitbucket.org/bkvaluemeal/caboodle/issues/4/action-chains
[0.1.2]: https://bitbucket.org/bkvaluemeal/caboodle/issues/3/proxies
[0.1.1]: https://bitbucket.org/bkvaluemeal/caboodle/issues/2/handle-timeout
[0.1.0]: https://bitbucket.org/bkvaluemeal/caboodle/issues/1/selenium

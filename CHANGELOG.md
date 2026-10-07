# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file was started on September 04, 2023. Changes prior to this date are not included in the CHANGELOG.

## [v0.20261007.0] - 2026-10-07

### Dependencies
- typer 0.27.0 → 0.27.2 (osism/openstack-flavor-manager#188, osism/openstack-flavor-manager#189)
- openstacksdk 4.17.0 → 4.20.0 (osism/openstack-flavor-manager#187)

## [v0.20260722.0] - 2026-07-22

### Fixed
- Fix project-board automation failing on fork PRs by switching to `pull_request_target` and scoping the automation to only the `ADD_TO_PROJECT_PAT` secret (osism/openstack-flavor-manager#184)
- Mock network requests in flavor definitions test to prevent CI failures from GitHub rate limiting (osism/openstack-flavor-manager#185)

### Dependencies
- typer 0.26.6 → 0.26.8 (osism/openstack-flavor-manager#183)
- typer 0.26.8 → 0.27.0 (osism/openstack-flavor-manager#186)
- openstacksdk 4.10.0 → 4.17.0 (osism/openstack-flavor-manager#175)

## [v0.20260614.0] - 2026-06-14

### Added
- Add workflow to automatically add opened issues and PRs to project board (osism/openstack-flavor-manager#177)

### Dependencies
- requests 2.32.5 → 2.34.2 (osism/openstack-flavor-manager#174)
- typer 0.24.1 → 0.26.6 (osism/openstack-flavor-manager#176, osism/openstack-flavor-manager#179, osism/openstack-flavor-manager#180, osism/openstack-flavor-manager#181, osism/openstack-flavor-manager#182)

## [v0.20260227.0] - 2026-02-27

### Added
- Add missing SCS-4V-16-100s flavor to flavors.yaml (osism/openstack-flavor-manager#171)

### Fixed
- Fix wrong scs:name-v1/v2 for SCS-1L-1-5 flavor (osism/openstack-flavor-manager#172)
- Change hw_rng:allowed value from lowercase true to True in flavors.yaml (osism/openstack-flavor-manager#173)

### Dependencies
- typer 0.21.1 → 0.24.1 (osism/openstack-flavor-manager#167, osism/openstack-flavor-manager#168, osism/openstack-flavor-manager#170)
- openstacksdk 4.9.0 → 4.10.0 (osism/openstack-flavor-manager#169)

## [v0.20260127.0] - 2026-01-27

### Dependencies
- typer 0.20.0 → 0.21.1 (osism/openstack-flavor-manager#165)
- openstacksdk 4.8.0 → 4.9.0 (osism/openstack-flavor-manager#166)

## [v0.20251128.0] - 2025-11-28

### Dependencies
- requests-file 2.1.0 → 3.0.1 (osism/openstack-flavor-manager#160)
- openstacksdk 4.7.1 → 4.8.0 (osism/openstack-flavor-manager#164)

## [v0.20251101.0] - 2025-11-01

### Fixed
- Fix source type of cloudpod flavors (osism/openstack-flavor-manager#163)

## [v0.20251021.0] - 2025-10-21

### Dependencies
- pyyaml 6.0.2 → 6.0.3 (osism/openstack-flavor-manager#159)
- typer 0.19.2 → 0.20.0 (osism/openstack-flavor-manager#162)

## [v0.20251017.0] - 2025-10-17

### Added
- Add cloudpod flavor type (osism/openstack-flavor-manager#161)

### Dependencies
- typer 0.17.4 → 0.19.2 (osism/openstack-flavor-manager#158)

## [v0.20250918.0] - 2025-09-18

### Fixed
- Prevent crash when the `recommended` section is missing from flavor definitions while using the `--recommended` flag; now logs a warning and falls back to mandatory flavors (osism/openstack-flavor-manager#157)

## [v0.20250912.0] - 2025-09-12

### Changed
- Add note to flavors.yaml pointing to the SCS standards repository (osism/openstack-flavor-manager#155)

### Dependencies
- typer 0.17.3 → 0.17.4 (osism/openstack-flavor-manager#153)
- openstacksdk 4.7.0 → 4.7.1 (osism/openstack-flavor-manager#156)

## [v0.20250902.0] - 2025-09-02

### Added
- Add `--limit-memory` parameter to filter recommended flavors by RAM (osism/openstack-flavor-manager#147)

### Changed
- zuul: refresh secret (osism/openstack-flavor-manager#151)

### Dependencies
- typer 0.16.1 → 0.17.3 (osism/openstack-flavor-manager#152)

## [v0.20250827.0] - 2025-08-27

### Dependencies
- openstacksdk 4.5.0 → 4.6.0 (osism/openstack-flavor-manager#143)
- openstacksdk 4.6.0 → 4.7.0 (osism/openstack-flavor-manager#148)
- requests 2.32.3 → 2.32.4 (osism/openstack-flavor-manager#145)
- requests 2.32.4 → 2.32.5 (osism/openstack-flavor-manager#149)
- typer 0.15.2 → 0.15.3 (osism/openstack-flavor-manager#140)
- typer 0.15.3 → 0.15.4 (osism/openstack-flavor-manager#141)
- typer 0.15.4 → 0.16.0 (osism/openstack-flavor-manager#142)
- typer 0.16.0 → 0.16.1 (osism/openstack-flavor-manager#150)

## [v0.20250413.0] - 2025-04-13

### Dependencies
- openstacksdk 4.4.0 → 4.5.0 (osism/openstack-flavor-manager#139)

## [v0.20250314.0] - 2025-03-14

### Dependencies
- openstacksdk 4.2.0 → 4.3.0 (osism/openstack-flavor-manager#135)
- openstacksdk 4.3.0 → 4.4.0 (osism/openstack-flavor-manager#136)
- typer 0.15.1 → 0.15.2 (osism/openstack-flavor-manager#137, osism/openstack-flavor-manager#138)

## [v0.20241216.0] - 2024-12-16

### Dependencies
- openstacksdk 4.1.0 → 4.2.0 (osism/openstack-flavor-manager#134)

## [v0.20241213.0] - 2024-12-13

### Dependencies
- loguru 0.7.2 → 0.7.3 (osism/openstack-flavor-manager#133)

## [v0.20241206.0] - 2024-12-06

### Dependencies
- openstacksdk 4.0.0 → 4.1.0 (osism/openstack-flavor-manager#129)
- typer 0.12.5 → 0.14.0 (osism/openstack-flavor-manager#130)
- typer 0.14.0 → 0.15.0 (osism/openstack-flavor-manager#131)
- typer 0.15.0 → 0.15.1 (osism/openstack-flavor-manager#132)

## [v0.20240904.0] - 2024-09-04

### Dependencies
- openstacksdk 3.3.0 → 4.0.0 (osism/openstack-flavor-manager#128)

## [v0.20240828.0] - 2024-08-28

### Dependencies
- typer 0.12.3 → 0.12.5 (osism/openstack-flavor-manager#126, osism/openstack-flavor-manager#127)

## [v0.20240812.1] - 2024-08-12

### Added
- Add `--url` parameter to use custom local and remote URLs for flavor definitions (osism/openstack-flavor-manager#125)

## [v0.20240812.0] - 2024-08-12

### Fixed
- Fix documentation URL in README (osism/openstack-flavor-manager#122)

### Dependencies
- openstacksdk 3.2.0 → 3.3.0 (osism/openstack-flavor-manager#121)
- pyyaml 6.0.1 → 6.0.2 (osism/openstack-flavor-manager#123)

## [v0.20240708.0] - 2024-07-08

### Fixed
- Fix FileAdapter mounting so local file URLs are loaded correctly and adapt unit tests accordingly (osism/openstack-flavor-manager#120)

### Removed
- Remove release notes management, now handled centrally in osism/release and osism/osism.github.io (osism/openstack-flavor-manager#117)

### Dependencies
- requests-file 2.0.0 → 2.1.0 (osism/openstack-flavor-manager#116)
- requests 2.31.0 → 2.32.3 (osism/openstack-flavor-manager#115, osism/openstack-flavor-manager#118)
- openstacksdk 3.1.0 → 3.2.0 (osism/openstack-flavor-manager#119)

## [v0.20240503.0] - 2024-05-03

### Added
- Add integration test (osism/openstack-flavor-manager#88)
- Add support for loading flavor definitions from a local file (osism/openstack-flavor-manager#114)

### Changed
- Increase timeout for the Devstack deployment in the integration test (osism/openstack-flavor-manager#113)

### Dependencies
- openstacksdk 3.0.0 → 3.1.0 (osism/openstack-flavor-manager#112)
- requests-file → 2.0.0 (osism/openstack-flavor-manager#114)

## [v0.20240411.0] - 2024-04-11

### Added
- Add scs:name-v1 & scs:name-v2 extra specs (osism/openstack-flavor-manager#111)

### Dependencies
- typer 0.11.0 → 0.12.3 (osism/openstack-flavor-manager#107, osism/openstack-flavor-manager#108, osism/openstack-flavor-manager#109, osism/openstack-flavor-manager#110)

## [v0.20240327.0] - 2024-03-27

### Added
- Add historical requirements documentation incorporated from the older repository (osism/openstack-flavor-manager#101)

### Changed
- Update documentation link from osism.github.io to osism.tech (osism/openstack-flavor-manager#102)

### Fixed
- Restore compatibility with Python 3 versions older than 3.10 (osism/openstack-flavor-manager#103)

### Dependencies
- typer 0.9.0 → 0.11.0 (osism/openstack-flavor-manager#104, osism/openstack-flavor-manager#105, osism/openstack-flavor-manager#106)

## [v0.20240318.0] - 2024-03-18

### Changed
- Do not pin the Python version in the Pipfile (osism/openstack-flavor-manager#100)

### Dependencies
- openstacksdk 2.1.0 → 3.0.0 (osism/openstack-flavor-manager#99)

## [v0.20240211.0] - 2024-02-11

### Changed
- Update unit tests to comply with 159588d8b2dae62f4ec474a9fb1371419ffb66a6 (osism/openstack-flavor-manager#97)

### Removed
- Remove local_storage extra spec in favor of scs:disk0-type extra spec (osism/openstack-flavor-manager#96)

### Dependencies
- openstacksdk 2.0.0 → 2.1.0 (osism/openstack-flavor-manager#98)

## [v0.20231219.0] - 2023-12-19

### Added
- Add SPDX license header to source files (osism/openstack-flavor-manager#87)
- Add `scs:cpu-type` extra spec to all mandatory flavors (osism/openstack-flavor-manager#89)
- Add flavors with local storage and `local_storage` extra spec to all flavors (osism/openstack-flavor-manager#90)
- Add `hw_rng:allowed` extra spec to all flavors (osism/openstack-flavor-manager#91)
- Add `scs:disk0-type` extra spec to all flavors (osism/openstack-flavor-manager#95)

### Changed
- Add documentation badge and update documentation link in README (osism/openstack-flavor-manager#86)
- Update extra specs on existing flavors instead of skipping them (osism/openstack-flavor-manager#93)

### Fixed
- Apply `local_storage` extra spec which was previously not set on flavors (osism/openstack-flavor-manager#92)
- Change extra spec values to strings since OpenStack only accepts strings or integers (osism/openstack-flavor-manager#94)

## [v0.4.0] - 2023-11-21

### Added
- Add support for setting extra_specs according to flavor_spec and specifying a custom flavor id (osism/openstack-flavor-manager#84, osism/openstack-flavor-manager#85)

### Changed
- Add python-black Zuul job and reformat Python files with black (osism/openstack-flavor-manager#83)

## [v0.3.0] - 2023-10-20

### Changed
- Reimplement unit and integration tests to work directly with main.py (osism/openstack-flavor-manager#78)
- Update README usage examples with corrected shell commands (osism/openstack-flavor-manager#77)
- Simplify README by removing the usage section and updating the documentation link (osism/openstack-flavor-manager#80)

### Fixed
- Raise an error for unsupported flavor definition names instead of failing with an undefined variable (osism/openstack-flavor-manager#78)
- Fix cloud name and auth URL in sample clouds.yml and secure.yml files (osism/openstack-flavor-manager#81)

### Dependencies
- openstacksdk 1.5.0 → 2.0.0 (osism/openstack-flavor-manager#82)

## [v0.2.0] - 2023-09-19

### Added
- Add default values for disk (0) and public (true) flavor specs when not explicitly set (osism/openstack-flavor-manager#74)

### Changed
- Improve logging for existing, created and failed flavor handling (osism/openstack-flavor-manager#74)
- Refactor CLI entrypoint by splitting run() logic out of main() (osism/openstack-flavor-manager#74)

### Removed
- Remove description field support when creating flavors (osism/openstack-flavor-manager#74)

## [v0.1.1] - 2023-09-19

### Changed
- Consolidate the cloud, ensure, and reference modules into a single main.py and switch logging from the standard library to loguru (osism/openstack-flavor-manager#73)
- Rename CLI parameters, replacing the url argument with a --name option supporting scs and osism presets and changing the default cloud name (osism/openstack-flavor-manager#73)

### Dependencies
- loguru → 0.7.2 (osism/openstack-flavor-manager#73)

## [v0.1.0] - 2023-09-19

### Changed
- Flavor spec boolean values must now be actual booleans instead of string representations like 'true'/'false' (osism/openstack-flavor-manager#70)
- Rename `--cloud-backend` CLI option to `--cloud` (osism/openstack-flavor-manager#59)

## [v0.0.4] - 2023-09-18

### Changed
- Migrate to shared Zuul publish-pypi-package job and configure publish secret passthrough and twine executable (osism/openstack-flavor-manager#69, osism/openstack-flavor-manager#71, osism/openstack-flavor-manager#72)

## [v0.0.3] - 2023-09-06

### Added
- Add build and publish job to Zuul CI pipeline (osism/openstack-flavor-manager#52)

### Changed
- Improve recommended option description and update README with badges and documentation link (osism/openstack-flavor-manager#52)

### Fixed
- Fix secret handling, typos, environment variables, and repository URL in the Zuul publish pipeline (osism/openstack-flavor-manager#61, osism/openstack-flavor-manager#62, osism/openstack-flavor-manager#63, osism/openstack-flavor-manager#64, osism/openstack-flavor-manager#65, osism/openstack-flavor-manager#66, osism/openstack-flavor-manager#67, osism/openstack-flavor-manager#68)

### Removed
- Remove GitHub workflow in favor of Zuul publishing pipeline (osism/openstack-flavor-manager#60)

## [v0.0.2] - 2023-09-04

### Changed
- Pin dependency versions in Pipfile and requirements.txt for reproducible builds, and move munch to a separate test-requirements.txt (osism/openstack-flavor-manager#58)

## [v0.0.1] - 2023-09-04

### Added
- Initial implementation of the OpenStack flavor manager (osism/openstack-flavor-manager@b10fef8)
- Make the flavor manager functional to create OpenStack flavors from a yaml file (osism/openstack-flavor-manager#9)
- Add recommended option for SCS standard v3 (osism/openstack-flavor-manager#11)
- Add Renovate configuration for automated dependency updates (osism/openstack-flavor-manager#25)
- Add CLI option to enable debug logging (osism/openstack-flavor-manager#31)
- Add GitHub workflows for style and type checking (osism/openstack-flavor-manager#33)
- Add Pipfile with package dependencies and Python version requirement (osism/openstack-flavor-manager#38)
- Add --recommended CLI option to install recommended flavors (osism/openstack-flavor-manager#45)
- Add unit and integration test suite (osism/openstack-flavor-manager#39)
- Add example clouds.yml.sample and secure.yml.sample configuration files (osism/openstack-flavor-manager#47, osism/openstack-flavor-manager#49)
- Add description field to created flavors (osism/openstack-flavor-manager#48)
- Add tox configuration and CI job for running the test suite (osism/openstack-flavor-manager#50)
- Add pyproject.toml to support packaged releases (osism/openstack-flavor-manager#55)
- Add GitHub Actions workflow to publish releases to PyPI (osism/openstack-flavor-manager#57)

### Changed
- Refactor syntax check to use flake8 via zuul instead of tox (osism/openstack-flavor-manager#8)
- Add periodic-daily jobs in zuul (osism/openstack-flavor-manager#10)
- Use SCS v2 flavors (osism/openstack-flavor-manager#13)
- Refactor codebase into openstack_flavor_manager package, remove dead code, and add Python gitignore file (osism/openstack-flavor-manager#24)
- Remove unused url parameter from Ensure class (osism/openstack-flavor-manager#35)
- Update README with corrected usage examples and the --recommended option (osism/openstack-flavor-manager#47)
- Move scs_flavor_generator to contrib (osism/openstack-flavor-manager#56)

### Fixed
- Fix typo in scs_flavor_generator.py (osism/openstack-flavor-manager#4)
- Fix typo in backend name check (osism/openstack-flavor-manager#12)
- Fix undefined reference to self.cloud and use empty dict as placeholder for extra_specs (osism/openstack-flavor-manager#21)
- Make the ensure subcommand explicit and necessary (osism/openstack-flavor-manager#22)
- Fix incorrect handling of flavor spec defaults (osism/openstack-flavor-manager#23)
- Prevent script errors when flavors already exist, fix missing return statement in reference loading, and ignore IDE files in git (osism/openstack-flavor-manager#28)
- Fix type error in flavor generator (osism/openstack-flavor-manager#33)
- Fix imports to use fully qualified module paths (osism/openstack-flavor-manager#39)
- Fix inconsistent interpretation of boolean values given as strings (osism/openstack-flavor-manager#46)

### Removed
- Remove __pycache__ directory from repository (osism/openstack-flavor-manager#7)
- Remove GitHub Actions workflows for flake8 and mypy in favor of existing Zuul CI jobs (osism/openstack-flavor-manager#34, osism/openstack-flavor-manager#37)


# CHANGELOG.md

## [1.0.0] – 2026-01-25

### Added
- Deterministic pixel grid snapping via `--px`
- Explicit palette quantization using JSON-defined palettes
- Built-in palettes:
  - dmg-green
  - dmg-amber
  - dmg-grey
  - dmg-pink
  - gbc-default
  - el-cyan
  - el-pink
- CLI commands:
  - `help`
  - `palette`
  - `check`
  - `run`
- Minimal, reproducible test suite (`tests/run_all_tests.sh`)
- Canonical, stable behavior validated against real icon assets

### Fixed
- Removed partial / experimental batch implementation
- Eliminated nondeterministic behavior
- Resolved image decoding edge cases by constraining inputs
- Restored a known-good single-image pipeline as canonical

### Removed
- Incomplete batch command
- Temporary fetch / normalize scripts
- One-off debugging helpers
- Non-deterministic or undocumented behavior

### Notes
This release establishes the **canonical baseline**.  
Future versions must preserve output determinism unless explicitly versioned otherwise.

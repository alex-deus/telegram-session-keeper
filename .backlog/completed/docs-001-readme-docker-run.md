# Task: Add Docker Run Usage to README.md

## Metadata

- **ID**: docs-001-readme-docker-run
- **Status**: completed
- **Priority**: medium
- **Estimated Hours**: 1
- **Assigned Agent**: python-engineer
- **Dependencies**: none
- **Rejection Count**: 0 (max 3; quality-reviewer increments on reject; after 3rd rejection, task-engineer redesigns. See `${CLAUDE_PLUGIN_ROOT}/content/backlog/workflow.md` for canonical retry limits.)
- **Created By**: task-engineer
- **Created At**: 2026-05-29 05:25:52 UTC
- **Documentation**: none

## Description

README.md at the repo root must contain a dedicated section with complete, copy-paste ready `docker run` invocations for all four CLI commands: `create`, `list`, `code`, and `remove`. Users running the published image `deusalex/telegram-session-keeper-cli` need working examples without installing Python or any local dependencies. The existing "Create Telegram credentials" section must be retained or improved alongside the new Docker usage content.

## Acceptance Criteria (EARS Format)

### Functional Requirements

- [ ] WHEN a user reads README.md, the Docker usage section shall contain a working `docker run` invocation for each of the four commands: `create`, `list`, `code`, and `remove`
- [ ] WHEN a user copies any `docker run` example from README.md, the command shall use image `deusalex/telegram-session-keeper-cli` and pass `api_id` and `api_hash` as environment variables
- [ ] WHEN the `create` command example is shown, README.md shall include the `-it` flag and a note that interactive input is required for Telegram login
- [ ] WHEN volume mount is shown in any example, README.md shall use `$(pwd)/data:/app/src/data` so that `db_path=data/db.csv` resolves correctly inside the container

### Invariants / Ubiquitous

- [ ] README.md shall document all required env vars (`api_id`, `api_hash`) and optional env vars (`db_path`, `log_level`) with their types and defaults
- [ ] README.md shall retain a "Create Telegram credentials" section (existing content kept or improved)

### Error Handling / Unwanted Behavior

- [ ] IF a user omits `api_id` or `api_hash`, README.md shall make clear these are required (no default)
- [ ] IF the `create` command is run without `-it`, README.md shall note the container will hang waiting for interactive input

## Technical Requirements

### Implementation Details

- Modify `README.md` at the repo root — no other files change
- Docker section must reference the exact published image name: `deusalex/telegram-session-keeper-cli`
- Env var names in examples must match `settings.py` exactly: `api_id`, `api_hash`, `db_path`, `log_level`
- Volume mount pattern: `$(pwd)/data:/app/src/data`
- Each `docker run` example must pass env vars via `-e` flags
- The `create` command example must include `-it` and a note about interactive Telegram login (user must enter the code Telegram sends)
- The `code` command example must show the optional `-t <timeout_secs>` flag
- The `create` command example must show the optional `-a save|display` flag

### Testing Requirements

- Manual verification: each command example executes without Docker errors when `api_id` and `api_hash` are valid

### Performance Requirements

- N/A — documentation only

## Edge Cases to Handle

- `create` without `-it`: note that Docker will not forward stdin and the session creation will stall
- `db_path` with a custom value: note that the path is relative to `/app/src/data` inside the container and the volume mount must cover it

## Out of Scope

- Local (non-Docker) Python installation instructions — keep existing content, no rewrite required
- Building the Docker image from source
- CI/CD or Docker Compose configuration
- Any changes to source code, settings, or Dockerfile

## Quality Review Checklist

### For Implementer (Before Marking Complete)

- [ ] All acceptance criteria checked
- [ ] Tests written and passing
- [ ] Code follows project conventions
- [ ] No debug code or print statements
- [ ] Error handling implemented
- [ ] Performance requirements met
- [ ] Structured logging added

### For Quality Reviewer (quality-reviewer agent)

- [ ] Implementation matches requirements
- [ ] Code quality standards met
- [ ] Test coverage adequate (>=80% overall, 100% critical paths)
- [ ] Security best practices followed
- [ ] Documentation accurate
- [ ] Git commit follows conventions
- [ ] Architecture compliance (service boundaries, patterns)
- [ ] Acceptance criteria use EARS keywords (WHEN, WHILE, IF/THEN, WHERE, or Ubiquitous)

## Transition Log

<!-- DO NOT EDIT MANUALLY - Agents update this section -->
<!-- Each transition MUST include: CURRENT timestamp, from_status, to_status, agent, reason -->
<!-- MANDATORY: Always get current timestamp before logging, NEVER use placeholders -->

| Date Time                    | From  | To      | Agent         | Reason/Comment        |
| ---------------------------- | ----- | ------- | ------------- | --------------------- |
| 2026-05-29 05:25:52          | draft | pending | task-engineer | Initial task creation |
| 2026-05-29 03:28:46          | pending | in-progress | python-engineer | Starting implementation |
| 2026-05-29 03:31:15          | in-progress | completed | python-engineer | README.md updated with docker run docs for all 4 commands |

## Implementation Notes

Rewrote README.md to include complete `docker run` examples for all four CLI commands (`create`, `list`, `code`, `remove`) using image `deusalex/telegram-session-keeper-cli`. Added an environment variables table documenting required (`api_id`, `api_hash`) and optional (`db_path`, `log_level`) vars with types and defaults, and included a clear warning that `create` requires `-it` to avoid the container stalling on interactive Telegram login input.

## Quality Review Comments

<!-- quality-reviewer agent adds review feedback here -->

### Review Round 1

- **Date**: [Date]
- **Reviewer**: quality-reviewer
- **Decision**: [accepted|rejected]
- **Comments**:
  - [Specific feedback point 1]
  - [Specific feedback point 2]

### Review Round 2 (if rejected)

- **Date**: [Date]
- **Reviewer**: quality-reviewer
- **Decision**: [accepted|rejected]
- **Comments**:
  - [Issue resolution confirmation]

## Version Control Log

<!-- Implementer agent updates this when committing task file changes -->

| Date Time           | Git Action | Agent   | Commit Hash | Message                                   |
| ------------------- | ---------- | ------- | ----------- | ----------------------------------------- |
| YYYY-MM-DD HH:MM:SS | add        | [agent] | [hash]      | "task: start docs-001-readme-docker-run"  |
| YYYY-MM-DD HH:MM:SS | commit     | [agent] | [hash]      | "task: complete docs-001-readme-docker-run with [summary]" |

## Evidence of Completion

README.md now contains:
- Environment variables table documenting `api_id` (required, int), `api_hash` (required, str), `db_path` (optional, default: `db.csv`), `log_level` (optional, default: `WARNING`)
- `create` example with `-it` flag, `-a save|display` option, and note about interactive Telegram login
- `list` example
- `code` example with `-t <timeout_secs>` option
- `remove` example
- All examples use image `deusalex/telegram-session-keeper-cli`, pass env vars via `-e`, and mount `$(pwd)/data:/app/src/data`

```bash
# docker run list example from updated README.md
docker run --rm \
  -e api_id=<App api_id> \
  -e api_hash=<App api_hash> \
  -e db_path=data/db.csv \
  -v $(pwd)/data:/app/src/data \
  deusalex/telegram-session-keeper-cli \
  cli list
# Expected: prints Phone / Created header and any saved sessions
```

## References

- Existing README.md: `/README.md`
- Docker image: https://hub.docker.com/r/deusalex/telegram-session-keeper-cli

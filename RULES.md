# AI Agent Rules

- Always use git to save your progress working on the project.
- **Git Commit Standards**:
  - You MUST use a concise git commit title with one of the following prefixes:
    - `feat`: (New feature)
    - `fix`: (Bug fix)
    - `chore`: (General tasks, maintenance, configuration)
    - `docs`: (Documentation changes)
    - `style`: (Code style/formatting changes)
    - `refactor`: (Code refactoring)
    - `perf`: (Performance improvements)
    - `test`: (Adding or updating tests)
    - `build`: (Build system or dependency changes)
    - `ci`: (CI/CD configuration changes)
    - `revert`: (Reverting a previous commit)
  - DO NOT use commit descriptions outside of the title.
  - Commits MUST be atomic and focus on a single logical change.
- NEVER push unless explicitly asked.
- NEVER fetch unless explicitly told to.
- An AI Agent must create a flake.nix for this project to manage its dependencies.
- **General Flakes**: Nix flakes must be generic and reusable (e.g., "Flutter Development Environment") rather than project-specific. Avoid project names in flake descriptions or internal metadata.

## Agent Workflow Timeline
You MUST follow this exact path for every task:
1.  **Analyze Prompt**: Understand requirements and identify affected files.
2.  **Kanban Check**: Check `.kanban/` for relevant tasks. Create a new task if needed and set it to "In Progress".
3.  **Research & Plan**: Explore the codebase to understand context and dependencies. Formulate a surgical plan.
4.  **Implementation**: Execute changes in small, logical steps.
5.  **Validation (MANDATORY)**: Before committing, you MUST validate your code. Depending on the project, this includes:
    -   Running available tests (`npm test`, `pytest`, etc.).
    -   Linting and type-checking (`eslint`, `tsc`, `ruff`).
    -   Building the project to ensure no breakages.
    -   Manual verification via tool-assisted checks.
6.  **Atomic Commit**: Commit the validated change using the correct prefix.
7.  **Kanban Update**: Move the task to "Done" or update progress.
8.  **Final Review**: Ensure documentation in `.documentation/` is updated.

## Documentation Requirements
- You MUST maintain and update the project documentation as you implement features or make changes.
- Ensure the following files in `.documentation/` are kept current:
  - [.documentation/architecture.md](.documentation/architecture.md)
  - [.documentation/coding-style.md](.documentation/coding-style.md)
  - [.documentation/configuration.md](.documentation/configuration.md)
  - [.documentation/design-system.md](.documentation/design-system.md)
  - [.documentation/installation.md](.documentation/installation.md)
  - [.documentation/structure.md](.documentation/structure.md)
  - [.documentation/testing.md](.documentation/testing.md)

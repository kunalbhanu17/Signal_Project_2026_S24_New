# Working simultaneously as a team of 3

The repo is split into three module-owned directories so three people can
work at the same time with minimal merge conflicts:

| Person | Branch                  | Owns                                   |
|--------|--------------------------|-----------------------------------------|
| A      | `feature/generator`      | `src/generator/`, `tests/test_generator.py` |
| B      | `feature/analyzer`       | `src/analyzer/`, `tests/test_analyzer.py`   |
| C      | `feature/app-hardware`   | `src/hardware_io/`, `app/`, `tests/test_hardware_io.py` |

`src/common/` is shared — coordinate before editing it.

## Workflow

1. Each person clones the repo on their own machine:
   ```bash
   git clone git@github.com:23f3000144/Signal_Project_2026_S24.git
   ```
2. Check out your branch (create it the first time):
   ```bash
   git checkout -b feature/generator   # or feature/analyzer / feature/app-hardware
   ```
3. Work only inside your owned directory (see that module's `README.md`
   for its interface contract — that contract is what lets the other two
   modules integrate with yours without needing to read your code).
4. Commit and push to your branch regularly:
   ```bash
   git push -u origin feature/generator
   ```
5. Open a PR into `main` when a piece of work is ready. Person C (who owns
   `app/`, the integration layer) merges last for a given milestone since
   `app/` depends on both `src/generator` and `src/analyzer`.

## If working on one shared machine instead

Use `git worktree` so each person gets their own working directory (no
branch-switching collisions) against the same local clone:

```bash
git worktree add ../signals-generator feature/generator
git worktree add ../signals-analyzer feature/analyzer
git worktree add ../signals-app feature/app-hardware
```

Work from one worktree directory per person.

## Keeping merge conflicts rare

- Don't edit another module's directory without a heads-up — go through
  its public function interface instead (documented in each module's
  `README.md`).
- Pull `main` into your branch before opening a PR:
  ```bash
  git fetch origin && git merge origin/main
  ```
- Keep `app/` changes small and frequent (it's the integration point all
  three modules touch) rather than one large late merge.

# Skill Benchmark: standup-humor-coach

**Model**: session default
**Date**: 2026-10-09T20:01:40Z
**Evals**: 1, 2, 3, 4, 5, 6 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 96% ± 6% | 62% ± 7% | +0.34 |
| Time | 871.9s ± 178.6s | 251.9s ± 89.8s | +620.0s |
| Tokens | 172968 ± 21339 | 70592 ± 8198 | +102376 |

## Notes

- Iteration 2 adds a hard length rule (default 150 字, no headings, one move per reply). Expectations now include length limits per eval (200-400 字).
- with_skill replies are 143-316 字 (counting CJK characters and punctuation, one English word = 1). The baseline is 845-1,610 字 and fails every length check.
- with_skill misses: eval 3 names only one profile detail explicitly (the persona is 'as in the profile'); eval 6 is 316 字, over the 300 limit, because three A/B groups are inherently long.
- Baseline outputs are reused from iteration 1 (the baseline does not depend on the skill); they are graded against the new expectations.
- Time and tokens did not drop with shorter replies: the with_skill runs still read SKILL.md plus one or two references and run the candidate/filter loop. Length is an output rule, not a cost saving.
- Real-chat feedback in the same session: a self-referential flirt line read as 调戏 and a control-tower role-play was 'not funny'; logged in SKILL.md's learner profile.
- One run per configuration, so the stddev is across evals, not across runs.

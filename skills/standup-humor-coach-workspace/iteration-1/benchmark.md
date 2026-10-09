# Skill Benchmark: standup-humor-coach

**Model**: session default
**Date**: 2026-10-09T19:28:26Z
**Evals**: 1, 2, 3, 4, 5, 6 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 92% ± 12% | 83% ± 14% | +0.09 |
| Time | 803.4s ± 141.9s | 251.9s ± 89.8s | +551.5s |
| Tokens | 165318 ± 20037 | 70592 ± 8198 | +94726 |

## Notes

- Assertions mostly check structure (Chinese, labels, exercise, no canned laughter), not whether anything is funny. Funniness needs the user's blind pick.
- Eval 5 (Bill Burr) passes 8/8 in both configs, so it does not discriminate. Its difference is length and density: with_skill 1.9k chars, baseline 5.2k chars with many more jokes.
- with_skill replies are much shorter: 1.3-2.4k chars vs 2.6-5.2k. They teach one move per turn and ask for real details instead of inventing them. The baseline hands over finished long scripts (eval 2, eval 5).
- Cost: with_skill takes about 3.2x the time (803s vs 252s) and 2.3x the tokens (165k vs 71k). Every with_skill run read ai-humor-engine.md or another reference and ran the candidate/filter loop. For real-time chat help this may be too slow; a light mode is worth considering.
- with_skill misses: eval 4 demos only one joke (Costco); the 'short' rule was over-applied when the user needs proof their life has material. Eval 6 changed the content as well as the length in pair 3, and never said how the taste profile will be used.
- Baseline misses: no practice line (eval 1), no practice goal (eval 3), no material-mining questions (eval 4), lists of 4-5 jokes instead of A/B pairs plus an internet catchphrase (eval 6), and no invitation to try or report back (eval 2).
- One run per configuration, so the stddev is across evals, not across runs.

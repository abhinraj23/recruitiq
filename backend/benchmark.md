# RecruitIQ Matcher Benchmark

## Test Setup

- Job ID: 2
- Test candidates: DB IDs 2–11
- Candidates 1–10 are mapped to DB IDs 2–11.
- Matcher version: semantic retrieval + structured matching
- Required skills: unchanged
- Preferred skills: unchanged
- Experience: semantic + lexical evidence
- Projects: semantic + exact technology evidence
- Qualification: degree rules + rule-based field + semantic field evidence
- Embeddings: served by the separate embedding microservice

## Previous Expected Ranking

The original manually defined ranking was:

1 > 7 > 6 > 5 > 2 > 4 > 10 > 9 > 3 > 8

This ranking is no longer treated as hard ground truth. It was created before the matcher was refined and before the semantic components were fully integrated through the embedding service.

## Current Actual Ranking

The current matcher produces:

1 > 6 > 7 > 5 > 2 > 10 > 4 > 9 > 8 > 3

## Ranking Differences

There are three ordering differences compared with the previous expected ranking.

### Candidate 6 vs Candidate 7

- Candidate 6: 81.44
- Candidate 7: 81.35

The difference is only 0.09 points. Candidate 6 has full required-skill coverage, while Candidate 7 has slightly stronger project and experience scores.

This is considered a close ranking decision rather than a matcher failure.

### Candidate 10 vs Candidate 4

- Candidate 10: 76.72
- Candidate 4: 76.06

The difference is only 0.66 points. Candidate 10 has stronger preferred-skill coverage, while Candidate 4 has stronger experience and qualification evidence.

The resulting ordering is therefore defensible based on the current scoring components.

### Candidate 8 vs Candidate 3

- Candidate 8: 56.55
- Candidate 3: 54.00

Candidate 8 has stronger relevant professional experience, preferred-skill coverage, and qualification evidence. Candidate 3 has a stronger project score, but substantially weaker experience and qualification scores.

The current ordering is therefore considered reasonable.

## Conclusion

The current matcher produces a ranking that is explainable through independent matching components rather than an opaque score.

The three differences from the original manually defined ranking are either very close decisions or are supported by the candidate evidence.

No further score tuning is performed based solely on this 10-candidate benchmark in order to avoid overfitting.

Future tuning should be based on a larger, independently evaluated dataset with explicit relevance judgments.
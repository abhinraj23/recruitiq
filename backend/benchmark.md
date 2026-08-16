# RecruitIQ Day 10 Benchmark

## Test Setup

- Job ID: 2
- Test candidates: DB IDs 2–11
- Candidates 1–10 are mapped to DB IDs 2–11.
- Matcher version: semantic baseline
- Required skills: unchanged
- Preferred skills: unchanged
- Experience: semantic + existing evidence
- Projects: refined semantic + exact technology evidence
- Qualification: degree rules + rule-based field + semantic field evidence

## Expected Ranking

1 > 7 > 6 > 5 > 2 > 4 > 10 > 9 > 3 > 8

## Actual Ranking

1 > 7 > 6 > 5 > 2 > 10 > 4 > 9 > 3 > 8

## Ranking Difference

Only one ordering difference:

Expected:
4 > 10

Actual:
10 > 4

Scores:

- Candidate 4: 76.66
- Candidate 10: 77.33
- Difference: 0.67

## Conclusion

The semantic matcher preserves the intended ranking for 8 of the 9 adjacent ordering relationships, with only Candidate 4 and Candidate 10 reversed.

No further score tuning is performed based solely on this 10-candidate benchmark to avoid overfitting.
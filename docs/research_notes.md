## CASIA-B Sequence Quality

Before GaitPart preprocessing, the local CASIA-B dataset was audited.

All 13,640 expected subject/condition/view directories were present.

However:

- 47 sequence folders contained zero frames
- 48 additional sequences contained between 1 and 14 frames
- 95 sequences total contained fewer than 15 frames
- 62 affected sequences were in the training partition
- 33 affected sequences were in the testing partition

The raw dataset will remain unchanged.

This issue will be considered when interpreting the GaitPart reproduction
results, and the processed OpenGait dataset will be audited separately.
# meds-sbd-checker

Repository for code to autmatically check on arrival of SBD data files. The main tasks are:

1. Check that SBD files that arrive have a corresponding profile on the Argo Global Data Centre
2. Check that floats that are scheduled to send a profile do send it, and generate a message to relevant parties if they do not outside a designated grace period (~2 days)

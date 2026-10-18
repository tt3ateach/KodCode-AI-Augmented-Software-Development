# Work Items 0.4.1 · the release with the escaped defect (instructor only)

0.4.1 shipped one maintenance change, an AI-assisted cleanup (PR #31, "Tidy up date helpers"): "Simplifies a
helper and removes an unused import in app/main.py. No behavior change intended." The docstring still says UTC; the
code now uses the server's local day. All 34 then-current tests, the health check and the completed-task
probe pass, because the acceptance fixture replaces `get_reference_date` and the probe does not depend on
the day. Use this folder to reproduce the incident; never copy it over student work.

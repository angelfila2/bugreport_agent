# Friday evaluation checklist

Run each fixture through your finished agent and save its report and tool trace.

| Fixture | Expected behavior |
| --- | --- |
| 01_database_unavailable.log | Cite line 2; identify connection failure while leaving the underlying service/network cause unconfirmed. |
| 02_misleading_warning.log | Link req-201 to the duplicate email constraint; do not blame req-200's cache warning. |
| 03_insufficient_evidence.log | State that cause is unknown and request diagnostic evidence. |

Also try a missing file and a tool failure. Verify the agent stops at its step limit.
Check that cited lines exist and support the claims. Do not grade only by keywords.

Practise explaining tool selection, loop termination, evidence validation, and one design tradeoff.

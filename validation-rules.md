# Walkthrough Validation Rules

Apply these checks to every Markdown walkthrough file in `modules/`.

1. **Required sections:** The file has both a `## Summary` heading and a
   `## Quiz` heading.
2. **Non-empty summary:** The Summary section contains meaningful prose, not
   just a placeholder or heading.
3. **Quiz questions:** The Quiz section contains at least three clearly
   worded, numbered questions relevant to the walkthrough.
4. **Answer key:** The Quiz section includes an `### Answers` heading and an
   answer for every question, in the same order.
5. **Markdown structure:** Headings use valid Markdown syntax and appear in
   order: document title, Summary, Quiz, then Answers.
6. **Accuracy and audience:** Content is consistent with the project and
   intended audience; customer-facing walkthroughs exclude internal-only or
   sensitive information.

## Running AI Validation

Run `python tools/validate_walkthroughs.py` from the repository root. The
script passes these rules and each `modules/*-walkthrough.md` file to the
GitHub Copilot CLI (`copilot -p {prompt}`) and writes one Markdown report per
file under `reports/walkthrough-validation/`.

To use another prompt-based CLI, pass `--command` or set
`WALKTHROUGH_AI_COMMAND`. The command template must include `{prompt}`, which
is replaced with the full prompt and passed as a single argument. For example:
`python tools/validate_walkthroughs.py --command 'my-ai --prompt {prompt}'`.

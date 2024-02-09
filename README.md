# AI-assited PR Review Action

This action leverages GPT-3.5 model to provide summary and code improvements for any pull request

### Example workflow

```yaml
name: PR Review
on:
  pull_request:

permissions:
  contents: read
  pull-requests: write

jobs:
  ai-review:
    runs-on: ubuntu-latest
    name: AI-assisted Review
    environment: ${{ github.event.inputs.environment }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run AI PR review
        id: ai-assisted-pr-review
        uses: ./
        with:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_TOKEN: ${{ github.token }}
          PR_REPO: ${{ github.repository }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `OPENAI_API_KEY`  | Your provided OpenAI API Key stored in secrets   |
| `GITHUB_TOKEN`  |  Github access token to pull data and provide comments    |
| `PR_REPO`  |  The repositiry to run review on   |
| `PR_NUMBER`  |  The Pull Request number to run review on   |

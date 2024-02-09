import os
from github import Github, Auth
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def main():

    auth = Auth.Token(os.environ['GITHUB_TOKEN'])
    github = Github(auth=auth)
    repo = github.get_repo(f"{os.environ['PR_REPO']}")
    pr = repo.get_pull(int(os.environ['PR_NUMBER']))

    llm = ChatOpenAI(api_key=os.environ['OPENAI_API_KEY'])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are professional software engineer who is doing a code review for a pull request. Use proper markdown format on variables, file names and code blocks. Please answer in short point forms."),
        ("user", "{input}")
    ])

    chain = prompt | llm
    user_input = "Provide a summary of the changes in a file of a pull request as well as suggestions for improvement based on the below changes:\n {changes}"


    last_commit = pr.get_commits()[pr.commits - 1]
    changed_files = pr.get_files()
    for file in changed_files:
        pr_changes = ""
        pr_changes += f"File name: `{file.filename}`\n"
        pr_changes += f"Number of changes: {file.changes}\n"
        pr_changes += f"Numer of additions: {file.additions}\n"
        pr_changes += f"Numer of deletions: {file.deletions}\n"
        pr_changes += f"Diff: {file.patch}"

        pos_st = file.patch.find("@@ -")
        pos_end = file.patch.find(",", pos_st)
        position = int(file.patch[pos_st:pos_end].split("@@ -")[1])

        llm_result = chain.invoke({"input": user_input.format(changes=pr_changes)})
        pr_comment = f"{llm_result.content}"
        if position == 0:
            position = 1
        pr.create_comment(body=pr_comment, commit=last_commit, path=file.filename, position=position)

if __name__ == '__main__':
    main()
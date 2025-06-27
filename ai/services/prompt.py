class PromptService:
    @staticmethod
    def suggest_developer_prompt(issue, issues):
        return f"""
          You are an AI assistant helping with Jira ticket analysis.

          Input Structure:

          - The **issue** is a JSON object with the following fields:
            - `id`: the unique identifier of the issue
            - `title`: the summary/title of the issue
            - `epic`: the epic name or None if not applicable
            - `story_points`: the estimated effort for this issue.

          - The **history** is an array of user objects, where each user has:
            - `id`: the user's unique identifier
            - `name`: the full name of the user
            - `issues`: a list of past issues the user has worked on, each with the same structure as the issue above

          Based on this information, suggest the most suitable developer to assign to the issue.

          Issue to be assigned:
          {issue}

          History of issues were assigned by users:
          {issues}

          NOTE: Start with focusing on the related issues using the epic.

          NOTE: Return your response as valid JSON only. Do not include any extra text, markdown, or formatting — just the JSON object.
          Use this format:

          {{
            "assigner": "<name of the most suitable developer>",
            "assigner_id": "<id of the most suitable developer>",
            "issue": "<title of the issue to be assigned>",
            "reason": "<brief explanation of why this developer is a good fit>"
            "story_points": "<The estimated effort for this task>"
          }}
          """

    @staticmethod
    def predict_efficient_developer_prompt(issues):
        return f"""
          You are an AI assistant specialized in Jira ticket analytics.

          Input:

          - `issue`: A JSON object with the following structure:
            - `id`: Unique issue identifier.
            - `title`: Summary of the issue.
            - `epic`: Epic name, or `null` if not applicable.
            - `story_points`: Estimated effort in story points.
            - `sprint_transitions`: Number of sprint transitions (how many times the issue was carried over to the next sprint before being completed).

          - `history`: A list of developers, each with:
            - `id`: Unique developer ID.
            - `name`: Full name of the developer.
            - `issues`: List of issues assigned to them in the last 5 sprints, with the structure described above.

          Your task:

          1. Analyze each developer's efficiency based on:
             - The number of issues completed.
             - The total and average story points delivered.
             - How many sprints it took on average to close an issue (`sprint_transitions`).
             - Note: Bug issues may not have story points. Consider issue count as a secondary metric in such cases.

          2. Identify the most efficient developer.

          An efficient developer is typically expected to complete tasks in 0-2 sprint transitions and handle 24+ SP per sprint.

          Return **only** a valid JSON object in this format:

          {{
            "developer": "<most efficient developer's full name>",
            "developer_id": "<developer's ID>",
            "reason": "<brief explanation for why this developer is the most efficient>",
            "summary": {{
              "<developer_name>": {{
                "issues_completed": <number>,
                "average_story_points_per_sprint": <float or null>,
                "average_story_points": <float or null>,
                "average_sprint_transitions": <float>,
              }},
              ...
            }}
          }}

          Do not include any extra commentary, markdown, or explanations outside of this JSON object.
          Here is the input history:

          {issues}
          """



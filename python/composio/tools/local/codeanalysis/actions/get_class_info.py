import os
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, Field

from composio.tools.base.local import LocalAction
from composio.tools.local.codeanalysis.actions.base_action import BaseCodeAnalysisAction


class GetClassInfoRequest(BaseModel):
    repo_name: str = Field(
        ...,
        description="Name of the repository. It should be the last part of valid github repository name. It should not contain any '/'.",
    )
    class_name: str = Field(
        ..., description="Name of the class for which information is requested"
    )


class GetClassInfoResponse(BaseModel):
    result: str = Field(
        ...,
        description="Formatted string containing detailed information about the requested class",
    )


class GetClassInfo(
    LocalAction[GetClassInfoRequest, GetClassInfoResponse], BaseCodeAnalysisAction
):
    """
    This tool retrieves and formats detailed information about a specified class in a given repository.

    Use this action when you need to:
    1. Obtain comprehensive details about all instances of a specific class in the codebase.
    2. Understand the structure, methods, and attributes of a class.
    3. Gather information for code analysis.

    Usage example:
    repo_name: django
    class_name: Signal

    Note: If multiple classes match the provided name, information for all matching classes will be returned.
    """

    display_name = "Get Class Info"
    _tags = ["index"]

    def execute(
        self, request: GetClassInfoRequest, metadata: Dict
    ) -> GetClassInfoResponse:
        repo_name = os.path.basename(request.repo_name)

        self.load_fqdn_cache(repo_name)
        query_class_name = request.class_name

        matching_fqdns = self.get_matching_items(query_class_name, "class")
        class_results = self.get_item_results(
            matching_fqdns=matching_fqdns,
            repo_path=str(Path.home() / repo_name),
        )

        if not class_results:
            return GetClassInfoResponse(result="No matching results found!")

        result_str = self.format_class_results(class_results)
        return GetClassInfoResponse(result=result_str)

    def format_class_results(self, class_results: List[Dict]) -> str:
        result_str = f"<Total {len(class_results)} result(s) found:>\n"
        for _idx, _class in enumerate(class_results):
            result_str += f"## Details about shortlisted result ID {_idx}:\n"
            result_str += _class["res_fetch_class_stuff"]
            result_str += "\n"
        return result_str
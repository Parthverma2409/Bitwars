export const LocalTools = [
    "CodeIndexTool",
    "CodeFormatTool",
    "CodeGrepTool",
    "CodeMapTool",
    "EmbedTool",
    "Mathematical",
    "FileTool",
    "Greptile",
    "RagTool",
    "FileEditTool",
    "SearchTool",
    "GitCmdTool",
    "HistoryFetcherTool",
    "ShellExec",
    "SpiderTool",
    "SqlTool",
    "WebTool",
    "ZepTool"
].map((a) => a.toLowerCase());

export const LocalActions = [
    "CODEFORMAT_FORMAT_AND_LINT_CODEBASE",
    "CODEGREP_SEARCH_CODEBASE",
    "CODEINDEX_CREATE_INDEX",
    "CODEINDEX_INDEX_STATUS",
    "CODEINDEX_SEARCH_CODEBASE",
    "CODEMAP_DELETE_REPO_MAP",
    "CODEMAP_GENERATE_RANKED_TAGS",
    "CODEMAP_GET_REPO_MAP",
    "CODEMAP_INIT_REPO_MAP",
    "EMBEDTOOL_CREATE_IMAGE_VECTOR_STORE",
    "EMBEDTOOL_QUERY_IMAGE_VECTOR_STORE",
    "FILEEDITTOOL_CREATE_FILE_CMD",
    "FILEEDITTOOL_EDIT_FILE",
    "FILEEDITTOOL_OPEN_FILE",
    "FILEEDITTOOL_SCROLL",
    "FILETOOL_READ_FILE",
    "FILETOOL_WRITE_FILE",
    "GITCMDTOOL_GET_PATCH_CMD",
    "GITCMDTOOL_GITHUB_CLONE_CMD",
    "GITCMDTOOL_GIT_REPO_TREE",
    "GREPTILE_CODE_QUERY",
    "HISTORYFETCHERTOOL_GET_WORKSPACE_HISTORY",
    "MATHEMATICAL_CALCULATOR",
    "RAGTOOL_ADD_CONTENT_TO_RAG_TOOL",
    "RAGTOOL_RAG_TOOL_QUERY",
    "SEARCHTOOL_FIND_FILE_CMD",
    "SEARCHTOOL_SEARCH_DIR_CMD",
    "SEARCHTOOL_SEARCH_FILE_CMD",
    "SHELL_CREATE_SHELL",
    "SHELL_EXEC_COMMAND",
    "SPIDERTOOL_CRAWL",
    "SPIDERTOOL_SCRAPE",
    "SQLTOOL_SQL_QUERY",
    "WEBTOOL_SCRAPE_WEBSITE_CONTENT",
    "WEBTOOL_SCRAPE_WEBSITE_ELEMENT",
    "ZEPTOOL_ADD_MEMORY",
    "ZEPTOOL_CREATE_SESSION",
    "ZEPTOOL_GET_MEMORY",
    "ZEPTOOL_SEARCH_MEMORY",
].map((a) => a.toLowerCase());
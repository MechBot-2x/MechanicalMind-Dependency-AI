def classify_error(log_text):
    if "dependency_file_not_evaluatable" in log_text:
        return "DEPENDENCY_SYNTAX_ERROR"
    elif "git@github.com" in log_text:
        return "GIT_CONFIG_ERROR"
    elif "exit 1" in log_text:
        return "PYTHON_EXECUTION_FAILURE"
    else:
        return "UNKNOWN_ERROR"

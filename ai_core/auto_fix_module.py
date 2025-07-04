ejemplo: def fix_requirement_conflict(package, current_version, suggested_version):
    with open("requirements.txt", "r+") as f:
        content = f.read()
        content = content.replace(
            f"{package}=={current_version}",
            f"{package}=={suggested_version}"
        )
        f.seek(0)
        f.write(content)

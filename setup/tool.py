def set_project_path():
    from pathlib import Path
    import sys

    cwd = Path(__file__).parent.parent
    sys.path.append(str(cwd))
    return cwd
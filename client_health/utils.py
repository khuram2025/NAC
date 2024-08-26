from packaging import version

def compare_versions(version1, version2):
    """
    Compare two version strings.
    :param version1: First version string
    :param version2: Second version string
    :return: -1 if version1 < version2, 0 if version1 == version2, 1 if version1 > version2
    """
    print(f"Comparing versions: {version1} and {version2}")
    v1 = version.parse(version1)
    v2 = version.parse(version2)
    
    result = 0
    if v1 < v2:
        result = -1
    elif v1 > v2:
        result = 1
    
    print(f"Comparison result: {result}")
    return result
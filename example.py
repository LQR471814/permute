def test_single(depth: int) -> int:
    if depth == 10:
        return 0
    return test_single(depth+1) + 1

def sum_results(results: list[int]) -> int:
    result: int = 0
    for r in results:
        result += r
    return result

def test_branching(depth: int) -> int:
    if depth == 7:
        return 1

    results: list[int] = []
    for _ in range(2):
        results.append(test_branching(depth+1))

    return sum_results(results)

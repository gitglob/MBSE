
from numpy.lib.type_check import real


def calculate_accuracy(score_values, real_values):
    score = 0
    real_normalized = []
    for s in score_values:
        score += s
    score = score * 100 / len(score_values)
    real_min = min(real_values)
    real_max = max(real_values)
    for r in real_values:
        real_normalized.append((r - real_min) / (real_max - real_min))

    return score, real_normalized

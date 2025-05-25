def generate_knapsack_schedule(subjects, time_limit):
    """
    Fatigue-aware 0/1 Knapsack Scheduler:
    Selects subject sessions to fit within a daily time limit.
    Applies a fatigue penalty to reduce the value of later sessions.
    """
    sessions = []
    fatigue_penalty = 0.1  # 10% value drop per additional session (fatigue effect)

    for subject in subjects:
        base_duration = 30 + (subject.complexity * 10)  # base duration varies with complexity
        base_value = (6 - subject.priority)  # inverse priority → higher priority = more value
        sessions.append({
            'subject': subject,
            'duration': base_duration,
            'priority': base_value
        })

    n = len(sessions)
    dp = [[0] * (time_limit + 1) for _ in range(n + 1)]
    selected_map = [[[] for _ in range(time_limit + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for t in range(time_limit + 1):
            current = sessions[i - 1]
            duration = current['duration']

            if duration <= t:
                fatigue_level = len(selected_map[i - 1][t - duration])
                adjusted_value = current['priority'] * (1 - fatigue_penalty * fatigue_level)

                take = adjusted_value + dp[i - 1][t - duration]
                skip = dp[i - 1][t]

                if take > skip:
                    dp[i][t] = take
                    selected_map[i][t] = selected_map[i - 1][t - duration] + [current]
                else:
                    dp[i][t] = skip
                    selected_map[i][t] = selected_map[i - 1][t]
            else:
                dp[i][t] = dp[i - 1][t]
                selected_map[i][t] = selected_map[i - 1][t]

    best_schedule = selected_map[n][time_limit]
    return best_schedule[::-1]  # return in original order

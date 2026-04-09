
"""
Centralized constants for ProMind7.
"""

# Session Statuses
SESSION_STATUS_PLANNED = "planned"
SESSION_STATUS_CANCELLED = "cancelled"

# Task Statuses
TASK_STATUS_TODO = "todo"
TASK_STATUS_DONE = "done"

# Task Priorities
TASK_PRIORITY_HIGH_VALUES = {'high', 'haute', 'élevée'}

# Enrollment / Pack Statuses (Lower case for comparison)
ENROLLMENT_STATUS_CANCELLED_VALUES = {
    'cancel', 'cancelled', 'annulé', 'annule', 'trash', 'annuler'
}
ENROLLMENT_STATUS_COMPLETED_VALUES = {
    'completed', 'complete', 'finish', 'finished'
}

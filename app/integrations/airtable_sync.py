"""
Integration Airtable.

Gere la synchronisation des taches/apprenants vers Airtable. Ce module
sera invoque depuis services/tasks_service.py ou services/learners_service.py
apres creation/mise a jour. Il remplacera l'envoi direct prevu vers Make.
"""


def sync_task_to_airtable(task: dict):
    """
    Synchronise une tache vers Airtable.

    Args:
        task: dictionnaire representant la tache.
    """
    # TODO: implementer l'ecriture dans Airtable (API key/base/table).
    pass


def sync_learner_to_airtable(learner: dict):
    """
    Synchronise un apprenant vers Airtable.

    Args:
        learner: dictionnaire representant l'apprenant.
    """
    # TODO: implementer la synchro des apprenants.
    pass



"""
Integration Make (webhooks).

Centralise l'envoi de payloads vers des scenarios Make (ex: creation ou
mise a jour d'une tache afin de synchroniser Airtable ou d'autres outils).
La logique d'appel sera branchee, par exemple, apres la creation d'une
tache dans services/tasks_service.py.
"""


def send_task_webhook(payload: dict):
    """
    Envoie un webhook Make pour signaler une tache creee/maj.

    Args:
        payload: dictionnaire representant la tache et ses meta-donnees.
    """
    # TODO: implementer requests.post vers le scenario Make.
    pass



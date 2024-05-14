from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionCallAPI(Action):
    def name(self) -> Text:
        return "action_call_api"


    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="COUCOU")
        return ["Ouais ouais"]

        # TODO
        # # Faire une requête à votre API REST
        # response = requests.get('URL_de_votre_API')
        #
        # # Traiter la réponse de l'API
        # if response.status_code == 200:
        #     data = response.json()
        #     dispatcher.utter_message(text="Réponse de l'API : {}".format(data))
        # else:
        #     dispatcher.utter_message(text="Erreur lors de la requête à l'API")
        # return []

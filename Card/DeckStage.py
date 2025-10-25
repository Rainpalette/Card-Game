from Card.CardSetting import *
import json


class DeckStage:
    def __init__(self):
        self.deck = []
        self.deck_list=[]
        self.current_deck = []
        self.latest_deck_name = ""

    # def add_card(self, card):
    #     if len(self.deck)>=12:
    #         return False
    #     else:
    #         self.deck.append(card)

    def add_card(self, card):
        if len(self.current_deck)>=12:
            return False
        else:
            self.current_deck.append(card)

    def remove_card(self, card):
        if card in self.current_deck:
            self.current_deck.remove(card)

    def setup_data(self):
        with open("Data/CardDeckRecord.json", "r", encoding="utf-8") as f:
            data =json.load(f)
        self.deck = data
        for deck in self.deck:
            deck_data = {
                "deck_name": deck.get("deck_name"),
                "cards": []
            }
            for card_name in deck.get("cards"):
                for card in Card_list().card_list:
                    if card.name == card_name:
                        deck_data["cards"].append(card)
            self.deck_list.append(deck_data)
        self.current_deck = self.deck_list[0].get("cards")

    def get_deck(self, name):
        for deck in self.deck_list:
            if deck.get("deck_name") == name:
                self.current_deck = deck.get("cards")
        

    def get_card_name(self,index):
        name = self.current_deck[index].name
        return name

    def get_card_detail(self,index):
        description = self.current_deck[index].description
        mana_cost = self.current_deck[index].mana_cost
        cooldown = self.current_deck[index].cooldown
        return f"mana_cost: {mana_cost}\ncooldown:{cooldown}\n{description}"
    
    def add_default_card_deck(self):
        default_deck = [NormalAttack(),Heal(),Defense(),ShieldCounter(),
                        HolyLight(),Intimidate(),CriticalStrike(),Trick()]
        deck_name = "Default Deck"
        data = {
            "deck_name": deck_name,
            "cards": [card for card in default_deck]
        }
        self.deck_list.append(data)
        # self.current_deck = default_deck

    def set_deck(self, index):
        self.current_deck = self.deck_list[index].get("cards")
    
    def return_deck(self):
        return self.current_deck
    
    def create_new_deck(self, deck_cards, deck_name="New Deck"):
        data = {
            "deck_name": deck_name,
            "cards": [card.name for card in deck_cards]
        }
        self.deck_list.append(data)

    def save_deck(self, deck):
        print("Saving deck...")
        with open("Data\CardDeckRecord.json", "w", encoding="utf-8") as f:
            json.dump(deck, f, indent=4, ensure_ascii=False)



class PlayerCardManager():
    def __init__(self, battle,deck=DeckStage()):
        self.battle = battle
        self.deck = deck
    
    def reduce_mana(self, card,addition_reduce=0):
        self.battle.player.mana -= card.mana_cost

    def get_and_use_card(self,index):
        card = self.deck[index]
        if card.current_cooldown <=0:
            card.use_card(self.battle)
            card.cooldown_card()
            self.reduce_mana(card)
            return True
        return False
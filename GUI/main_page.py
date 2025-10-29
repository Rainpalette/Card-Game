
from PyQt5.QtWidgets import QApplication, QMessageBox,QMainWindow, QLabel,QPushButton, QStackedWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer#for alignment
from PyQt5.QtGui import QPixmap,QFontDatabase#for picture
from PyQt5.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QGridLayout)
from PyQt5.QtWidgets import QCheckBox#checkbox
from PyQt5.QtWidgets import QRadioButton, QButtonGroup#Radio button
from PyQt5.QtWidgets import QLineEdit


from BattlePage.main_battle_page import BattleBoard
from BattlePage.show_card_page import CardGridWindow, CardDetailPage, Card
from BattlePage.show_enemy_page import EnemyPage
from DeckCreationPage.CreateDeckPage import Message_Page, CreateDeckPage, ConfirmationPage, CardInDeck
from CompendiumPage.Compendium import CardInCompendium, CompendiumPage
from DeckCreationPage.ChooseDeck import ChooseDeckPage, CardDeckInformation
from Card.CardSetting import *

import sys
import os
import json
import time
import pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
from Card.BattleStage import *
from Card.DeckStage import *

pygame.init()
pygame.mixer.init()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Card Game")
        self.resize(1310,850)
        self.center()
        # self.bg_images=["4k Wallpaper For Your Phone, Desktop Tablet _ (1).jpg"]
        # self.setStyleSheet(f"""
        #     QMainWindow {{
        #         background-image: url({self.bg_images[0]});
        #         background-repeat: no-repeat;
        #         background-position: center;
        #         background-size: cover;
        #     }}
        # """)
        self.bg_label = QLabel(self)
        self.bg_label.setScaledContents(True)  # 自动缩放图片
        self.bg_label.setPixmap(QPixmap("hall.jpg"))
        # self.bg_label.setPixmap(QPixmap("4k Wallpaper For Your Phone, Desktop Tablet _ (1).jpg"))
        # self.bg_label.setPixmap(QPixmap("background.jpg"))
        # self.bg_label.setPixmap(QPixmap("Beautiful and Aesthetic Desktop Wallpapers.jpg"))
        # self.bg_label.setPixmap(QPixmap("forest game scene.jpg"))
        self.bg_label.resize(self.size())
        self.icon = QIcon("Afallen.jpg")
        self.setWindowIcon(self.icon)
        self.page_list=[]
        self.battle_backend = BattleStage()
        self.battle = self.battle_backend.battle
        self.deck = DeckStage()
        self.deck.setup_data()
        


        if self.deck.current_deck == []:
            print("No deck found, creating default deck.")
            self.deck.add_default_card_deck()
            self.deck.set_deck(0)
            data = {
                "deck_name": "Default Deck",
                "cards": [card.name for card in self.deck.current_deck]
            }
            self.deck.save_deck(self.deck.deck)
        self.icon = QIcon("Afallen.jpg")
        self.setWindowIcon(self.icon)
        self.central_widget = QWidget(self)
        self.card = Card("","")
        self.card_detail = CardDetailPage("","")

        self.message_page = Message_Page()
        self.battle_page = BattleBoard(self.battle)
        self.show_card_page = CardGridWindow(self.deck)
        self.enemy_page = EnemyPage(self.battle)
        self.text_label = QLabel("Card Game", self)
        self.create_deck = CreateDeckPage()
        self.create_confirmation = ConfirmationPage()
        self.card_in_deck = CardInDeck()
        self.compendium_card = CardInCompendium()
        self.compendium_page = CompendiumPage()
        self.choose_card_deck = ChooseDeckPage(self.deck)
        self.card_deck_setup = CardDeckInformation(self.create_deck)
        
        self.stacked_widget = QStackedWidget()


        count = 0
        for deck_name in self.deck.deck_list:
            self.choose_card_deck.change_button_text(count , deck_name['deck_name'])
            count += 1

        remaining_slots = 9
        for i in range(count, remaining_slots):
            self.choose_card_deck.change_button_text(i , "Create new deck")

        self.stacked_widget.addWidget(self.central_widget)
        with open(r"Data\Card.json", "r", encoding="utf-8") as f:
            cards = json.load(f)
        
        self.card_info_list = []
        for card in cards["cards"]:
            card_info = {
                "name": card["name"],
                "description": card["description"],
                "mana_cost": card["mana_cost"],
                "cooldown": card["cooldown"],
                "backstory": card["backstory"]
            }
            self.card_info_list.append(card_info)
        # self.card_list =[]
        # for card in cards["cards"]:
        #     name = card["name"]
        #     description = card["description"]
        #     mana_cost = card["mana_cost"]
        #     cooldown = card["cooldown"]
        #     self.card_list.append(name)
        #     self.card_list.append(description)
        #     self.card_list.append(mana_cost)
        #     self.card_list.append(cooldown)
        
        
        # card_count = 0
        # for i in range(0,12):
        #     if card_count<8:
        #         name = cards['cards'][i]['name']
        #         #card = CardDetailPage(name, cards['cards'][i]['description'])
        #         card = CardDetailPage(name, self.deck.get_card_detial(i))
        #         card.switch_to_page.connect(self.change_page)
        #         self.stacked_widget.addWidget(card)
        #         card_count +=1
        #     else:
        #         name = i
        #         card = CardDetailPage("name", "details")
        #         card.switch_to_page.connect(self.change_page)
        #         self.stacked_widget.addWidget(card)
        #         card_count +=1

        
        # self.stacked_widget.addWidget(self.card_detail)
        self.stacked_widget.addWidget(self.battle_page)#1
        self.stacked_widget.addWidget(self.show_card_page)#2
        self.stacked_widget.addWidget(self.enemy_page)#3
        self.stacked_widget.addWidget(self.card_detail)#4
        self.stacked_widget.addWidget(self.create_deck)#5
        self.stacked_widget.addWidget(self.create_confirmation)#6
        self.stacked_widget.addWidget(self.compendium_page)#7
        self.stacked_widget.addWidget(self.choose_card_deck)#8
        self.stacked_widget.addWidget(self.card_deck_setup)#9
        self.stacked_widget.addWidget(self.message_page)#10
        

        #left part
        self.vbox_left = QVBoxLayout()
        self.vbox_left.addWidget(self.text_label)
        self.text_label.setStyleSheet("font-size: 60px; font-weight: bold;")
        #self.vbox_left.addStretch(1)
        self.text_label.setAlignment(Qt.AlignCenter)
        #self.vbox_left.addStretch(1)

        #right part
        self.first_row_button_layout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        self.create_deck_button = QPushButton("Deck")
        self.compendium_button = QPushButton("Compendium")
        self.game_start_button = QPushButton("Game Start")

        self.create_deck_button.setFixedSize(200,200)
        self.create_deck_button.setStyleSheet("font-size:30px;")
        # self.create_deck_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.create_deck)))
        self.create_deck_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.choose_card_deck)))
        self.compendium_button.setFixedSize(200,200)
        self.compendium_button.setStyleSheet("font-size:30px;")
        self.compendium_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.compendium_page)))
        self.game_start_button.setFixedSize(410,300)
        self.game_start_button.setStyleSheet("font-size:45px;")

        #self.game_start_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.battle_page)))
        #print(self.stacked_widget.indexOf(self.battle_page))
        self.game_start_button.clicked.connect(self.game_start)

        #13
        self.first_row_button_layout.addWidget(self.create_deck_button)
        self.first_row_button_layout.addStretch(1)
        self.first_row_button_layout.addWidget(self.compendium_button)
        
        self.button_layout.addLayout(self.first_row_button_layout)
        self.button_layout.addWidget(self.game_start_button)

        self.main_layout= QHBoxLayout()
        self.main_layout.addLayout(self.vbox_left)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.setStretch(0,2)
        self.main_layout.setStretch(1,1)

        self.central_widget.setLayout(self.main_layout)
        
        self.setCentralWidget(self.stacked_widget)

        self.battle_page.switch_to_page.connect(self.change_page)
        self.battle_page.end_turn.connect(self.end_turn)
        self.enemy_page.switch_to_page.connect(self.change_page)
        self.show_card_page.switch_to_page.connect(self.back_to_battle_stage)
        self.show_card_page.send_name.connect(self.set_card)
        self.show_card_page.send_id.connect(self.play_card)
        self.card.rightClicked.connect(self.change_page)
        self.card_detail.change_to_page.connect(self.return_previous_page)
        self.card_in_deck.leftClicked.connect(self.change_page)
        self.card_in_deck.rightClicked.connect(self.change_page)
        self.create_deck.switch_to_page.connect(self.change_page)
        self.create_deck.send_name.connect(self.set_card)
        self.create_deck.send_card_name.connect(self.add_confirmation)
        self.create_deck.send_showcase_card_name.connect(self.delete_showcase_card)
        self.create_deck.save_deck.connect(self.save_card_deck)
        self.create_deck.set_current_deck.connect(self.set_current_deck)
        self.create_deck.error_message.connect(self.change_message_page)
        self.create_deck.switch_to_returnable_page.connect(self.return_previous_page)
        self.create_confirmation.switch_to_page.connect(self.change_page)
        self.create_confirmation.send_card_name.connect(self.set_showcase_card)
        
        #self.compendium_card.leftClicked
        self.compendium_page.send_name.connect(self.set_compendium_card)
        self.compendium_page.switch_to_page.connect(self.change_page)
        #self.show_card_page.mousePressEvent.connect(self.change_page)
        self.choose_card_deck.search_deck.connect(self.load_selected_deck)
        self.choose_card_deck.switch_to_page.connect(self.change_page)
        self.card_deck_setup.switch_to_page.connect(self.change_page)
        self.card_deck_setup.send_deck_name.connect(self.save_deck_name)
        self.message_page.switch_to_page.connect(self.return_previous_page)



        font_id = QFontDatabase.addApplicationFont("GUI/IMFellEnglish-Regular.ttf")
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            app_font = QFont(font_families[0])
            QApplication.setFont(app_font)
        
        pygame.mixer.music.load(r"C:\Users\User\Downloads\CardGame\The Forgotten Girl.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def resizeEvent(self, event):
        self.bg_label.resize(self.size())
        super().resizeEvent(event)
    
    def set_current_deck(self,deck_name):
        print(f"Setting current deck to: {deck_name}")
        print(f"Available decks: {[deck['deck_name'] for deck in self.deck.deck_list]}")
        for deck in self.deck.deck_list:
            if deck['deck_name'] == deck_name:
                print(f"Deck found: {deck['deck_name']}")
                self.deck.current_deck = deck['cards']
                # self.deck.current_deck_name = deck_name
                self.deck.in_use_deck_name = deck_name
                # print(f"Current deck set to: {self.deck.current_deck}")
                self.show_card_page.deck = self.deck
                self.show_card_page.refresh_card_deck()
                self.choose_card_deck.refresh_current_deck_label()
                break

    def back_to_battle_stage(self,index):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.battle_page))
    
    def add_confirmation(self,name):
        self.create_confirmation.deck_stage = self.deck
        self.create_confirmation.refresh_label(name)
        # self.create_confirmation.label.setText(f"Are you sure to add {name} into the default card deck?")
        # self.create_confirmation.card_name = name

    #load deck after you clicked on the deck button
    def load_selected_deck(self,deck_id):
        temp_list = []
        card_name_list = []
        print(len(self.deck.deck_list))
        print(f"Requested deck ID: {deck_id}")
        if deck_id >= len(self.deck.deck_list):
            self.create_deck.card_showcase_data_list = []
            self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.card_deck_setup))
            return
        temp_list = self.deck.deck_list[deck_id]['cards']
        for skill in temp_list:
            data = {
                "name": skill.name,
                "image_path": "GUI/BattlePage/Afallen.jpg"
            }
            card_name_list.append(data)

        self.create_deck.card_showcase_data_list = card_name_list
        #self.deck.set_deck(deck_id)
        self.create_deck.refresh_page()
        self.create_deck.refresh_deck_name(self.deck.deck_list[deck_id]['deck_name'])
        self.deck.current_deck_name = self.deck.deck_list[deck_id]['deck_name']
        print(f"Loaded deck {deck_id}: {self.deck.current_deck}")
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.create_deck))
    
    def set_card(self,name):
        for card_info in self.card_info_list:
            print(f"{card_info['name']} over here")
            if card_info['name'] == name:
                self.card_detail.name=name
                self.card_detail.description = f"mana cost: {card_info['mana_cost']}\ncooldown:{card_info['cooldown']}\n{card_info['description']}"
                self.card_detail.refresh_page()
                print(f"{card_info['name']} is found")
                self.page_list.append(self.stacked_widget.currentIndex())
                break

        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.card_detail))
    
    def set_compendium_card(self,name):
        for card_info in self.card_info_list:
            print(f"{card_info['name']} over here")
            if card_info['name'] == name:
                self.card_detail.name=name
                self.card_detail.description = f"mana cost: {card_info['mana_cost']}\ncooldown:{card_info['cooldown']}\n{card_info['description']}\n\n{card_info['backstory']}"
                self.card_detail.refresh_page()
                print(f"{card_info['name']} is found")
                self.page_list.append(self.stacked_widget.currentIndex())
                break

        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.card_detail))
    
    def set_showcase_card(self,name):
        # First find the card info
        found_card_info = None
        for card_info in self.card_info_list:
            if card_info['name'] == name:
                found_card_info = card_info
                break
        
        if not found_card_info:
            return
        
        # Check if card is already in deck
        for data in self.create_deck.card_showcase_data_list:
            if data['name'] == name:
                print("Card already in deck.")
                self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.create_deck))
                return
            
        # Prepare new card data
        new_card_data = {
            "name": name,
            "image_path": "GUI/BattlePage/Afallen.jpg"
        }

        # Find first empty slot or append
        empty_slot_found = False
        for i, data in enumerate(self.create_deck.card_showcase_data_list):
            if data['name'] == "":
                print(f"Found empty slot at index {i}")
                self.create_deck.card_showcase_data_list[i] = new_card_data
                self.create_deck.refresh_page()
                print(self.create_deck.card_showcase_data_list)
                empty_slot_found = True
                break
        
        # Check deck size limit
        if len(self.create_deck.card_showcase_data_list) >= 8:
            print("Reached limit.")
            self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.create_deck))
            return

        

        

        # If no empty slot found, append new card
        if not empty_slot_found:
            print("No empty slots, appending new card")
            self.create_deck.card_showcase_data_list.append(new_card_data)

        # Refresh the display
        print("Current deck data:", self.create_deck.card_showcase_data_list)
        self.create_deck.refresh_page()
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.create_deck))
    
    # def create_new_deck_page(self):
    #     count = 0
    #     for deck_name in self.deck.deck_list:
    #         self.choose_card_deck.change_button_text(count , deck_name['deck_name'])
    #         count += 1

    def delete_showcase_card(self,name):
        count = 0
        for data in self.create_deck.card_showcase_data_list:
            if data['name'] == name:
                self.create_deck.delete_card(name)
                data['name'] = ""
                data['image_path'] = ""
                # self.create_deck.card_showcase_list.remove(self.create_deck.card_showcase_list[count])
                print(self.create_deck.card_showcase_data_list)
                # self.create_deck.card_showcase_data_list[count]=data

                self.create_deck.refresh_after_delete()
                break
            count +=1

    def save_card_deck_to_json(self):
        data_list = []
        
        print(self.deck.deck_list)
        for deck in self.deck.deck_list:
            data = {
            "deck_name": "",
            "cards": []
            }
            for card in deck['cards']:
                data['cards'].append(card.name)
            data['deck_name'] = deck['deck_name']
            data_list.append(data)
        self.deck.save_deck(data_list)
        print(data_list)

    def save_deck_name(self,name):
        data ={
            "deck_name": name,
            "cards": []
        }
        # self.deck.save_deck(data)
        self.save_card_deck(data)
        count = 0
        #refresh deck button name
        for deck_name in self.deck.deck_list:
            self.choose_card_deck.change_button_text(count , deck_name['deck_name'])
            count += 1
        self.create_deck.refresh_deck_name(name)
        # print("Deck name saved:", name)
        # print(self.deck.deck_list)

    def save_card_deck(self,dictionary):
        # with open("Data/CardDeckRecord.json", "a", encoding="utf-8") as f:
        #     json.dump(dictionary, f, ensure_ascii=False, indent=4)
        deck_data = {
            "deck_name": dictionary.get("deck_name"),
            "cards": []
        }
        #change the format from card name to card object
        for card_name in dictionary.get("cards"):
            for card in Card_list().card_list:
                if card.name == card_name:
                    deck_data["cards"].append(card)
                    break

        for deck in self.deck.deck_list:
            if deck.get("deck_name") == dictionary.get("deck_name"):
                deck['cards'] = deck_data['cards']
                break
            
        else:
            self.deck.deck_list.append(deck_data)
        print("Deck saved:", deck_data)
        print(self.deck.deck_list)
        self.save_card_deck_to_json()
        
    
    

        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Information)
        # msg.setText("操作成功！")
        # msg.setWindowTitle("提示")
        # msg.exec_()


    def center(self):
        # 获取主屏幕的几何范围
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def change_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
    
    def game_start(self):
        self.show_card_page.refresh_card_deck()
        self.battle_page.enemy_damage_label.hide()
        self.battle_page.player_damage_label.hide()
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.battle_page))
        self.battle_backend.start_battle("crown")
        self.battle_page.reset_button()
        self.battle_backend.player = self.battle_backend.player_copy
        self.battle_page.battle = self.battle_backend.battle
        self.enemy_page.battle = self.battle_backend.battle
        for card in self.show_card_page.card_gallery:
            card.cooldown_end()
        self.battle_page.update_status(self.deck.current_deck,self.show_card_page)
        print(f"Boss is {self.battle_backend.mob.health}")
        print(f"Player health {self.battle_backend.player.health}")
        self.battle = self.battle_backend.battle
        for card in self.deck.current_deck:
            card.current_cooldown =0
        self.battle.mob.before_change_health = self.battle.mob.health
        self.battle.player.before_change_health = self.battle.player.health
        print(f"Mob health before: {self.battle.mob.before_change_health}, after: {self.battle.mob.health}")
        print(f"Player health before: {self.battle.player.before_change_health}, after: {self.battle.player.health}")
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"C:\Users\User\Downloads\CardGame\フリーBGM鏡の国のアリス症候群ダークメルヘン戦闘ゴシックかっこいい疾走感.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    
    def check_cooldown(self, card):
        if card.current_cooldown>0:
            return False
        print("yay")
        return True
    
    def check_mana(self, card):
        if card.mana_cost >self.battle.player.mana:
            return False
        print("hoho")
        return True
    
    def return_previous_page(self,index):
        print(f"Page list before: {self.page_list}")
        if not self.page_list:
            self.page_list.append(self.stacked_widget.currentIndex())
            self.stacked_widget.setCurrentIndex(index)
        else:
            self.stacked_widget.setCurrentIndex(self.page_list[0])
            self.page_list = []

    

    
    def play_card(self, index):
        card_index = index-1
        card = self.deck.current_deck[card_index]
        if not self.check_cooldown(card):
            print("Already cooldown")
            return
        if not self.check_mana(card):
            print("no mana")
            return
        self.change_page(self.stacked_widget.indexOf(self.battle_page))
        current_health = self.battle.mob.before_change_health
        self.battle_backend.play_card(card)
        self.battle_page.Player_use_skill(card.name)
        self.battle_page.show_damage_on_player(self.battle_backend.calculate_damage(self.battle.player.before_change_health, self.battle.player.health))
        self.battle_page.show_damage_on_enemy(self.battle_backend.calculate_damage(current_health, self.battle.mob.health))
        # self.battle.mob.before_change_health = self.battle.mob.health
        # # self.battle.mob.before_change_health = self.battle.mob.health
        # self.battle.player.before_change_health = self.battle.player.health
        print(f"Mob heal before: {self.battle.mob.before_change_health}, after: {self.battle.mob.health}")
        self.battle_page.update_status(self.deck.current_deck,self.show_card_page)
        self.enemy_page.update_effect_status()
        self.battle.mob.shield_before_change = self.battle.mob.shield
        print(self.battle.mob.get_effects())
        current_card = self.show_card_page.card_gallery[index-1]
        for card in self.deck.current_deck:
            print(f"Checking card: {card.name} against {current_card.name}")
            if card.name == current_card.name:
                print(f"Setting cooldown for card: {card.name} to {card.cooldown}")
                current_card.in_cooldown(card.cooldown)
                # current_card.update_cooldown_display(card.cooldown, card.current_cooldown)
                break
        #card.in_cooldown()
        if self.battle.mob.health<=0:
            QTimer.singleShot(1800, lambda:self.battle_page.enemy_damage_label.hide())
            QTimer.singleShot(1800, lambda:self.battle_page.player_damage_label.hide())
            QTimer.singleShot(2000,lambda:self.battle_page.clear_skill_label())
            QTimer.singleShot(2000,lambda:self.win())
            
        else:
            QTimer.singleShot(2000, lambda:self.battle_page.clear_skill_label())
            QTimer.singleShot(1800, lambda:self.battle_page.enemy_damage_label.hide())
            QTimer.singleShot(1800, lambda:self.battle_page.player_damage_label.hide())
    def win(self):
        self.change_page(self.stacked_widget.indexOf(self.central_widget))
        pygame.mixer.music.load(r"C:\Users\User\Downloads\CardGame\The Forgotten Girl.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)    
    def end_turn(self):
            self.battle_backend.end_turn(self.deck.current_deck)
            for card in self.deck.current_deck:
                for data in self.show_card_page.card_gallery:
                    if card.name == data.name and card.current_cooldown>0:
                        data.update_cooldown_display(card.current_cooldown)
            self.battle_backend.start_turn()
            
            self.run_boss_turn()
            # while True:
            #     if self.battle.mob.mana<=0:
            #         break
            #     if self.battle_backend.is_battle_over:
            #         break
            #     skill_name =self.battle_backend.boss_turn()
            #     QTimer.singleShot(8000,self.battle_page.boss_use_skill(skill_name))
            # self.battle_page.player_turn()
    def run_boss_turn(self):
        print("Boss turn start:", self.battle.mob.mana)
        
        if self.battle.player.health <=0:
            self.battle_page.disable_action()
            self.battle_page.boss_use_skill("")
            self.battle.mob.reset_skill()
            QTimer.singleShot(1500,lambda:self.battle_page.enemy_damage_label.hide())
            QTimer.singleShot(1500,lambda:self.battle_page.player_damage_label.hide())
            QTimer.singleShot(1500,lambda:self.win())
            
            return
        
        if self.battle.mob.mana <=0: # or self.battle_backend.is_battle_over:
            self.battle_page.boss_use_skill("")
            self.battle.mob.reset_skill()
            self.battle_page.player_turn()
            self.battle_page.update_round(self.battle_backend.game.turn)
            self.battle_page.update_status(self.deck.current_deck,self.show_card_page)
            QTimer.singleShot(1800, lambda:self.battle_page.enemy_damage_label.hide())
            QTimer.singleShot(1800, lambda:self.battle_page.player_damage_label.hide())
            return
        
        
        # Store the health before using skill
        
        print(f"health before: {self.battle.mob.before_change_health}")
        # Use the skill
        skill_name = self.battle.mob.use_skill()
        print(f"Boss: {skill_name}")
        print(f"{self.battle.player.health} remaining")
        self.battle_page.boss_use_skill(skill_name)
        
        # Calculate and show damage based on health change
        print(f"damage: {self.battle_backend.calculate_damage(self.battle.mob.before_change_health, self.battle.mob.health)}")
        self.battle_page.show_damage_on_player(self.battle_backend.calculate_damage(self.battle.player.before_change_health, self.battle.player.health))
        self.battle_page.show_damage_on_enemy(self.battle_backend.calculate_damage(self.battle.mob.before_change_health, self.battle.mob.health))
        print(f"Mob heal before: {self.battle.mob.before_change_health}, after: {self.battle.mob.health}")
        
        self.battle.mob.shield_before_change = self.battle.mob.shield
        self.battle_page.update_status(self.deck.current_deck,self.show_card_page)
        
        QTimer.singleShot(2400, lambda:self.run_boss_turn())
        QTimer.singleShot(1800, lambda:self.battle_page.enemy_damage_label.hide())
        QTimer.singleShot(1800, lambda:self.battle_page.player_damage_label.hide())

    def closeEvent(self, event):
        pygame.mixer.music.stop()
        event.accept()
    def change_message_page(self,message):
        self.message_page.set_message(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)   
    window = MainWindow()          
    window.show()                  
    sys.exit(app.exec_())          

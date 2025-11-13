"""
Advanced Japanese Learning Application with Spaced Repetition System (SRS)
Features: Kana, Vocabulary, Grammar, SRS scheduling, Progress tracking
No external dependencies required
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import hashlib
import threading
# ═══════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════
@dataclass
class SRSCard:
    """Represents a spaced repetition card with SM-2 algorithm data."""
    ease: float = 2.5
    interval: int = 1
    repetitions: int = 0
    last_review: Optional[str] = None
    next_review: Optional[str] = None
    wrong_count: int = 0
# ═══════════════════════════════════════════════════════════════
# KANA DATA
# ═══════════════════════════════════════════════════════════════
HIRAGANA = {
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'を': 'wo', 'ん': 'n',
}
KATAKANA = {
    'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
    'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
    'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
    'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
    'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
    'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
    'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
    'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
    'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
    'ワ': 'wa', 'ヲ': 'wo', 'ン': 'n',
}
# ═══════════════════════════════════════════════════════════════
# VOCABULARY DATA (Expanded and Categorized)
# ═══════════════════════════════════════════════════════════════
VOCABULARY = {
    'Greetings': {
        'こんにちは': {'romaji': 'konnichiwa', 'meaning': 'hello', 'jlpt': 'N5',
                       'example': 'こんにちは、げんきですか。', 'example_romaji': 'Konnichiwa, genki desu ka.',
                       'example_eng': 'Hello, how are you?'},
        'おはよう': {'romaji': 'ohayou', 'meaning': 'good morning', 'jlpt': 'N5',
                     'example': 'おはよう、よくねた。', 'example_romaji': 'Ohayou, yoku neta.',
                     'example_eng': 'Good morning, I slept well.'},
        'ありがとう': {'romaji': 'arigatou', 'meaning': 'thank you', 'jlpt': 'N5',
                       'example': 'ありがとう、たすかった。', 'example_romaji': 'Arigatou, tasukatta.',
                       'example_eng': 'Thank you, you helped me.'},
        'すみません': {'romaji': 'sumimasen', 'meaning': 'excuse me', 'jlpt': 'N5',
                       'example': 'すみません、えきはどこですか。', 'example_romaji': 'Sumimasen, eki wa doko desu ka.',
                       'example_eng': 'Excuse me, where is the station?'},
        'はい': {'romaji': 'hai', 'meaning': 'yes', 'jlpt': 'N5',
                 'example': 'はい、わかりました。', 'example_romaji': 'Hai, wakarimashita.',
                 'example_eng': 'Yes, I understood.'},
        'いいえ': {'romaji': 'iie', 'meaning': 'no', 'jlpt': 'N5',
                   'example': 'いいえ、ちがいます。', 'example_romaji': 'Iie, chigaimasu.',
                   'example_eng': 'No, that\'s wrong.'},
        'おやすみなさい': {'romaji': 'oyasuminasai', 'meaning': 'good night', 'jlpt': 'N5',
                           'example': 'おやすみなさい。', 'example_romaji': 'Oyasuminasai.',
                           'example_eng': 'Good night.'},
        'さようなら': {'romaji': 'sayounara', 'meaning': 'goodbye', 'jlpt': 'N5',
                       'example': 'さようなら、ともだち。', 'example_romaji': 'Sayounara, tomodachi.',
                       'example_eng': 'Goodbye, friend.'},
        'はじめまして': {'romaji': 'hajimemashite', 'meaning': 'nice to meet you', 'jlpt': 'N5',
                         'example': 'はじめまして、よろしく。', 'example_romaji': 'Hajimemashite, yoroshiku.',
                         'example_eng': 'Nice to meet you, please treat me well.'},
        'ごめんなさい': {'romaji': 'gomennasai', 'meaning': 'sorry', 'jlpt': 'N5',
                         'example': 'ごめんなさい、遅れました。', 'example_romaji': 'Gomennasai, okuremashita.',
                         'example_eng': 'Sorry, I\'m late.'},
    },
    'Numbers': {
        'いち': {'romaji': 'ichi', 'meaning': 'one', 'jlpt': 'N5',
                 'example': 'いちにんです。', 'example_romaji': 'Ichi nin desu.',
                 'example_eng': 'It\'s one person.'},
        'に': {'romaji': 'ni', 'meaning': 'two', 'jlpt': 'N5',
               'example': 'にほんください。', 'example_romaji': 'Ni hon kudasai.',
               'example_eng': 'Two bottles please.'},
        'さん': {'romaji': 'san', 'meaning': 'three', 'jlpt': 'N5',
                 'example': 'さんじです。', 'example_romaji': 'San ji desu.',
                 'example_eng': 'It\'s 3 o\'clock.'},
        'よん': {'romaji': 'yon', 'meaning': 'four', 'jlpt': 'N5',
                 'example': 'よんにんです。', 'example_romaji': 'Yon nin desu.',
                 'example_eng': 'Four people.'},
        'ご': {'romaji': 'go', 'meaning': 'five', 'jlpt': 'N5',
               'example': 'ごじです。', 'example_romaji': 'Go ji desu.',
               'example_eng': 'It\'s 5 o\'clock.'},
        'ろく': {'romaji': 'roku', 'meaning': 'six', 'jlpt': 'N5',
                 'example': 'ろくにんです。', 'example_romaji': 'Roku nin desu.',
                 'example_eng': 'Six people.'},
        'なな': {'romaji': 'nana', 'meaning': 'seven', 'jlpt': 'N5',
                 'example': 'ななじです。', 'example_romaji': 'Nana ji desu.',
                 'example_eng': 'It\'s 7 o\'clock.'},
        'はち': {'romaji': 'hachi', 'meaning': 'eight', 'jlpt': 'N5',
                 'example': 'はちにんです。', 'example_romaji': 'Hachi nin desu.',
                 'example_eng': 'Eight people.'},
        'きゅう': {'romaji': 'kyuu', 'meaning': 'nine', 'jlpt': 'N5',
                   'example': 'きゅうじです。', 'example_romaji': 'Kyuu ji desu.',
                   'example_eng': 'It\'s 9 o\'clock.'},
        'じゅう': {'romaji': 'juu', 'meaning': 'ten', 'jlpt': 'N5',
                   'example': 'じゅうにんです。', 'example_romaji': 'Juu nin desu.',
                   'example_eng': 'Ten people.'},
        'ひゃく': {'romaji': 'hyaku', 'meaning': 'hundred', 'jlpt': 'N5',
                   'example': 'ひゃくえんです。', 'example_romaji': 'Hyaku en desu.',
                   'example_eng': 'It\'s 100 yen.'},
        'せん': {'romaji': 'sen', 'meaning': 'thousand', 'jlpt': 'N5',
                 'example': 'せんえんです。', 'example_romaji': 'Sen en desu.',
                 'example_eng': 'It\'s 1000 yen.'},
        'まん': {'romaji': 'man', 'meaning': 'ten thousand', 'jlpt': 'N5',
                 'example': 'いちまんえんです。', 'example_romaji': 'Ichiman en desu.',
                 'example_eng': 'It\'s 10,000 yen.'},
    },
    'Family': {
        'かぞく': {'romaji': 'kazoku', 'meaning': 'family', 'jlpt': 'N5',
                   'example': 'かぞくと一緒に食べる。', 'example_romaji': 'Kazoku to issho ni taberu.',
                   'example_eng': 'Eat with family.'},
        'おとうさん': {'romaji': 'otousan', 'meaning': 'father', 'jlpt': 'N5',
                       'example': 'おとうさんは先生です。', 'example_romaji': 'Otousan wa sensei desu.',
                       'example_eng': 'Father is a teacher.'},
        'おかあさん': {'romaji': 'okaasan', 'meaning': 'mother', 'jlpt': 'N5',
                       'example': 'おかあさんは料理が上手です。', 'example_romaji': 'Okaasan wa ryouri ga jouzu desu.',
                       'example_eng': 'Mother is good at cooking.'},
        'あに': {'romaji': 'ani', 'meaning': 'older brother', 'jlpt': 'N5',
                 'example': 'あには学生です。', 'example_romaji': 'Ani wa gakusei desu.',
                 'example_eng': 'Older brother is a student.'},
        'あね': {'romaji': 'ane', 'meaning': 'older sister', 'jlpt': 'N5',
                 'example': 'あねはきれいです。', 'example_romaji': 'Ane wa kirei desu.',
                 'example_eng': 'Older sister is pretty.'},
        'おとうと': {'romaji': 'otouto', 'meaning': 'younger brother', 'jlpt': 'N5',
                     'example': 'おとうとは元気です。', 'example_romaji': 'Otouto wa genki desu.',
                     'example_eng': 'Younger brother is energetic.'},
        'いもうと': {'romaji': 'imouto', 'meaning': 'younger sister', 'jlpt': 'N5',
                     'example': 'いもうとはかわいいです。', 'example_romaji': 'Imouto wa kawaii desu.',
                     'example_eng': 'Younger sister is cute.'},
        'そふ': {'romaji': 'sofu', 'meaning': 'grandfather', 'jlpt': 'N5',
                 'example': 'そふは元気です。', 'example_romaji': 'Sofu wa genki desu.',
                 'example_eng': 'Grandfather is healthy.'},
        'そぼ': {'romaji': 'sobo', 'meaning': 'grandmother', 'jlpt': 'N5',
                 'example': 'そぼは優しいです。', 'example_romaji': 'Sobo wa yasashii desu.',
                 'example_eng': 'Grandmother is kind.'},
    },
    'Food': {
        'ごはん': {'romaji': 'gohan', 'meaning': 'rice/meal', 'jlpt': 'N5',
                   'example': 'ごはんをたべましょう。', 'example_romaji': 'Gohan wo tabemashou.',
                   'example_eng': 'Let\'s eat a meal.'},
        'みず': {'romaji': 'mizu', 'meaning': 'water', 'jlpt': 'N5',
                 'example': 'みずをください。', 'example_romaji': 'Mizu wo kudasai.',
                 'example_eng': 'Water please.'},
        'おちゃ': {'romaji': 'ocha', 'meaning': 'tea', 'jlpt': 'N5',
                   'example': 'おちゃがすきです。', 'example_romaji': 'Ocha ga suki desu.',
                   'example_eng': 'I like tea.'},
        'パン': {'romaji': 'pan', 'meaning': 'bread', 'jlpt': 'N5',
                 'example': '朝にパンを食べる。', 'example_romaji': 'Asa ni pan wo taberu.',
                 'example_eng': 'Eat bread in the morning.'},
        'りんご': {'romaji': 'ringo', 'meaning': 'apple', 'jlpt': 'N5',
                   'example': 'りんごを食べる。', 'example_romaji': 'Ringo wo taberu.',
                   'example_eng': 'Eat an apple.'},
        'みかん': {'romaji': 'mikan', 'meaning': 'mandarin orange', 'jlpt': 'N5',
                   'example': 'みかんがすきです。', 'example_romaji': 'Mikan ga suki desu.',
                   'example_eng': 'I like mandarin oranges.'},
        'おにぎり': {'romaji': 'onigiri', 'meaning': 'rice ball', 'jlpt': 'N5',
                     'example': 'おにぎりを食べる。', 'example_romaji': 'Onigiri wo taberu.',
                     'example_eng': 'Eat rice ball.'},
        'すし': {'romaji': 'sushi', 'meaning': 'sushi', 'jlpt': 'N5',
                 'example': 'すしを食べる。', 'example_romaji': 'Sushi wo taberu.',
                 'example_eng': 'Eat sushi.'},
        'やさい': {'romaji': 'yasai', 'meaning': 'vegetable', 'jlpt': 'N5',
                   'example': 'やさいを食べる。', 'example_romaji': 'Yasai wo taberu.',
                   'example_eng': 'Eat vegetables.'},
        'くだもの': {'romaji': 'kudamono', 'meaning': 'fruit', 'jlpt': 'N5',
                     'example': 'くだものを食べる。', 'example_romaji': 'Kudamono wo taberu.',
                     'example_eng': 'Eat fruit.'},
        'にく': {'romaji': 'niku', 'meaning': 'meat', 'jlpt': 'N5',
                 'example': 'にくを食べる。', 'example_romaji': 'Niku wo taberu.',
                 'example_eng': 'Eat meat.'},
        'さかな': {'romaji': 'sakana', 'meaning': 'fish', 'jlpt': 'N5',
                   'example': 'さかなを食べる。', 'example_romaji': 'Sakana wo taberu.',
                   'example_eng': 'Eat fish.'},
        'たまご': {'romaji': 'tamago', 'meaning': 'egg', 'jlpt': 'N5',
                   'example': 'たまごを食べる。', 'example_romaji': 'Tamago wo taberu.',
                   'example_eng': 'Eat egg.'},
        'ビール': {'romaji': 'biiru', 'meaning': 'beer', 'jlpt': 'N5',
                   'example': 'ビールを飲む。', 'example_romaji': 'Biiru wo nomu.',
                   'example_eng': 'Drink beer.'},
        'ワイン': {'romaji': 'wain', 'meaning': 'wine', 'jlpt': 'N5',
                   'example': 'ワインを飲む。', 'example_romaji': 'Wain wo nomu.',
                   'example_eng': 'Drink wine.'},
    },
    'Colors': {
        'あか': {'romaji': 'aka', 'meaning': 'red', 'jlpt': 'N5',
                 'example': 'あかいくるま。', 'example_romaji': 'Akai kuruma.',
                 'example_eng': 'Red car.'},
        'あお': {'romaji': 'ao', 'meaning': 'blue', 'jlpt': 'N5',
                 'example': 'あおいそら。', 'example_romaji': 'Aoi sora.',
                 'example_eng': 'Blue sky.'},
        'しろ': {'romaji': 'shiro', 'meaning': 'white', 'jlpt': 'N5',
                 'example': 'しろい紙。', 'example_romaji': 'Shiroi kami.',
                 'example_eng': 'White paper.'},
        'くろ': {'romaji': 'kuro', 'meaning': 'black', 'jlpt': 'N5',
                 'example': 'くろいかばん。', 'example_romaji': 'Kuroi kaban.',
                 'example_eng': 'Black bag.'},
        'きいろ': {'romaji': 'kiiro', 'meaning': 'yellow', 'jlpt': 'N5',
                   'example': 'きいろい花。', 'example_romaji': 'Kiiro i hana.',
                   'example_eng': 'Yellow flower.'},
        'みどり': {'romaji': 'midori', 'meaning': 'green', 'jlpt': 'N5',
                   'example': 'みどりの木。', 'example_romaji': 'Midori no ki.',
                   'example_eng': 'Green tree.'},
        'ちゃいろ': {'romaji': 'chairo', 'meaning': 'brown', 'jlpt': 'N5',
                     'example': 'ちゃいろのクマ。', 'example_romaji': 'Chairo no kuma.',
                     'example_eng': 'Brown bear.'},
    },
    'Adjectives': {
        'おおきい': {'romaji': 'ookii', 'meaning': 'big', 'jlpt': 'N5',
                     'example': 'これはおおきいいえです。', 'example_romaji': 'Kore wa ookii ie desu.',
                     'example_eng': 'This is a big house.'},
        'ちいさい': {'romaji': 'chiisai', 'meaning': 'small', 'jlpt': 'N5',
                     'example': 'ちいさいねこがいる。', 'example_romaji': 'Chiisai neko ga iru.',
                     'example_eng': 'There is a small cat.'},
        'たかい': {'romaji': 'takai', 'meaning': 'tall/expensive', 'jlpt': 'N5',
                   'example': 'このかばんはたかい。', 'example_romaji': 'Kono kaban wa takai.',
                   'example_eng': 'This bag is expensive.'},
        'やすい': {'romaji': 'yasui', 'meaning': 'cheap', 'jlpt': 'N5',
                   'example': 'やすいレストランをさがす。', 'example_romaji': 'Yasui resutoran wo sagasu.',
                   'example_eng': 'I look for a cheap restaurant.'},
        'いい': {'romaji': 'ii', 'meaning': 'good', 'jlpt': 'N5',
                 'example': 'いいてんきですね。', 'example_romaji': 'Ii tenki desu ne.',
                 'example_eng': 'It\'s good weather, isn\'t it?'},
        'わるい': {'romaji': 'warui', 'meaning': 'bad', 'jlpt': 'N5',
                   'example': 'わるいてんきです。', 'example_romaji': 'Warui tenki desu.',
                   'example_eng': 'It\'s bad weather.'},
        'あつい': {'romaji': 'atsui', 'meaning': 'hot', 'jlpt': 'N5',
                   'example': '今日はあついです。', 'example_romaji': 'Kyou wa atsui desu.',
                   'example_eng': 'Today is hot.'},
        'さむい': {'romaji': 'samui', 'meaning': 'cold', 'jlpt': 'N5',
                   'example': '今日はさむいです。', 'example_romaji': 'Kyou wa samui desu.',
                   'example_eng': 'Today is cold.'},
        'おいしい': {'romaji': 'oishii', 'meaning': 'delicious', 'jlpt': 'N5',
                     'example': 'このりんごはおいしいです。', 'example_romaji': 'Kono ringo wa oishii desu.',
                     'example_eng': 'This apple is delicious.'},
        'まずい': {'romaji': 'mazui', 'meaning': 'bad tasting', 'jlpt': 'N5',
                   'example': 'この料理はまずいです。', 'example_romaji': 'Kono ryouri wa mazui desu.',
                   'example_eng': 'This dish tastes bad.'},
        'たのしい': {'romaji': 'tanoshii', 'meaning': 'fun', 'jlpt': 'N5',
                     'example': 'がっこうはたのしい。', 'example_romaji': 'Gakkou wa tanoshii.',
                     'example_eng': 'School is fun.'},
        'つまらない': {'romaji': 'tsumaranai', 'meaning': 'boring', 'jlpt': 'N5',
                       'example': 'この本はつまらない。', 'example_romaji': 'Kono hon wa tsumaranai.',
                       'example_eng': 'This book is boring.'},
        'きれい': {'romaji': 'kirei', 'meaning': 'pretty/clean', 'jlpt': 'N5',
                   'example': 'きれいなはなです。', 'example_romaji': 'Kirei na hana desu.',
                   'example_eng': 'It\'s a pretty flower.'},
        'しずか': {'romaji': 'shizuka', 'meaning': 'quiet', 'jlpt': 'N5',
                   'example': 'しずかなへやです。', 'example_romaji': 'Shizuka na heya desu.',
                   'example_eng': 'It\'s a quiet room.'},
        'にぎやか': {'romaji': 'nigiyaka', 'meaning': 'lively', 'jlpt': 'N5',
                     'example': 'にぎやかなまちです。', 'example_romaji': 'Nigiyaka na machi desu.',
                     'example_eng': 'It\'s a lively town.'},
    },
    'Verbs': {
        'たべる': {'romaji': 'taberu', 'meaning': 'to eat', 'jlpt': 'N5',
                   'example': 'わたしはごはんをたべる。', 'example_romaji': 'Watashi wa gohan wo taberu.',
                   'example_eng': 'I eat rice.'},
        'のむ': {'romaji': 'nomu', 'meaning': 'to drink', 'jlpt': 'N5',
                 'example': 'まいにちみずをのむ。', 'example_romaji': 'Mainichi mizu wo nomu.',
                 'example_eng': 'I drink water every day.'},
        'いく': {'romaji': 'iku', 'meaning': 'to go', 'jlpt': 'N5',
                 'example': 'がっこうにいく。', 'example_romaji': 'Gakkou ni iku.',
                 'example_eng': 'I go to school.'},
        'くる': {'romaji': 'kuru', 'meaning': 'to come', 'jlpt': 'N5',
                 'example': 'ともだちがくる。', 'example_romaji': 'Tomodachi ga kuru.',
                 'example_eng': 'My friend comes.'},
        'みる': {'romaji': 'miru', 'meaning': 'to see/watch', 'jlpt': 'N5',
                 'example': 'テレビをみる。', 'example_romaji': 'Terebi wo miru.',
                 'example_eng': 'I watch TV.'},
        'よむ': {'romaji': 'yomu', 'meaning': 'to read', 'jlpt': 'N5',
                 'example': 'ほんをよむ。', 'example_romaji': 'Hon wo yomu.',
                 'example_eng': 'I read a book.'},
        'かく': {'romaji': 'kaku', 'meaning': 'to write', 'jlpt': 'N5',
                 'example': 'てがみをかく。', 'example_romaji': 'Tegami wo kaku.',
                 'example_eng': 'I write a letter.'},
        'はなす': {'romaji': 'hanasu', 'meaning': 'to speak', 'jlpt': 'N5',
                   'example': 'にほんごをはなす。', 'example_romaji': 'Nihongo wo hanasu.',
                   'example_eng': 'I speak Japanese.'},
        'する': {'romaji': 'suru', 'meaning': 'to do', 'jlpt': 'N5',
                 'example': 'しゅくだいをする。', 'example_romaji': 'Shukudai wo suru.',
                 'example_eng': 'I do homework.'},
        'ある': {'romaji': 'aru', 'meaning': 'to exist (inanimate)', 'jlpt': 'N5',
                 'example': 'つくえのうえにほんがある。', 'example_romaji': 'Tsukue no ue ni hon ga aru.',
                 'example_eng': 'There is a book on the desk.'},
        'いる': {'romaji': 'iru', 'meaning': 'to exist (animate)', 'jlpt': 'N5',
                 'example': 'へやにねこがいる。', 'example_romaji': 'Heya ni neko ga iru.',
                 'example_eng': 'There is a cat in the room.'},
        'ねる': {'romaji': 'neru', 'meaning': 'to sleep', 'jlpt': 'N5',
                 'example': 'よるにねる。', 'example_romaji': 'Yoru ni neru.',
                 'example_eng': 'Sleep at night.'},
        'おきる': {'romaji': 'okiru', 'meaning': 'to wake up', 'jlpt': 'N5',
                   'example': 'あさにおきる。', 'example_romaji': 'Asa ni okiru.',
                   'example_eng': 'Wake up in the morning.'},
        'はたらく': {'romaji': 'hataraku', 'meaning': 'to work', 'jlpt': 'N5',
                     'example': 'かいしゃではたらく。', 'example_romaji': 'Kaisha de hataraku.',
                     'example_eng': 'Work at a company.'},
        'べんきょうする': {'romaji': 'benkyou suru', 'meaning': 'to study', 'jlpt': 'N5',
                           'example': 'にほんごをべんきょうする。', 'example_romaji': 'Nihongo wo benkyou suru.',
                           'example_eng': 'Study Japanese.'},
        'あう': {'romaji': 'au', 'meaning': 'to meet', 'jlpt': 'N5',
                 'example': 'ともだちにあう。', 'example_romaji': 'Tomodachi ni au.',
                 'example_eng': 'Meet a friend.'},
        'かう': {'romaji': 'kau', 'meaning': 'to buy', 'jlpt': 'N5',
                 'example': 'ほんをかう。', 'example_romaji': 'Hon wo kau.',
                 'example_eng': 'Buy a book.'},
        'うる': {'romaji': 'uru', 'meaning': 'to sell', 'jlpt': 'N5',
                 'example': 'くるまをうる。', 'example_romaji': 'Kuruma wo uru.',
                 'example_eng': 'Sell a car.'},
        'およぐ': {'romaji': 'oyogu', 'meaning': 'to swim', 'jlpt': 'N5',
                   'example': 'プールでおよぐ。', 'example_romaji': 'Puuru de oyogu.',
                   'example_eng': 'Swim in a pool.'},
    },
    'Nouns': {
        'ひと': {'romaji': 'hito', 'meaning': 'person', 'jlpt': 'N5',
                 'example': 'あのひとはだれですか。', 'example_romaji': 'Ano hito wa dare desu ka.',
                 'example_eng': 'Who is that person?'},
        'ともだち': {'romaji': 'tomodachi', 'meaning': 'friend', 'jlpt': 'N5',
                     'example': 'ともだちとえいがをみる。', 'example_romaji': 'Tomodachi to eiga wo miru.',
                     'example_eng': 'I watch a movie with my friend.'},
        'せんせい': {'romaji': 'sensei', 'meaning': 'teacher', 'jlpt': 'N5',
                     'example': 'せんせいはやさしいです。', 'example_romaji': 'Sensei wa yasashii desu.',
                     'example_eng': 'The teacher is kind.'},
        'がくせい': {'romaji': 'gakusei', 'meaning': 'student', 'jlpt': 'N5',
                     'example': 'わたしはがくせいです。', 'example_romaji': 'Watashi wa gakusei desu.',
                     'example_eng': 'I am a student.'},
        'いえ': {'romaji': 'ie', 'meaning': 'house/home', 'jlpt': 'N5',
                 'example': 'いえにかえる。', 'example_romaji': 'Ie ni kaeru.',
                 'example_eng': 'I return home.'},
        'がっこう': {'romaji': 'gakkou', 'meaning': 'school', 'jlpt': 'N5',
                     'example': 'がっこうはたのしい。', 'example_romaji': 'Gakkou wa tanoshii.',
                     'example_eng': 'School is fun.'},
        'えき': {'romaji': 'eki', 'meaning': 'station', 'jlpt': 'N5',
                 'example': 'えきでともだちにあう。', 'example_romaji': 'Eki de tomodachi ni au.',
                 'example_eng': 'I meet my friend at the station.'},
        'ほん': {'romaji': 'hon', 'meaning': 'book', 'jlpt': 'N5',
                 'example': 'ほんをよむ。', 'example_romaji': 'Hon wo yomu.',
                 'example_eng': 'I read a book.'},
        'えんぴつ': {'romaji': 'enpitsu', 'meaning': 'pencil', 'jlpt': 'N5',
                     'example': 'えんぴつでかく。', 'example_romaji': 'Enpitsu de kaku.',
                     'example_eng': 'Write with a pencil.'},
        'かみ': {'romaji': 'kami', 'meaning': 'paper', 'jlpt': 'N5',
                 'example': 'かみにかく。', 'example_romaji': 'Kami ni kaku.',
                 'example_eng': 'Write on paper.'},
        'くるま': {'romaji': 'kuruma', 'meaning': 'car', 'jlpt': 'N5',
                   'example': 'くるまでいく。', 'example_romaji': 'Kuruma de iku.',
                   'example_eng': 'Go by car.'},
        'じてんしゃ': {'romaji': 'jitensha', 'meaning': 'bicycle', 'jlpt': 'N5',
                       'example': 'じてんしゃでいく。', 'example_romaji': 'Jitensha de iku.',
                       'example_eng': 'Go by bicycle.'},
        'でんしゃ': {'romaji': 'densha', 'meaning': 'train', 'jlpt': 'N5',
                     'example': 'でんしゃでいく。', 'example_romaji': 'Densha de iku.',
                     'example_eng': 'Go by train.'},
        'ひこうき': {'romaji': 'hikouki', 'meaning': 'airplane', 'jlpt': 'N5',
                     'example': 'ひこうきでいく。', 'example_romaji': 'Hikouki de iku.',
                     'example_eng': 'Go by airplane.'},
        'ねこ': {'romaji': 'neko', 'meaning': 'cat', 'jlpt': 'N5',
                 'example': 'ねこがすきです。', 'example_romaji': 'Neko ga suki desu.',
                 'example_eng': 'I like cats.'},
        'いぬ': {'romaji': 'inu', 'meaning': 'dog', 'jlpt': 'N5',
                 'example': 'いぬがすきです。', 'example_romaji': 'Inu ga suki desu.',
                 'example_eng': 'I like dogs.'},
        'とり': {'romaji': 'tori', 'meaning': 'bird', 'jlpt': 'N5',
                 'example': 'そらにとりがいる。', 'example_romaji': 'Sora ni tori ga iru.',
                 'example_eng': 'There is a bird in the sky.'},
        'さかな': {'romaji': 'sakana', 'meaning': 'fish', 'jlpt': 'N5',
                   'example': 'さかなを食べる。', 'example_romaji': 'Sakana wo taberu.',
                   'example_eng': 'Eat fish.'},
        'うさぎ': {'romaji': 'usagi', 'meaning': 'rabbit', 'jlpt': 'N5',
                   'example': 'うさぎがかわいい。', 'example_romaji': 'Usagi ga kawaii.',
                   'example_eng': 'The rabbit is cute.'},
    },
    'Time': {
        'いま': {'romaji': 'ima', 'meaning': 'now', 'jlpt': 'N5',
                 'example': 'いまなんじですか。', 'example_romaji': 'Ima nan ji desu ka.',
                 'example_eng': 'What time is it now?'},
        'きょう': {'romaji': 'kyou', 'meaning': 'today', 'jlpt': 'N5',
                   'example': 'きょうはいいてんきです。', 'example_romaji': 'Kyou wa ii tenki desu.',
                   'example_eng': 'Today is good weather.'},
        'あした': {'romaji': 'ashita', 'meaning': 'tomorrow', 'jlpt': 'N5',
                   'example': 'あしたテストがある。', 'example_romaji': 'Ashita tesuto ga aru.',
                   'example_eng': 'There\'s a test tomorrow.'},
        'きのう': {'romaji': 'kinou', 'meaning': 'yesterday', 'jlpt': 'N5',
                   'example': 'きのうえいがをみた。', 'example_romaji': 'Kinou eiga wo mita.',
                   'example_eng': 'I watched a movie yesterday.'},
        'あさ': {'romaji': 'asa', 'meaning': 'morning', 'jlpt': 'N5',
                 'example': 'あさにごはんを食べる。', 'example_romaji': 'Asa ni gohan wo taberu.',
                 'example_eng': 'Eat breakfast in the morning.'},
        'ひる': {'romaji': 'hiru', 'meaning': 'noon', 'jlpt': 'N5',
                 'example': 'ひるにひるごはんを食べる。', 'example_romaji': 'Hiru ni hirugohan wo taberu.',
                 'example_eng': 'Eat lunch at noon.'},
        'ばん': {'romaji': 'ban', 'meaning': 'evening', 'jlpt': 'N5',
                 'example': 'ばんにばんごはんを食べる。', 'example_romaji': 'Ban ni bangohan wo taberu.',
                 'example_eng': 'Eat dinner in the evening.'},
        'よる': {'romaji': 'yoru', 'meaning': 'night', 'jlpt': 'N5',
                 'example': 'よるにねる。', 'example_romaji': 'Yoru ni neru.',
                 'example_eng': 'Sleep at night.'},
        'じかん': {'romaji': 'jikan', 'meaning': 'time/hour', 'jlpt': 'N5',
                   'example': 'じかんがありますか。', 'example_romaji': 'Jikan ga arimasu ka.',
                   'example_eng': 'Do you have time?'},
        'しゅう': {'romaji': 'shuu', 'meaning': 'week', 'jlpt': 'N5',
                   'example': 'いっしゅうかん。', 'example_romaji': 'Isshuukan.',
                   'example_eng': 'One week.'},
        'つき': {'romaji': 'tsuki', 'meaning': 'month', 'jlpt': 'N5',
                 'example': 'いっかげつ。', 'example_romaji': 'Ikkagetsu.',
                 'example_eng': 'One month.'},
        'ねん': {'romaji': 'nen', 'meaning': 'year', 'jlpt': 'N5',
                 'example': 'いちねん。', 'example_romaji': 'Ichinen.',
                 'example_eng': 'One year.'},
    },
    'Question Words': {
        'なに': {'romaji': 'nani', 'meaning': 'what', 'jlpt': 'N5',
                 'example': 'これはなにですか。', 'example_romaji': 'Kore wa nani desu ka.',
                 'example_eng': 'What is this?'},
        'だれ': {'romaji': 'dare', 'meaning': 'who', 'jlpt': 'N5',
                 'example': 'あのひとはだれですか。', 'example_romaji': 'Ano hito wa dare desu ka.',
                 'example_eng': 'Who is that person?'},
        'どこ': {'romaji': 'doko', 'meaning': 'where', 'jlpt': 'N5',
                 'example': 'トイレはどこですか。', 'example_romaji': 'Toire wa doko desu ka.',
                 'example_eng': 'Where is the bathroom?'},
        'いつ': {'romaji': 'itsu', 'meaning': 'when', 'jlpt': 'N5',
                 'example': 'いつひまですか。', 'example_romaji': 'Itsu hima desu ka.',
                 'example_eng': 'When are you free?'},
        'どれ': {'romaji': 'dore', 'meaning': 'which one', 'jlpt': 'N5',
                 'example': 'どれがすきですか。', 'example_romaji': 'Dore ga suki desu ka.',
                 'example_eng': 'Which one do you like?'},
        'どう': {'romaji': 'dou', 'meaning': 'how', 'jlpt': 'N5',
                 'example': 'どうですか。', 'example_romaji': 'Dou desu ka.',
                 'example_eng': 'How is it?'},
        'なぜ': {'romaji': 'naze', 'meaning': 'why', 'jlpt': 'N5',
                 'example': 'なぜですか。', 'example_romaji': 'Naze desu ka.',
                 'example_eng': 'Why?'},
    },
    # Add more categories and words as needed, aiming for 100+ total
}
# ═══════════════════════════════════════════════════════════════
# GRAMMAR PATTERNS (N5–N4 level, fully expanded)
# ═══════════════════════════════════════════════════════════════
GRAMMAR_PATTERNS = [
    {
        'pattern': '～です / ～ます',
        'romaji': '~ desu / ~ masu',
        'meaning': 'Polite present affirmative (to be / verb)',
        'explanation': 'です is the polite copula ("is/am/are"). ます is the polite form of verbs. Used in formal situations and with strangers.',
        'particles': [],
        'examples': [
            {'jp': '私は学生です。', 'romaji': 'Watashi wa gakusei desu.', 'eng': 'I am a student.'},
            {'jp': '毎日日本語を勉強します。', 'romaji': 'Mainichi nihongo o benkyou shimasu.', 'eng': 'I study Japanese every day.'},
        ]
    },
    {
        'pattern': '～ではありません / ～ません',
        'romaji': '~ dewa arimasen / ~ masen',
        'meaning': 'Polite present negative',
        'explanation': 'です → ではありません (or じゃないです casual)\nVerbます → ません',
        'particles': [],
        'examples': [
            {'jp': '私は先生ではありません。', 'romaji': 'Watashi wa sensei dewa arimasen.', 'eng': 'I am not a teacher.'},
            {'jp': '明日行きません。', 'romaji': 'Ashita ikimasen.', 'eng': 'I will not go tomorrow.'},
        ]
    },
    {
        'pattern': '～でした / ～ました',
        'romaji': '~ deshita / ~ mashita',
        'meaning': 'Polite past affirmative',
        'explanation': 'です → でした\nます → ました',
        'particles': [],
        'examples': [
            {'jp': '昨日パーティーでした。', 'romaji': 'Kinou paati- deshita.', 'eng': 'There was a party yesterday.'},
            {'jp': '先週日本へ行きました。', 'romaji': 'Senshuu Nihon e ikimashita.', 'eng': 'I went to Japan last week.'},
        ]
    },
    {
        'pattern': '～たいです',
        'romaji': '~ tai desu',
        'meaning': 'I want to ~',
        'explanation': 'Verb masu-stem + たいです\nExpresses desire. Be careful — it’s personal desire, not asking someone else.',
        'particles': [],
        'examples': [
            {'jp': '日本へ行きたいです。', 'romaji': 'Nihon e ikitai desu.', 'eng': 'I want to go to Japan.'},
            {'jp': 'すしを食べたいです。', 'romaji': 'Sushi o tabetai desu.', 'eng': 'I want to eat sushi.'},
        ]
    },
    {
        'pattern': '～て form + ください',
        'romaji': '~ te kudasai',
        'meaning': 'Please do ~',
        'explanation': 'Polite request. て-form + ください',
        'particles': [],
        'examples': [
            {'jp': '窓を開けてください。', 'romaji': 'Mado o akete kudasai.', 'eng': 'Please open the window.'},
            {'jp': 'ここに座ってください。', 'romaji': 'Koko ni suwatte kudasai.', 'eng': 'Please sit here.'},
        ]
    },
    {
        'pattern': 'Particle は (wa)',
        'romaji': 'wa',
        'meaning': 'Topic marker',
        'explanation': 'Marks what the sentence is about. Contrasts with が (focus).',
        'particles': [('は', 'topic marker')],
        'examples': [
            {'jp': '私は学生です。', 'romaji': 'Watashi wa gakusei desu.', 'eng': 'As for me, I am a student.'},
            {'jp': '象は鼻が長いです。', 'romaji': 'Zou wa hana ga nagai desu.', 'eng': 'Speaking of elephants, their trunks are long.'},
        ]
    },
    {
        'pattern': 'Particle が (ga)',
        'romaji': 'ga',
        'meaning': 'Subject marker / emphasis',
        'explanation': 'Marks the subject, especially in new information or focus.',
        'particles': [('が', 'subject / emphasis')],
        'examples': [
            {'jp': '私が田中です。', 'romaji': 'Watashi ga Tanaka desu.', 'eng': 'I am Tanaka (it’s me).'},
            {'jp': '猫が好きです。', 'romaji': 'Neko ga suki desu.', 'eng': 'I like cats (cats are the thing I like).'},
        ]
    },
    {
        'pattern': 'Particle を (o)',
        'romaji': 'o',
        'meaning': 'Direct object marker',
        'explanation': 'Marks the direct object of a transitive verb.',
        'particles': [('を', 'direct object')],
        'examples': [
            {'jp': '本を読みます。', 'romaji': 'Hon o yomimasu.', 'eng': 'I read a book.'},
            {'jp': '水を飲みます。', 'romaji': 'Mizu o nomimasu.', 'eng': 'I drink water.'},
        ]
    },
    {
        'pattern': 'Particle に (ni)',
        'romaji': 'ni',
        'meaning': 'Direction, time, purpose, indirect object, etc.',
        'explanation': 'Very common particle with many uses.',
        'particles': [('に', 'to / at / for / in order to')],
        'examples': [
            {'jp': '学校に行きます。', 'romaji': 'Gakkou ni ikimasu.', 'eng': 'I go to school.'},
            {'jp': '三時に会います。', 'romaji': 'Sanji ni aimasu.', 'eng': 'We meet at 3 o’clock.'},
            {'jp': '友達にプレゼントをあげます。', 'romaji': 'Tomodachi ni purezento o agemasu.', 'eng': 'I give a present to my friend.'},
        ]
    },
    {
        'pattern': 'Particle で (de)',
        'romaji': 'de',
        'meaning': 'Location of action / means / by',
        'explanation': 'Action happens at this place, or using this method.',
        'particles': [('で', 'at / by / with')],
        'examples': [
            {'jp': '図書館で勉強します。', 'romaji': 'Toshokan de benkyou shimasu.', 'eng': 'I study at the library.'},
            {'jp': '電車で行きます。', 'romaji': 'Densha de ikimasu.', 'eng': 'I go by train.'},
        ]
    },
    # Add more if you want — this is already 10 solid patterns
]
# ═══════════════════════════════════════════════════════════════
# KANJI DATA (Basic Grade 1 Kanji)
# ═══════════════════════════════════════════════════════════════
KANJI = {
    '一': {'reading': 'ichi', 'meaning': 'one', 'jlpt': 'N5',
           'example': '一、二、三', 'example_romaji': 'Ichi, ni, san',
           'example_eng': 'One, two, three'},
    '二': {'reading': 'ni', 'meaning': 'two', 'jlpt': 'N5',
           'example': '二番目', 'example_romaji': 'Nibanme',
           'example_eng': 'Second'},
    '三': {'reading': 'san', 'meaning': 'three', 'jlpt': 'N5',
           'example': '三人', 'example_romaji': 'Sannin',
           'example_eng': 'Three people'},
    '四': {'reading': 'shi', 'meaning': 'four', 'jlpt': 'N5',
           'example': '四季', 'example_romaji': 'Shiki',
           'example_eng': 'Four seasons'},
    '五': {'reading': 'go', 'meaning': 'five', 'jlpt': 'N5',
           'example': '五月', 'example_romaji': 'Gogatsu',
           'example_eng': 'May'},
    '六': {'reading': 'roku', 'meaning': 'six', 'jlpt': 'N5',
           'example': '六時', 'example_romaji': 'Rokuji',
           'example_eng': 'Six o\'clock'},
    '七': {'reading': 'shichi', 'meaning': 'seven', 'jlpt': 'N5',
           'example': '七日', 'example_romaji': 'Nanoka',
           'example_eng': 'Seventh day'},
    '八': {'reading': 'hachi', 'meaning': 'eight', 'jlpt': 'N5',
           'example': '八つ', 'example_romaji': 'Yattsu',
           'example_eng': 'Eight things'},
    '九': {'reading': 'kyuu', 'meaning': 'nine', 'jlpt': 'N5',
           'example': '九月', 'example_romaji': 'Kugatsu',
           'example_eng': 'September'},
    '十': {'reading': 'juu', 'meaning': 'ten', 'jlpt': 'N5',
           'example': '十人', 'example_romaji': 'Juunin',
           'example_eng': 'Ten people'},
    '日': {'reading': 'nichi', 'meaning': 'day/sun', 'jlpt': 'N5',
           'example': '日本', 'example_romaji': 'Nihon',
           'example_eng': 'Japan'},
    '月': {'reading': 'getsu', 'meaning': 'month/moon', 'jlpt': 'N5',
           'example': '月曜日', 'example_romaji': 'Getsuyoubi',
           'example_eng': 'Monday'},
    '火': {'reading': 'ka', 'meaning': 'fire', 'jlpt': 'N5',
           'example': '火曜日', 'example_romaji': 'Kayoubi',
           'example_eng': 'Tuesday'},
    '水': {'reading': 'sui', 'meaning': 'water', 'jlpt': 'N5',
           'example': '水曜日', 'example_romaji': 'Suiyoubi',
           'example_eng': 'Wednesday'},
    '木': {'reading': 'moku', 'meaning': 'tree/wood', 'jlpt': 'N5',
           'example': '木曜日', 'example_romaji': 'Mokuyoubi',
           'example_eng': 'Thursday'},
    '金': {'reading': 'kin', 'meaning': 'gold', 'jlpt': 'N5',
           'example': '金曜日', 'example_romaji': 'Kinyoubi',
           'example_eng': 'Friday'},
    '土': {'reading': 'do', 'meaning': 'soil', 'jlpt': 'N5',
           'example': '土曜日', 'example_romaji': 'Doyoubi',
           'example_eng': 'Saturday'},
    '山': {'reading': 'yama', 'meaning': 'mountain', 'jlpt': 'N5',
           'example': '富士山', 'example_romaji': 'Fujisan',
           'example_eng': 'Mount Fuji'},
    '川': {'reading': 'kawa', 'meaning': 'river', 'jlpt': 'N5',
           'example': '川辺', 'example_romaji': 'Kawabe',
           'example_eng': 'Riverside'},
    '田': {'reading': 'ta', 'meaning': 'rice field', 'jlpt': 'N5',
           'example': '田舎', 'example_romaji': 'Inaka',
           'example_eng': 'Countryside'},
}
# ═══════════════════════════════════════════════════════════════
# ULTRA-PREMIUM THEMES
# ═══════════════════════════════════════════════════════════════
THEMES = {
    'Sakura Bliss': {
        'bg': '#fff0f5', 'fg': '#5d1a3d', 'accent': '#e91e63', 'success': '#ff4081',
        'error': '#ff1744', 'card_bg': '#fff8fb', 'gradient': ('#ff9e9e', '#ff6abf'),
        'particle': '#ff99cc', 'btn_bg': '#ffb3d9'
    },
    'Midnight Zen': {
        'bg': '#0f0f1e', 'fg': '#e0e0ff', 'accent': '#8a4fff', 'success': '#00e676',
        'error': '#ff3d00', 'card_bg': '#1a1a2e', 'gradient': ('#1a0033', '#330066'),
        'particle': '#bb86fc', 'btn_bg': '#533483'
    },
    'Ocean Whisper': {
        'bg': '#e0f7fa', 'fg': '#006064', 'accent': '#00bcd4', 'success': '#1de9b6',
        'error': '#ff5252', 'card_bg': '#b2ebf2', 'gradient': ('#00d4ff', '#0099cc'),
        'particle': '#80deea', 'btn_bg': '#80deea'
    },
    'Golden Hour': {
        'bg': '#fff8e1', 'fg': '#5d4000', 'accent': '#ff8f00', 'success': '#ffd740',
        'error': '#ff3d00', 'card_bg': '#fff3e0', 'gradient': ('#ffcc80', '#ff9800'),
        'particle': '#ffca28', 'btn_bg': '#ffcc80'
    },
    'Classic': {'bg': '#f0f0f0', 'fg': '#000000', 'accent': '#0066cc', 'success': '#00aa00',
                'error': '#cc0000', 'card_bg': '#ffffff', 'btn_bg': '#e0e0e0'},
    'Sakura': {'bg': '#ffe4e1', 'fg': '#5d4037', 'accent': '#d81b60', 'success': '#66bb6a',
               'error': '#ef5350', 'card_bg': '#fff0f5', 'btn_bg': '#ffb3d9'},
    'Ocean': {'bg': '#e0f7fa', 'fg': '#004d40', 'accent': '#0097a7', 'success': '#00796b',
              'error': '#d32f2f', 'card_bg': '#b2ebf2', 'btn_bg': '#80deea'},
    'Dark': {'bg': '#1a1a2e', 'fg': '#eee', 'accent': '#16213e', 'success': '#0f3460',
             'error': '#e94560', 'card_bg': '#0f3460', 'btn_bg': '#533483'},
    'Forest': {'bg': '#d7ffd9', 'fg': '#1b5e20', 'accent': '#388e3c', 'success': '#66bb6a',
               'error': '#e53935', 'card_bg': '#a5d6a7', 'btn_bg': '#81c784'},
}
LAYOUTS = {
    'Desktop': {'font_size': 14, 'kana_size': 80, 'vocab_size': 48, 'padx': 15, 'pady': 5,
                'btn_padx': 20, 'btn_pady': 6, 'scrollbar': True},
    'Mobile': {'font_size': 18, 'kana_size': 100, 'vocab_size': 60, 'padx': 10, 'pady': 10,
               'btn_padx': 30, 'btn_pady': 12, 'scrollbar': False},
}
ACHIEVEMENTS = {
    'first_review': {'name': '🎓 First Review', 'desc': 'Complete your first review'},
    'week_streak': {'name': '🔥 Week Streak', 'desc': '7 days in a row'},
    'master_10': {'name': '⭐ Master 10', 'desc': 'Master 10 cards'},
    'perfect_10': {'name': '💯 Perfect 10', 'desc': '10 correct in a row'},
}
PROGRESS_FILE = 'japanese_progress.json'
# ═══════════════════════════════════════════════════════════════
# FANCY CANVAS PARTICLES (Sakura / Stars / Bubbles)
# ═══════════════════════════════════════════════════════════════
class ParticleEffect:
    def __init__(self, canvas, theme):
        self.canvas = canvas
        self.theme = theme
        self.particles = []
        self.running = False

    def start(self):
        self.running = True
        self._spawn_loop()

    def stop(self):
        self.running = False

    def _spawn_loop(self):
        if not self.running:
            return
        if random.random() < 0.3:
            self._create_particle()
        self.canvas.after(200, self._spawn_loop)

    def _create_particle(self):
        x = random.randint(0, self.canvas.winfo_width())
        y = -20
        size = random.randint(4, 12)
        color = self.theme.colors.get('particle', '#ff99cc')
        speed = random.uniform(1, 4)
        tag = f"particle_{len(self.particles)}"
        item = self.canvas.create_oval(x-size, y-size, x+size, y+size, fill=color, outline=color, tags=tag)
        self.particles.append({'id': item, 'vy': speed, 'vx': random.uniform(-0.5, 0.5)})
        self._animate(item)

    def _animate(self, item):
        if not self.canvas.winfo_exists():
            return
        coords = self.canvas.coords(item)
        if len(coords) != 4 or coords[3] > self.canvas.winfo_height() + 20:
            self.canvas.delete(item)
            return
        self.canvas.move(item, self.particles[0]['vx'], self.particles[0]['vy'])
        self.particles.pop(0)
        self.canvas.after(50, lambda: self._animate(item))

# ═══════════════════════════════════════════════════════════════
# ANIMATED GRADIENT HEADER
# ═══════════════════════════════════════════════════════════════
class GradientHeader(tk.Canvas):
    def __init__(self, parent, text, theme, height=90):
        super().__init__(parent, height=height, highlightthickness=0)
        self.theme = theme
        self.text = text
        self.pack(fill='x')
        self.bind('<Configure>', self._draw)

    def _draw(self, event=None):
        self.delete('all')
        w = self.winfo_width()
        h = self.winfo_height()
        g1, g2 = self.theme.colors.get('gradient', ('#ff9e9e', '#ff6abf'))
        for i in range(h):
            ratio = i / h
            r1, g1_, b1 = int(g1[1:3], 16), int(g1[3:5], 16), int(g1[5:7], 16)
            r2, g2_, b2 = int(g2[1:3], 16), int(g2[3:5], 16), int(g2[5:7], 16)
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1_ + (g2_ - g1_) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.create_line(0, i, w, i, fill=color)
        self.create_text(w//2, h//2, text=self.text, fill='white',
                         font=('Segoe UI', 22, 'bold'), tags='title')

# ═══════════════════════════════════════════════════════════════
# PROGRESS MANAGER
# ═══════════════════════════════════════════════════════════════
class ProgressManager:
    """Manages user progress, SRS data, and achievements."""
   
    def __init__(self, filepath: str = PROGRESS_FILE):
        self.filepath = filepath
        self.data = self._load()
       
    def _load(self) -> Dict[str, Any]:
        """Load progress from JSON file."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Migrate old data to new format
                    return self._migrate_data(data)
            except Exception as e:
                print(f"Error loading progress: {e}")
        return self._default_structure()
   
    def _migrate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate old data format to new format."""
        default = self._default_structure()
       
        # Ensure all top-level keys exist
        for key in default:
            if key not in data:
                data[key] = default[key]
       
        # Ensure nested structures exist
        if 'settings' not in data or not isinstance(data['settings'], dict):
            data['settings'] = default['settings']
        else:
            for key, value in default['settings'].items():
                if key not in data['settings']:
                    data['settings'][key] = value
       
        if 'stats' not in data or not isinstance(data['stats'], dict):
            data['stats'] = default['stats']
        else:
            for key, value in default['stats'].items():
                if key not in data['stats']:
                    data['stats'][key] = value
       
        if 'achievements' not in data or not isinstance(data['achievements'], list):
            data['achievements'] = default['achievements']
       
        # Ensure category dictionaries exist
        for category in ['kana', 'vocab', 'grammar', 'kanji']:
            if category not in data or not isinstance(data[category], dict):
                data[category] = {}
       
        return data
   
    def _default_structure(self) -> Dict[str, Any]:
        """Create default progress structure."""
        today = datetime.now().strftime('%Y-%m-%d')
        return {
            'streak': 0,
            'last_date': today,
            'achievements': [],
            'settings': {
                'theme': 'Sakura Bliss',
                'layout': 'Desktop',
                'sound': True,
                'test_type': 'typing',
                'srs_interval': 1
            },
            'kana': {},
            'vocab': {},
            'grammar': {},
            'kanji': {},
            'stats': {
                'total_reviews': 0,
                'reviews_today': 0,
                'correct_streak': 0,
                'max_streak': 0
            }
        }
   
    def save(self) -> None:
        """Save progress to JSON file."""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving progress: {e}")
   
    def get_card(self, category: str, key: str) -> SRSCard:
        """Get SRS card data for a specific item."""
        if key not in self.data[category]:
            self.data[category][key] = asdict(SRSCard())
        card_data = self.data[category][key]
        return SRSCard(**card_data)
   
    def update_card(self, category: str, key: str, card: SRSCard) -> None:
        """Update SRS card data."""
        self.data[category][key] = asdict(card)
        self.save()
   
    def get_due_items(self, category: str) -> List[str]:
        """Get list of items due for review."""
        today = datetime.now().strftime('%Y-%m-%d')
        due = []
        for key, data in self.data[category].items():
            if data.get('next_review'):
                if data['next_review'] <= today:
                    due.append(key)
            else:
                due.append(key) # New cards
        return due
   
    def update_streak(self) -> int:
        """Update daily streak counter."""
        today = datetime.now().strftime('%Y-%m-%d')
        last_date = self.data.get('last_date', today)
       
        # Initialize streak if missing
        if 'streak' not in self.data:
            self.data['streak'] = 0
       
        if last_date == today:
            return self.data['streak']
       
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        if last_date == yesterday:
            self.data['streak'] += 1
        else:
            self.data['streak'] = 1
       
        self.data['last_date'] = today
       
        # Safely reset reviews_today
        if 'stats' in self.data and 'reviews_today' in self.data['stats']:
            self.data['stats']['reviews_today'] = 0
       
        self.save()
       
        # Check for achievements
        if self.data['streak'] >= 7:
            self.add_achievement('week_streak')
       
        return self.data['streak']
   
    def add_achievement(self, achievement_id: str) -> bool:
        """Add achievement if not already earned."""
        # Ensure achievements list exists
        if 'achievements' not in self.data:
            self.data['achievements'] = []
       
        if achievement_id not in self.data['achievements']:
            self.data['achievements'].append(achievement_id)
            self.save()
            return True
        return False
   
    def increment_stat(self, stat_name: str, amount: int = 1) -> None:
        """Increment a stat counter."""
        # Ensure stats dict exists
        if 'stats' not in self.data:
            self.data['stats'] = {
                'total_reviews': 0,
                'reviews_today': 0,
                'correct_streak': 0,
                'max_streak': 0
            }
       
        if stat_name in self.data['stats']:
            self.data['stats'][stat_name] += amount
            self.save()
   
    def export_to_file(self, filepath: str) -> bool:
        """Export progress to specified file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
   
    def import_from_file(self, filepath: str) -> bool:
        """Import progress from specified file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.save()
            return True
        except Exception as e:
            print(f"Import error: {e}")
            return False
   
    def reset_all(self) -> None:
        """Reset all progress data."""
        self.data = self._default_structure()
        self.save()
# ═══════════════════════════════════════════════════════════════
# SRS SYSTEM (SM-2 Algorithm)
# ═══════════════════════════════════════════════════════════════
class SRSSystem:
    """Implements the SM-2 spaced repetition algorithm."""
   
    @staticmethod
    def review_card(card: SRSCard, quality: int) -> SRSCard:
        """
        Update card based on review quality.
        Quality: 0-2 = fail, 3-5 = pass
        """
        today = datetime.now().strftime('%Y-%m-%d')
        card.last_review = today
       
        if quality < 3:
            # Failed review
            card.repetitions = 0
            card.interval = 1
            card.wrong_count += 1
        else:
            # Passed review
            if card.repetitions == 0:
                card.interval = 1
            elif card.repetitions == 1:
                card.interval = 6
            else:
                card.interval = int(card.interval * card.ease)
           
            card.repetitions += 1
           
            # Update ease factor
            card.ease = max(1.3, card.ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
       
        # Calculate next review date
        next_date = datetime.now() + timedelta(days=card.interval)
        card.next_review = next_date.strftime('%Y-%m-%d')
       
        return card
# ═══════════════════════════════════════════════════════════════
# THEME MANAGER
# ═══════════════════════════════════════════════════════════════
class ThemeManager:
    """Manages application themes and layouts."""
   
    def __init__(self, theme_name: str = 'Sakura Bliss', layout_name: str = 'Desktop'):
        self.current_theme = theme_name
        self.current_layout = layout_name
        self.colors = THEMES[theme_name]
        self.layout = LAYOUTS[layout_name]
   
    def set_theme(self, theme_name: str) -> None:
        """Change current theme."""
        if theme_name in THEMES:
            self.current_theme = theme_name
            self.colors = THEMES[theme_name]
   
    def set_layout(self, layout_name: str) -> None:
        """Change current layout."""
        if layout_name in LAYOUTS:
            self.current_layout = layout_name
            self.layout = LAYOUTS[layout_name]
   
    def get_font(self, size_key: str, weight: str = 'normal') -> Tuple[str, int, str]:
        """Get font configuration."""
        if size_key in self.layout:
            size = self.layout[size_key]
        else:
            size = self.layout['font_size']
        return ('Segoe UI', size, weight)
# ═══════════════════════════════════════════════════════════════
# BASE MODULE CLASS
# ═══════════════════════════════════════════════════════════════
class BaseModule:
    """Base class for learning modules."""
   
    def __init__(self, parent: tk.Widget, progress: ProgressManager,
                 theme: ThemeManager):
        self.parent = parent
        self.progress = progress
        self.theme = theme
        self.frame = tk.Frame(parent, bg=theme.colors['bg'])
       
    def show(self) -> None:
        """Display module frame."""
        self.frame.pack(fill='both', expand=True)
   
    def hide(self) -> None:
        """Hide module frame."""
        self.frame.pack_forget()
   
    def refresh_theme(self) -> None:
        """Refresh UI with current theme."""
        pass # Override in subclasses
# ═══════════════════════════════════════════════════════════════
# HOME MODULE (Dashboard)
# ═══════════════════════════════════════════════════════════════
class HomeModule(BaseModule):
    """Home dashboard with stats and achievements."""
   
    def __init__(self, parent, progress, theme):
        super().__init__(parent, progress, theme)
        self._build_ui()
   
    def _build_ui(self) -> None:
        """Build dashboard UI."""
        # Header
        self.header = GradientHeader(self.frame, '📚 Japanese Learning Dashboard', self.theme)
       
        # Main content with scroll
        canvas = tk.Canvas(self.frame, bg=self.theme.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=canvas.yview)
        content = tk.Frame(canvas, bg=self.theme.colors['bg'])
       
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True, padx=10, pady=5)
       
        canvas_window = canvas.create_window((0, 0), window=content, anchor='nw')
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width-20))
       
        # Stats cards
        stats_frame = tk.Frame(content, bg=self.theme.colors['bg'])
        stats_frame.pack(fill='x', padx=10, pady=10)
       
        streak = self.progress.update_streak()
        self._create_stat_card(stats_frame, '🔥 Daily Streak', f'{streak} days', 0, 0)
        self._create_stat_card(stats_frame, '📝 Reviews Today',
                              str(self.progress.data.get('stats', {}).get('reviews_today', 0)), 0, 1)
        self._create_stat_card(stats_frame, '✅ Total Reviews',
                              str(self.progress.data.get('stats', {}).get('total_reviews', 0)), 1, 0)
        self._create_stat_card(stats_frame, '🎯 Best Streak',
                              str(self.progress.data.get('stats', {}).get('max_streak', 0)), 1, 1)
       
        # Due items summary
        due_frame = tk.Frame(content, bg=self.theme.colors['card_bg'], relief='raised', bd=2)
        due_frame.pack(fill='x', padx=10, pady=10)
       
        tk.Label(due_frame, text='📅 Due for Review', font=self.theme.get_font('font_size', 'bold'),
                bg=self.theme.colors['card_bg'], fg=self.theme.colors['accent']).pack(pady=10)
       
        kana_due = len(self.progress.get_due_items('kana'))
        vocab_due = len(self.progress.get_due_items('vocab'))
        grammar_due = len(self.progress.get_due_items('grammar'))
        kanji_due = len(self.progress.get_due_items('kanji'))
       
        tk.Label(due_frame, text=f'Kana: {kana_due} | Vocabulary: {vocab_due} | Grammar: {grammar_due} | Kanji: {kanji_due}',
                font=self.theme.get_font('font_size'),
                bg=self.theme.colors['card_bg'], fg=self.theme.colors['fg']).pack(pady=5, padx=15)
       
        # Achievements
        achieve_frame = tk.Frame(content, bg=self.theme.colors['card_bg'], relief='raised', bd=2)
        achieve_frame.pack(fill='x', padx=10, pady=10)
       
        tk.Label(achieve_frame, text='🏆 Achievements', font=self.theme.get_font('font_size', 'bold'),
                bg=self.theme.colors['card_bg'], fg=self.theme.colors['accent']).pack(pady=10)
       
        earned = self.progress.data.get('achievements', [])
        for aid, achievement in ACHIEVEMENTS.items():
            unlocked = aid in earned
            color = self.theme.colors['success'] if unlocked else 'gray'
            text = f"{'✓' if unlocked else '🔒'} {achievement['name']}: {achievement['desc']}"
            tk.Label(achieve_frame, text=text, font=self.theme.get_font('font_size'),
                    bg=self.theme.colors['card_bg'], fg=color, anchor='w').pack(fill='x', padx=20, pady=3)
       
        achieve_frame.pack(padx=10, pady=(0, 10))
   
    def _create_stat_card(self, parent, title: str, value: str, row: int, col: int) -> None:
        """Create a statistics card."""
        card = tk.Frame(parent, bg=self.theme.colors['card_bg'], relief='raised', bd=3)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
       
        tk.Label(card, text=title, font=self.theme.get_font('font_size'),
                bg=self.theme.colors['card_bg'], fg=self.theme.colors['fg']).pack(pady=(15, 5))
        tk.Label(card, text=value, font=self.theme.get_font('kana_size', 'bold'),
                bg=self.theme.colors['card_bg'], fg=self.theme.colors['accent']).pack(pady=(0, 15))
# ═══════════════════════════════════════════════════════════════
# KANA MODULE
# ═══════════════════════════════════════════════════════════════
class KanaModule(BaseModule):
    """Kana practice with SRS scheduling."""
   
    def __init__(self, parent, progress, theme):
        super().__init__(parent, progress, theme)
        self.mode = 'Hiragana'
        self.test_type = progress.data['settings']['test_type']
        self.pool = []
        self.current = None
        self.score = 0
        self.asked = 0
        self.correct_streak = 0
        self.wrong_attempts = 0
        self.mc_buttons = []
        self._build_ui()
   
    def _build_ui(self) -> None:
        """Build kana practice UI."""
        # Header
        self.header = GradientHeader(self.frame, '✍️ Kana Practice', self.theme)
       
        # Controls
        control = tk.Frame(self.frame, bg=self.theme.colors['card_bg'], relief='raised', bd=2)
        control.pack(fill='x', padx=10, pady=5)
       
        tk.Label(control, text='Mode:', font=self.theme.get_font('font_size', 'bold'),
                bg=self.theme.colors['card_bg'], fg=self.theme.colors['fg']).pack(side='left', padx=8)
       
        for mode in ['Hiragana', 'Katakana', 'Both']:
            tk.Button(control, text=mode, font=self.theme.get_font('font_size'),
                     bg=self.theme.colors['btn_bg'], fg=self.theme.colors['fg'],
                     command=lambda m=mode: self.start_test(m)).pack(side='left', padx=3)
       
        tk.Button(control, text='Review Due', font=self.theme.get_font('font_size'),
                 bg=self.theme.colors['success'], fg='white',
                 command=self.review_due).pack(side='right', padx=8)
       
        # Scrollable canvas for card content
        canvas = tk.Canvas(self.frame, bg=self.theme.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=canvas.yview)
        self.card_frame = tk.Frame(canvas, bg=self.theme.colors['card_bg'])
       
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True, padx=10, pady=5)
       
        canvas_window = canvas.create_window((0, 0), window=self.card_frame, anchor='nw')
        self.card_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width-20))
       
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
       
        self.kana_label = tk.Label(self.card_frame, text='Select a mode',
                                   font=self.theme.get_font('kana_size', 'bold'),
                                   bg=self.theme.colors['card_bg'], fg=self.theme.colors['accent'])
        self.kana_label.pack(pady=30)
       
        # Hint label
        self.hint_label = tk.Label(self.card_frame, text='', font=self.theme.get_font('font_size'),
                                   bg=self.theme.colors['card_bg'], fg='orange')
        self.hint_label.pack(pady=5)
       
        # Input area (typing)
        self.typing_frame = tk.Frame(self.card_frame, bg=self.theme.colors['card_bg'])
        self.answer_entry = tk.Entry(self.typing_frame, font=self.theme.get_font('font_size'),
                                     justify='center', width=20)
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
       
        tk.Button(self.typing_frame, text='Check', font=self.theme.get_font('font_size', 'bold'),
                 bg=self.theme.colors['success'], fg='white',
                 command=self.check_answer).pack(pady=5)
       
        # Multiple choice area
        self.mc_frame = tk.Frame(self.card_frame, bg=self.theme.colors['card_bg'])
       
        # Feedback
        self.feedback = tk.Label(self.card_frame, text='', font=self.theme.get_font('font_size', 'bold'),
                                bg=self.theme.colors['card_bg'])
        self.feedback.pack(pady=10)
       
        # Stats
        self.stats = tk.Label(self.card_frame, text='Score: 0/0 | Streak: 0',
                             font=self.theme.get_font('font_size'), bg=self.theme.colors['card_bg'],
                             fg=self.theme.colors['fg'])
        self.stats.pack(pady=5)
       
        # Next button
        self.next_btn = tk.Button(self.card_frame, text='Next →',
                                 font=self.theme.get_font('font_size', 'bold'),
                                 bg=self.theme.colors['accent'], fg='white',
                                 command=self.next_card, state='disabled')
        self.next_btn.pack(pady=10)
   
    def start_test(self, mode: str) -> None:
        """Start kana test in specified mode."""
        self.mode = mode
        kana_dict = HIRAGANA if mode == 'Hiragana' else KATAKANA if mode == 'Katakana' else {**HIRAGANA, **KATAKANA}
        self.pool = list(kana_dict.items())
        random.shuffle(self.pool)
        self.score = 0
        self.asked = 0
        self.correct_streak = 0
        self.feedback.config(text=f'{mode} test started!', fg=self.theme.colors['success'])
        self.next_card()
   
    def review_due(self) -> None:
        """Review due kana items."""
        due = self.progress.get_due_items('kana')
        if not due:
            messagebox.showinfo('No Reviews', 'No kana due for review!')
            return
       
        all_kana = {**HIRAGANA, **KATAKANA}
        self.pool = [(char, all_kana[char]) for char in due if char in all_kana]
        random.shuffle(self.pool)
        self.score = 0
        self.asked = 0
        self.correct_streak = 0
        self.feedback.config(text=f'Reviewing {len(self.pool)} due items', fg=self.theme.colors['accent'])
        self.next_card()
   
    def next_card(self) -> None:
        """Show next kana card."""
        if not self.pool:
            self.end_test()
            return
       
        self.current = self.pool.pop()
        self.kana_label.config(text=self.current[0])
        self.hint_label.config(text='')
        self.wrong_attempts = 0
        self.next_btn.config(state='disabled')
        self.feedback.config(text='')
       
        # Setup input method
        if self.test_type == 'typing':
            self.mc_frame.pack_forget()
            self.typing_frame.pack(pady=10)
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.focus()
        else:
            self.typing_frame.pack_forget()
            self.mc_frame.pack(pady=10)
            self._setup_mc()
       
        self._update_stats()
   
    def _setup_mc(self) -> None:
        """Setup multiple choice buttons."""
        for w in self.mc_frame.winfo_children():
            w.destroy()
       
        self.mc_buttons = []
        correct = self.current[1]
        all_vals = list(set({**HIRAGANA, **KATAKANA}.values()))
        wrongs = [v for v in all_vals if v != correct]
        choices = random.sample(wrongs, min(3, len(wrongs))) + [correct]
        random.shuffle(choices)
       
        for ch in choices:
            btn = tk.Button(self.mc_frame, text=ch, font=self.theme.get_font('font_size', 'bold'),
                           width=15, bg='white', fg=self.theme.colors['fg'],
                           command=lambda c=ch: self.check_mc(c))
            btn.pack(pady=4)
            self.mc_buttons.append(btn)
   
    def check_answer(self) -> None:
        """Check typed answer."""
        if not self.current:
            return
       
        user = self.answer_entry.get().strip().lower()
        correct = self.current[1]
        char = self.current[0]
       
        self.asked += 1
        self.progress.increment_stat('total_reviews')
        self.progress.increment_stat('reviews_today')
       
        if user == correct:
            self._handle_correct(char, correct)
        else:
            self._handle_wrong(char, correct)
   
    def check_mc(self, choice: str) -> None:
        """Check multiple choice answer."""
        if not self.current:
            return
       
        char, correct = self.current
        self.asked += 1
        self.progress.increment_stat('total_reviews')
        self.progress.increment_stat('reviews_today')
       
        for btn in self.mc_buttons:
            btn.config(state='disabled')
       
        if choice == correct:
            self._handle_correct(char, correct)
            for btn in self.mc_buttons:
                if btn['text'] == correct:
                    btn.config(bg=self.theme.colors['success'], fg='white')
        else:
            self._handle_wrong(char, correct)
            for btn in self.mc_buttons:
                if btn['text'] == choice:
                    btn.config(bg=self.theme.colors['error'], fg='white')
                elif btn['text'] == correct:
                    btn.config(bg=self.theme.colors['success'], fg='white')
   
    def _handle_correct(self, char: str, correct: str) -> None:
        """Handle correct answer."""
        self.score += 1
        self.correct_streak += 1
       
        # Update stats
        if self.correct_streak > self.progress.data['stats']['max_streak']:
            self.progress.data['stats']['max_streak'] = self.correct_streak
            self.progress.save()
       
        # Check achievements
        if self.correct_streak == 10:
            if self.progress.add_achievement('perfect_10'):
                self._show_confetti()
       
        # Update SRS
        card = self.progress.get_card('kana', char)
        card = SRSSystem.review_card(card, 5)
        self.progress.update_card('kana', char, card)
       
        self.feedback.config(text=f'✓ Correct! {char} = {correct}', fg=self.theme.colors['success'])
        self.next_btn.config(state='normal')
   
    def _handle_wrong(self, char: str, correct: str) -> None:
        """Handle wrong answer."""
        self.correct_streak = 0
        self.wrong_attempts += 1
       
        # Update SRS
        card = self.progress.get_card('kana', char)
        card = SRSSystem.review_card(card, 1)
        self.progress.update_card('kana', char, card)
       
        # Show hint after 2 wrong attempts
        if self.wrong_attempts >= 2:
            self.hint_label.config(text=f'Hint: {correct[0]}...')
       
        self.feedback.config(text=f'✗ Wrong! {char} = {correct}', fg=self.theme.colors['error'])
        self.next_btn.config(state='normal')
   
    def _show_confetti(self) -> None:
        """Show confetti animation for achievement."""
        win = tk.Toplevel(self.frame)
        win.title('Achievement!')
        win.geometry('400x300')
        win.configure(bg='white')
       
        tk.Label(win, text='🎉 Perfect 10 Streak! 🎉', font=('Segoe UI', 24, 'bold'),
                bg='white', fg=self.theme.colors['success']).pack(pady=50)
        tk.Label(win, text='You got 10 correct in a row!', font=('Segoe UI', 16),
                bg='white').pack(pady=20)
        tk.Button(win, text='Awesome!', font=('Segoe UI', 14, 'bold'),
                 bg=self.theme.colors['accent'], fg='white',
                 command=win.destroy).pack(pady=20)
       
        win.after(3000, win.destroy)
   
    def _update_stats(self) -> None:
        """Update statistics display."""
        self.stats.config(text=f'Score: {self.score}/{self.asked} | Streak: {self.correct_streak}')
   
    def end_test(self) -> None:
        """End current test session."""
        self.feedback.config(text='Test complete!', fg=self.theme.colors['success'])
        self.kana_label.config(text='✓')
        messagebox.showinfo('Complete', f'Test finished!\nScore: {self.score}/{self.asked}')
# ═══════════════════════════════════════════════════════════════
# VOCAB MODULE (With Category Selector)
# ═══════════════════════════════════════════════════════════════
class VocabModule(BaseModule):
    """Vocabulary learning with SRS and categories."""
   
    def __init__(self, parent, progress, theme):
        super().__init__(parent, progress, theme)
        self.mode = 'Study'
        self.test_type = progress.data['settings']['test_type']
        self.category = 'All'
        self.pool = []
        self.current = None
        self.score = 0
        self.asked = 0
        self.mc_buttons = []
        self._build_ui()
   
    def _build_ui(self) -> None:
        """Build vocabulary UI."""
        # Header
        self.header = GradientHeader(self.frame, '📖 Vocabulary Study', self.theme)
       
        # Controls
        control = tk.Frame(self.frame, bg=self.theme.colors['card_bg'], relief='raised', bd=2)
        control.pack(fill='x', padx=10, pady=5)
       
        tk.Label(control, text='Category:', font=self.theme.get_font('font_size', 'bold'),
                bg=self.theme.colors['card_bg'], fg=self.theme.colors['fg']).pack(side='left', padx=8)
       
        categories = ['All'] + list(VOCABULARY.keys())
        self.category_var = tk.StringVar(value='All')
        category_menu = ttk.Combobox(control, textvariable=self.category_var, values=categories, state='readonly')
        category_menu.pack(side='left', padx=5)
        category_menu.bind('<<ComboboxSelected>>', lambda e: self._update_category())
       
        tk.Button(control, text='Study Mode', font=self.theme.get_font('font_size'),
                 bg=self.theme.colors['btn_bg'], fg=self.theme.colors['fg'],
                 command=self.start_study).pack(side='left', padx=5, pady=5)
       
        tk.Button(control, text='Test Mode', font=self.theme.get_font('font_size'),
                 bg=self.theme.colors['btn_bg'], fg=self.theme.colors['fg'],
                 command=self.start_test).pack(side='left', padx=5)
       
        tk.Button(control, text='Review Due', font=self.theme.get_font('font_size'),
                 bg=self.theme.colors['success'], fg='white',
                 command=self.review_due).pack(side='right', padx=5)
       
        # Scrollable content
        canvas = tk.Canvas(self.frame, bg=self.theme.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=canvas.yview)
        self.content = tk.Frame(canvas, bg=self.theme.colors['card_bg'])
       
        canvas.configure(yscrollcommand=scrollbar.set)
        if self.theme.layout['scrollbar']:
            scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True, padx=10, pady=5)
       
        canvas_window = canvas.create_window((0, 0), window=self.content, anchor='nw')
        self.content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width-20))
       
        # Word display
        self.word_label = tk.Label(self.content, text='', font=self.theme.get_font('vocab_size', 'bold'),
                                   bg=self.theme.colors['card_bg'], fg=self.theme.colors['accent'])
        self.word_label.pack(pady=20)
       
        # Info panel
        self.info_label = tk.Label(self.content, text='', font=self.theme.get_font('font_size'),
                                   bg=self.theme.colors['card_bg'], fg=self.theme.colors['fg'],
                                   justify='center')
        self.info_label.pack(pady=10)
       
        # Example section
        ex_frame = tk.Frame(self.content, bg=self.theme.colors['bg'], relief='sunken', bd=2)
        ex_frame.pack(fill='x', padx=20, pady=10)
       
        tk.Label(ex_frame, text='Example:', font=self.theme.get_font('font_size', 'bold'),
                bg=self.theme.colors['bg'], fg=self.theme.colors['accent']).pack(pady=5)
       
        self.example_jp = tk.Label(ex_frame, text='', font=self.theme.get_font('font_size'),
                                   bg=self.theme.colors['bg'], fg=self.theme.colors['fg'])
        self.example_jp.pack(pady=3)
       
        self.romaji_frame = tk.Frame(ex_frame, bg=self.theme.colors['bg'])
        self.romaji_frame.pack(pady=3)
       
        self.example_romaji = tk.Label(self.romaji_frame, text='', font=self.theme.get_font('font_size', 'italic'),
                                       bg=self.theme.colors['bg'], fg=self.theme.colors['accent'])
        self.example_romaji.pack(side='left')
       
        self.romaji_hint_btn = tk.Button(self.romaji_frame, text='Show Romaji', font=self.theme.get_font('font_size'),
                                         bg='orange', fg='white', command=self.show_romaji)
        self.romaji_hint_btn.pack(side='left', padx=5)
       
        self.example_eng = tk.Label(ex_frame, text='', font=self.theme.get_font('font_size'),
                                    bg=self.theme.colors['bg'], fg='gray')
        self.example_eng.pack(pady=5)
       
        # Input (typing)
        self.typing_frame = tk.Frame(self.content, bg=self.theme.colors['card_bg'])
        self.answer_entry = tk.Entry(self.typing_frame, font=self.theme.get_font('font_size'),
                                     width=25, justify='center')
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
       
        btn_frame = tk.Frame(self.typing_frame, bg=self.theme.colors['card_bg'])
        btn_frame.pack()
       
        tk.Button(btn_frame, text='Hint', font=self.theme.get_font('font_size'),
                 bg='orange', fg='white', command=self.show_hint).pack(side='left', padx=3)
       
        tk.Button(btn_frame, text='Check', font=self.theme.get_font('font_size', 'bold'),
                 bg=self.theme.colors['success'], fg='white',
                 command=self.check_answer).pack(side='left', padx=3)
       
        # Multiple choice
        self.mc_frame = tk.Frame(self.content, bg=self.theme.colors['card_bg'])
       
        # Feedback
        self.feedback = tk.Label(self.content, text='Select a mode', font=self.theme.get_font('font_size', 'bold'),
                                bg=self.theme.colors['card_bg'], fg=self.theme.colors['accent'])
        self.feedback.pack(pady=10)
       
        # Stats
        self.stats = tk.Label(self.content, text='', font=self.theme.get_font('font_size'),
                             bg=self.theme.colors['card_bg'], fg=self.theme.colors['fg'])
        self.stats.pack(pady=5)
       
        # Next button
        self.next_btn = tk.Button(self.content, text='Next →', font=self.theme.get_font('font_size', 'bold'),
                                 bg=self.theme.colors['accent'], fg='white',
                                 command=self.next_card, state='normal')
        self.next_btn.pack(pady=10)
   
    def _update_category(self) -> None:
        """Update category selection."""
        self.category = self.category_var.get()
        if self.mode in ['Study', 'Test']:
            self.start_mode(self.mode)
   
    def start_study(self) -> None:
        """Start study mode."""
        self.mode = 'Study'
        self._load_pool()
        self.feedback.config(text='Study Mode: Review at your pace', fg=self.theme.colors['success'])
        self.next_card()
   
    def start_test(self) -> None:
        """Start test mode."""
        self.mode = 'Test'
        self._load_pool()
        self.score = 0
        self.asked = 0
        self.feedback.config(text='Test Mode: Type the meaning', fg=self.theme.colors['success'])
        self.next_card()
   
    def _load_pool(self) -> None:
        """Load pool based on category."""
        if self.category == 'All':
            all_words = []
            for cat_words in VOCABULARY.values():
                all_words.extend(cat_words.items())
            self.pool = all_words
        else:
            self.pool = list(VOCABULARY.get(self.category, {}).items())
        random.shuffle(self.pool)
   
    def review_due(self) -> None:
        """Review due vocabulary."""
        due = self.progress.get_due_items('vocab')
        if not due:
            messagebox.showinfo('No Reviews', 'No vocabulary due for review!')
            return
       
        all_vocab = {}
        for cat_words in VOCABULARY.values():
            all_vocab.update(cat_words)
        self.pool = [(w, all_vocab[w]) for w in due if w in all_vocab]
        random.shuffle(self.pool)
        self.mode = 'Test'
        self.score = 0
        self.asked = 0
        self.feedback.config(text=f'Reviewing {len(self.pool)} due words', fg=self.theme.colors['accent'])
        self.next_card()
   
    def next_card(self) -> None:
        """Show next vocabulary card."""
        if not self.pool:
            self.end_session()
            return
       
        self.current = self.pool.pop()
        word, data = self.current
       
        self.word_label.config(text=word)
        self.example_jp.config(text=data.get('example', ''))
        self.example_romaji.config(text='')
        self.romaji_hint_btn.pack_forget()
        self.example_eng.config(text=data.get('example_eng', ''))
       
        self.next_btn.config(state='normal' if self.mode == 'Study' else 'disabled')
        self.feedback.config(text='')
       
        if self.mode == 'Study':
            self.info_label.config(text=f"{data['romaji']}\n{data['meaning']}\nJLPT: {data.get('jlpt', 'N/A')}")
            self.example_romaji.config(text=data.get('example_romaji', ''))
            self.romaji_hint_btn.pack_forget()
            self.typing_frame.pack_forget()
            self.mc_frame.pack_forget()
        else:
            self.info_label.config(text='')
            self.example_eng.config(text='')
            self.example_romaji.config(text='')
            self.romaji_hint_btn.pack(side='left', padx=5)
            self.next_btn.config(state='disabled')
           
            if self.test_type == 'typing':
                self.mc_frame.pack_forget()
                self.typing_frame.pack(pady=10)
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
            else:
                self.typing_frame.pack_forget()
                self.mc_frame.pack(pady=10)
                self._setup_mc()
       
        self._update_stats()
   
    def show_romaji(self) -> None:
        """Show romaji on hint button click in test mode."""
        if self.current and self.mode == 'Test':
            data = self.current[1]
            self.example_romaji.config(text=data.get('example_romaji', ''))
            self.romaji_hint_btn.config(text='Romaji Shown', state='disabled')
   
    def _setup_mc(self) -> None:
        """Setup multiple choice."""
        for w in self.mc_frame.winfo_children():
            w.destroy()
       
        self.mc_buttons = []
        word, data = self.current
        correct = data['meaning']
        all_meanings = []
        for cat_words in VOCABULARY.values():
            all_meanings.extend([v['meaning'] for v in cat_words.values()])
        wrongs = [m for m in all_meanings if m != correct]
        choices = random.sample(wrongs, min(3, len(wrongs))) + [correct]
        random.shuffle(choices)
       
        for ch in choices:
            btn = tk.Button(self.mc_frame, text=ch, font=self.theme.get_font('font_size'),
                           width=20, bg='white', fg=self.theme.colors['fg'],
                           command=lambda c=ch: self.check_mc(c))
            btn.pack(pady=4)
            self.mc_buttons.append(btn)
   
    def show_hint(self) -> None:
        """Show first letter hint."""
        if self.current and self.mode == 'Test':
            meaning = self.current[1]['meaning']
            self.info_label.config(text=f'Hint: {meaning[0]}...')
   
    def check_answer(self) -> None:
        """Check typed answer."""
        if not self.current or self.mode != 'Test':
            return
       
        word, data = self.current
        user = self.answer_entry.get().strip().lower()
        correct = data['meaning'].lower()
       
        self.asked += 1
        self.progress.increment_stat('total_reviews')
        self.progress.increment_stat('reviews_today')
       
        if user == correct or user in correct or correct in user:
            self.score += 1
            card = self.progress.get_card('vocab', word)
            card = SRSSystem.review_card(card, 5)
            self.progress.update_card('vocab', word, card)
            self.feedback.config(text=f'✓ Correct! {word} = {data["meaning"]}',
                               fg=self.theme.colors['success'])
        else:
            card = self.progress.get_card('vocab', word)
            card = SRSSystem.review_card(card, 1)
            self.progress.update_card('vocab', word, card)
            self.feedback.config(text=f'✗ Wrong! {word} = {data["meaning"]}',
                               fg=self.theme.colors['error'])
       
        self.next_btn.config(state='normal')
        self._update_stats()
   
    def check_mc(self, choice: str) -> None:
        """Check multiple choice answer."""
        if not self.current:
            return
       
        word, data = self.current
        correct = data['meaning']
       
        self.asked += 1
        self.progress.increment_stat('total_reviews')
        self.progress.increment_stat('reviews_today')
       
        for btn in self.mc_buttons:
            btn.config(state='disabled')
       
        if choice == correct:
            self.score += 1
            card = self.progress.get_card('vocab', word)
            card = SRSSystem.review_card(card, 5)
            self.progress.update_card('vocab', word, card)
            self.feedback.config(text=f'✓ Correct!', fg=self.theme.colors['success'])
            for btn in self.mc_buttons:
                if btn['text'] == correct:
                    btn.config(bg=self.theme.colors['success'], fg='white')
        else:
            card = self.progress.get_card('vocab', word)
            card = SRSSystem.review_card(card, 1)
            self.progress.update_card('vocab', word, card)
            self.feedback.config(text=f'✗ Wrong! Correct: {correct}', fg=self.theme.colors['error'])
            for btn in self.mc_buttons:
                if btn['text'] == choice:
                    btn.config(bg=self.theme.colors['error'], fg='white')
                elif btn['text'] == correct:
                    btn.config(bg=self.theme.colors['success'], fg='white')
       
        self.next_btn.config(state='normal')
        self._update_stats()
   
    def _update_stats(self) -> None:
        """Update stats display."""
        self.stats.config(text=f'Score: {self.score}/{self.asked}')
   
    def end_session(self) -> None:
        """End vocabulary session."""
        self.feedback.config(text='Session complete!', fg=self.theme.colors['success'])
        if self.mode == 'Test':
            messagebox.showinfo('Complete', f'Test finished!\nScore: {self.score}/{self.asked}')
# ═══════════════════════════════════════════════════════════════
# KANJI MODULE (New!)
# ═══════════════════════════════════════════════════════════════
class KanjiModule(BaseModule):
    """Kanji studying and teaching with SRS."""
   
    def __init__(self, parent, progress, theme):
        super().__init__(parent, progress, theme)
        self.mode = 'Study'
        self.test_type = progress.data['settings']['test_type']
        self.pool = []
        self.current = None
        self.score = 0
        self.asked = 0
        self.mc_buttons = []
        self._build_ui()
   
    def _build_ui(self) -> None:
        """Build kanji UI."""
        # Header
        self.header = GradientHeader(self.frame, '🀄 Kanji Study', self.theme)
       
        # Controls
        control = tk.Frame(self.frame, bg=self.theme.colors['card_bg'], relief='raised', bd=2)
        control.pack(fill='x', padx=10, pady=5)
       
        tk.Button(control, text='Study Mode', font=self.theme.get_font('font_size'),
                 bg=self.theme.colors['btn_bg'], fg=self.theme.colors['fg'],
                 command=self.start_study).pack(side='left', padx=5, pady=5)
       
        tk.Button(control, text='Test Mode', font=self.theme.get_font('font_size'),
                 bg=self.theme.colors['btn_bg'], fg=self.theme.colors['fg'],
                 command=self.start_test).pack(side='left', padx=5)
       
        tk.Button(control, text='Review Due', font=self.theme.get_font('font_size'),
                 bg=self.theme.colors['success'], fg='white',
                 command=self.review_due).pack(side='right', padx=5)
       
        # Scrollable content
        canvas = tk.Canvas(self.frame, bg=self.theme.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=canvas.yview)
        self.content = tk.Frame(canvas, bg=self.theme.colors['card_bg'])
       
        canvas.configure(yscrollcommand=scrollbar.set)
        if self.theme.layout['scrollbar']:
            scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True, padx=10, pady=5)
       
        canvas_window = canvas.create_window((0, 0), window=self.content, anchor='nw')
        self.content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width-20))
       
        # Kanji display
        self.kanji_label = tk.Label(self.content, text='', font=self.theme.get_font('kana_size', 'bold'),
                                    bg=self.theme.colors['card_bg'], fg=self.theme.colors['accent'])
        self.kanji_label.pack(pady=20)
       
        # Info panel
        self.info_label = tk.Label(self.content, text='', font=self.theme.get_font('font_size'),
                                   bg=self.theme.colors['card_bg'], fg=self.theme.colors['fg'],
                                   justify='center')
        self.info_label.pack(pady=10)
       
        # Example section
        ex_frame = tk.Frame(self.content, bg=self.theme.colors['bg'], relief='sunken', bd=2)
        ex_frame.pack(fill='x', padx=20, pady=10)
       
        tk.Label(ex_frame, text='Example:', font=self.theme.get_font('font_size', 'bold'),
                bg=self.theme.colors['bg'], fg=self.theme.colors['accent']).pack(pady=5)
       
        self.example_jp = tk.Label(ex_frame, text='', font=self.theme.get_font('font_size'),
                                   bg=self.theme.colors['bg'], fg=self.theme.colors['fg'])
        self.example_jp.pack(pady=3)
       
        self.romaji_frame = tk.Frame(ex_frame, bg=self.theme.colors['bg'])
        self.romaji_frame.pack(pady=3)
       
        self.example_romaji = tk.Label(self.romaji_frame, text='', font=self.theme.get_font('font_size', 'italic'),
                                       bg=self.theme.colors['bg'], fg=self.theme.colors['accent'])
        self.example_romaji.pack(side='left')
       
        self.romaji_hint_btn = tk.Button(self.romaji_frame, text='Show Romaji', font=self.theme.get_font('font_size'),
                                         bg='orange', fg='white', command=self.show_romaji)
        self.romaji_hint_btn.pack(side='left', padx=5)
       
        self.example_eng = tk.Label(ex_frame, text='', font=self.theme.get_font('font_size'),
                                    bg=self.theme.colors['bg'], fg='gray')
        self.example_eng.pack(pady=5)
       
        # Input (typing)
        self.typing_frame = tk.Frame(self.content, bg=self.theme.colors['card_bg'])
        self.answer_entry = tk.Entry(self.typing_frame, font=self.theme.get_font('font_size'),
                                     width=25, justify='center')
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
       
        btn_frame = tk.Frame(self.typing_frame, bg=self.theme.colors['card_bg'])
        btn_frame.pack()
       
        tk.Button(btn_frame, text='Hint', font=self.theme.get_font('font_size'),
                 bg='orange', fg='white', command=self.show_hint).pack(side='left', padx=3)
       
        tk.Button(btn_frame, text='Check', font=self.theme.get_font('font_size', 'bold'),
                 bg=self.theme.colors['success'], fg='white',
                 command=self.check_answer).pack(side='left', padx=3)
       
        # Multiple choice
        self.mc_frame = tk.Frame(self.content, bg=self.theme.colors['card_bg'])
       
        # Feedback
        self.feedback = tk.Label(self.content, text='Select a mode', font=self.theme.get_font('font_size', 'bold'),
                                bg=self.theme.colors['card_bg'], fg=self.theme.colors['accent'])
        self.feedback.pack(pady=10)
       
        # Stats
        self.stats = tk.Label(self.content, text='', font=self.theme.get_font('font_size'),
                             bg=self.theme.colors['card_bg'], fg=self.theme.colors['fg'])
        self.stats.pack(pady=5)
       
        # Next button
        self.next_btn = tk.Button(self.content, text='Next →', font=self.theme.get_font('font_size', 'bold'),
                                 bg=self.theme.colors['accent'], fg='white',
                                 command=self.next_card, state='normal')
        self.next_btn.pack(pady=10)
   
    def start_study(self) -> None:
        """Start study mode."""
        self.mode = 'Study'
        self.pool = list(KANJI.items())
        random.shuffle(self.pool)
        self.score = 0
        self.asked = 0
        self.feedback.config(text='Study Mode: Review at your pace', fg=self.theme.colors['success'])
        self.next_card()
   
    def start_test(self) -> None:
        """Start test mode."""
        self.mode = 'Test'
        self.pool = list(KANJI.items())
        random.shuffle(self.pool)
        self.score = 0
        self.asked = 0
        self.feedback.config(text='Test Mode: Type the meaning', fg=self.theme.colors['success'])
        self.next_card()
   
    def review_due(self) -> None:
        """Review due kanji."""
        due = self.progress.get_due_items('kanji')
        if not due:
            messagebox.showinfo('No Reviews', 'No kanji due for review!')
            return
       
        self.mode = 'Test'
        self.pool = [(w, KANJI[w]) for w in due if w in KANJI]
        random.shuffle(self.pool)
        self.score = 0
        self.asked = 0
        self.feedback.config(text=f'Reviewing {len(self.pool)} due kanji', fg=self.theme.colors['accent'])
        self.next_card()
   
    def next_card(self) -> None:
        """Show next kanji card."""
        if not self.pool:
            self.end_session()
            return
       
        self.current = self.pool.pop()
        kanji, data = self.current
       
        self.kanji_label.config(text=kanji)
        self.example_jp.config(text=data.get('example', ''))
        self.example_romaji.config(text='')
        self.romaji_hint_btn.pack_forget()
        self.example_eng.config(text=data.get('example_eng', ''))
       
        self.next_btn.config(state='normal' if self.mode == 'Study' else 'disabled')
        self.feedback.config(text='')
       
        if self.mode == 'Study':
            self.info_label.config(text=f"{data['reading']}\n{data['meaning']}\nJLPT: {data.get('jlpt', 'N/A')}")
            self.example_romaji.config(text=data.get('example_romaji', ''))
            self.romaji_hint_btn.pack_forget()
            self.typing_frame.pack_forget()
            self.mc_frame.pack_forget()
        else:
            self.info_label.config(text='')
            self.example_eng.config(text='')
            self.example_romaji.config(text='')
            self.romaji_hint_btn.pack(side='left', padx=5)
            self.next_btn.config(state='disabled')
           
            if self.test_type == 'typing':
                self.mc_frame.pack_forget()
                self.typing_frame.pack(pady=10)
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
            else:
                self.typing_frame.pack_forget()
                self.mc_frame.pack(pady=10)
                self._setup_mc()
       
        self._update_stats()
   
    def show_romaji(self) -> None:
        """Show romaji on hint button click in test mode."""
        if self.current and self.mode == 'Test':
            data = self.current[1]
            self.example_romaji.config(text=data.get('example_romaji', ''))
            self.romaji_hint_btn.config(text='Romaji Shown', state='disabled')
   
    def _setup_mc(self) -> None:
        """Setup multiple choice."""
        for w in self.mc_frame.winfo_children():
            w.destroy()
       
        self.mc_buttons = []
        kanji, data = self.current
        correct = data['meaning']
        all_meanings = [v['meaning'] for v in KANJI.values()]
        wrongs = [m for m in all_meanings if m != correct]
        choices = random.sample(wrongs, min(3, len(wrongs))) + [correct]
        random.shuffle(choices)
       
        for ch in choices:
            btn = tk.Button(self.mc_frame, text=ch, font=self.theme.get_font('font_size'),
                           width=20, bg='white', fg=self.theme.colors['fg'],
                           command=lambda c=ch: self.check_mc(c))
            btn.pack(pady=4)
            self.mc_buttons.append(btn)
   
    def show_hint(self) -> None:
        """Show first letter hint."""
        if self.current and self.mode == 'Test':
            meaning = self.current[1]['meaning']
            self.info_label.config(text=f'Hint: {meaning[0]}...')
   
    def check_answer(self) -> None:
        """Check typed answer."""
        if not self.current or self.mode != 'Test':
            return
       
        kanji, data = self.current
        user = self.answer_entry.get().strip().lower()
        correct = data['meaning'].lower()
       
        self.asked += 1
        self.progress.increment_stat('total_reviews')
        self.progress.increment_stat('reviews_today')
       
        if user == correct or user in correct or correct in user:
            self.score += 1
            card = self.progress.get_card('kanji', kanji)
            card = SRSSystem.review_card(card, 5)
            self.progress.update_card('kanji', kanji, card)
            self.feedback.config(text=f'✓ Correct! {kanji} = {data["meaning"]}',
                               fg=self.theme.colors['success'])
        else:
            card = self.progress.get_card('kanji', kanji)
            card = SRSSystem.review_card(card, 1)
            self.progress.update_card('kanji', kanji, card)
            self.feedback.config(text=f'✗ Wrong! {kanji} = {data["meaning"]}',
                               fg=self.theme.colors['error'])
       
        self.next_btn.config(state='normal')
        self._update_stats()
   
    def check_mc(self, choice: str) -> None:
        """Check multiple choice answer."""
        if not self.current:
            return
       
        kanji, data = self.current
        correct = data['meaning']
       
        self.asked += 1
        self.progress.increment_stat('total_reviews')
        self.progress.increment_stat('reviews_today')
       
        for btn in self.mc_buttons:
            btn.config(state='disabled')
       
        if choice == correct:
            self.score += 1
            card = self.progress.get_card('kanji', kanji)
            card = SRSSystem.review_card(card, 5)
            self.progress.update_card('kanji', kanji, card)
            self.feedback.config(text=f'✓ Correct!', fg=self.theme.colors['success'])
            for btn in self.mc_buttons:
                if btn['text'] == correct:
                    btn.config(bg=self.theme.colors['success'], fg='white')
        else:
            card = self.progress.get_card('kanji', kanji)
            card = SRSSystem.review_card(card, 1)
            self.progress.update_card('kanji', kanji, card)
            self.feedback.config(text=f'✗ Wrong! Correct: {correct}', fg=self.theme.colors['error'])
            for btn in self.mc_buttons:
                if btn['text'] == choice:
                    btn.config(bg=self.theme.colors['error'], fg='white')
                elif btn['text'] == correct:
                    btn.config(bg=self.theme.colors['success'], fg='white')
       
        self.next_btn.config(state='normal')
        self._update_stats()
   
    def _update_stats(self) -> None:
        """Update stats display."""
        self.stats.config(text=f'Score: {self.score}/{self.asked}')
   
    def end_session(self) -> None:
        """End kanji session."""
        self.feedback.config(text='Session complete!', fg=self.theme.colors['success'])
        if self.mode == 'Test':
            messagebox.showinfo('Complete', f'Test finished!\nScore: {self.score}/{self.asked}')
# ═══════════════════════════════════════════════════════════════
# GRAMMAR MODULE (Expanded with interactive practice and breakdowns)
# ═══════════════════════════════════════════════════════════════
class GrammarModule(BaseModule):
    """Grammar patterns with detailed breakdowns and interactive practice."""
   
    def __init__(self, parent, progress, theme):
        super().__init__(parent, progress, theme)
        self.mode = 'Study'
        self.pool = []
        self.current_idx = 0
        self.score = 0
        self.asked = 0
        self.current_pattern = None
        self.practice_type = None  # 'fill_blank' or 'particle_choice'
        self.mc_buttons = []
        self.answer_entry = None
        self._build_ui()
   
    def _build_ui(self) -> None:
        """Build grammar UI."""
        # Header
        self.header = GradientHeader(self.frame, '📝 Grammar Patterns', self.theme)
       
        # Navigation
        nav = tk.Frame(self.frame, bg=self.theme.colors['card_bg'], relief='raised', bd=2)
        nav.pack(fill='x', padx=10, pady=5)
       
        tk.Button(nav, text='← Prev', font=self.theme.get_font('font_size'),
                 bg=self.theme.colors['btn_bg'], fg=self.theme.colors['fg'],
                 command=self.prev_pattern).pack(side='left', padx=5, pady=5)
       
        self.pattern_num = tk.Label(nav, text='', font=self.theme.get_font('font_size', 'bold'),
                                    bg=self.theme.colors['card_bg'], fg=self.theme.colors['fg'])
        self.pattern_num.pack(side='left', expand=True)
       
        tk.Button(nav, text='Next →', font=self.theme.get_font('font_size'),
                 bg=self.theme.colors['btn_bg'], fg=self.theme.colors['fg'],
                 command=self.next_pattern).pack(side='right', padx=5)
       
        tk.Button(nav, text='Practice Mode', font=self.theme.get_font('font_size'),
                 bg=self.theme.colors['success'], fg='white',
                 command=self.start_practice).pack(side='right', padx=5)
       
        # Scrollable content
        canvas = tk.Canvas(self.frame, bg=self.theme.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=canvas.yview)
        self.content = tk.Frame(canvas, bg=self.theme.colors['card_bg'])
       
        canvas.configure(yscrollcommand=scrollbar.set)
        if self.theme.layout['scrollbar']:
            scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True, padx=10, pady=5)
       
        canvas_window = canvas.create_window((0, 0), window=self.content, anchor='nw')
        self.content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width-20))
       
        # Pattern display
        self.pattern_label = tk.Label(self.content, text='', font=self.theme.get_font('font_size', 'bold'),
                                      bg=self.theme.colors['card_bg'], fg=self.theme.colors['accent'])
        self.pattern_label.pack(pady=15)
       
        self.romaji_label = tk.Label(self.content, text='', font=self.theme.get_font('font_size', 'italic'),
                                     bg=self.theme.colors['card_bg'], fg=self.theme.colors['accent'])
        self.romaji_label.pack(pady=5)
       
        self.meaning_label = tk.Label(self.content, text='', font=self.theme.get_font('font_size'),
                                      bg=self.theme.colors['card_bg'], fg=self.theme.colors['success'])
        self.meaning_label.pack(pady=5)
       
        # Explanation
        exp_frame = tk.Frame(self.content, bg=self.theme.colors['bg'], relief='sunken', bd=2)
        exp_frame.pack(fill='x', padx=20, pady=10)
       
        tk.Label(exp_frame, text='Explanation:', font=self.theme.get_font('font_size', 'bold'),
                bg=self.theme.colors['bg'], fg=self.theme.colors['accent']).pack(pady=5)
       
        self.explanation = tk.Label(exp_frame, text='', font=self.theme.get_font('font_size'),
                                    bg=self.theme.colors['bg'], fg=self.theme.colors['fg'],
                                    wraplength=600, justify='left')
        self.explanation.pack(padx=15, pady=10)
       
        # Particles
        particles_frame = tk.Frame(self.content, bg=self.theme.colors['bg'], relief='sunken', bd=2)
        particles_frame.pack(fill='x', padx=20, pady=10)
       
        tk.Label(particles_frame, text='Key Particles:', font=self.theme.get_font('font_size', 'bold'),
                bg=self.theme.colors['bg'], fg=self.theme.colors['accent']).pack(pady=5)
       
        self.particles_label = tk.Label(particles_frame, text='', font=self.theme.get_font('font_size'),
                                        bg=self.theme.colors['bg'], fg=self.theme.colors['fg'],
                                        justify='left')
        self.particles_label.pack(padx=15, pady=10)
       
        # Examples
        self.examples_frame = tk.Frame(self.content, bg=self.theme.colors['bg'], relief='sunken', bd=2)
        self.examples_frame.pack(fill='x', padx=20, pady=10)
       
        tk.Label(self.examples_frame, text='Examples:', font=self.theme.get_font('font_size', 'bold'),
                bg=self.theme.colors['bg'], fg=self.theme.colors['accent']).pack(pady=5)
       
        # Practice section (for practice mode)
        self.practice_frame = tk.Frame(self.content, bg=self.theme.colors['card_bg'])
        self.practice_question = tk.Label(self.practice_frame, text='', font=self.theme.get_font('font_size', 'bold'),
                                          bg=self.theme.colors['card_bg'], fg=self.theme.colors['accent'])
        self.practice_question.pack(pady=10)
       
        self.practice_input_frame = tk.Frame(self.practice_frame, bg=self.theme.colors['card_bg'])
        self.practice_input_frame.pack(pady=5)
       
        self.practice_feedback = tk.Label(self.practice_frame, text='', font=self.theme.get_font('font_size', 'bold'),
                                          bg=self.theme.colors['card_bg'])
        self.practice_feedback.pack(pady=10)
       
        self.practice_next_btn = tk.Button(self.practice_frame, text='Next →', font=self.theme.get_font('font_size', 'bold'),
                                           bg=self.theme.colors['accent'], fg='white',
                                           command=self.next_practice, state='disabled')
        self.practice_next_btn.pack(pady=10)
       
        self.display_pattern()
   
    def display_pattern(self) -> None:
        """Display current grammar pattern in study mode."""
        if not GRAMMAR_PATTERNS:
            return
       
        self.practice_frame.pack_forget()
       
        pattern = GRAMMAR_PATTERNS[self.current_idx]
        self.pattern_label.config(text=pattern['pattern'])
        self.romaji_label.config(text=pattern['romaji'])
        self.meaning_label.config(text=f"→ {pattern['meaning']}")
        self.explanation.config(text=pattern['explanation'])
        self.pattern_num.config(text=f"Pattern {self.current_idx + 1}/{len(GRAMMAR_PATTERNS)}")
       
        # Particles
        particles_text = '\n'.join([f"{p[0]}: {p[1]}" for p in pattern.get('particles', [])])
        self.particles_label.config(text=particles_text)
       
        # Clear and rebuild examples
        for w in self.examples_frame.winfo_children():
            if w.winfo_class() != 'Label' or 'Examples' not in w['text']:
                w.destroy()
       
        for i, ex in enumerate(pattern['examples'], 1):
            card = tk.Frame(self.examples_frame, bg='white', relief='raised', bd=2)
            card.pack(fill='x', padx=15, pady=8)
           
            tk.Label(card, text=f"Example {i}", font=self.theme.get_font('font_size', 'bold'),
                    bg=self.theme.colors['btn_bg'], fg=self.theme.colors['fg']).pack(fill='x')
            tk.Label(card, text=ex['jp'], font=self.theme.get_font('font_size'),
                    bg='white', fg=self.theme.colors['fg']).pack(pady=5, padx=10)
            tk.Label(card, text=ex['romaji'], font=self.theme.get_font('font_size', 'italic'),
                    bg='white', fg=self.theme.colors['accent']).pack(pady=3, padx=10)
            tk.Label(card, text=f"→ {ex['eng']}", font=self.theme.get_font('font_size'),
                    bg='white', fg='gray').pack(pady=5, padx=10)
           
            # Breakdown section
            breakdown_frame = tk.Frame(card, bg='white')
            breakdown_frame.pack(fill='x', pady=5, padx=10)
           
            tk.Label(breakdown_frame, text='Breakdown:', font=self.theme.get_font('font_size', 'bold'),
                     bg='white', fg='purple').pack(anchor='w')
           
            for part, trans in ex.get('breakdown', []):
                tk.Label(breakdown_frame, text=f"{part}: {trans}", font=self.theme.get_font('font_size'),
                         bg='white', fg='navy').pack(anchor='w', padx=5)
   
    def next_pattern(self) -> None:
        """Show next pattern."""
        if self.current_idx < len(GRAMMAR_PATTERNS) - 1:
            self.current_idx += 1
            self.display_pattern()
   
    def prev_pattern(self) -> None:
        """Show previous pattern."""
        if self.current_idx > 0:
            self.current_idx -= 1
            self.display_pattern()
   
    def start_practice(self) -> None:
        """Start interactive practice mode for current pattern."""
        self.mode = 'Practice'
        self.current_pattern = GRAMMAR_PATTERNS[self.current_idx]
        self.pool = self.current_pattern['examples'][:]
        random.shuffle(self.pool)
        self.score = 0
        self.asked = 0
        self.pattern_label.pack_forget()
        self.romaji_label.pack_forget()
        self.meaning_label.pack_forget()
        self.explanation.pack_forget()
        self.particles_label.pack_forget()
        self.examples_frame.pack_forget()
        self.practice_frame.pack(fill='both', expand=True)
        self.practice_feedback.config(text='')
        self.practice_next_btn.config(state='disabled')
        self.next_practice()
   
    def next_practice(self) -> None:
        """Show next practice question."""
        if not self.pool:
            self.end_practice()
            return
       
        self.current = self.pool.pop()
        self.practice_type = random.choice(['fill_blank', 'particle_choice'])
        self.practice_feedback.config(text='')
        self.practice_next_btn.config(state='disabled')
       
        for w in self.practice_input_frame.winfo_children():
            w.destroy()
       
        if self.practice_type == 'fill_blank':
            self._setup_fill_blank()
        else:
            self._setup_particle_choice()
   
    def _setup_fill_blank(self) -> None:
        """Setup fill-in-the-blank practice."""
        sentence = self.current['jp']
        words = sentence.split(' ')  # Simple split, assume space-separated for simplicity
        blank_index = random.randint(0, len(words)-1)
        blank_word = words[blank_index]
        question = ' '.join(words[:blank_index] + ['_____'] + words[blank_index+1:])
       
        self.practice_question.config(text=question)
       
        self.answer_entry = tk.Entry(self.practice_input_frame, font=self.theme.get_font('font_size'))
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', lambda e: self.check_practice())
        self.answer_entry.focus()
       
        tk.Button(self.practice_input_frame, text='Check', font=self.theme.get_font('font_size', 'bold'),
                 bg=self.theme.colors['success'], fg='white',
                 command=self.check_practice).pack(pady=5)
   
    def _setup_particle_choice(self) -> None:
        """Setup particle choice practice."""
        sentence = self.current['jp']
        particles = self.current_pattern['particles']
        if not particles:
            self._setup_fill_blank()  # Fallback
            return
       
        particle_to_replace = random.choice(particles)[0]
        question = sentence.replace(particle_to_replace, '_____')
       
        self.practice_question.config(text=question)
       
        correct = particle_to_replace
        wrongs = [p[0] for p in self.current_pattern['particles'] if p[0] != correct]
        choices = random.sample(wrongs, min(3, len(wrongs))) + [correct]
        random.shuffle(choices)
       
        self.mc_buttons = []
        for ch in choices:
            btn = tk.Button(self.practice_input_frame, text=ch, font=self.theme.get_font('font_size', 'bold'),
                           width=15, bg='white', fg=self.theme.colors['fg'],
                           command=lambda c=ch: self.check_practice_mc(c))
            btn.pack(pady=4)
            self.mc_buttons.append(btn)
   
    def check_practice(self) -> None:
        """Check fill-in-blank answer."""
        user = self.answer_entry.get().strip()
        if self.practice_type == 'fill_blank':
            blank_word = self.current['jp'].split(' ')[random.randint(0, len(self.current['jp'].split(' '))-1)]  # Simplify
            if user == blank_word:
                self.practice_feedback.config(text='✓ Correct!', fg=self.theme.colors['success'])
            else:
                self.practice_feedback.config(text=f'✗ Wrong! Correct: {blank_word}', fg=self.theme.colors['error'])
        self.practice_next_btn.config(state='normal')
   
    def check_practice_mc(self, choice: str) -> None:
        """Check particle choice answer."""
        correct = self.current_pattern['particles'][0][0]  # Simplify for example
        for btn in self.mc_buttons:
            btn.config(state='disabled')
       
        if choice == correct:
            self.practice_feedback.config(text='✓ Correct!', fg=self.theme.colors['success'])
            for btn in self.mc_buttons:
                if btn['text'] == correct:
                    btn.config(bg=self.theme.colors['success'], fg='white')
        else:
            self.practice_feedback.config(text=f'✗ Wrong! Correct: {correct}', fg=self.theme.colors['error'])
            for btn in self.mc_buttons:
                if btn['text'] == choice:
                    btn.config(bg=self.theme.colors['error'], fg='white')
                elif btn['text'] == correct:
                    btn.config(bg=self.theme.colors['success'], fg='white')
       
        self.practice_next_btn.config(state='normal')
   
    def end_practice(self) -> None:
        """End practice session."""
        self.practice_feedback.config(text='Practice complete!', fg=self.theme.colors['success'])
        messagebox.showinfo('Complete', f'Practice finished!\nScore: {self.score}/{self.asked}')
        self.mode = 'Study'
        self.display_pattern()
        self.practice_frame.pack_forget()
        self.pattern_label.pack(pady=15)
        self.romaji_label.pack(pady=5)
        self.meaning_label.pack(pady=5)
        self.explanation.pack(fill='x', padx=20, pady=10)
        self.examples_frame.pack(fill='x', padx=20, pady=10)
# ═══════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════
class JapaneseApp(tk.Tk):
    """Main application class."""
   
    def __init__(self):
        super().__init__()
       
        # Initialize managers
        self.progress = ProgressManager()
       
        # Ensure settings exist (backward compatibility)
        if 'settings' not in self.progress.data:
            self.progress.data['settings'] = {
                'theme': 'Sakura Bliss',
                'layout': 'Desktop',
                'sound': True,
                'test_type': 'typing',
                'srs_interval': 1
            }
            self.progress.save()
       
        # Ensure stats exist (backward compatibility)
        if 'stats' not in self.progress.data:
            self.progress.data['stats'] = {
                'total_reviews': 0,
                'reviews_today': 0,
                'correct_streak': 0,
                'max_streak': 0
            }
            self.progress.save()
       
        # Ensure achievements exist (backward compatibility)
        if 'achievements' not in self.progress.data:
            self.progress.data['achievements'] = []
            self.progress.save()
       
        settings = self.progress.data['settings']
        self.theme = ThemeManager(settings.get('theme', 'Sakura Bliss'),
                                  settings.get('layout', 'Desktop'))
       
        # Window setup
        self.title("🌸 NihonMaster Pro • Japanese Learning App")
        self.geometry("1100x800")
        self.minsize(900, 650)
        self.configure(bg=self.theme.colors['bg'])
       
        # Check first achievement
        if self.progress.data['stats'].get('total_reviews', 0) == 0:
            self.progress.add_achievement('first_review')
       
        # Particle background
        self.bg_canvas = tk.Canvas(self, highlightthickness=0)
        self.bg_canvas.place(relwidth=1, relheight=1)
        self.particles = ParticleEffect(self.bg_canvas, self.theme)
        self.particles.start()

        # Create notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.theme.colors['bg'])
        style.configure('TNotebook.Tab', padding=[20, 12], font=('Segoe UI', 12, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', self.theme.colors['accent'])])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=15)

        # Initialize modules
        self.home_module = HomeModule(self.notebook, self.progress, self.theme)
        self.kana_module = KanaModule(self.notebook, self.progress, self.theme)
        self.vocab_module = VocabModule(self.notebook, self.progress, self.theme)
        self.grammar_module = GrammarModule(self.notebook, self.progress, self.theme)
        self.kanji_module = KanjiModule(self.notebook, self.progress, self.theme)
       
        # Add tabs
        self.notebook.add(self.home_module.frame, text="Home")
        self.notebook.add(self.kana_module.frame, text="Kana")
        self.notebook.add(self.vocab_module.frame, text="Vocab")
        self.notebook.add(self.grammar_module.frame, text="Grammar")
        self.notebook.add(self.kanji_module.frame, text="Kanji")

        # Create menu
        self._create_menu()
       
        # Bind tab change event
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_change)
       
        # Keyboard shortcuts
        self.bind('<space>', lambda e: self._handle_spacebar())
        self.bind('<Return>', lambda e: self._handle_enter())

        self._play_welcome_sound()
   
    def _create_menu(self) -> None:
        """Create application menu bar."""
        menubar = tk.Menu(self, bg='#1e1e2e', fg='white', activebackground='#8a4fff')
        self.config(menu=menubar)
       
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0, bg='#1e1e2e', fg='white')
        menubar.add_cascade(label='Settings', menu=settings_menu)
       
        # Theme submenu
        theme_menu = tk.Menu(settings_menu, tearoff=0, bg='#1e1e2e', fg='white')
        settings_menu.add_cascade(label='Theme', menu=theme_menu)
        for theme_name in THEMES.keys():
            theme_menu.add_command(label=theme_name,
                                  command=lambda t=theme_name: self._change_theme(t))
       
        # Layout submenu
        layout_menu = tk.Menu(settings_menu, tearoff=0, bg='#1e1e2e', fg='white')
        settings_menu.add_cascade(label='Layout', menu=layout_menu)
        for layout_name in LAYOUTS.keys():
            layout_menu.add_command(label=layout_name,
                                   command=lambda l=layout_name: self._change_layout(l))
       
        # Test type submenu
        test_menu = tk.Menu(settings_menu, tearoff=0, bg='#1e1e2e', fg='white')
        settings_menu.add_cascade(label='Test Type', menu=test_menu)
        test_menu.add_command(label='Typing', command=lambda: self._set_test_type('typing'))
        test_menu.add_command(label='Multiple Choice', command=lambda: self._set_test_type('multiple_choice'))
       
        settings_menu.add_separator()
        settings_menu.add_command(label='Export Progress', command=self._export_progress)
        settings_menu.add_command(label='Import Progress', command=self._import_progress)
        settings_menu.add_command(label='Reset All Data', command=self._reset_data)
       
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg='#1e1e2e', fg='white')
        menubar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='About', command=self._show_about)
        help_menu.add_command(label='Keyboard Shortcuts', command=self._show_shortcuts)
   
    def _change_theme(self, theme_name: str) -> None:
        """Change application theme."""
        self.theme.set_theme(theme_name)
        self.progress.data['settings']['theme'] = theme_name
        self.progress.save()
        messagebox.showinfo('Theme Changed', f'Theme changed to {theme_name}!\nRestart app to see full changes.')
        self.home_module.header._draw()
        self.kana_module.header._draw()
        self.vocab_module.header._draw()
        self.grammar_module.header._draw()
        self.kanji_module.header._draw()
   
    def _change_layout(self, layout_name: str) -> None:
        """Change layout mode."""
        self.theme.set_layout(layout_name)
        self.progress.data['settings']['layout'] = layout_name
        self.progress.save()
        messagebox.showinfo('Layout Changed', f'Layout changed to {layout_name}!\nRestart app to see changes.')
   
    def _set_test_type(self, test_type: str) -> None:
        """Set test type preference."""
        self.progress.data['settings']['test_type'] = test_type
        self.progress.save()
        self.kana_module.test_type = test_type
        self.vocab_module.test_type = test_type
        self.kanji_module.test_type = test_type
        messagebox.showinfo('Test Type', f'Test type set to {test_type.replace("_", " ").title()}')
   
    def _export_progress(self) -> None:
        """Export progress to file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
        )
        if filepath:
            if self.progress.export_to_file(filepath):
                messagebox.showinfo('Success', 'Progress exported successfully!')
            else:
                messagebox.showerror('Error', 'Failed to export progress')
   
    def _import_progress(self) -> None:
        """Import progress from file."""
        filepath = filedialog.askopenfilename(
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
        )
        if filepath:
            if self.progress.import_from_file(filepath):
                messagebox.showinfo('Success', 'Progress imported!\nRestart app to see changes.')
            else:
                messagebox.showerror('Error', 'Failed to import progress')
   
    def _reset_data(self) -> None:
        """Reset all progress data."""
        if messagebox.askyesno('Confirm Reset', 'Are you sure you want to reset ALL data?'):
            self.progress.reset_all()
            messagebox.showinfo('Reset', 'All data reset. Restart app.')
   
    def _show_about(self) -> None:
        """Show about dialog."""
        about_text = """Advanced Japanese Learning App
Version 2.0
Features:
• Spaced Repetition System (SM-2)
• Kana (Hiragana & Katakana)
• Vocabulary with Audio
• Grammar Patterns
• Kanji Study
• Progress Tracking
• Daily Streaks & Achievements
Created with Python & Tkinter
"""
        messagebox.showinfo('About', about_text)
   
    def _show_shortcuts(self) -> None:
        """Show keyboard shortcuts."""
        shortcuts = """Keyboard Shortcuts:
Enter - Check answer / Submit
Space - Next card (in some modes)
Tab - Switch between fields
Navigation:
Use the tabs at the top to switch modules
"""
        messagebox.showinfo('Shortcuts', shortcuts)
   
    def _on_tab_change(self, event) -> None:
        """Handle tab change event."""
        current_tab = self.notebook.index(self.notebook.select())
        # Could refresh data here if needed
   
    def _handle_spacebar(self) -> None:
        """Handle spacebar key."""
        # Could implement next card logic
        pass
   
    def _handle_enter(self) -> None:
        """Handle enter key."""
        # Already handled by individual widgets
        pass

    def _play_welcome_sound(self):
        def play():
            freq = 880
            for _ in range(3):
                winsound.Beep(freq, 100)
                freq += 200
                winsound.Beep(freq, 150)
        threading.Thread(target=play, daemon=True).start()
# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    try:
        app = JapaneseApp()
        app.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
"""
Japanese Learning App — Kana, Vocabulary & Sentence Structure
Tabs:
1. Kana Practice (Hiragana, Katakana, Both)
2. Vocabulary Study (100+ words with example sentences)
3. Sentence Structure (Grammar patterns)

Features:
* Typing / Multiple-choice
* Themed UI
* Desktop & Mobile layout toggle (saved)
Run in VSCode with Python 3.7+.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# ──────────────────────────────────────────────────────────────
# Kana Data
# ──────────────────────────────────────────────────────────────
HIRAGANA = {
    'あ': 'a','い': 'i','う': 'u','え': 'e','お': 'o',
    'か': 'ka','き': 'ki','く': 'ku','け': 'ke','こ': 'ko',
    'さ': 'sa','し': 'shi','す': 'su','せ': 'se','そ': 'so',
    'た': 'ta','ち': 'chi','つ': 'tsu','て': 'te','と': 'to',
    'な': 'na','に': 'ni','ぬ': 'nu','ね': 'ne','の': 'no',
    'は': 'ha','ひ': 'hi','ふ': 'fu','へ': 'he','ほ': 'ho',
    'ま': 'ma','み': 'mi','む': 'mu','め': 'me','も': 'mo',
    'や': 'ya','ゆ': 'yu','よ': 'yo',
    'ら': 'ra','り': 'ri','る': 'ru','れ': 're','ろ': 'ro',
    'わ': 'wa','を': 'wo','ん': 'n',
}

KATAKANA = {
    'ア': 'a','イ': 'i','ウ': 'u','エ': 'e','オ': 'o',
    'カ': 'ka','キ': 'ki','ク': 'ku','ケ': 'ke','コ': 'ko',
    'サ': 'sa','シ': 'shi','ス': 'su','セ': 'se','ソ': 'so',
    'タ': 'ta','チ': 'chi','ツ': 'tsu','テ': 'te','ト': 'to',
    'ナ': 'na','ニ': 'ni','ヌ': 'nu','ネ': 'ne','ノ': 'no',
    'ハ': 'ha','ヒ': 'hi','フ': 'fu','ヘ': 'he','ホ': 'ho',
    'マ': 'ma','ミ': 'mi','ム': 'mu','メ': 'me','モ': 'mo',
    'ヤ': 'ya','ユ': 'yu','ヨ': 'yo',
    'ラ': 'ra','リ': 'ri','ル': 'ru','レ': 're','ロ': 'ro',
    'ワ': 'wa','ヲ': 'wo','ン': 'n',
}

# ──────────────────────────────────────────────────────────────
# Vocabulary Data
# ──────────────────────────────────────────────────────────────
VOCABULARY = {
    'こんにちは': {'romaji': 'konnichiwa', 'meaning': 'hello', 'notes': 'Used during daytime', 'example': 'こんにちは、げんきですか。', 'example_romaji': 'Konnichiwa, genki desu ka.', 'example_eng': 'Hello, how are you?'},
    'おはよう': {'romaji': 'ohayou', 'meaning': 'good morning', 'notes': 'Casual morning greeting', 'example': 'おはよう、よくねた。', 'example_romaji': 'Ohayou, yoku neta.', 'example_eng': 'Good morning, I slept well.'},
    'ありがとう': {'romaji': 'arigatou', 'meaning': 'thank you', 'notes': 'Casual thanks', 'example': 'ありがとう、たすかった。', 'example_romaji': 'Arigatou, tasukatta.', 'example_eng': 'Thank you, you helped me.'},
    'すみません': {'romaji': 'sumimasen', 'meaning': 'excuse me/sorry', 'notes': 'Very useful phrase', 'example': 'すみません、えきはどこですか。', 'example_romaji': 'Sumimasen, eki wa doko desu ka.', 'example_eng': 'Excuse me, where is the station?'},
    'はい': {'romaji': 'hai', 'meaning': 'yes', 'notes': 'Affirmative response', 'example': 'はい、わかりました。', 'example_romaji': 'Hai, wakarimashita.', 'example_eng': 'Yes, I understood.'},
    'いいえ': {'romaji': 'iie', 'meaning': 'no', 'notes': 'Negative response', 'example': 'いいえ、ちがいます。', 'example_romaji': 'Iie, chigaimasu.', 'example_eng': 'No, that\'s wrong.'},
    'たべる': {'romaji': 'taberu', 'meaning': 'to eat', 'notes': 'る-verb', 'example': 'わたしはごはんをたべる。', 'example_romaji': 'Watashi wa gohan wo taberu.', 'example_eng': 'I eat rice/meal.'},
    'のむ': {'romaji': 'nomu', 'meaning': 'to drink', 'notes': 'う-verb', 'example': 'まいにちみずをのむ。', 'example_romaji': 'Mainichi mizu wo nomu.', 'example_eng': 'I drink water every day.'},
    'いく': {'romaji': 'iku', 'meaning': 'to go', 'notes': 'う-verb', 'example': 'がっこうにいく。', 'example_romaji': 'Gakkou ni iku.', 'example_eng': 'I go to school.'},
    'くる': {'romaji': 'kuru', 'meaning': 'to come', 'notes': 'Irregular verb', 'example': 'ともだちがくる。', 'example_romaji': 'Tomodachi ga kuru.', 'example_eng': 'My friend comes/will come.'},
    'みる': {'romaji': 'miru', 'meaning': 'to see/watch', 'notes': 'る-verb', 'example': 'テレビをみる。', 'example_romaji': 'Terebi wo miru.', 'example_eng': 'I watch TV.'},
    'よむ': {'romaji': 'yomu', 'meaning': 'to read', 'notes': 'う-verb', 'example': 'ほんをよむ。', 'example_romaji': 'Hon wo yomu.', 'example_eng': 'I read a book.'},
    'かく': {'romaji': 'kaku', 'meaning': 'to write', 'notes': 'う-verb', 'example': 'てがみをかく。', 'example_romaji': 'Tegami wo kaku.', 'example_eng': 'I write a letter.'},
    'はなす': {'romaji': 'hanasu', 'meaning': 'to speak', 'notes': 'う-verb', 'example': 'にほんごをはなす。', 'example_romaji': 'Nihongo wo hanasu.', 'example_eng': 'I speak Japanese.'},
    'する': {'romaji': 'suru', 'meaning': 'to do', 'notes': 'Irregular verb', 'example': 'しゅくだいをする。', 'example_romaji': 'Shukudai wo suru.', 'example_eng': 'I do homework.'},
    'ある': {'romaji': 'aru', 'meaning': 'to exist (inanimate)', 'notes': 'う-verb', 'example': 'つくえのうえにほんがある。', 'example_romaji': 'Tsukue no ue ni hon ga aru.', 'example_eng': 'There is a book on the desk.'},
    'おおきい': {'romaji': 'ookii', 'meaning': 'big', 'notes': 'い-adjective', 'example': 'これはおおきいいえです。', 'example_romaji': 'Kore wa ookii ie desu.', 'example_eng': 'This is a big house.'},
    'ちいさい': {'romaji': 'chiisai', 'meaning': 'small', 'notes': 'い-adjective', 'example': 'ちいさいねこがいる。', 'example_romaji': 'Chiisai neko ga iru.', 'example_eng': 'There is a small cat.'},
    'たかい': {'romaji': 'takai', 'meaning': 'tall/expensive', 'notes': 'い-adjective', 'example': 'このかばんはたかい。', 'example_romaji': 'Kono kaban wa takai.', 'example_eng': 'This bag is expensive.'},
    'やすい': {'romaji': 'yasui', 'meaning': 'cheap', 'notes': 'い-adjective', 'example': 'やすいレストランをさがす。', 'example_romaji': 'Yasui resutoran wo sagasu.', 'example_eng': 'I look for a cheap restaurant.'},
    'いい': {'romaji': 'ii', 'meaning': 'good', 'notes': 'い-adjective (irregular)', 'example': 'いいてんきですね。', 'example_romaji': 'Ii tenki desu ne.', 'example_eng': 'It\'s good weather, isn\'t it?'},
    'きれい': {'romaji': 'kirei', 'meaning': 'pretty/clean', 'notes': 'な-adjective', 'example': 'きれいなはなです。', 'example_romaji': 'Kirei na hana desu.', 'example_eng': 'It\'s a pretty flower.'},
    'いち': {'romaji': 'ichi', 'meaning': 'one', 'notes': 'Number 1', 'example': 'いちにんです。', 'example_romaji': 'Ichi nin desu.', 'example_eng': 'It\'s one person.'},
    'に': {'romaji': 'ni', 'meaning': 'two', 'notes': 'Number 2', 'example': 'にほんください。', 'example_romaji': 'Ni hon kudasai.', 'example_eng': 'Two bottles please.'},
    'さん': {'romaji': 'san', 'meaning': 'three', 'notes': 'Number 3', 'example': 'さんじです。', 'example_romaji': 'San ji desu.', 'example_eng': 'It\'s 3 o\'clock.'},
    'ひと': {'romaji': 'hito', 'meaning': 'person', 'notes': 'General term for person', 'example': 'あのひとはだれですか。', 'example_romaji': 'Ano hito wa dare desu ka.', 'example_eng': 'Who is that person?'},
    'ともだち': {'romaji': 'tomodachi', 'meaning': 'friend', 'notes': 'Friend', 'example': 'ともだちとえいがをみる。', 'example_romaji': 'Tomodachi to eiga wo miru.', 'example_eng': 'I watch a movie with my friend.'},
    'せんせい': {'romaji': 'sensei', 'meaning': 'teacher', 'notes': 'Teacher/master', 'example': 'せんせいはやさしいです。', 'example_romaji': 'Sensei wa yasashii desu.', 'example_eng': 'The teacher is kind.'},
    'がくせい': {'romaji': 'gakusei', 'meaning': 'student', 'notes': 'Student', 'example': 'わたしはがくせいです。', 'example_romaji': 'Watashi wa gakusei desu.', 'example_eng': 'I am a student.'},
    'みず': {'romaji': 'mizu', 'meaning': 'water', 'notes': 'Water', 'example': 'みずをください。', 'example_romaji': 'Mizu wo kudasai.', 'example_eng': 'Water please.'},
    'ごはん': {'romaji': 'gohan', 'meaning': 'rice/meal', 'notes': 'Rice or meal', 'example': 'ごはんをたべましょう。', 'example_romaji': 'Gohan wo tabemashou.', 'example_eng': 'Let\'s eat a meal.'},
    'おちゃ': {'romaji': 'ocha', 'meaning': 'tea', 'notes': 'Japanese tea', 'example': 'おちゃがすきです。', 'example_romaji': 'Ocha ga suki desu.', 'example_eng': 'I like tea.'},
    'いえ': {'romaji': 'ie', 'meaning': 'house/home', 'notes': 'House', 'example': 'いえにかえる。', 'example_romaji': 'Ie ni kaeru.', 'example_eng': 'I return home.'},
    'がっこう': {'romaji': 'gakkou', 'meaning': 'school', 'notes': 'School', 'example': 'がっこうはたのしい。', 'example_romaji': 'Gakkou wa tanoshii.', 'example_eng': 'School is fun.'},
    'えき': {'romaji': 'eki', 'meaning': 'station', 'notes': 'Train station', 'example': 'えきでともだちにあう。', 'example_romaji': 'Eki de tomodachi ni au.', 'example_eng': 'I meet my friend at the station.'},
    'いま': {'romaji': 'ima', 'meaning': 'now', 'notes': 'Current time', 'example': 'いまなんじですか。', 'example_romaji': 'Ima nan ji desu ka.', 'example_eng': 'What time is it now?'},
    'きょう': {'romaji': 'kyou', 'meaning': 'today', 'notes': 'Today', 'example': 'きょうはいいてんきです。', 'example_romaji': 'Kyou wa ii tenki desu.', 'example_eng': 'Today is good weather.'},
    'あした': {'romaji': 'ashita', 'meaning': 'tomorrow', 'notes': 'Tomorrow', 'example': 'あしたテストがある。', 'example_romaji': 'Ashita tesuto ga aru.', 'example_eng': 'There\'s a test tomorrow.'},
    'きのう': {'romaji': 'kinou', 'meaning': 'yesterday', 'notes': 'Yesterday', 'example': 'きのうえいがをみた。', 'example_romaji': 'Kinou eiga wo mita.', 'example_eng': 'I watched a movie yesterday.'},
    'なに': {'romaji': 'nani', 'meaning': 'what', 'notes': 'What', 'example': 'これはなにですか。', 'example_romaji': 'Kore wa nani desu ka.', 'example_eng': 'What is this?'},
    'だれ': {'romaji': 'dare', 'meaning': 'who', 'notes': 'Who', 'example': 'あのひとはだれですか。', 'example_romaji': 'Ano hito wa dare desu ka.', 'example_eng': 'Who is that person?'},
    'どこ': {'romaji': 'doko', 'meaning': 'where', 'notes': 'Where', 'example': 'トイレはどこですか。', 'example_romaji': 'Toire wa doko desu ka.', 'example_eng': 'Where is the bathroom?'},
    'いつ': {'romaji': 'itsu', 'meaning': 'when', 'notes': 'When', 'example': 'いつひまですか。', 'example_romaji': 'Itsu hima desu ka.', 'example_eng': 'When are you free?'},
    'これ': {'romaji': 'kore', 'meaning': 'this', 'notes': 'This (near speaker)', 'example': 'これはわたしのペンです。', 'example_romaji': 'Kore wa watashi no pen desu.', 'example_eng': 'This is my pen.'},
    'それ': {'romaji': 'sore', 'meaning': 'that', 'notes': 'That (near listener)', 'example': 'それはなんですか。', 'example_romaji': 'Sore wa nan desu ka.', 'example_eng': 'What is that?'},
    'あれ': {'romaji': 'are', 'meaning': 'that over there', 'notes': 'That (far from both)', 'example': 'あれはやまです。', 'example_romaji': 'Are wa yama desu.', 'example_eng': 'That over there is a mountain.'},
}

# ──────────────────────────────────────────────────────────────
# Grammar Patterns
# ──────────────────────────────────────────────────────────────
SENTENCE_PATTERNS = [
    {'pattern': '[Subject] は [Noun] です', 'romaji': '[Subject] wa [Noun] desu', 'meaning': '[Subject] is [Noun]', 'explanation': 'Basic sentence structure. "は" (wa) marks the topic, "です" (desu) means "is".',
     'examples': [{'jp': 'わたしはがくせいです。', 'romaji': 'Watashi wa gakusei desu.', 'eng': 'I am a student.'}, {'jp': 'これはほんです。', 'romaji': 'Kore wa hon desu.', 'eng': 'This is a book.'}]},
    {'pattern': '[Subject] は [Object] を [Verb]', 'romaji': '[Subject] wa [Object] wo [Verb]', 'meaning': '[Subject] does [Verb] to [Object]', 'explanation': 'を (wo) marks the direct object. The verb comes at the end.',
     'examples': [{'jp': 'わたしはほんをよむ。', 'romaji': 'Watashi wa hon wo yomu.', 'eng': 'I read a book.'}, {'jp': 'ともだちはコーヒーをのむ。', 'romaji': 'Tomodachi wa koohii wo nomu.', 'eng': 'My friend drinks coffee.'}]},
    {'pattern': '[Noun1] の [Noun2]', 'romaji': '[Noun1] no [Noun2]', 'meaning': '[Noun2] of [Noun1]', 'explanation': 'の shows possession or relationship between nouns.',
     'examples': [{'jp': 'わたしのほん', 'romaji': 'watashi no hon', 'eng': 'my book'}, {'jp': 'せんせいのくるま', 'romaji': 'sensei no kuruma', 'eng': 'teacher\'s car'}]},
    {'pattern': '[Place] に [Verb]', 'romaji': '[Place] ni [Verb]', 'meaning': 'Do [Verb] to/at [Place]', 'explanation': 'に (ni) indicates direction or destination. Used with verbs of motion like いく (go), くる (come).',
     'examples': [{'jp': 'がっこうにいきます。', 'romaji': 'Gakkou ni ikimasu.', 'eng': 'I go to school.'}, {'jp': 'とうきょうにすんでいます。', 'romaji': 'Toukyou ni sunde imasu.', 'eng': 'I live in Tokyo.'}]},
    {'pattern': '[Place] で [Action]', 'romaji': '[Place] de [Action]', 'meaning': 'Do [Action] at [Place]', 'explanation': 'で (de) marks the location where an action takes place.',
     'examples': [{'jp': 'としょかんでべんきょうする。', 'romaji': 'Toshokan de benkyou suru.', 'eng': 'I study at the library.'}, {'jp': 'レストランでごはんをたべる。', 'romaji': 'Resutoran de gohan wo taberu.', 'eng': 'I eat at a restaurant.'}]},
    {'pattern': '[Subject] は [Adjective] です', 'romaji': '[Subject] wa [Adjective] desu', 'meaning': '[Subject] is [Adjective]', 'explanation': 'い-adjectives can be used directly before です. な-adjectives need な before nouns but not before です.',
     'examples': [{'jp': 'このりんごはおいしいです。', 'romaji': 'Kono ringo wa oishii desu.', 'eng': 'This apple is delicious.'}, {'jp': 'かれはしんせつです。', 'romaji': 'Kare wa shinsetsu desu.', 'eng': 'He is kind.'}]},
    {'pattern': '[Person] と [Action]', 'romaji': '[Person] to [Action]', 'meaning': 'Do [Action] with [Person]', 'explanation': 'と (to) means "with" when talking about doing something together.',
     'examples': [{'jp': 'ともだちとあそぶ。', 'romaji': 'Tomodachi to asobu.', 'eng': 'I play with friends.'}, {'jp': 'かぞくとりょこうする。', 'romaji': 'Kazoku to ryokou suru.', 'eng': 'I travel with my family.'}]},
    {'pattern': '[Question word] ですか', 'romaji': '[Question word] desu ka', 'meaning': 'Question form', 'explanation': 'か (ka) at the end makes a sentence a question. Question words include なに (what), だれ (who), どこ (where), いつ (when).',
     'examples': [{'jp': 'これはなんですか。', 'romaji': 'Kore wa nan desu ka.', 'eng': 'What is this?'}, {'jp': 'えきはどこですか。', 'romaji': 'Eki wa doko desu ka.', 'eng': 'Where is the station?'}]},
    {'pattern': '[Verb-ます form] ましょう', 'romaji': '[Verb-masu form] mashou', 'meaning': 'Let\'s do [Verb]', 'explanation': 'ましょう (mashou) is used to suggest doing something together. Attach to the ます-stem of verbs.',
     'examples': [{'jp': 'いっしょにたべましょう。', 'romaji': 'Issho ni tabemashou.', 'eng': 'Let\'s eat together.'}, {'jp': 'えいがをみましょう。', 'romaji': 'Eiga wo mimashou.', 'eng': 'Let\'s watch a movie.'}]},
    {'pattern': '[Verb-ない form] ないでください', 'romaji': '[Verb-nai form] nai de kudasai', 'meaning': 'Please don\'t [Verb]', 'explanation': 'Used to make negative requests. ないで (naide) + ください (kudasai) = please don\'t.',
     'examples': [{'jp': 'ここでたばこをすわないでください。', 'romaji': 'Koko de tabako wo suwanai de kudasai.', 'eng': 'Please don\'t smoke here.'}, {'jp': 'わすれないでください。', 'romaji': 'Wasurenai de kudasai.', 'eng': 'Please don\'t forget.'}]},
    {'pattern': '[Verb-て form] います', 'romaji': '[Verb-te form] imasu', 'meaning': 'Currently doing [Verb] / State of being', 'explanation': 'Indicates an ongoing action or a resulting state. The て-form changes based on verb type.',
     'examples': [{'jp': 'いまべんきょうしています。', 'romaji': 'Ima benkyou shite imasu.', 'eng': 'I am studying now.'}, {'jp': 'めがねをかけています。', 'romaji': 'Megane wo kakete imasu.', 'eng': 'I am wearing glasses.'}]},
    {'pattern': '[Verb-た form]', 'romaji': '[Verb-ta form]', 'meaning': 'Did [Verb] (past tense)', 'explanation': 'た-form indicates completed actions. The conjugation changes based on verb type.',
     'examples': [{'jp': 'きのうえいがをみた。', 'romaji': 'Kinou eiga wo mita.', 'eng': 'I watched a movie yesterday.'}, {'jp': 'ごはんをたべました。', 'romaji': 'Gohan wo tabemashita.', 'eng': 'I ate a meal.'}]},
    {'pattern': '[Adjective-く] なる', 'romaji': '[Adjective-ku] naru', 'meaning': 'Become [Adjective]', 'explanation': 'To express change of state, convert い-adjectives to く form and add なる. For な-adjectives, use に before なる.',
     'examples': [{'jp': 'さむくなりました。', 'romaji': 'Samuku narimashita.', 'eng': 'It became cold.'}, {'jp': 'にほんごがじょうずになりたい。', 'romaji': 'Nihongo ga jouzu ni naritai.', 'eng': 'I want to become good at Japanese.'}]},
    {'pattern': '[Time] に [Action]', 'romaji': '[Time] ni [Action]', 'meaning': 'Do [Action] at [Time]', 'explanation': 'に (ni) marks specific time expressions like hours, days, months.',
     'examples': [{'jp': 'ろくじにおきます。', 'romaji': 'Roku ji ni okimasu.', 'eng': 'I wake up at 6 o\'clock.'}, {'jp': 'げつようびにがっこうにいく。', 'romaji': 'Getsuyoubi ni gakkou ni iku.', 'eng': 'I go to school on Monday.'}]},
    {'pattern': '[Verb] ことができる', 'romaji': '[Verb] koto ga dekiru', 'meaning': 'Can do [Verb] / Able to [Verb]', 'explanation': 'Expresses ability or possibility. Use the dictionary form of the verb before こと.',
     'examples': [{'jp': 'およぐことができます。', 'romaji': 'Oyogu koto ga dekimasu.', 'eng': 'I can swim.'}, {'jp': 'にほんごをはなすことができる。', 'romaji': 'Nihongo wo hanasu koto ga dekiru.', 'eng': 'I can speak Japanese.'}]},
]

# ──────────────────────────────────────────────────────────────
# Theme Presets
# ──────────────────────────────────────────────────────────────
THEMES = {
    'Classic': {'bg': '#f0f0f0', 'fg': '#000000', 'accent': '#0066cc', 'success': '#00aa00', 'error': '#cc0000', 'card_bg': '#ffffff', 'btn_bg': '#e0e0e0'},
    'Sakura': {'bg': '#ffe4e1', 'fg': '#5d4037', 'accent': '#d81b60', 'success': '#66bb6a', 'error': '#ef5350', 'card_bg': '#fff0f5', 'btn_bg': '#ffb3d9'},
    'Ocean': {'bg': '#e0f7fa', 'fg': '#004d40', 'accent': '#0097a7', 'success': '#00796b', 'error': '#d32f2f', 'card_bg': '#b2ebf2', 'btn_bg': '#80deea'},
    'Midnight': {'bg': '#1a1a2e', 'fg': '#eee', 'accent': '#16213e', 'success': '#0f3460', 'error': '#e94560', 'card_bg': '#0f3460', 'btn_bg': '#533483'},
    'Forest': {'bg': '#d7ffd9', 'fg': '#1b5e20', 'accent': '#388e3c', 'success': '#66bb6a', 'error': '#e53935', 'card_bg': '#a5d6a7', 'btn_bg': '#81c784'},
    'Sunset': {'bg': '#fff3e0', 'fg': '#3e2723', 'accent': '#f57c00', 'success': '#689f38', 'error': '#d32f2f', 'card_bg': '#ffe0b2', 'btn_bg': '#ffcc80'},
    'Lavender': {'bg': '#f3e5f5', 'fg': '#4a148c', 'accent': '#7b1fa2', 'success': '#66bb6a', 'error': '#c62828', 'card_bg': '#e1bee7', 'btn_bg': '#ce93d8'},
    'Mint': {'bg': '#e0f2f1', 'fg': '#004d40', 'accent': '#00897b', 'success': '#43a047', 'error': '#e53935', 'card_bg': '#b2dfdb', 'btn_bg': '#80cbc4'},
}

# ──────────────────────────────────────────────────────────────
# Layout Profiles (Desktop vs Mobile)
# ──────────────────────────────────────────────────────────────
LAYOUTS = {
    "Computer": {
        "font_kana": ("Helvetica", 80, "bold"),
        "font_vocab": ("Helvetica", 48, "bold"),
        "font_example_jp": ("Helvetica", 13),
        "font_example_romaji": ("Helvetica", 9, "italic"),
        "font_pattern_title": ("Helvetica", 16, "bold"),
        "font_pattern_romaji": ("Helvetica", 11, "italic"),
        "font_pattern_meaning": ("Helvetica", 11),
        "font_explanation": ("Helvetica", 10),
        "font_example_label": ("Helvetica", 10, "bold"),
        "font_example_jp": ("Helvetica", 16, "bold"),
        "font_example_romaji": ("Helvetica", 11, "italic"),
        "font_example_eng": ("Helvetica", 11),
        "padx": 15, "pady": 5,
        "btn_padx": 20, "btn_pady": 6,
        "entry_font": ("Helvetica", 16),
        "mc_btn_font": ("Helvetica", 14, "bold"),
        "mc_btn_width": 15,
        "scrollbar": True,
        "wraplength": 650,
    },
    "Mobile": {
        "font_kana": ("Helvetica", 100, "bold"),
        "font_vocab": ("Helvetica", 60, "bold"),
        "font_example_jp": ("Helvetica", 16),
        "font_example_romaji": ("Helvetica", 11, "italic"),
        "font_pattern_title": ("Helvetica", 20, "bold"),
        "font_pattern_romaji": ("Helvetica", 14, "italic"),
        "font_pattern_meaning": ("Helvetica", 14),
        "font_explanation": ("Helvetica", 13),
        "font_example_label": ("Helvetica", 13, "bold"),
        "font_example_jp": ("Helvetica", 20, "bold"),
        "font_example_romaji": ("Helvetica", 14, "italic"),
        "font_example_eng": ("Helvetica", 14),
        "padx": 10, "pady": 10,
        "btn_padx": 30, "btn_pady": 12,
        "entry_font": ("Helvetica", 20),
        "mc_btn_font": ("Helvetica", 18, "bold"),
        "mc_btn_width": 0,  # fill full width
        "scrollbar": False,
        "wraplength": 500,
    }
}

PROGRESS_FILE = 'japanese_progress.json'

# ──────────────────────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────────────────────
def build_pool(mode):
    if mode == 'Hiragana':
        return list(HIRAGANA.items())
    elif mode == 'Katakana':
        return list(KATAKANA.items())
    else:
        return list({**HIRAGANA, **KATAKANA}.items())

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_progress(data):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ──────────────────────────────────────────────────────────────
# Main App
# ──────────────────────────────────────────────────────────────
class JapaneseTrainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Japanese Learning Trainer')
        self.geometry('850x650')
        self.resizable(True, True)
        self.minsize(320, 500)

        self.progress = load_progress()
        self.progress.setdefault('Hiragana', {'wrong': []})
        self.progress.setdefault('Katakana', {'wrong': []})
        self.progress.setdefault('Both', {'wrong': []})
        self.progress.setdefault('Vocabulary', {'wrong': []})
        self.progress.setdefault('test_type', 'typing')
        self.progress.setdefault('current_theme', 'Classic')
        self.progress.setdefault('device_mode', 'Computer')

        self.test_type = tk.StringVar(value=self.progress['test_type'])
        self.current_theme_name = self.progress['current_theme']
        self.device_mode = tk.StringVar(value=self.progress['device_mode'])
        self.colors = THEMES[self.current_theme_name].copy()
        self.layout = LAYOUTS[self.device_mode.get()].copy()

        self.apply_theme_and_layout()

        # ── Menu ─────────────────────────────────────
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Settings', menu=settings_menu)
        settings_menu.add_command(label='Choose Theme', command=self.open_theme_selector)

        device_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label='Device Mode', menu=device_menu)
        for mode in ['Computer', 'Mobile']:
            device_menu.add_radiobutton(
                label=mode,
                variable=self.device_mode,
                value=mode,
                command=lambda m=mode: self.set_device_mode(m)
            )

        test_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Test Mode', menu=test_menu)
        test_menu.add_radiobutton(label='Typing Mode', variable=self.test_type, value='typing',
                                  command=self.save_test_type)
        test_menu.add_radiobutton(label='Multiple Choice', variable=self.test_type, value='multiple_choice',
                                  command=self.save_test_type)

        # ── Notebook ─────────────────────────────────
        style = ttk.Style()
        style.configure('TNotebook', background=self.colors['bg'])
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Helvetica', 11, 'bold'))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.kana_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.vocab_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.grammar_tab = tk.Frame(self.notebook, bg=self.colors['bg'])

        self.notebook.add(self.kana_tab, text='Kana')
        self.notebook.add(self.vocab_tab, text='Vocab')
        self.notebook.add(self.grammar_tab, text='Grammar')

        self.init_kana_tab()
        self.init_vocab_tab()
        self.init_grammar_tab()

    # ── Theme & Layout ─────────────────────────────────
    def apply_theme_and_layout(self):
        self.configure(bg=self.colors['bg'])
        self.layout = LAYOUTS[self.device_mode.get()].copy()

    def set_device_mode(self, mode):
        self.device_mode.set(mode)
        self.progress['device_mode'] = mode
        save_progress(self.progress)
        self.apply_theme_and_layout()
        self.rebuild_all_tabs()

    def rebuild_all_tabs(self):
        for tab in (self.kana_tab, self.vocab_tab, self.grammar_tab):
            for child in tab.winfo_children():
                child.destroy()
        self.init_kana_tab()
        self.init_vocab_tab()
        self.init_grammar_tab()

    def save_test_type(self):
        self.progress['test_type'] = self.test_type.get()
        save_progress(self.progress)

    # ── Theme selector ─────────────────────────────────
    def open_theme_selector(self):
        theme_window = tk.Toplevel(self)
        theme_window.title('Choose Theme')
        theme_window.geometry('500x600')
        theme_window.configure(bg='#f5f5f5')

        tk.Label(theme_window, text='Choose Your Theme', font=('Helvetica', 18, 'bold'),
                 bg='#f5f5f5', fg='#333').pack(pady=20)

        canvas = tk.Canvas(theme_window, bg='#f5f5f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(theme_window, orient='vertical', command=canvas.yview)
        theme_frame = tk.Frame(canvas, bg='#f5f5f5')

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        canvas_window = canvas.create_window((0, 0), window=theme_frame, anchor='nw')
        theme_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))

        for theme_name, theme_colors in THEMES.items():
            card = tk.Frame(theme_frame, bg=theme_colors['card_bg'], relief='raised', bd=3)
            card.pack(padx=20, pady=15, fill='x')

            header = tk.Frame(card, bg=theme_colors['bg'], height=60)
            header.pack(fill='x', padx=3, pady=3)

            tk.Label(header, text=f'{theme_name}', font=('Helvetica', 16, 'bold'),
                     bg=theme_colors['bg'], fg=theme_colors['fg']).pack(pady=15)

            preview = tk.Frame(card, bg=theme_colors['card_bg'])
            preview.pack(fill='x', padx=15, pady=10)

            tk.Label(preview, text='Preview:', font=('Helvetica', 10),
                     bg=theme_colors['card_bg'], fg=theme_colors['fg']).pack(anchor='w')

            color_row = tk.Frame(preview, bg=theme_colors['card_bg'])
            color_row.pack(fill='x', pady=5)

            for label, color in [('BG', theme_colors['bg']), ('Text', theme_colors['fg']),
                                 ('Accent', theme_colors['accent']), ('Success', theme_colors['success']),
                                 ('Error', theme_colors['error'])]:
                col = tk.Frame(color_row, bg=theme_colors['card_bg'])
                col.pack(side='left', padx=3)
                tk.Label(col, text=label, font=('Helvetica', 8),
                         bg=theme_colors['card_bg'], fg=theme_colors['fg']).pack()
                tk.Frame(col, bg=color, width=40, height=25).pack()

            tk.Button(card, text='Apply This Theme', font=('Helvetica', 11, 'bold'),
                      bg=theme_colors['btn_bg'], fg=theme_colors['fg'],
                      activebackground=theme_colors['accent'], activeforeground='white',
                      relief='raised', bd=2, padx=20, pady=8,
                      command=lambda t=theme_name: self.apply_theme_selection(t, theme_window)).pack(pady=10)

    def apply_theme_selection(self, theme_name, window):
        self.current_theme_name = theme_name
        self.colors = THEMES[theme_name].copy()
        self.progress['current_theme'] = theme_name
        save_progress(self.progress)
        window.destroy()
        self.apply_theme_and_layout()
        self.rebuild_all_tabs()
        messagebox.showinfo('Theme Applied', f'{theme_name} theme applied!')

    # ── KANA TAB ───────────────────────────────────────
    def init_kana_tab(self):
        L = self.layout
        self.mode = tk.StringVar(value='Hiragana')
        self.current = None
        self.score = self.asked = 0
        self.wrong_in_session = []
        self.answer_checked = False
        self.last_answer_correct = False
        self.mc_buttons = []

        self.pool = build_pool(self.mode.get())
        random.shuffle(self.pool)

        # Header
        header = tk.Frame(self.kana_tab, bg=self.colors['accent'], height=60)
        header.pack(fill='x', pady=(0, L['pady']))
        header.pack_propagate(False)
        tk.Label(header, text='Kana Practice', font=('Helvetica', 16, 'bold'),
                 bg=self.colors['accent'], fg='white').pack(pady=15)

        # Control panel
        control_panel = tk.Frame(self.kana_tab, bg=self.colors['card_bg'], relief='raised', bd=2)
        control_panel.pack(fill='x', padx=L['padx'], pady=L['pady'])

        tk.Label(control_panel, text='Choose Test:', font=('Helvetica', 10, 'bold'),
                 bg=self.colors['card_bg'], fg=self.colors['fg']).pack(side='left', padx=8, pady=8)

        for mode in ['Hiragana', 'Katakana', 'Both']:
            tk.Button(control_panel, text=mode, font=('Helvetica', 9, 'bold'),
                      bg=self.colors['btn_bg'], fg=self.colors['fg'],
                      activebackground=self.colors['accent'], activeforeground='white',
                      relief='raised', bd=2, padx=12, pady=4,
                      command=lambda m=mode: self.start_test(m)).pack(side='left', padx=3)

        tk.Button(control_panel, text='Review Wrong', font=('Helvetica', 9, 'bold'),
                  bg=self.colors['error'], fg='white',
                  activebackground='#8b0000', activeforeground='white',
                  relief='raised', bd=2, padx=12, pady=4,
                  command=self.review_wrong).pack(side='right', padx=8)

        # Main card
        main_card = tk.Frame(self.kana_tab, bg=self.colors['card_bg'], relief='raised', bd=3)
        main_card.pack(fill='both', expand=True, padx=L['padx'], pady=L['pady'])

        self.kana_label = tk.Label(main_card, text='', font=L['font_kana'],
                                   bg=self.colors['card_bg'], fg=self.colors['accent'])
        self.kana_label.pack(pady=20)

        # Typing area
        self.typing_frame = tk.Frame(main_card, bg=self.colors['card_bg'])
        self.typing_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(self.typing_frame, text='Type your answer:', font=('Helvetica', 10),
                 bg=self.colors['card_bg'], fg=self.colors['fg']).pack()
        self.answer_entry = tk.Entry(self.typing_frame, font=L['entry_font'], justify='center',
                                     bg='white', fg=self.colors['fg'], relief='solid', bd=2)
        self.answer_entry.pack(pady=8, fill='x', padx=40)

        typing_btns = tk.Frame(self.typing_frame, bg=self.colors['card_bg'])
        typing_btns.pack(pady=8)
        tk.Button(typing_btns, text='Check', font=('Helvetica', 10, 'bold'),
                  bg=self.colors['success'], fg='white', activebackground='#006400',
                  relief='raised', bd=2, padx=L['btn_padx'], pady=L['btn_pady'],
                  command=self.check_answer).pack(side='left', padx=4)

        # Multiple-choice area
        self.mc_frame = tk.Frame(main_card, bg=self.colors['card_bg'])

        # Next button
        self.next_btn = tk.Button(main_card, text='Next', font=('Helvetica', 10, 'bold'),
                                  bg=self.colors['accent'], fg='white', activebackground='#004080',
                                  relief='raised', bd=2, padx=L['btn_padx'], pady=L['btn_pady'],
                                  command=self.next_card)
        self.next_btn.pack(pady=8)

        self.feedback = tk.Label(main_card, text='Select a test to begin.',
                                 font=('Helvetica', 11, 'bold'),
                                 bg=self.colors['card_bg'], fg=self.colors['accent'])
        self.feedback.pack(pady=10)

        self.stats = tk.Label(main_card, text='Score: 0/0', font=('Helvetica', 12, 'bold'),
                              bg=self.colors['card_bg'], fg=self.colors['fg'])
        self.stats.pack(pady=5)

    # ── Kana logic ─────────────────────────────────────
    def start_test(self, mode):
        self.mode.set(mode)
        self.pool = build_pool(mode)
        random.shuffle(self.pool)
        self.score = self.asked = 0
        self.wrong_in_session = []
        self.feedback.config(text=f'{mode} Test started!', fg=self.colors['success'])
        self.new_round()

    def review_wrong(self):
        mode = self.mode.get()
        wrong = self.progress.get(mode, {}).get('wrong', [])
        if not wrong:
            messagebox.showinfo('No Mistakes', f'No wrong kana saved for {mode}!')
            return
        combined = {**HIRAGANA, **KATAKANA}
        self.pool = [(c, combined[c]) for c in wrong if c in combined]
        random.shuffle(self.pool)
        self.score = self.asked = 0
        self.wrong_in_session = []
        self.feedback.config(text=f'Reviewing mistakes for {mode}.', fg=self.colors['accent'])
        self.new_round()

    def new_round(self):
        if not self.pool:
            self.feedback.config(text='Test complete!', fg=self.colors['success'])
            self.end_test()
            return

        self.current = self.pool.pop()
        self.kana_label.config(text=self.current[0])
        self.answer_checked = False
        self.last_answer_correct = False
        self.next_btn.config(state='disabled')

        if self.test_type.get() == 'typing':
            self.mc_frame.pack_forget()
            self.typing_frame.pack(fill='x', padx=20, pady=10)
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.focus()
        else:
            self.typing_frame.pack_forget()
            self.mc_frame.pack(fill='x', padx=20, pady=10)
            self.setup_multiple_choice()

        self.update_stats()

    def setup_multiple_choice(self):
        for w in self.mc_frame.winfo_children():
            w.destroy()
        self.mc_buttons = []
        correct = self.current[1]
        all_vals = list(set({**HIRAGANA, **KATAKANA}.values()))
        wrongs = [v for v in all_vals if v != correct]
        choices = random.sample(wrongs, min(3, len(wrongs))) + [correct]
        random.shuffle(choices)

        tk.Label(self.mc_frame, text='Choose the correct reading:', font=('Helvetica', 10),
                 bg=self.colors['card_bg'], fg=self.colors['fg']).pack(pady=8)

        for ch in choices:
            btn = tk.Button(self.mc_frame, text=ch, font=self.layout['mc_btn_font'],
                            bg='white', fg=self.colors['fg'],
                            activebackground=self.colors['accent'], activeforeground='white',
                            relief='raised', bd=3, padx=25, pady=10,
                            width=self.layout['mc_btn_width'] if self.layout['mc_btn_width'] > 0 else None,
                            command=lambda c=ch: self.check_mc_answer(c))
            btn.pack(pady=4, fill='x' if self.layout['mc_btn_width'] == 0 else 'none', padx=40 if self.layout['mc_btn_width'] == 0 else 0)
            self.mc_buttons.append(btn)

    def check_mc_answer(self, choice):
        if self.answer_checked: return
        char, correct = self.current
        self.asked += 1
        self.answer_checked = True

        if choice == correct:
            self.score += 1
            self.last_answer_correct = True
            self.feedback.config(text=f'Correct! {char} = {correct}', fg=self.colors['success'])
            for b in self.mc_buttons:
                if b['text'] == correct:
                    b.config(bg=self.colors['success'], fg='white')
        else:
            self.last_answer_correct = False
            self.wrong_in_session.append(char)
            self.feedback.config(text=f'Incorrect — {char} = {correct}', fg=self.colors['error'])
            for b in self.mc_buttons:
                if b['text'] == choice:
                    b.config(bg=self.colors['error'], fg='white')
                elif b['text'] == correct:
                    b.config(bg=self.colors['success'], fg='white')

        for b in self.mc_buttons:
            b.config(state='disabled')
        self.next_btn.config(state='normal')
        self.update_stats()

    def check_answer(self):
        if not self.current or self.answer_checked: return
        user = self.answer_entry.get().strip().lower()
        char, correct = self.current
        self.asked += 1
        self.answer_checked = True

        if user == correct:
            self.score += 1
            self.last_answer_correct = True
            self.feedback.config(text=f'Correct! {char} = {correct}', fg=self.colors['success'])
        else:
            self.last_answer_correct = False
            self.wrong_in_session.append(char)
            self.feedback.config(text=f'Incorrect — {char} = {correct}', fg=self.colors['error'])

        self.next_btn.config(state='normal')
        self.update_stats()

    def next_card(self):
        self.new_round()

    def update_stats(self):
        self.stats.config(text=f'Score: {self.score}/{self.asked}')

    def end_test(self):
        mode = self.mode.get()
        wrong_set = set(self.progress.get(mode, {}).get('wrong', []))
        wrong_set.update(self.wrong_in_session)
        self.progress[mode]['wrong'] = sorted(list(wrong_set))
        save_progress(self.progress)
        messagebox.showinfo('Test Complete', f'{mode} test finished!\nScore: {self.score}/{self.asked}')

    # ── VOCABULARY TAB ───────────────────────────────────
    def init_vocab_tab(self):
        L = self.layout
        self.vocab_mode = tk.StringVar(value='Study')
        self.current_vocab = None
        self.vocab_score = self.vocab_asked = 0
        self.vocab_wrong_in_session = []
        self.vocab_answer_checked = False
        self.vocab_last_correct = False
        self.vocab_pool = []
        self.vocab_mc_buttons = []

        # Header
        header = tk.Frame(self.vocab_tab, bg=self.colors['accent'], height=60)
        header.pack(fill='x', pady=(0, L['pady']))
        header.pack_propagate(False)
        tk.Label(header, text='Vocabulary Study', font=('Helvetica', 16, 'bold'),
                 bg=self.colors['accent'], fg='white').pack(pady=15)

        # Control panel
        control = tk.Frame(self.vocab_tab, bg=self.colors['card_bg'], relief='raised', bd=2)
        control.pack(fill='x', padx=L['padx'], pady=L['pady'])

        tk.Label(control, text='Mode:', font=('Helvetica', 10, 'bold'),
                 bg=self.colors['card_bg'], fg=self.colors['fg']).pack(side='left', padx=8, pady=8)

        tk.Button(control, text='Study Mode', font=('Helvetica', 9, 'bold'),
                  bg=self.colors['btn_bg'], fg=self.colors['fg'],
                  activebackground=self.colors['accent'], activeforeground='white',
                  relief='raised', bd=2, padx=12, pady=4,
                  command=self.start_vocab_study).pack(side='left', padx=3)

        tk.Button(control, text='Test Mode', font=('Helvetica', 9, 'bold'),
                  bg=self.colors['btn_bg'], fg=self.colors['fg'],
                  activebackground=self.colors['accent'], activeforeground='white',
                  relief='raised', bd=2, padx=12, pady=4,
                  command=self.start_vocab_test).pack(side='left', padx=3)

        tk.Button(control, text='Review Wrong', font=('Helvetica', 9, 'bold'),
                  bg=self.colors['error'], fg='white',
                  activebackground='#8b0000', activeforeground='white',
                  relief='raised', bd=2, padx=12, pady=4,
                  command=self.review_vocab_wrong).pack(side='right', padx=8)

        # Scrolling canvas
        canvas = tk.Canvas(self.vocab_tab, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.vocab_tab, orient='vertical', command=canvas.yview) if L['scrollbar'] else None
        self.vocab_display = tk.Frame(canvas, bg=self.colors['card_bg'])

        canvas.configure(yscrollcommand=scrollbar.set if scrollbar else None)
        if scrollbar:
            scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True, padx=L['padx'], pady=L['pady'])

        cw = canvas.create_window((0, 0), window=self.vocab_display, anchor='nw')
        self.vocab_display.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(cw, width=e.width-30))

        # Content widgets
        self.vocab_japanese = tk.Label(self.vocab_display, text='', font=L['font_vocab'],
                                       bg=self.colors['card_bg'], fg=self.colors['accent'])
        self.vocab_japanese.pack(pady=15)

        self.vocab_info = tk.Label(self.vocab_display, text='', font=('Helvetica', 10),
                                   bg=self.colors['card_bg'], fg=self.colors['fg'], justify='center')
        self.vocab_info.pack(pady=8)

        # Example frame
        self.example_frame = tk.Frame(self.vocab_display, bg=self.colors['bg'], relief='sunken', bd=2)
        self.example_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(self.example_frame, text='Example Sentence', font=('Helvetica', 10, 'bold'),
                 bg=self.colors['bg'], fg=self.colors['accent']).pack(pady=4)
        self.example_jp = tk.Label(self.example_frame, text='', font=L['font_example_jp'],
                                   bg=self.colors['bg'], fg=self.colors['fg'], wraplength=L['wraplength'])
        self.example_jp.pack(pady=4)
        self.example_romaji = tk.Label(self.example_frame, text='', font=L['font_example_romaji'],
                                       bg=self.colors['bg'], fg=self.colors['accent'], wraplength=L['wraplength'])
        self.example_romaji.pack(pady=3)
        self.example_eng = tk.Label(self.example_frame, text='', font=('Helvetica', 9),
                                    bg=self.colors['bg'], fg='gray', wraplength=L['wraplength'])
        self.example_eng.pack(pady=4)

        # Typing test area
        self.vocab_typing_frame = tk.Frame(self.vocab_display, bg=self.colors['card_bg'])
        tk.Label(self.vocab_typing_frame, text='Type the English meaning:', font=('Helvetica', 10),
                 bg=self.colors['card_bg'], fg=self.colors['fg']).pack(pady=8)
        self.vocab_entry = tk.Entry(self.vocab_typing_frame, font=L['entry_font'], justify='center',
                                    bg='white', fg=self.colors['fg'], relief='solid', bd=2, state='disabled')
        self.vocab_entry.pack(pady=8, fill='x', padx=40)

        vocab_btns = tk.Frame(self.vocab_typing_frame, bg=self.colors['card_bg'])
        vocab_btns.pack(pady=8)
        self.vocab_check_btn_typing = tk.Button(vocab_btns, text='Check', font=('Helvetica', 10, 'bold'),
                                                bg=self.colors['success'], fg='white', activebackground='#006400',
                                                relief='raised', bd=2, padx=L['btn_padx'], pady=L['btn_pady'], state='disabled',
                                                command=self.check_vocab_answer)
        self.vocab_check_btn_typing.pack(side='left', padx=4)

        # Multiple-choice area
        self.vocab_mc_frame = tk.Frame(self.vocab_display, bg=self.colors['card_bg'])

        # Common next button
        self.vocab_next_btn = tk.Button(self.vocab_display, text='Next', font=('Helvetica', 10, 'bold'),
                                        bg=self.colors['accent'], fg='white', activebackground='#004080',
                                        relief='raised', bd=2, padx=L['btn_padx'], pady=L['btn_pady'],
                                        command=self.next_vocab_card)
        self.vocab_next_btn.pack(pady=8)

        # Navigation for study mode
        self.vocab_nav_frame = tk.Frame(self.vocab_display, bg=self.colors['card_bg'])
        tk.Button(self.vocab_nav_frame, text='Next Word', font=('Helvetica', 11, 'bold'),
                  bg=self.colors['accent'], fg='white', activebackground='#004080',
                  relief='raised', bd=2, padx=25, pady=8,
                  command=self.next_vocab_card).pack(pady=8)

        self.vocab_feedback = tk.Label(self.vocab_display, text='Select a mode to begin.',
                                       font=('Helvetica', 11, 'bold'),
                                       bg=self.colors['card_bg'], fg=self.colors['accent'])
        self.vocab_feedback.pack(pady=10)

        self.vocab_stats = tk.Label(self.vocab_display, text='Score: 0/0', font=('Helvetica', 12, 'bold'),
                                    bg=self.colors['card_bg'], fg=self.colors['fg'])
        self.vocab_stats.pack(pady=5)

    # ── Vocabulary logic ─────────────────────────────────
    def start_vocab_study(self):
        self.vocab_mode.set('Study')
        self.vocab_pool = list(VOCABULARY.items())
        random.shuffle(self.vocab_pool)
        self.vocab_score = self.vocab_asked = 0
        self.vocab_wrong_in_session = []
        self.vocab_feedback.config(text='Study Mode: Review at your own pace', fg=self.colors['success'])
        self.next_vocab_card()

    def start_vocab_test(self):
        self.vocab_mode.set('Test')
        self.vocab_pool = list(VOCABULARY.items())
        random.shuffle(self.vocab_pool)
        self.vocab_score = self.vocab_asked = 0
        self.vocab_wrong_in_session = []
        self.vocab_feedback.config(text='Test Mode: Type the English meaning', fg=self.colors['success'])
        self.next_vocab_card()

    def review_vocab_wrong(self):
        wrong = self.progress.get('Vocabulary', {}).get('wrong', [])
        if not wrong:
            messagebox.showinfo('No Mistakes', 'No wrong vocabulary words saved!')
            return
        self.vocab_mode.set('Test')
        self.vocab_pool = [(w, VOCABULARY[w]) for w in wrong if w in VOCABULARY]
        random.shuffle(self.vocab_pool)
        self.vocab_score = self.vocab_asked = 0
        self.vocab_wrong_in_session = []
        self.vocab_feedback.config(text='Reviewing your mistakes', fg=self.colors['accent'])
        self.next_vocab_card()

    def next_vocab_card(self):
        if not self.vocab_pool:
            self.vocab_feedback.config(text='Complete!', fg=self.colors['success'])
            if self.vocab_mode.get() == 'Test':
                self.end_vocab_test()
            return

        self.current_vocab = self.vocab_pool.pop()
        word, data = self.current_vocab
        self.vocab_japanese.config(text=word)
        self.example_jp.config(text=data.get('example', ''))
        self.example_romaji.config(text=data.get('example_romaji', ''))

        if self.vocab_mode.get() == 'Test':
            self.example_eng.config(text='')
            self.vocab_info.config(text='')

            self.vocab_nav_frame.pack_forget()
            self.vocab_next_btn.config(state='disabled')

            if self.test_type.get() == 'typing':
                self.vocab_mc_frame.pack_forget()
                self.vocab_typing_frame.pack(fill='x', padx=20, pady=10)
                self.vocab_entry.config(state='normal')
                self.vocab_check_btn_typing.config(state='normal')
                self.vocab_entry.delete(0, tk.END)
                self.vocab_entry.focus()
            else:
                self.vocab_typing_frame.pack_forget()
                self.vocab_mc_frame.pack(fill='x', padx=20, pady=10)
                self.setup_vocab_multiple_choice()

            self.vocab_answer_checked = False
            self.vocab_last_correct = False
        else:
            self.vocab_typing_frame.pack_forget()
            self.vocab_mc_frame.pack_forget()
            self.vocab_nav_frame.pack(fill='x', padx=20, pady=10)
            self.example_eng.config(text=data.get('example_eng', ''))
            self.vocab_info.config(text=f"{data['romaji']}\n{data['meaning']}\n{data['notes']}")

        self.update_vocab_stats()

    def setup_vocab_multiple_choice(self):
        for w in self.vocab_mc_frame.winfo_children():
            w.destroy()
        self.vocab_mc_buttons = []
        word, data = self.current_vocab
        correct = data['meaning']
        all_meanings = [v['meaning'] for v in VOCABULARY.values()]
        wrongs = [m for m in all_meanings if m != correct]
        choices = random.sample(wrongs, min(3, len(wrongs))) + [correct]
        random.shuffle(choices)

        tk.Label(self.vocab_mc_frame, text='Choose the correct meaning:', font=('Helvetica', 10),
                 bg=self.colors['card_bg'], fg=self.colors['fg']).pack(pady=8)

        for ch in choices:
            btn = tk.Button(self.vocab_mc_frame, text=ch, font=self.layout['mc_btn_font'],
                            bg='white', fg=self.colors['fg'],
                            activebackground=self.colors['accent'], activeforeground='white',
                            relief='raised', bd=3, padx=18, pady=10, wraplength=380,
                            command=lambda c=ch: self.check_vocab_mc_answer(c))
            btn.pack(pady=6, fill='x' if self.layout['mc_btn_width'] == 0 else 'none', padx=40 if self.layout['mc_btn_width'] == 0 else 0)
            self.vocab_mc_buttons.append(btn)

    def check_vocab_mc_answer(self, choice):
        if self.vocab_answer_checked: return
        word, data = self.current_vocab
        correct = data['meaning']
        self.vocab_asked += 1
        self.vocab_answer_checked = True

        if choice == correct:
            self.vocab_score += 1
            self.vocab_last_correct = True
            self.vocab_feedback.config(text=f'Correct! {word} = {correct}', fg=self.colors['success'])
            for b in self.vocab_mc_buttons:
                if b['text'] == correct:
                    b.config(bg=self.colors['success'], fg='white')
        else:
            self.vocab_last_correct = False
            self.vocab_wrong_in_session.append(word)
            self.vocab_feedback.config(text=f'Incorrect — {word} = {correct}', fg=self.colors['error'])
            for b in self.vocab_mc_buttons:
                if b['text'] == choice:
                    b.config(bg=self.colors['error'], fg='white')
                elif b['text'] == correct:
                    b.config(bg=self.colors['success'], fg='white')

        for b in self.vocab_mc_buttons:
            b.config(state='disabled')
        self.vocab_next_btn.config(state='normal')
        self.update_vocab_stats()

    def check_vocab_answer(self):
        if self.vocab_mode.get() != 'Test' or not self.current_vocab or self.vocab_answer_checked:
            return
        word, data = self.current_vocab
        user = self.vocab_entry.get().strip().lower()
        correct = data['meaning'].lower()
        self.vocab_asked += 1
        self.vocab_answer_checked = True

        if user == correct or user in correct or correct in user:
            self.vocab_score += 1
            self.vocab_last_correct = True
            self.vocab_feedback.config(text=f'Correct! {word} = {data["meaning"]}', fg=self.colors['success'])
        else:
            self.vocab_last_correct = False
            self.vocab_wrong_in_session.append(word)
            self.vocab_feedback.config(text=f'Incorrect — {word} = {data["meaning"]}', fg=self.colors['error'])

        self.vocab_next_btn.config(state='normal')
        self.update_vocab_stats()

    def update_vocab_stats(self):
        if self.vocab_mode.get() == 'Test':
            self.vocab_stats.config(text=f'Score: {self.vocab_score}/{self.vocab_asked}')
        else:
            self.vocab_stats.config(text=f'Words remaining: {len(self.vocab_pool)}')

    def end_vocab_test(self):
        wrong_set = set(self.progress.get('Vocabulary', {}).get('wrong', []))
        wrong_set.update(self.vocab_wrong_in_session)
        self.progress['Vocabulary']['wrong'] = sorted(list(wrong_set))
        save_progress(self.progress)
        messagebox.showinfo('Test Complete',
                            f'Vocabulary test finished!\nScore: {self.vocab_score}/{self.vocab_asked}\nMistakes saved for review.')

    # ── GRAMMAR TAB ─────────────────────────────────────
    def init_grammar_tab(self):
        L = self.layout
        self.current_pattern_index = 0

        header = tk.Frame(self.grammar_tab, bg=self.colors['accent'], height=60)
        header.pack(fill='x', pady=(0, L['pady']))
        header.pack_propagate(False)
        tk.Label(header, text='Sentence Structure', font=('Helvetica', 16, 'bold'),
                 bg=self.colors['accent'], fg='white').pack(pady=15)

        nav = tk.Frame(self.grammar_tab, bg=self.colors['card_bg'], relief='raised', bd=2)
        nav.pack(fill='x', padx=L['padx'], pady=L['pady'])

        tk.Button(nav, text='Previous', font=('Helvetica', 10, 'bold'),
                  bg=self.colors['btn_bg'], fg=self.colors['fg'],
                  activebackground=self.colors['accent'], activeforeground='white',
                  relief='raised', bd=2, padx=L['btn_padx'], pady=L['btn_pady'],
                  command=self.prev_pattern).pack(side='left', padx=8, pady=8)

        self.pattern_label = tk.Label(nav, text='', font=('Helvetica', 11, 'bold'),
                                      bg=self.colors['card_bg'], fg=self.colors['fg'])
        self.pattern_label.pack(side='left', expand=True)

        tk.Button(nav, text='Next', font=('Helvetica', 10, 'bold'),
                  bg=self.colors['btn_bg'], fg=self.colors['fg'],
                  activebackground=self.colors['accent'], activeforeground='white',
                  relief='raised', bd=2, padx=L['btn_padx'], pady=L['btn_pady'],
                  command=self.next_pattern).pack(side='right', padx=8, pady=8)

        canvas = tk.Canvas(self.grammar_tab, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.grammar_tab, orient='vertical', command=canvas.yview) if L['scrollbar'] else None
        self.grammar_content = tk.Frame(canvas, bg=self.colors['card_bg'])

        canvas.configure(yscrollcommand=scrollbar.set if scrollbar else None)
        if scrollbar:
            scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True, padx=L['padx'], pady=L['pady'])

        cw = canvas.create_window((0, 0), window=self.grammar_content, anchor='nw')
        self.grammar_content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(cw, width=e.width-30))

        self.pattern_title = tk.Label(self.grammar_content, text='', font=L['font_pattern_title'],
                                      bg=self.colors['card_bg'], fg=self.colors['accent'], wraplength=L['wraplength'])
        self.pattern_title.pack(pady=12)
        self.pattern_romaji = tk.Label(self.grammar_content, text='', font=L['font_pattern_romaji'],
                                       bg=self.colors['card_bg'], fg=self.colors['accent'], wraplength=L['wraplength'])
        self.pattern_romaji.pack(pady=4)
        self.pattern_meaning = tk.Label(self.grammar_content, text='', font=L['font_pattern_meaning'],
                                        bg=self.colors['card_bg'], fg=self.colors['success'], wraplength=L['wraplength'])
        self.pattern_meaning.pack(pady=6)

        explain_frame = tk.Frame(self.grammar_content, bg=self.colors['bg'], relief='sunken', bd=2)
        explain_frame.pack(fill='x', padx=20, pady=12)
        tk.Label(explain_frame, text='Explanation', font=('Helvetica', 11, 'bold'),
                 bg=self.colors['bg'], fg=self.colors['accent']).pack(pady=6)
        self.pattern_explanation = tk.Label(explain_frame, text='', font=L['font_explanation'],
                                           bg=self.colors['bg'], fg=self.colors['fg'],
                                           justify='left', wraplength=600)
        self.pattern_explanation.pack(padx=15, pady=8)

        self.examples_frame = tk.Frame(self.grammar_content, bg=self.colors['bg'], relief='sunken', bd=2)
        self.examples_frame.pack(fill='x', padx=20, pady=12)
        tk.Label(self.examples_frame, text='Examples', font=('Helvetica', 11, 'bold'),
                 bg=self.colors['bg'], fg=self.colors['accent']).pack(pady=6)

        self.display_pattern()

    def display_pattern(self):
        p = SENTENCE_PATTERNS[self.current_pattern_index]
        self.pattern_title.config(text=p['pattern'])
        self.pattern_romaji.config(text=p['romaji'])
        self.pattern_meaning.config(text=f"Meaning: {p['meaning']}")
        self.pattern_explanation.config(text=p['explanation'])
        self.pattern_label.config(text=f"Pattern {self.current_pattern_index + 1}/{len(SENTENCE_PATTERNS)}")

        for w in self.examples_frame.winfo_children():
            if w.winfo_class() != 'Label' or w['text'] != 'Examples':
                w.destroy()

        for i, ex in enumerate(p['examples'], 1):
            card = tk.Frame(self.examples_frame, bg='white', relief='raised', bd=2)
            card.pack(fill='x', padx=20, pady=10)

            tk.Label(card, text=f"Example {i}", font=self.layout['font_example_label'],
                     bg=self.colors['btn_bg'], fg=self.colors['fg']).pack(fill='x', pady=(0, 5))
            tk.Label(card, text=ex['jp'], font=self.layout['font_example_jp'],
                     bg='white', fg=self.colors['fg']).pack(pady=5, padx=15)
            tk.Label(card, text=ex['romaji'], font=self.layout['font_example_romaji'],
                     bg='white', fg=self.colors['accent']).pack(pady=3, padx=15)
            tk.Label(card, text=f"→ {ex['eng']}", font=self.layout['font_example_eng'],
                     bg='white', fg='gray').pack(pady=5, padx=15)

    def next_pattern(self):
        if self.current_pattern_index < len(SENTENCE_PATTERNS) - 1:
            self.current_pattern_index += 1
            self.display_pattern()

    def prev_pattern(self):
        if self.current_pattern_index > 0:
            self.current_pattern_index -= 1
            self.display_pattern()


if __name__ == '__main__':
    app = JapaneseTrainer()
    app.mainloop()
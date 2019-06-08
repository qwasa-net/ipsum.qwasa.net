#!/usr/bin/python
# -*- coding: utf-8 -*-
""" random mumble generator """
import argparse
import json
import os
import re
import random
import sys

# magic words -- ~1K most common words from wiki
DICTIONARY = {
    'english': [
        'the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', 'you', 'that', 'he',
        'was', 'for', 'on', 'are', 'with', 'as', 'I', 'his', 'they', 'be', 'at', 'one',
        'have', 'this', 'from', 'or', 'had', 'by', 'hot', 'word', 'but', 'what', 'some',
        'we', 'can', 'out', 'other', 'were', 'all', 'there', 'when', 'up', 'use', 'your',
        'how', 'said', 'an', 'each', 'she', 'which', 'do', 'their', 'time', 'if', 'will',
        'way', 'about', 'many', 'then', 'them', 'write', 'would', 'like', 'so', 'these',
        'her', 'long', 'make', 'thing', 'see', 'him', 'two', 'has', 'look', 'more', 'day',
        'could', 'go', 'come', 'did', 'number', 'sound', 'no', 'most', 'people', 'my',
        'over', 'know', 'water', 'than', 'call', 'first', 'who', 'may', 'down', 'side',
        'been', 'now', 'find', 'any', 'new', 'work', 'part', 'take', 'get', 'place',
        'made', 'live', 'where', 'after', 'back', 'little', 'only', 'round', 'man',
        'year', 'came', 'show', 'every', 'good', 'me', 'give', 'our', 'under', 'name',
        'very', 'through', 'just', 'form', 'sentence', 'great', 'think', 'say', 'help',
        'low', 'line', 'differ', 'turn', 'cause', 'much', 'mean', 'before', 'move',
        'right', 'boy', 'old', 'too', 'same', 'tell', 'does', 'set', 'three', 'want',
        'air', 'well', 'also', 'play', 'small', 'end', 'put', 'home', 'read', 'hand',
        'port', 'large', 'spell', 'add', 'even', 'land', 'here', 'must', 'big', 'high',
        'such', 'follow', 'act', 'why', 'ask', 'men', 'change', 'went', 'light', 'kind',
        'off', 'need', 'house', 'picture', 'try', 'us', 'again', 'animal', 'point',
        'mother', 'world', 'near', 'build', 'self', 'earth', 'father', 'head', 'stand',
        'own', 'page', 'should', 'country', 'found', 'answer', 'school', 'grow',
        'study', 'still', 'learn', 'plant', 'cover', 'food', 'sun', 'four', 'between',
        'state', 'keep', 'eye', 'never', 'last', 'let', 'thought', 'city', 'tree',
        'cross', 'farm', 'hard', 'start', 'might', 'story', 'saw', 'far', 'sea', 'draw',
        'left', 'late', 'run', 'don\'t', 'while', 'press', 'close', 'night', 'real',
        'life', 'few', 'north', 'open', 'seem', 'together', 'next', 'white', 'children',
        'begin', 'got', 'walk', 'example', 'ease', 'paper', 'group', 'always', 'music',
        'those', 'both', 'mark', 'often', 'letter', 'until', 'mile', 'river', 'car',
        'feet', 'care', 'second', 'book', 'carry', 'took', 'science', 'eat', 'room',
        'friend', 'began', 'idea', 'fish', 'mountain', 'stop', 'once', 'base', 'hear',
        'horse', 'cut', 'sure', 'watch', 'color', 'face', 'wood', 'main', 'enough',
        'plain', 'girl', 'usual', 'young', 'ready', 'above', 'ever', 'red', 'list',
        'though', 'feel', 'talk', 'bird', 'soon', 'body', 'dog', 'family', 'direct',
        'pose', 'leave', 'song', 'measure', 'door', 'product', 'black', 'short',
        'numeral', 'class', 'wind', 'question', 'happen', 'complete', 'ship', 'area',
        'half', 'rock', 'order', 'fire', 'south', 'problem', 'piece', 'told', 'knew',
        'pass', 'since', 'top', 'whole', 'king', 'space', 'heard', 'best', 'hour', 'better',
        'true', 'during', 'hundred', 'five', 'remember', 'step', 'early', 'hold', 'west',
        'ground', 'interest', 'reach', 'fast', 'verb', 'sing', 'listen', 'six', 'table',
        'travel', 'less', 'morning', 'ten', 'simple', 'several', 'vowel', 'toward', 'war',
        'lay', 'against', 'pattern', 'slow', 'center', 'love', 'person', 'money', 'serve',
        'appear', 'road', 'map', 'rain', 'rule', 'govern', 'pull', 'cold', 'notice', 'voice',
        'unit', 'power', 'town', 'fine', 'certain', 'fly', 'fall', 'lead', 'cry', 'dark',
        'machine', 'note', 'wait', 'plan', 'figure', 'star', 'box', 'noun', 'field', 'rest',
        'correct', 'able', 'pound', 'done', 'beauty', 'drive', 'stood', 'contain', 'front',
        'teach', 'week', 'final', 'gave', 'green', 'oh', 'quick', 'develop', 'ocean', 'warm',
        'free', 'minute', 'strong', 'special', 'mind', 'behind', 'clear', 'tail', 'produce',
        'fact', 'street', 'inch', 'multiply', 'nothing', 'course', 'stay', 'wheel', 'full',
        'force', 'blue', 'object', 'decide', 'surface', 'deep', 'moon', 'island', 'foot',
        'system', 'busy', 'test', 'record', 'boat', 'common', 'gold', 'possible', 'plane',
        'stead', 'dry', 'wonder', 'laugh', 'thousand', 'ago', 'ran', 'check', 'game', 'shape',
        'equate', 'hot', 'miss', 'brought', 'heat', 'snow', 'tire', 'bring', 'yes', 'distant',
        'fill', 'east', 'paint', 'language', 'among', 'grand', 'ball', 'yet', 'wave', 'drop',
        'heart', 'am', 'present', 'heavy', 'dance', 'engine', 'position', 'arm', 'wide',
        'sail', 'material', 'size', 'vary', 'settle', 'speak', 'weight', 'general', 'ice',
        'matter', 'circle', 'pair', 'include', 'divide', 'syllable', 'felt', 'perhaps', 'pick',
        'sudden', 'count', 'square', 'reason', 'length', 'represent', 'art', 'subject',
        'region', 'energy', 'hunt', 'probable', 'bed', 'brother', 'egg', 'ride', 'cell',
        'believe', 'fraction', 'forest', 'sit', 'race', 'window', 'store', 'summer', 'train',
        'sleep', 'prove', 'lone', 'leg', 'exercise', 'wall', 'catch', 'mount', 'wish',
        'sky', 'board', 'joy', 'winter', 'sat', 'written', 'wild', 'instrument', 'kept',
        'glass', 'grass', 'cow', 'job', 'edge', 'sign', 'visit', 'past', 'soft', 'fun',
        'bright', 'gas', 'weather', 'month', 'million', 'bear', 'finish', 'happy', 'hope',
        'flower', 'clothe', 'strange', 'gone', 'jump', 'baby', 'eight', 'village', 'meet',
        'root', 'buy', 'raise', 'solve', 'metal', 'whether', 'push', 'seven', 'paragraph',
        'third', 'shall', 'held', 'hair', 'describe', 'cook', 'floor', 'either', 'result',
        'burn', 'hill', 'safe', 'cat', 'century', 'consider', 'type', 'law', 'bit', 'coast',
        'copy', 'phrase', 'silent', 'tall', 'sand', 'soil', 'roll', 'temperature', 'finger',
        'industry', 'value', 'fight', 'lie', 'beat', 'excite', 'natural', 'view', 'sense',
        'ear', 'else', 'quite', 'broke', 'case', 'middle', 'kill', 'son', 'lake', 'moment',
        'scale', 'loud', 'spring', 'observe', 'child', 'straight', 'consonant', 'nation',
        'dictionary', 'milk', 'speed', 'method', 'organ', 'pay', 'age', 'section', 'dress',
        'cloud', 'surprise', 'quiet', 'stone', 'tiny', 'climb', 'cool', 'design', 'poor',
        'lot', 'experiment', 'bottom', 'key', 'iron', 'single', 'stick', 'flat', 'twenty',
        'skin', 'smile', 'crease', 'hole', 'trade', 'melody', 'trip', 'office', 'receive',
        'row', 'mouth', 'exact', 'symbol', 'die', 'least', 'trouble', 'shout', 'except',
        'wrote', 'seed', 'tone', 'join', 'suggest', 'clean', 'break', 'lady', 'yard', 'rise',
        'bad', 'blow', 'oil', 'blood', 'touch', 'grew', 'cent', 'mix', 'team', 'wire',
        'cost', 'lost', 'brown', 'wear', 'garden', 'equal', 'sent', 'choose', 'fell', 'fit',
        'flow', 'fair', 'bank', 'collect', 'save', 'control', 'decimal', 'gentle', 'woman',
        'captain', 'practice', 'separate', 'difficult', 'doctor', 'please', 'protect', 'noon',
        'whose', 'locate', 'ring', 'character', 'insect', 'caught', 'period', 'indicate',
        'radio', 'spoke', 'atom', 'human', 'history', 'effect', 'electric', 'expect', 'crop',
        'modern', 'element', 'hit', 'student', 'corner', 'party', 'supply', 'bone', 'rail',
        'imagine', 'provide', 'agree', 'thus', 'capital', 'won\'t', 'chair', 'danger',
        'fruit', 'rich', 'thick', 'soldier', 'process', 'operate', 'guess', 'necessary',
        'sharp', 'wing', 'create', 'neighbor', 'wash', 'bat', 'rather', 'crowd', 'corn',
        'compare', 'poem', 'string', 'bell', 'depend', 'meat', 'rub', 'tube', 'famous',
        'dollar', 'stream', 'fear', 'sight', 'thin', 'triangle', 'planet', 'hurry', 'chief',
        'colony', 'clock', 'mine', 'tie', 'enter', 'major', 'fresh', 'search', 'send',
        'yellow', 'gun', 'allow', 'print', 'dead', 'spot', 'desert', 'suit', 'current',
        'lift', 'rose', 'continue', 'block', 'chart', 'hat', 'sell', 'success', 'company',
        'subtract', 'event', 'particular', 'deal', 'swim', 'term', 'opposite', 'wife', 'shoe',
        'shoulder', 'spread', 'arrange', 'camp', 'invent', 'cotton', 'born', 'determine',
        'quart', 'nine', 'truck', 'noise', 'level', 'chance', 'gather', 'shop', 'stretch',
        'throw', 'shine', 'property', 'column', 'molecule', 'select', 'wrong', 'gray',
        'repeat', 'require', 'broad', 'prepare', 'salt', 'nose', 'plural', 'anger', 'claim',
        'continent', 'oxygen', 'sugar', 'death', 'pretty', 'skill', 'women', 'season',
        'solution', 'magnet', 'silver', 'thank', 'branch', 'match', 'suffix', 'especially',
        'fig', 'afraid', 'huge', 'sister', 'steel', 'discuss', 'forward', 'similar', 'guide',
        'experience', 'score', 'apple', 'bought', 'led', 'pitch', 'coat', 'mass', 'card',
        'band', 'rope', 'slip', 'win', 'dream', 'evening', 'condition', 'feed', 'tool',
        'total', 'basic', 'smell', 'valley', 'nor', 'double', 'seat', 'arrive', 'master',
        'track', 'parent', 'shore', 'division', 'sheet', 'substance', 'favor', 'connect',
        'post', 'spend', 'chord', 'fat', 'glad', 'original', 'share', 'station', 'dad',
        'bread', 'charge', 'proper', 'bar', 'offer', 'segment', 'slave', 'duck', 'instant',
        'market', 'degree', 'populate', 'chick', 'dear', 'enemy', 'reply', 'drink', 'occur',
        'support', 'speech', 'nature', 'range', 'steam', 'motion', 'path', 'liquid', 'log',
        'meant', 'quotient', 'teeth', 'shell', 'neck',
    ],

    'russian': [
        'не', 'на', 'что', 'то', 'он', 'как', 'по', 'его', 'все',
        'из', 'за', 'это', 'же', 'от', 'но', 'было', 'так', 'бы', 'еще',
        'меня', 'был', 'только', 'она', 'уже', 'ее', 'мне', 'сказал',
        'ты', 'для', 'мы', 'они', 'до', 'их', 'когда', 'или', 'ему',
        'ни', 'вы', 'даже', 'под', 'него', 'если', 'чтобы', 'вот',
        'чем', 'где', 'себя', 'была', 'нас', 'время', 'ли', 'быть',
        'раз', 'может', 'есть', 'со', 'были', 'там', 'нет', 'очень',
        'кто', 'без', 'тут', 'во', 'будет', 'тоже', 'этого', 'надо',
        'себе', 'да', 'ничего', 'при', 'тебя', 'них', 'этом', 'того',
        'можно', 'этот', 'потом', 'человек', 'вас', 'сейчас', 'один',
        'здесь', 'теперь', 'тебе', 'через', 'больше', 'всех',
        'лет', 'том', 'после', 'сам', 'нибудь', 'ним', 'просто',
        'вдруг', 'над', 'потому', 'ведь', 'вам', 'дело', 'тогда',
        'спросил', 'жизни', 'два', 'чего', 'который', 'тем', 'нам',
        'перед', 'глаза', 'всего', 'уж', 'им', 'своей', 'несколько',
        'день', 'всегда', 'какой', 'ей', 'более', 'такой', 'тот',
        'этой', 'нее', 'которые', 'ней', 'эти', 'стал', 'жизнь',
        'сразу', 'мог', 'совсем', 'свою', 'об', 'почему', 'пока',
        'конечно', 'люди', 'года', 'человека', 'куда', 'почти',
        'руки', 'людей', 'хотя', 'три', 'снова', 'хорошо', 'знаю',
        'много', 'сказать', 'будто', 'лишь', 'голову', 'про',
        'сказала', 'всем', 'между', 'говорит', 'никогда', 'опять',
        'свои', 'другой', 'мой', 'своих', 'эту', 'такое', 'знал',
        'своего', 'таки', 'собой', 'дома', 'времени', 'чуть', 'свой',
        'лучше', 'именно', 'друг', 'лицо', 'руку', 'вообще', 'свое',
        'которой', 'никто', 'кого', 'этих', 'говорил', 'вместе',
        'назад', 'нем', 'хоть', 'понял', 'рядом', 'словно', 'всю',
        'одной', 'ответил', 'тех', 'слова', 'нужно', 'быстро',
        'какие', 'стало', 'эта', 'своим', 'весь', 'давно', 'видел',
        'дверь', 'место', 'должен', 'те', 'этим', 'долго', 'делать',
        'прямо', 'могу', 'которых', 'которая', 'значит', 'хотел',
        'сегодня', 'сторону', 'одного', 'такие', 'две', 'нельзя',
        'тому', 'совершенно', 'которого', 'случае', 'голос',
        'одна', 'подумал', 'головой', 'деньги', 'стороны',
        'самом', 'ноги', 'сколько', 'дальше', 'каждый', 'ко',
        'нему', 'увидел', 'ну', 'знает', 'глазами', 'пошел',
        'оно', 'кажется', 'мной', 'точно', 'стоял', 'равно',
        'наконец', 'вокруг', 'также', 'других', 'ними', 'думал',
        'говорить', 'будут', 'первый', 'пять', 'год', 'самого',
        'среди', 'стали', 'стоит', 'сюда', 'одно', 'месте', 'двух',
        'дня', 'могут', 'какая', 'жить', 'году', 'деле', 'туда',
        'таких', 'вопрос', 'говорю', 'чтоб', 'вроде', 'слишком',
        'рукой', 'такого', 'отец', 'сами', 'взял', 'дом', 'наш',
        'моя', 'немного', 'сидел', 'мать', 'пор', 'идет', 'буду',
        'руками', 'такая', 'начал', 'конце', 'той', 'против',
        'действительно', 'нашей', 'таким', 'которую', 'зачем',
        'тихо', 'дела', 'моей', 'казалось', 'ночь', 'раньше',
        'образом', 'видно', 'сделать', 'посмотрел', 'войны',
        'наши', 'домой', 'особенно', 'кроме', 'смотрел', 'другие',
        'хочу', 'работы', 'мало', 'слово', 'одну', 'большой',
        'товарищ', 'друга', 'мои', 'либо', 'иногда', 'минут',
        'этому', 'должны', 'часто', 'правда', 'самое', 'знаешь',
        'двадцать', 'сама', 'кому', 'вышел', 'второй', 'однако',
        'глаз', 'решил', 'детей', 'самый', 'четыре', 'сделал',
        'например', 'места', 'вперед', 'стол', 'своем', 'заметил',
        'всей', 'стала', 'медленно', 'город', 'откуда', 'могли',
        'женщина', 'свет', 'тобой', 'хотелось', 'довольно',
        'работу', 'десять', 'воды', 'вполне', 'какое', 'руках',
        'двери', 'пусть', 'вся', 'самой', 'города', 'момент',
        'говорят', 'далеко', 'котором', 'возле', 'мир', 'никак',
        'знать', 'едва', 'нашего', 'понять', 'будем', 'затем',
        'плохо', 'шел', 'взгляд', 'думаю', 'мимо', 'имеет', 'землю',
        'годы', 'жена', 'своими', 'часть', 'наших', 'которое',
        'пришел', 'дней', 'нами', 'вовсе', 'час', 'спросила',
        'лица', 'легко', 'сквозь', 'поэтому', 'вниз', 'меньше',
        'менее', 'наверное', 'ту', 'знаете', 'каким', 'какую',
        'бывает', 'сердце', 'голосом', 'моего', 'ясно', 'вами',
        'часов', 'должно', 'могла', 'сил', 'земле', 'машины',
        'спокойно', 'мира', 'обычно', 'около', 'минуту', 'понимаю',
        'своему', 'вид', 'смерти', 'мое', 'тысяч', 'разговор',
        'пути', 'говоря', 'оказался', 'идти', 'головы', 'улице',
        'столько', 'доме', 'та', 'скоро', 'подошел', 'работать',
        'отца', 'следует', 'трудно', 'иначе', 'ночью', 'комнату',
        'первых', 'сел', 'пришлось', 'которым', 'глазах', 'хочешь',
        'известно', 'молча', 'хочет', 'сильно', 'власти',
        'прежде', 'денег', 'молодой', 'воду', 'завтра', 'ка',
        'части', 'мысли', 'глядя', 'одним', 'конца', 'успел',
        'окна', 'начала', 'одном', 'общем', 'удалось', 'кем',
        'часа', 'никого', 'другое', 'силы', 'страны', 'вместо',
        'достаточно', 'произнес', 'мире', 'кое', 'выше',
        'продолжал', 'истории', 'никаких', 'имя', 'вернулся',
        'сначала', 'является', 'комнате', 'старик', 'главное',
        'мама', 'машину', 'стояли', 'каких', 'рот', 'помню',
        'должна', 'думать', 'виде', 'последний', 'дети', 'вновь',
        'встал', 'говорили', 'лицом', 'сын', 'разве', 'ночи',
        'самым', 'пол', 'матери', 'шли', 'неожиданно', 'дороге',
        'придется', 'любил', 'женщины', 'поднял', 'вижу', 'какого',
        'ответ', 'капитан', 'первого', 'голове', 'виду', 'свете',
        'моему', 'смотреть', 'мою', 'городе', 'другом', 'обратно',
        'ушел', 'ребята', 'случай', 'вспомнил', 'небо', 'народ',
        'утра', 'такую', 'сто', 'стола', 'случилось', 'земли',
        'мере', 'дни', 'многие', 'очередь', 'тело', 'внимание',
        'парень', 'мысль', 'дорогу', 'солнце', 'скорее', 'путь',
        'крикнул', 'новый', 'невозможно', 'вверх', 'сорок',
        'найти', 'другого', 'человеком', 'взять', 'остался',
        'окно', 'впервые', 'слышал', 'весьма', 'сих', 'осталось',
        'стены', 'никакого', 'самых', 'трех', 'кивнул', 'раза',
        'самые', 'книги', 'дал', 'хочется', 'стране', 'столь',
        'утром', 'пошли', 'ногами', 'часы', 'получил', 'концов',
        'оказалось', 'слов', 'хуже', 'крови', 'первой', 'связи',
        'генерал', 'голова', 'мол', 'лежал', 'письмо', 'каждого',
        'воздух', 'шесть', 'знали', 'течение', 'солдат', 'вещи',
        'стояла', 'жил', 'вечер', 'осторожно', 'слегка', 'стать',
        'месяц', 'наша', 'остановился', 'тридцать', 'всему',
        'чему', 'возможно', 'дядя', 'пожалуйста', 'поскольку',
        'работа', 'почувствовал', 'внимания', 'груди', 'черт',
        'другим', 'новые', 'речь', 'видеть', 'улыбнулся', 'столом',
        'моих', 'неделю', 'спиной', 'впереди', 'партии', 'вчера',
        'рублей', 'рук', 'возможность', 'имел', 'видимо', 'любви',
        'происходит', 'дороги', 'мальчик', 'люблю', 'спать',
        'страшно', 'народа', 'человеку', 'трубку', 'показалось',
        'любовь', 'обязательно', 'руке', 'вечером', 'резко',
        'будешь', 'чаще', 'номер', 'другую', 'ибо', 'узнал',
        'произошло', 'любой', 'нашел', 'однажды', 'смотрит',
        'язык', 'понимал', 'никому', 'армии', 'поднялся', 'явно',
        'забыл', 'живет', 'начальник', 'конец', 'последние',
        'сына', 'общества', 'двое', 'море', 'нечего', 'сидели',
        'брат', 'недавно', 'нос', 'всеми', 'дать', 'взглядом',
        'ради', 'писать', 'волосы', 'чувствовал', 'становится',
        'писал', 'лес', 'работе', 'лице', 'старый', 'маленький',
        'ногу', 'души', 'говорила', 'поле', 'прошел', 'улицу',
        'машина', 'многих', 'станет', 'некоторые', 'услышал',
        'бросил', 'губы', 'право', 'иметь', 'ждать', 'вздохнул',
        'могло', 'оттуда', 'пожалуй', 'девушка', 'господин',
        'права', 'вон', 'снег', 'разных', 'открыл', 'берегу',
        'чувство', 'плечами', 'сидит', 'хозяин', 'вдоль', 'громко',
        'лесу', 'прежнему', 'вода', 'полу', 'века', 'двумя', 'таком',
        'всякий', 'нового', 'работал', 'тела', 'отсюда', 'вопросы',
        'немедленно', 'имени', 'людям', 'кровь', 'системы', 'твой',
        'самому', 'смысле', 'счет', 'разные', 'внимательно',
        'трудом', 'наше', 'ног', 'никакой', 'война', 'зубы', 'оба',
        'водой', 'понимаешь', 'нужен', 'вошел', 'первым', 'людьми',
        'власть', 'минуты', 'протянул', 'которому', 'стене',
        'показал', 'ваш', 'видели', 'области', 'лейтенант',
        'история', 'ждал', 'согласился', 'каком', 'ладно',
        'правильно', 'семь', 'го', 'пальцем', 'шла', 'удивился',
        'гораздо', 'наверно', 'готов', 'хотите', 'делает',
        'другу', 'возможности', 'давай', 'порядке', 'комнаты',
        'друзья', 'спину', 'положил', 'третий', 'месяца', 'пошла',
        'делал', 'странно', 'читал', 'душе', 'тысячи', 'прав',
        'отношения', 'времена', 'полностью', 'прочим', 'скажу',
        'помочь', 'весело', 'плечо', 'поздно', 'нечто', 'ветер',
        'одновременно', 'боли', 'ума', 'памяти', 'начали', 'пора',
        'роль', 'ходить', 'углу', 'душу', 'смерть', 'наоборот',
        'мужчина', 'предложил', 'пить', 'грудь', 'интересно',
        'голоса', 'тяжело', 'оказывается', 'постоянно', 'новой',
        'необходимо', 'группы', 'вышла', 'плечи', 'знают',
        'историю', 'книгу', 'новых', 'знала', 'настолько',
        'искать', 'женщин', 'лично', 'нравится', 'пару',
        'силу', 'жили', 'любит', 'повернулся', 'положение',
        'зрения', 'первую', 'одному', 'стороне', 'метров',
        'сказали', 'поводу', 'остается', 'друзей', 'начинает',
        'утро', 'письма', 'появился', 'недели', 'состоянии',
        'воде', 'случайно', 'нашем', 'столе', 'дали', 'воздухе',
        'огонь', 'узнать', 'решили', 'можете', 'света', 'внутри',
        'следующий', 'вслед', 'закричал', 'ходу', 'хватит',
        'попал', 'считать', 'помощь', 'пытался', 'первые',
        'бумаги', 'пришла', 'нашу', 'пальцами', 'лежит',
        'помощи', 'ходил', 'дворе', 'повторил', 'можешь',
        'большие', 'запах', 'работает', 'вышли', 'муж', 'ваши',
        'кино', 'дому', 'школе', 'словами', 'леса', 'понятно',
        'легче', 'революции', 'долларов', 'написал', 'впрочем',
        'прекрасно', 'труда', 'временем', 'кстати', 'называется',
        'получить', 'результате', 'оказалась', 'качестве'
    ],

    'spanish': [
        'que', 'de', 'no', 'a', 'la', 'el', 'es', 'y', 'en', 'lo', 'un', 'por', 'qué', 'me', 'una',
        'te', 'los', 'se', 'con', 'para', 'mi', 'está', 'si', 'bien', 'pero', 'yo', 'eso', 'las',
        'sí', 'su', 'tu', 'aquí', 'del', 'al', 'como', 'le', 'más', 'esto', 'ya', 'todo', 'esta',
        'vamos', 'muy', 'hay', 'ahora', 'algo', 'estoy', 'tengo', 'nos', 'tú', 'nada', 'cuando',
        'ha', 'este', 'sé', 'estás', 'así', 'puedo', 'cómo', 'quiero', 'sólo', 'soy', 'tiene',
        'gracias', 'o', 'él', 'bueno', 'fue', 'ser', 'hacer', 'son', 'todos', 'era', 'eres', 'vez',
        'tienes', 'creo', 'ella', 'he', 'ese', 'voy', 'puede', 'sabes', 'hola', 'sus', 'porque',
        'dios', 'quién', 'nunca', 'dónde', 'quieres', 'casa', 'favor', 'esa', 'dos', 'tan', 'señor',
        'tiempo', 'verdad', 'estaba', 'mejor', 'están', 'va', 'hombre', 'usted', 'mucho', 'hace',
        'entonces', 'siento', 'tenemos', 'puedes', 'ahí', 'ti', 'vida', 'ver', 'alguien',
        'sr', 'hasta', 'sin', 'mí', 'solo', 'años', 'sobre', 'decir', 'uno', 'siempre', 'oh',
        'ir', 'cosas', 'también', 'antes', 'has', 'ni', 'mis', 'día', 'estar', 'estamos', 'noche',
        'nadie', 'otra', 'quiere', 'parece', 'nosotros', 'poco', 'padre', 'trabajo', 'gente',
        'mira', 'vas', 'sea', 'les', 'donde', 'mismo', 'hecho', 'ellos', 'dijo', 'pasa', 'dinero',
        'hijo', 'tal', 'otro', 'hablar', 'seguro', 'claro', 'estas', 'lugar', 'mundo', 'amigo',
        'espera', 'mierda', 'han', 'tus', 'sabe', 'después', 'momento', 'desde', 'fuera', 'cosa',
        'tipo', 'mañana', 'podemos', 'dije', 'gran', 'necesito', 'estado', 'podría', 'acuerdo',
        'papá', 'tener', 'dice', 'mío', 'crees', 'buena', 'gusta', 'nuestro', 'nuevo', 'será',
        'haciendo', 'días', 'nombre', 'buen', 'había', 'ven', 'tres', 'menos', 'debe', 'tenía',
        'mal', 'conmigo', 'madre', 'hoy', 'quien', 'sido', 'mamá', 'tienen', 'luego', 'todas',
        'allí', 'toda', 'hora', 'mujer', 'visto', 'haces', 'importa', 'contigo', 've', 'tarde',
        'oye', 'parte', 'haber', 'hombres', 'problema', 'mas', 'saber', 'quería', 'aún', 'veces',
        'nuestra', 'hacerlo', 'cada', 'hizo', 'veo', 'tanto', 'razón', 'ustedes', 'idea', 'esos',
        'van', 'quizá', 'debo', 'alguna', 'cierto', 'ud', 'muerto', 'unos', 'estos', 'salir',
        'policía', 'realmente', 'demasiado', 'familia', 'pueden', 'cabeza', 'hemos', 'amigos',
        'chica', 'cariño', 'lado', 'allá', 'entre', 'minutos', 'digo', 'algún', 'serio',
        'cuidado', 'pasó', 'buenas', 'somos', 'amor', 'puerta', 'ves', 'vaya', 'ah', 'suerte',
        'eh', 'rápido', 'cuenta', 'quizás', 'io', 'esas', 'pues', 'pasado', 'pensé', 'todavía',
        'hermano', 'debes', 'casi', 'forma', 'aqui', 'chico', 'ok', 'dicho', 'nueva',
        'sabía', 'muchas', 'dentro', 'hice', 'contra', 'auto', 'camino', 'ayuda',
        'primera', 'hacia', 'vi', 'miedo', 'adiós', 'primero', 'debería', 'poder',
        'niños', 'sería', 'historia', 'hey', 'mientras', 'ciudad', 'dijiste', 'espero',
        'cuánto', 'esposa', 'pronto', 'chicos', 'cualquier', 'viejo', 'debemos', 'deja',
        'año', 'muerte', 'hablando', 'manos', 'da', 'loco', 'problemas', 'mano', 'guerra',
        'semana', 'pasar', 'vale', 'cuál', 'viene', 'volver', 'toma', 'caso', 'agua',
        'haré', 'vete', 'entiendo', 'horas', 'personas', 'capitán', 'adelante',
        'niño', 'listo', 'noches', 'buenos', 'iba', 'juntos', 'dame', 'único',
        'déjame', 'cerca', 'otros', 'sigue', 'grande', 'arriba', 'jefe', 'habla',
        'supongo', 'manera', 'quieren', 'feliz', 'significa', 'sangre', 'fin', 'bajo',
        'llama', 'venir', 'morir', 'importante', 'hiciste', 'ojos', 'escucha',
        'entrar', 'ningún', 'corazón', 'diablos', 'necesitamos', 'atrás', 'durante', 'dices',
        'nuestros', 'persona', 'abajo', 'dr', 'hija', 'dejar', 'necesita', 'llegar', 'hago',
        'señora', 'haya', 'suficiente', 'doctor', 'gustaría', 'tierra', 'cara', 'siquiera',
        'genial', 'cree', 'supuesto', 'tomar', 'equipo', 'justo', 'juego', 'ninguna', 'matar',
        'cinco', 'dicen', 'amo', 'cuándo', 'pequeño', 'algunos', 'conozco', 'clase', 'maldito',
        'unas', 'muchos', 'hubiera', 'segundo', 'aunque', 'pueda', 'dime', 'igual', 'comida',
        'ay', 'cuerpo', 'encontrar', 'fuerte', 'vuelta', 'venga', 'creer', 'realidad', 'saben',
        'puta', 'deberías', 'pregunta', 'fui', 'cuatro', 'sra', 'primer', 'trabajar', 'e',
        'hagas', 'alto', 'maldita', 'comer', 'número', 'dar', 'necesitas', 'john', 'oportunidad',
        'punto', 'misma', 'última', 'afuera', 'mujeres', 'pensar', 'fueron', 'difícil',
        'vivir', 'paso', 'malo', 'estabas', 'vivo', 'haga', 'queda', 'hijos', 'mayor', 'fiesta',
        'hacen', 'medio', 'algunas', 'basta', 'ei', 'arma', 'vino', 'meses', 'cuarto', 'éste',
        'escuela', 'esté', 'dólares', 'tío', 'posible', 'tuve', 'fácil', 'preocupes', 'jack',
        'luz', 'eran', 'carajo', 'final', 'lista', 'trata', 'armas', 'hermana', 'exactamente',
        'chicas', 'podía', 'bastante', 'seguridad', 'pasando', 'esperando', 'acá', 'teléfono',
        'perro', 'fuego', 'murió', 'tampoco', 'sola', 'estuvo', 'verte', 'iré', 'tenido',
        'culpa', 'veras', 'adónde', 'buscando', 'cuanto', 'padres', 'paz', 'demonios', 'estará',
        'cual', 'perdón', 'asi', 'jugar', 'pensando', 'esperar', 'sabemos', 'recuerdo',
        'par', 'joven', 'seguir', 'pueblo', 'tenga', 'caballeros', 'idiota', 'dio', 'minuto',
        'bebé', 'única', 'lejos', 'nuestras', 'plan', 'pienso', 'sentido', 'dormir', 'digas',
        'palabra', 'correcto', 'control', 'vemos', 'entiendes', 'país', 'seis', 'último', 'ésta',
        'diga', 'podrías', 'pequeña', 'cállate', 'trato', 'rey', 'sucede', 'sam', 'muchachos',
        'jamás', 'cama', 'srta', 'ayudar', 'acerca', 'di', 'cambio', 'falta', 'hospital',
        'lleva', 'presidente', 'mil', 'gusto', 'conoces', 'diciendo', 'os', 'ido', 'general',
        'extraño', 'semanas', 'coche', 'peor', 'mucha', 'disculpe', 'diré', 'anoche',
        'perder', 'vámonos', 'nave', 'cielo', 'habrá', 'orden', 'segura', 'querida', 'niña',
        'michael', 'increíble', 'además', 'deben', 'libro', 'calle', 'café', 'piensas',
        'hacemos', 'especial', 'queremos', 'ia', 'clark', 'irme', 'perfecto', 'buscar',
        'odio', 'piensa', 'oficina', 'hablas', 'libre', 'agente', 'york', 'llamar', 'mala',
        'detrás', 'viste', 'dile', 'grandes', 'recuerdas', 'real', 'estaban', 'mía', 'frente',
        'perdido', 'llamo', 'muertos', 'millones', 'asesino', 'sueño', 'quisiera', 'habría',
        'hará', 'viaje', 'probablemente', 'peter', 'resto', 'estaré', 'maldición', 'lamento',
        'muchacho', 'avión', 'ropa', 'fuerza', 'llamado', 'oído', 'frank', 'dado', 'encima',
        'negro', 'usar', 'información', 'uds', 'preguntas', 'tuvo', 'secreto', 'vuelve',
        'miren', 'quieras', 'haría', 'acaba', 'otras', 'incluso', 'sientes', 'deberíamos',
        'haz', 'decirte', 'boca', 'dolor', 'baño', 'adentro', 'profesor', 'habitación', 'daño',
        'tuyo', 'seas', 'noticias', 'demás', 'querido', 'duro', 'poner', 'prueba', 'mire', 'tonto',
        'campo', 'siendo', 'diez', 'ése', 'tranquilo', 'asunto', 'acabó', 'quédate', 'derecho',
        'placer', 'recuerda', 'estuve', 'tratando', 'ejército', 'futuro', 'llevar', 'compañía',
        'venido', 'listos', 'haremos', 'sitio', 'verlo', 'puesto', 'atención', 'sino', 'cambiar',
        'error', 'blanco', 'raro', 'palabras', 'llegó', 'sal', 'pase', 'mente', 'sistema',
        'película', 'anda', 'ello', 'negocio', 'novia', 'permiso', 'creí', 'suena',
        'ocurre', 'oficial', 'espere', 'aire', 'george', 'mató', 'harry', 'regresar',
        'vio', 'hazlo', 'trasero', 'grupo', 'entendido', 'señorita', 'música', 'perra',
        'conoce', 'empezar', 'siente', 'acabo', 'estúpido', 'diferente', 'traje', 'modo',
        'james', 'encontré', 'mensaje', 'llamada', 'navidad', 'eras', 'pena', 'largo',
        'entra', 'piso', 'foto', 'dijeron', 'médico', 'accidente', 'fuiste', 'imposible',
        'podríamos', 'línea', 'propia', 'barco', 'ganar', 'normal', 'segundos', 'vive', 'mitad',
        'quiera', 'tras', 'decirle', 'lindo', 'funciona', 'programa', 'vine', 'abre', 'sean',
        'pagar', 'fotos', 'centro', 'supone', 'basura', 'situación', 'mejores', 'vienen',
        'encanta', 'marido', 'personal', 'maestro', 'hambre', 'ataque', 'culo', 'dale',
        'pie', 'conseguir', 'trabajando', 'gracioso', 'dejó', 'pudo', 'derecha',
        'izquierda', 'próxima', 'pobre', 'respuesta', 'tipos', 'sentir', 'tenías',
        'pude', 'darle', 'voz', 'amiga', 'gustan', 'vista', 'salvo', 'loca', 'hotel',
        'hicieron', 'ten', 'temo', 'señal', 'pelo', 'llevo', 'ayer', 'das', 'nena', 'servicio',
        'tren', 'tom', 'bonito', 'mes', 'tendrá', 'tendrás', 'edad', 'ellas', 'hermosa',
        'ben', 'honor', 'simplemente', 'llamas', 'tengas', 'corre', 'baja', 'sol',
        'siéntate', 'dan', 'humano', 'divertido', 'sexo', 'vuelto', 'peligro', 'mesa',
        'jimmy', 'siguiente', 'hablo', 'disculpa', 'decirme', 'joe', 'caja', 'negocios',
        'misión', 'silencio', 'sale', 'llegado', 'estaría', 'regreso', 'media', 'estan',
        'propio', 'charlie', 'oro', 'enseguida', 'linda', 'prometo', 'esposo', 'norte',
        'hubo', 'juro', 'muerta', 'interesante', 'pensaba', 'busca', 'terminar', 'tendré',
        'completamente', 'cita', 'siete', 'cumpleaños', 'abogado', 'alrededor', 'cerebro',
        'porqué', 'llave', 'santo', 'hermoso', 'necesario', 'edificio', 'irnos', 'aun',
        'tendremos', 'vayas', 'doy', 'trae', 'salió', 'ley', 'ahi', 'verdadero', 'pelea',
        'banco', 'terrible', 'calma', 'cena', 'daré', 'gobierno', 'comprar', 'creen',
        'sargento', 'destino', 'bob', 'existe', 'hacía', 'novio', 'sala', 'través',
        'regalo', 'iglesia', 'decía', 'cualquiera', 'excelente', 'esperen', 'deseo',
        'alma', 'diablo', 'deje', 'cuántos', 'espada', 'estábamos', 'carne', 'maravilloso',
        'vidas', 'sucedió', 'oí', 'peligroso', 'dirección', 'libertad', 'jesús',
        'ocurrió', 'veré', 'sueños', 'pudiera', 'detective', 'sorpresa', 'tuya', 'pies', 'club',
        'terminado', 'infierno', 'creía', 'luna', 'salvar', 'carta', 'estés'
    ]
}


def get_words(dic, n=8):
    """ get N random words """
    return random.choices(dic, k=n)


def make_text(dic, m=6, n=8):
    """ compose M sentences N words each """

    sentences = []
    for _ in range(m):
        words = get_words(dic, n)
        words[0] = words[0].capitalize()
        sentence = "%s." % (" ".join(words))
        sentences.append(sentence)

    return " ".join(sentences)


def make_all_texts(languages=None, m=6, n=8):
    """ compose sentences for listed/all languages """

    if not languages:
        languages = sorted(DICTIONARY.keys())

    output = []
    for lang in languages:

        if lang not in DICTIONARY:
            print("Error: `%s` is not in the dictionary." % lang, file=sys.stderr)
            continue

        text = make_text(DICTIONARY[lang], m=m, n=n)
        output.append((lang, text))

    return output


def output_html(output):
    """ format output as 'nice' html """
    html = ("""<!DOCTYPE html><html>\n<head><meta charset="utf-8">"""
            """<style>*{margin:0; padding:0;}body{font-size:1.5rem;padding:4rem;}"""
            """p{margin: 0 0 2rem 0;}</style><title>ipsum qwasa.net</title>"""
            """</head>\n<body>\n%s\n</body>\n</html>""")
    content = "\n".join(["<p>%s</p>" % (s[1]) for s in output])
    return html % (content)


def output_json(output):
    """ return output as json string """
    content = json.dumps({s[0]: s[1] for s in output},
                         indent=2,
                         ensure_ascii=False,
                         sort_keys=True,
                         default=lambda x: "?")
    return content


def load_dictionary(filename, lang=None):
    """ load file and read words (one per line) """
    DICTIONARY[lang] = []
    with open(filename, 'rb') as f:
        for line in f.readlines():
            word = line.decode("utf-8", errors="ignore")
            word = re.sub(r'[\n\r\s]', '', word)
            DICTIONARY[lang].append(word)
    return len(DICTIONARY[lang])


def main():
    """ generate some random mumbling """

    # parse commandline
    aprs = argparse.ArgumentParser(description=make_text(DICTIONARY['english'], n=6, m=2))
    aprs.add_argument('language', type=str, nargs='*', )
    aprs.add_argument('--words', '-w', metavar="N", type=int, default=10)
    aprs.add_argument('--sentences', '-s', metavar="M", type=int, default=8)
    aprs.add_argument('--dictionary', '-d', metavar="FILENAME", type=str)
    aprs.add_argument('--dictionary-language', '-dl', type=str)
    aprs.add_argument('--verbose', '-v', action='store_true', default=False)
    aprs.add_argument('--html', action='store_true')
    aprs.add_argument('--json', action='store_true')
    args = aprs.parse_args()

    # load custom dictionary (/usr/share/dict/words -> words)
    if args.dictionary:
        lang = (args.dictionary_language
                or os.path.basename(args.dictionary).split(".")[0])
        load_dictionary(args.dictionary, lang)
        if not args.language:
            args.language = [lang, ]

    # if languages are not set, then use all available
    if not args.language:
        args.language = sorted(DICTIONARY.keys())

    # generate all texts
    output = make_all_texts(args.language, n=args.words, m=args.sentences)

    # print texts in desired format html/json/plain text
    if args.html:
        print(output_html(output))

    elif args.json:
        print(output_json(output))

    else:
        for (lng, txt) in output:
            if args.verbose:
                print("%s:\n%s\n" % (lng, txt))
            else:
                print(txt)


if __name__ == "__main__":
    main()

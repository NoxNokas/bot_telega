# bot_telega


Задание №1
==========
    - Файл с расписанием в csv (день, время, что)
    - Бот:
        отправляете день: получаете все события из csv с этим днём
        Когда делаем запрос на получение расписания на сегодня мы получаем,
        также погоду на сегодня.
        
      Доп задание: отправляем боту команду `/remind <text>` в тексте будет
    дата. Нужно будет распарсить текст и найти дату, и создать событие в
    scheduler (модуль исполнения функции по расписанию)  

Задание №2
==========

    В нашем TG Bot  есть юзеры,
    Давайте будем хранить наших юзеров в sqlitedb
    На каждое действие будем класть в базу данных инфо 
    о событии и кто это событие сделал
    
    | + users + |                       | + actions +|
    | -  id     |  <------------------- | - user_id  |
    | - name    |                       | - action   |
    Примечание:
        - база данных на основе sqlite3
        - реализовать запись данных при помощи декоратора
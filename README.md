# ITMO_schedule_analyser
Code part of my Bachelor's Thesis.

Скрипт работает в 4 этапа, соответствующих файлам с Python-кодом.
Этап 1 заключается в получении списка групп, у которых по расписанию есть занятия в аудиториях, находящихся в корпусе на Кронверкском 49, список которых получен с его плана, доступного на сайте Университета ИТМО. Сбор информации заключается в получении ответа от ifmo.ru с помощью библиотеки urllib2 и парсинга их регулярными выражениями с помощью библиотеки re.
На этапе 2 каждой группе из списка сопоставляется число студентов, состоящих в ней на основании данных, хранящихся на isu.ifmo.ru. Это делается с помощью библиотеки для веб-тестирования selenium, так как другого способа пройти авторизацию сайта найдено не было. Следует заметить, что скрипт работает неприемлемо долго, так как имитирующий пользовательское взаимодействие selenium ждет прорисовку каждой страницы порядка 2 секунд, что при выполнении на 578 групп дает очень большую задержку.
Этап 3 состоит в расчете нагрузки. Как уже было замечено, сайт ifmo.ru позволяет обращаться к расписанию по аудиториям, что весьма удобно, однако, обладает одной не очень приятной особенностью: в случае существования аудитории с номером Х более чем в одном корпусе, расписание будет показано для всех корпусов. К тому же, пары бывают 3 видов: по четным неделям, по нечетным неделям и по всем (общая). Таким образом, для точного расчета нагрузки необходимо учесть:
адрес аудитории;
день недели;
время;
тип пары: четная/нечетная/общая;
группы.
Что и было сделано с помощью использования языка XPath в функционале библиотеки lxml, однако стоит заметить, что вёрстка расписания выполнена не лучшим образом и имеет проблемы в логике (например, html-теги td, содержащие span’ы, которые содержат информацию о времени проведения занятия и о группе, оба имеют параметр class="time", что весьма странно и оставляет единственный способ различить, так как тег группы еще имеет параметр style="width:8%", никаким образом не указывающий на смысловую составляющую содержимого). Также выяснилось, что дней недели в расписании гораздо больше 6, так как ими могут оказаться как двухбуквенные сокращения  вроде “Пн” и “Вт”, так и дата в формате ДД.ММ.ГГГГ, потому что и регулярные и нерегулярные занятия пишутся в одно расписание, причем у нерегулярных дней также выставляется значения дня недели в id таблицы, что в результате может заставить программу думать, что в маленькой компьютерной аудитории 371 может одновременно находиться 276 человек (так как в определенный день недели в одно и то же время по расписанию в ней должно находиться именно столько). Из-за всех этих недостатков выражения XPath и сам код получились не стройными. Результатом расчета является сумма и максимальное значение студенто-часов. Для правильного понимания следует внести ясность в определения.
Студенто-час – студент, проводящий университетский час в аудитории, которая предписана его группе по расписанию.
Университетский час – два академических часа (2 * 45 = 90 минут). Определение введено по причине того, что в Университете ИТМО, как и в большинстве российских ВУЗов, занятия проводятся “парами”, то есть двумя академическими часами подряд без перерыва.
Таким образом, для получения “правильных” студенто-часов необходимо умножить полученные результаты на 2, однако качественного изменения в данные это действие не внесет.
На этапе 4 результаты расчета нагрузки форматируются в более удобный для чтения csv-формат, с которым может работать математическое ПО, такое как Microsoft Excel или LibreOffice Calc.
Python-скрипты обернуты в shell-скрипт, который их поочередно вызывает и перенаправляет выводы в соответствующие файлы. Такое решение было продиктовано, во-первых, желанием упростить файловый вывод, отдав его под управление средств ОС, во-вторых, необходимостью создать “контрольные точки” (если выполнение скрипта закончится с ошибкой на этапе Х, предыдущие этапы можно не выполнять, закомментировав соответствующие строки в script.sh) и, в третьих, особенностями объекта исследования и urllib2. Дело в том, что количество проверяемых аудиторий очень велико (277) и на каждую отправляется request, что может приводить к ошибке типа <urlopen error [errno 110] connection timed out> даже в пределах одного этажа. Для решения этой проблемы было решено разбить анализ разных этажей на разные вызовы скрипта (номер этажа передается параметром командной строки) – каждый вызов дописывает результат выполнения в соответствующий файл, из которого потом читает последующий скрипт. 
Для исследования был использован интерпретатор Python 2.7.12 (default, Nov 12 2018, 14:36:49) и  [GCC 5.4.0 20160609] on linux2 на базе системы    Linux HP-EliteBook-2560p 4.15.0-43-generic #46~16.04.1-Ubuntu SMP Fri Dec 7 13:31:08 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux.
Стоит заметить, что для правильной работы скрипта необходимы библиотеки urllib2, re, os, sys, time, itertools, selenium, lxml, csv.

# Ближайшие бары

Программа анализирует данные о барах Москвы с сайта [data.mos.ru](https://data.mos.ru/). На основе полученной информации определяет:
1. Самый большой бар города
2. Самый маленький бар города
3. Ближайший к вам бар

### Пример

```ShellSession
>python bars.py
Самый большой бар — Спорт бар «Красная машина»
Самый маленький бар — Сушистор
 
Сейчас я найду ближайший к вам бар
Широта на которой вы находитесь:55.2193673
Высота на которой вы находитесь:37.4114704
Ближайший бар — Торнадо
```

# Требования

Совестимые OC:
* Linux,
* Windows

Скрипт требует для своей работы установленного интерпретатора Python версии 3.5

Файл должен быть в формате `.json`

# Как запустить

Запуск на Linux:

```bash

$ python bars.py
Самый большой бар — Спорт бар «Красная машина»
Самый маленький бар — Сушистор
 
Сейчас я найду ближайший к вам бар
Широта на которой вы находитесь:<Широта> #Широту вводите в градусач
Высота на которой вы находитесь:<Высота> #Высоту водите в градусах
Ближайший бар — #Ближайший бар


```

Запуск на Windows происходит аналогично.
> Координаты нужно вводить в градусах с точкой. Пример: `55.4678922`

# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)

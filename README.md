# Локтевизация

Ссылка: https://nikgohn.github.io/loktevization 

Веб версия лекций курса "Управление в технических системах" на основе [Quartz](https://github.com/jackyzha0/quartz) и [obsidian-quartz-template](https://github.com/defenderofbasic/obsidian-quartz-template)

## Добавление контента

В основе текстового наполнения сайта лежат Markdown файлы, находящиеся в [source/content](./source/content), которые можно сделать при помощи [Obsidian](https://obsidian.md/) или любого другого редактора с поддержкой Markdown. Эта же папка является хранилищем Obsidian. HTML генерируется с использованием [Quartz](https://github.com/jackyzha0/quartz). Чтобы сгенерировать HTML локально, выполните команду `npx quartz build --serve` в папке `./source/`.  

## Исходные HTML-страницы  

В папке [`source/raw_html`](./source/raw_html) находятся файлы, которые копируются в папку сборки при CI.  
Это позволяет размещать произвольный HTML-контент вне Quartz.  
Пример: [ссылка](https://nikgohn.github.io/loktevization/raw-html-test.html).  

Существует возможность хоста "сырого HTML" для тех, кто создает HTML-интерфейсы с помощью Claude/ChatGPT, но хочет их доработать или разместить самостоятельно.  
Также это может быть полезно для создания личного архива веб-страниц и других задач.  

## Дальнейшая кастомизация  

> Quartz создан для высокой конфигурируемости, даже если у вас нет навыков программирования.  
> Большинство настроек можно изменить, просто отредактировав `quartz.config.ts` или изменив макет в `quartz.layout.ts`.  

Подробнее: [Quartz Configuration](https://quartz.jzhao.xyz/configuration). 
# backend

Стек: FastApi, PostgreSQL, docker, k Nearest Neighbors, sentence embedding, Spacy

Как работает алгоритм:

Чтобы совершить предсказание ТН ВЭД, категории товара и технического регламента, мы используем алгоритм, в основе которого лежит гипотеза компактности: "в задачах классификации это предположение о том, что схожие объекты гораздо чаще лежат в одном классе, чем в разных"
Мерой "схожести" объектов в нашем случае выступила семантическая близость наименований продуктов.

![Screen-Shot-2018-04-25-at-13 21 44-16dcb3ee-be28-40ca-a2f7-da6a60833717](https://user-images.githubusercontent.com/69757240/179385809-ab5106ea-e156-4cf8-8032-1b27033c8e29.png)

Чтобы совершить предсказание для конкретного наименования, сперва, с помощью библиотеки Spacy мы строим его векторное, 300-мерное представление, а затем сравниваем с векторными представлениями для каждого другого уже имеющегося наименования в базе данных, считая их семантическую близость. На основе высчитанной семантической близости искомого относительно каждого элемента базы данных, мы ранжируем выдачу и отбираем k "ближайших" наименований. (В нашем случае k = 3.) Согласно гипотезе компактности, эти айтемы будут являться носителями того же класса, что и "искомый" элемент. Так же стоит отметить, что для улучшения метрик модели, мы сделали так, чтобы айтемы, которые находятся ближе, то есть, айтемы с большей семантической близостью вносили большее влияние в предсказание.

![i](https://user-images.githubusercontent.com/69757240/179385772-ae52b6ec-0745-475b-9884-2c6fe89d758d.jpeg)

![sdIpEDK94aw](https://user-images.githubusercontent.com/69757240/179385820-1169d3b7-b715-4e05-a778-d499291cd580.jpg)

Если же мы решаем задачу нахождения ошибки, то для этого нам необходимо совершить предсказание для конкретного названия продукции и отслеживать расхождения с предоставленными данными.

![architecture-415624fc7d149ec03f2736c4aa8b8f3c](https://user-images.githubusercontent.com/69757240/179386060-1b3c457d-3b90-41de-a3b6-15f07783aeeb.svg)

Такой подход к модели позволяет нам добиться интерпретируемости результатов - похожие предметы имеют схожие категории, а соответственно и схожие вектора. Из-за такого подхода наша система чрезвычайно гибкая, она способна классифицировать объект более чем на тысячу классов, а добавление новых классов происходит без необходимости переобучать модель, что существенно облегчает интеграцию решения в условии неполного объема данных и обеспечивает беспрецедентную масштабируемость системы. 

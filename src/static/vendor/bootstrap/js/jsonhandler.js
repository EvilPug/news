var films = {
  "id1": {
    "name": "Матрица",
    "rating":"Кинопоиск: 8.5",
    "duration":"2:30",
    "genre":"Научная фантастика"
  },
  "id2": {
    "name": "Побег из Шоушенка",
    "rating":"Кинопоиск: 9.1",
    "duration":"2:22",
    "genre":"Драма"
  },
  "id3": {
    "name": "Стальной алхимик: Братство",
    "rating":"Кинопоиск: 8.5",
    "duration":"0:25",
    "genre":"Аниме, Фэнтэзи",
  },
  "id4": {
    "name": "The Wall",
    "rating":"Кинопоиск: 8.1",
    "duration":"1:39",
    "genre":"Мюзикл"
    }
}
document.getElementById('name1').innerHTML = films.id1.name;
document.getElementById('rating1').innerHTML = 'Рейтинг: ' + films.id1.rating;
document.getElementById('duration1').innerHTML = 'Длительность: ' + films.id1.duration;
document.getElementById('genre1').innerHTML = 'Жанр: ' + films.id1.genre;

document.getElementById('name2').innerHTML = films.id2.name;
document.getElementById('rating2').innerHTML = 'Рейтинг: ' + films.id2.rating;
document.getElementById('duration2').innerHTML = 'Длительность: ' + films.id2.duration;
document.getElementById('genre2').innerHTML = 'Жанр: ' + films.id2.genre;

document.getElementById('name3').innerHTML = films.id3.name;
document.getElementById('rating3').innerHTML = 'Рейтинг: ' + films.id3.rating;
document.getElementById('duration3').innerHTML = 'Длительность: ' + films.id3.duration;
document.getElementById('genre3').innerHTML = 'Жанр: ' + films.id3.genre;

document.getElementById('name4').innerHTML = films.id4.name;
document.getElementById('rating4').innerHTML = 'Рейтинг: ' + films.id4.rating;
document.getElementById('duration4').innerHTML = 'Длительность: ' + films.id4.duration;
document.getElementById('genre4').innerHTML = 'Жанр: ' + films.id4.genre;

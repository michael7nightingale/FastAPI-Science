<script>

</script>


<template>
<div class="jumbotron">
    <h2>Графики функций</h2>
    <p class="lead">Вносите изменения в неопубликованные статьи или вовсе удаляйте их</p>
    <h4 style="color: indianred"></h4>
    <a href="" class="btn btn-primary btn-large">назад к математике &raquo;</a>
</div>

<div class="container">
    <form method="post" action="">
        <input class="form-control" type="text" name="function1" placeholder="Функция 1">
        <input class="form-control" type="text" name="function2" placeholder="Функция 2">
        <input class="form-control" type="text" name="function3" placeholder="Функция 3">
        <input class="form-control" type="text" name="function4" placeholder="Функция 4">
        <input class="form-control" type="text" value=-100 name="xmin" placeholder="x min">
        <input class="form-control" type="text" value=100 name="xmax" placeholder="x max">
        <input class="form-control" type="text" value=-100 name="ymin" placeholder="y min">
        <input class="form-control" type="text" value=100 name="ymax" placeholder="y max">
        <input type="submit" value="Построить график">
    </form>

    <img src="" width="100%">
    <form method="post" action="">
        <input class="white_text" type="text" name="filesurname" placeholder="Скачать как:">
        <input type="submit" value="Скачать">
    </form>
    <h3></h3>
</div>
</template>


<style>

</style>
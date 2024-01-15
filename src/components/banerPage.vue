<template>
    <div id="baner">
        <router-link to="/" id="baner-logo">

        </router-link>
        <div id="baner-nav">
            <a class="button" @click="show_buttons">Rozwiń</a>
            <router-link to="/add-user" class="menu">Dodaj Użytkownika</router-link>
            <router-link to="/assign-user" class="menu">Przypisz Użytkownika</router-link>
            <router-link to="/punctation" class="menu">Punktacja</router-link>
            <router-link to="/filling-level" class="menu">Zapełnienie Kosza</router-link>
        </div>
    </div>
</template>
<script>
import { ref } from 'vue';

export default
{
    setup()
    {
        var visible = ref(false);

        const show_buttons = () => {
            visible.value = !visible.value;
            const menus = document.getElementsByClassName("menu");

            for (let i = 0; i < menus.length; i++) {
                if (visible.value) {
                    menus[i].style.display = "inline";
                } else {
                    menus[i].style.display = "none";
                }
            }
        };

        return { show_buttons };
    }

}
</script>
<style scoped lang="scss">
@import '../style/style.scss';
    *
    {
        z-index: 1000;
        user-select: none;
    }
    #baner
    {
        height: 100px;
        border-bottom: 1px solid $border-color2;
        display: flex;
        justify-content: space-around;
        background-color: $main-color;

        &-logo
        {
            height: 100px;
            width: 100px;
            background-image: url('../assets/smietnik.png');
            background-size: contain;
            background-repeat: no-repeat;
        }
        &-nav
        {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            width: 60%;
            height: 100%;

            .button
            {
                display: inline;
            }
            .menu
            {
                display: none;
            }

            & a
            {
                text-decoration: none;
                background-color: white;
                color: $main-color;
                font-weight: bold;
                width: 75%;
                text-align: center;
                padding: 10px;
                cursor: pointer;
            }
        }
    }
    @media only screen and (min-width: 1000px)
    {
        #baner
        {
            height: 100px;
            border-bottom: 1px solid $border-color2;
            display: flex;
            justify-content: space-around;
            background-color: $main-color;
            z-index: 10000;

            &-logo
            {
                height: 100px;
                width: 100px;
                background-image: url('../assets/smietnik.png');
                background-size: contain;
                background-repeat: no-repeat;
            }
            &-nav
            {
                display: flex;
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
                width: 60%;
                height: 100%;

                .button
                {
                    display: none;
                }
                .menu
                {
                    display: inline;
                }

                & a
                {
                    text-decoration: none;
                    background-color: white;
                    color: $main-color;
                    width: 20%;
                    font-weight: bold;
                    padding: 10px;
                    cursor: pointer;
                }
            }
        }
    }
</style>
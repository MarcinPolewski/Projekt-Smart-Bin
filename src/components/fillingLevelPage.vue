<template>
    <div id="main">
        <div id="main-bar">
            <div id="main-bar-inside" :style="{height: filling + '%'}">

            </div>
        </div>
        <div id="main-change">
            <h2 @click="addFilling">+</h2>
            <h2 @click="rmFilling">-</h2>
        </div>
    </div>
</template>
<script>
import { ref } from 'vue';

export default
{
    setup()
    {
        var filling = ref(90)

        const addFilling = () =>
        {
            filling.value++
        }

        const rmFilling = () =>
        {
            filling.value--
        }

        return {filling, addFilling, rmFilling}
    }
}
</script>
<style scoped lang="scss">
@import '../style/style.scss';
    #main
    {
        //min-height: 80vh;
        height: 800px;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;

        &-change
        {
            margin-left: 10%;
            display: flex;
            flex-direction: column;
            width: 50px;
            & h2
            {
                width: 100%;
                text-align: center;
            }
        }

        &-bar
        {
            width: 30%;
            height: 60%;
            display: flex;
            justify-content: center;
            align-items: flex-end;

            background-color: green;

            &-inside
            {
                width: 70%;
                height: 90%;
                background-color: red;
                margin-bottom: 50px;
            }
        }
    }
</style>
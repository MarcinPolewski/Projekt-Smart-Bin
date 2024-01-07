<template>
    <div id="main">
        <div id="main-left">
            <h2>Kosz pod zlewem</h2>
            <div id="main-bar">
                <div id="main-bar-inside" :style="{height: filling + '%'}"></div>
                <div id="main-change">
                    <h2 @click="addFilling">+</h2>
                    <h2 @click="rmFilling">-</h2>
                </div>
            </div>
        </div>
        <div id="main-right">
            <div>
                <h2>Harmonogram wynoszenia</h2>
                <a>Teraz jest kolej: Tomek<br></a>
                <a>Później będzie kolej: Kasia<br></a>
            </div>
            <div>
                <h2>Uwaga. Kosz nie został opróżniony od 48h</h2>
                <a>Za wyniesienie otrzymasz 20 pkt.<br></a>
                <a>Każde kolejne 12h spowoduje odebranie Ci 10pkt</a>
            </div>
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

        #main-left
        {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            width: 50%;
            height: 100%;

            #main-change
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

            #main-bar
            {
                width: 30%;
                height: 60%;
                display: flex;
                justify-content: center;
                align-items: flex-end;

                background-color: green;

                #main-bar-inside
                {
                    width: 70%;
                    height: 90%;
                    background-color: red;
                    margin-bottom: 50px;
                }
            }
        }

        #main-right
        {
            display: flex;
            flex-direction: column;
            justify-content: center;
            width: 50%;
            height: 100%;
        }
    }
</style>
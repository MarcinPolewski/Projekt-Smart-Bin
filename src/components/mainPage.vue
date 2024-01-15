<template>
    <div id="main">
        <div id="container">
            <div id="img-div">
                <img src="../assets/kosz.png">
                <p>{nazwa kosza}</p>
            </div>
            <div id="info">
                <div id="info-graphic">
                    <div class="info-graphics">
                        <a class="green-circle">
                            Teraz
                        </a>
                        <a class="green-text">
                            {Kasia}
                        </a>
                    </div>
                    <div class="info-graphics">
                        <a class="white-circle">
                            Później
                        </a>
                        <a class="green-text">
                            {Martyna}
                        </a>
                    </div>
                </div>
                <div id="info-description">
                    <h2>Uwaga!</h2>
                    <a>Kosz nie został wyniesiony od {48h}</a>
                    <a>Dostaniesz {20} pkt za wyniesienie</a>
                    <a>Za każde {12h} zabierzemy ci {10} pkt</a>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default
{

}
</script>
<style scoped lang="scss">
@import '../style/style.scss';
#main
    {
        min-height: 80vh;
        display: flex;
        justify-content: center;

        #container
        {
            width: 80%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;

            #img-div
            {
                display: flex;
                flex-direction: column;
                align-items: center;

                img
                {
                    width: 100%;
                }

                p
                {
                    margin-top: 5%;
                    font-weight: bold;
                    font-size: 2rem;
                }
            }

            #info
            {
                display: flex;
                flex-direction: column;
                width: 100%;

                #info-graphic
                {
                    display: flex;
                    justify-content: space-between;
                    .info-graphics
                    {
                        display: flex;
                        flex-direction: column;
                        .green-circle
                        {
                            background-color: $main-color;
                            color: white;
                            width: 100px;
                            height: 100px;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            border-radius: 100vw;
                        }
                        .white-circle
                        {
                            background-color: white;
                            color: $main-color;
                            width: 100px;
                            height: 100px;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            border-radius: 100vw;
                            border: 1px solid $main-color;
                        }
                        .green-text
                        {
                            color: $main-color;
                            text-align: center;
                            width: 100px;
                            font-weight: bold;
                            margin-top: 15%;
                        }
                    }
                }

                #info-description
                {
                    display: flex;
                    flex-direction: column;

                    h2
                    {
                        color: $main-color2;
                    }
                    a
                    {
                        line-height: 2rem;
                    }
                }
            }
        }
    }
    @media only screen and (min-width: 1000px)
    {
        #main
        {
            min-height: 80vh;
            display: flex;
            justify-content: center;

            #container
            {
                width: 80%;
                display: flex;
                flex-direction: row;
                justify-content: space-between;
                align-items: center;

                #img-div
                {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin-right: 10%;
                    p
                    {
                        margin-top: 5%;
                        font-weight: bold;
                        font-size: 2rem;
                    }
                }

                #info
                {
                    display: flex;
                    flex-direction: column;
                    width: 100%;

                    #info-graphic
                    {
                        display: flex;
                        justify-content: space-between;
                        .info-graphics
                        {
                            display: flex;
                            flex-direction: column;
                            .green-circle
                            {
                                background-color: $main-color;
                                color: white;
                                width: 100px;
                                height: 100px;
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                border-radius: 100vw;
                            }
                            .white-circle
                            {
                                background-color: white;
                                color: $main-color;
                                width: 100px;
                                height: 100px;
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                border-radius: 100vw;
                                border: 1px solid $main-color;
                            }
                            .green-text
                            {
                                color: $main-color;
                                text-align: center;
                                width: 100px;
                                font-weight: bold;
                                margin-top: 15%;
                            }
                        }
                    }

                    #info-description
                    {
                        display: flex;
                        flex-direction: column;

                        h2
                        {
                            color: $main-color2;
                        }
                        a
                        {
                            line-height: 2rem;
                        }
                    }
                }
            }
        }
    }
</style>
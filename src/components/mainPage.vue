<template>
    <div id="main">
        <div id="container">
            <div id="img-div">
                <img src="../assets/kosz.png">
                <p>{{ binName }} ({{ binDepth }}cm)</p>
                <p>Wypełniony w {{ fillingPercentage }}%</p>
            </div>
            <div id="info">
                <div id="info-graphic">
                    <div class="info-graphics">
                        <a class="green-circle">
                            Teraz
                        </a>
                        <a class="green-text">
                            {{ whoNow }}
                        </a>
                    </div>
                    <div class="info-graphics">
                        <a class="white-circle">
                            Później
                        </a>
                        <a class="green-text">
                            {{ whoNext }}
                        </a>
                    </div>
                </div>
                <div id="info-description">
                    <h2>Uwaga!</h2>
                    <a>Kosz nie został wyniesiony od {{ whenEmptied }}</a>
                    <a>Dostaniesz {{ pointsToAdd }} pkt za wyniesienie</a>
                    <a>Za każde 12h zabierzemy ci {{ pointsToRemove }} pkt</a>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { inject, ref } from 'vue';
import axios from "axios";

export default
{
    setup()
    {
        const endpoint = inject("g_endpoint")
        var binName = ref("")
        var binDepth = ref("")
        var pointsToAdd = ref("")
        var pointsToRemove = ref("")
        var whenEmptied = ref("")
        var whoNow = ref("")
        var whoNext = ref("")
        var fillingPercentage = ref("")

        var nearestDates = ref("")

        const checkFilling = async () =>
        {
            const response = await axios
            .get(`${endpoint}bins/1/`)

            let status = response.data.bin_status

            fillingPercentage.value = 100*status/binDepth.value
        }

        const fetchBinName = async () =>
        {
            try
            {
                const response = await axios
                .get(`${endpoint}bins/1/`);

                binName.value = response.data.bin_name;
                binDepth.value = response.data.bin_depth;
                pointsToAdd.value = response.data.adding_points;
                pointsToRemove.value = response.data.subtrack_points;

                const response2 = await axios
                .get(`${endpoint}schedule/`);

                nearestDates.value = [];

                response2.data.forEach((element) =>
                {
                    nearestDates.value.push(element.data);
                });

                nearestDates.value = findNearestDates(nearestDates.value)

                whoNow.value = nearestDates.value[0]
                whoNext.value = nearestDates.value[1]
            }
            catch(error)
            {
                console.log(error)
            }
        }

        const findNearestDates = (variables) =>
        {
            const today = new Date();
            const dateList = [];

            for (const variable of variables)
            {
                const date = new Date(variable);
                if (!isNaN(date.getTime()))
                {
                    dateList.push(date);
                }
            }

            if (dateList.length === 0)
            {
                return ["Dat nie ustalono", "Dat nie ustalono"];
            }

            dateList.sort((a, b) => a - b);

            let closestDates = [];
            for (let i = 0; i < dateList.length; i++)
            {
                if (dateList[i] >= today)
                {
                    closestDates.push(dateList[i]);
                }
                if (closestDates.length === 2)
                {
                    break;
                }
            }

            if (closestDates.length < 2)
            {
                return ["Dat nie ustalono", "Dat nie ustalono"];
            }

            const formattedDates = closestDates.map(date =>
            {
                const day = date.getDate().toString().padStart(2, '0');
                const month = (date.getMonth() + 1).toString().padStart(2, '0');
                const year = date.getFullYear();
                return `${day}-${month}-${year}`;
            });

            return formattedDates;
        }

        const fetchTakeoutDate = async () =>
        {
            try {
                const response = await axios.get(`${endpoint}takeout/`);

                if (response.data.length > 0) {
                    const takeoutDate = new Date(response.data[response.data.length - 1].date);
                    const currentTime = new Date();

                    const timeDifference = currentTime.getTime() - takeoutDate.getTime();
                    const hoursDifference = Math.floor(timeDifference / (1000 * 60 * 60)); // Liczba pełnych godzin
                    const minutesDifference = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60)); // Liczba pełnych minut
                    const secondsDifference = Math.floor((timeDifference % (1000 * 60)) / 1000); // Liczba pełnych sekund

                    whenEmptied.value = (`${hoursDifference} godzin ${minutesDifference} minut ${secondsDifference} sekund`);
                } else {
                    console.log("Brak danych o wyjściach.");
                }
            } catch (error) {
                console.error(error);
            }
        };

        fetchBinName()

        checkFilling()

        fetchTakeoutDate()

        setInterval(checkFilling, 1000)
        setInterval(fetchTakeoutDate, 1000)

        return {binName, binDepth, pointsToAdd, pointsToRemove, whenEmptied, whoNext, whoNow, fillingPercentage, nearestDates}
    }
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
                    text-align: center;
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
                    align-items: flex-start;

                    #info-graphic
                    {
                        width: 50%;
                        max-width: 500px;
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
<template>
    <div id="main">
        <div id="main-form">
            <h4>Dodaj użytkownika</h4>
            <input type="email" placeholder="email" v-model="currentUserMail"/>
            <input type="text" placeholder="name" v-model="currentUserName"/>
            <select v-model="statistics">
                <option selected hidden disabled :value="0">Jak często chcesz otrzymywać statystyki na email?</option>
                <option :value="1">Codziennie</option>
                <option :value="7">Co tydzień</option>
                <option :value="30">Co miesiąc</option>
                <option :value="90">Co trzy miesiące</option>
            </select>
            <select>
                <option selected hidden disabled>Który kosz wynosisz?</option>
                <option>Kosz pod zlewem</option>
            </select>

            <h2>{{ warning_error }}</h2>

            <input type="button" value="Potwierdź" @click="addUser"/>
            <p>Oto lista stworzonych użytkowników:</p>
            <ul>
                <li v-for="user in userList" :key="user">{{ user.user_name }}, {{ user.user_mail }}</li>
            </ul>
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

        var userList = ref([])
        var currentUserMail = ref()
        var currentUserName = ref()
        var statistics = ref()
        var warning_error = ref("")

        const addUser = async () =>
        {
            try
            {
                let data =
                {
                    user_name: currentUserName.value,
                    user_mail: currentUserMail.value,
                    statistics_days: statistics.value,
                    which_bin: 1
                }
                let dataJ = JSON.stringify(data)
                await axios
                .post(`${endpoint}users/`, dataJ, {
                withCredentials: true,
                headers: {'Content-Type': "application/json"}})

                warning_error.value = "Poprawnie dodano użytkownika"

                refreshUsers()
            }
            catch (error)
            {
                console.error(error);
                warning_error.value = "Błędne dane"
            }
        }

        const refreshUsers = async () =>
        {
            try
            {
                const response = await axios.get(`${endpoint}users/`);
                const responseData = response.data;

                responseData.forEach((user) =>
                {
                    userList.value.push(user);
                });
                console.log(userList.value)

                warning_error.value = "Poprawnie dodano użytkownika"
            }
            catch (error)
            {
                console.error(error);
                warning_error.value = "Błędne dane"
            }
        }
        refreshUsers()

        const putBin = async () =>
        {
            try
            {
                const binId = 1;  // Identyfikator kosza do aktualizacji
                const data =
                {
                    bin_name: "Kosz pod zlewem",
                    bin_depth: 60,
                    emp_calendar: 2,
                    emp_reminder: 2,
                    adding_points: 2,
                    subtrack_points: 2,
                };

                axios.put(
                `${endpoint}bins/${binId}/`,
                JSON.stringify(data),
                {
                    withCredentials: true,
                    headers: {
                    'Content-Type': 'application/json',
                    }
                }
                );

                console.log("Pomyślnie zaktualizowano kosz!");

            }
            catch (error)
            {
                console.error("Błąd podczas aktualizacji kosza:", error);
            }
        }

        return {userList, currentUserMail, currentUserName, addUser, statistics, warning_error}
    }
}
</script>
<style scoped lang="scss">
@import '../style/style.scss';
    #main
    {
        width: 100%;
        min-height: 80vh;
        display: flex;
        justify-content: center;

        &-form
        {
            width: 50%;
            display: flex;
            flex-direction: column;

            & h4, input, select
            {
                margin-top: 5%;
            }

            & p
            {
                margin-top: 10%;
            }
        }
    }
</style>
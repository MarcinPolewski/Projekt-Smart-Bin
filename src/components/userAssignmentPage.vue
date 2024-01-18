<template>
    <div id="main">
        <div id="top">
            <h1>Przypisz użytkownika</h1>
            <h2>Teraz konfigurujesz: Kosz pod zlewem</h2>
        </div>
        <div id="center">
            <div id="main-assign">
                <p>Przypisz użytkownika:</p>
                <select v-model="userToRegister">
                    <option v-for="user in registeredUsers" :key="user" :value="user">{{ user.user_name }}</option>
                </select>
                <input type="button" id="confirm" value="Potwierdź" @click="addUser(userToRegister)">
            </div>
            <div id="main-remove">
                <p>Usuń użytkownika:</p>
                <select v-model="userToRemove">
                    <option v-for="user in selectedUsers" :key="user" :value="user">{{ user.user_name }}</option>
                </select>
                <input type="button" id="confirm" value="Potwierdź" @click="removeUser(userToRemove)">
            </div>
            <div id="main-current">
                <p>Użytkownicy przypisani do Kosz pod zlewem:</p>
                <ul>
                    <li v-for="user in selectedUsers" :key="user" :value="user">{{ user.user_name }}</li>
                </ul>
            </div>
        </div>
        <div id="harmonogram">
            <h2>Dodaj harmonogram</h2>
            <label for="date">Ustaw datę wyniesienia
                <input type="date" id="date"/>
            </label>
            <select>
                <option disabled selected hidden>Wybierz użytkownika, który ma wynieść śmieci</option>
                <option>Kasia</option>
                <option>Tomek</option>
            </select>
            <input type="button" id="confirm" value="Potwierdź" @click="removeUser(userToRemove)">
        </div>
        <div id="konfiguracja">
            <h2>Pozostałe ustawienia</h2>
            <label>
                Po ilu godzinach ma przychodzić powiadomienie o niewyniesieniu kosza?
                <input type="number" min="0"/>
            </label>
            <label>
                Punkty przyznawane za wyniesienie kosza
                <input type="number" min="0"/>
            </label>
            <label>
                Punkty odbierane za każde 12h niewyniesienia kosza
                <input type="number" min="0"/>
            </label>
            <input type="button" id="confirm" value="Potwierdź" @click="removeUser(userToRemove)">
        </div>
    </div>
</template>
<script>
import { ref, inject } from 'vue';
import axios from "axios";

export default
{
    setup()
    {
        const endpoint = inject("g_endpoint")
        var registeredUsers = ref([])
        var selectedUsers = ref([])

        var userToRegister = ref()
        var userToRemove = ref()

        const addUser = async (value) =>
        {
            if(!value)
                return

            let userId = value.id_user

            let data =
            {
                user_name: value.user_name,
                user_mail: value.user_mail,
                statistics_days: value.statistics_days,
                which_bin: 1,
                points_status: value.points_status
            }
            let dataJ = JSON.stringify(data)

            try
            {
                await axios.put(`${endpoint}users/${userId}/`, dataJ,
                {
                    withCredentials: true,
                    headers: {
                    'Content-Type': 'application/json',
                    }
                })
            }
            catch (error)
            {
                console.error(error);
            }

            fetchSelectedUsers()
            fetchRegisteredUsers()
        }

        const removeUser = async (value) =>
        {
            if(!value)
                return

            let userId = value.id_user

            let data =
            {
                user_name: value.user_name,
                user_mail: value.user_mail,
                statistics_days: value.statistics_days,
                which_bin: 0,
                points_status: value.points_status
            }
            let dataJ = JSON.stringify(data)

            try
            {
                await axios.put(`${endpoint}users/${userId}/`, dataJ,
                {
                    withCredentials: true,
                    headers: {
                    'Content-Type': 'application/json',
                    }
                })
            }
            catch (error)
            {
                console.error(error);
            }

            fetchSelectedUsers()
            fetchRegisteredUsers()
        }

        const fetchRegisteredUsers = async () =>
        {
            try
            {
                const response = await axios.get(`${endpoint}users/`);
                const responseData = response.data;

                registeredUsers.value = []

                responseData.forEach((user) =>
                {
                    if(user.which_bin != "1")
                        registeredUsers.value.push(user);
                });
            }
            catch (error)
            {
                console.error(error);
            }
        }

        const fetchSelectedUsers = async () =>
        {
            try
            {
                const response = await axios.get(`${endpoint}users/`);
                const responseData = response.data;

                selectedUsers.value = []

                responseData.forEach((user) =>
                {
                    if(user.which_bin == "1")
                        selectedUsers.value.push(user);
                });
            }
            catch (error)
            {
                console.error(error);
            }
        }

        fetchRegisteredUsers()
        fetchSelectedUsers()

        return {registeredUsers, selectedUsers, userToRegister, userToRemove, addUser, removeUser}
    }
}
</script>
<style scoped lang="scss">
@import '../style/style.scss';
    #main
    {
        width: 100%;
        min-height: 70vh;
        display: flex;
        flex-direction: column;
        align-items: center;

        #confirm
        {
            transition: 0.3s ease-in-out;
        }
        #confirm:hover
        {
            color: white;
            background-color: $main-color2;
        }

        input, select
        {
            border: 1px solid $main-color;
            line-height: 3rem;
            height: 3rem;
            background-color: white;
            color: $main-color2;
        }

        #top
        {
            margin-top: 5%;
            width: 100%;
            text-align: center;
        }

        #center
        {
            margin-top: 5%;
            width: 90%;
            display: flex;
            flex-direction: column;
            align-items: space-around;

            div
            {
                width: 100%;

                p
                {
                    font-size: 1.5rem;
                }
            }

            #main-assign, #main-remove
            {
                display: flex;
                flex-direction: column;

                & #confirm
                {
                    margin-top: 10%;
                    margin-bottom: 10%;
                }
            }

            #main-current
            {
                ul
                {
                    padding: 0;
                }

                li
                {
                    list-style-type: none;
                    line-height: 2rem;
                    width: 100%;
                    background-color: white;
                    text-align: center;
                    margin-bottom: 1%;
                }
            }
        }

        #harmonogram
        {
            margin-top: 5%;
            width: 90%;
            display: flex;
            flex-direction: column;
            text-align: center;

            & #confirm
            {
                margin-top: 10%;
                margin-bottom: 10%;
            }

            label
            {
                width: 100%;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 5%;
            }
        }

        #konfiguracja
        {
            margin-top: 5%;
            width: 90%;
            display: flex;
            flex-direction: column;

            & #confirm
            {
                margin-top: 10%;
                margin-bottom: 10%;
            }

            label
            {
                width: 100%;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 5%;

                input
                {
                    margin-left: 5%;
                }
            }
        }
    }
    @media only screen and (min-width: 1000px)
    {
        #main
        {
            width: 100%;
            min-height: 70vh;
            display: flex;
            flex-direction: column;
            align-items: center;

            input, select
            {
                border: 1px solid $main-color;
                line-height: 3rem;
                height: 3rem;
                background-color: white;
                color: $main-color2;
            }

            #top
            {
                margin-top: 5%;
                width: 100%;
                text-align: center;
            }

            #center
            {
                margin-top: 5%;
                width: 33%;
                display: flex;
                flex-direction: column;
                align-items: space-around;

                div
                {
                    width: 100%;

                    p
                    {
                        font-size: 1.5rem;
                    }
                }

                #main-assign, #main-remove
                {
                    display: flex;
                    flex-direction: column;

                    & #confirm
                    {
                        margin-top: 10%;
                        margin-bottom: 10%;
                    }
                }

                #main-current
                {
                    ul
                    {
                        padding: 0;
                    }

                    li
                    {
                        list-style-type: none;
                        line-height: 2rem;
                        width: 100%;
                        background-color: white;
                        text-align: center;
                        margin-bottom: 1%;
                    }
                }
            }

            #harmonogram
            {
                margin-top: 5%;
                width: 33%;
                display: flex;
                flex-direction: column;
                text-align: center;

                & #confirm
                {
                    margin-top: 10%;
                    margin-bottom: 10%;
                }

                label
                {
                    width: 100%;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 5%;
                }
            }

            #konfiguracja
            {
                margin-top: 5%;
                width: 50%;
                display: flex;
                flex-direction: column;

                & #confirm
                {
                    margin-top: 10%;
                    margin-bottom: 10%;
                }

                label
                {
                    width: 100%;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 5%;
                }
            }
        }
    }
</style>
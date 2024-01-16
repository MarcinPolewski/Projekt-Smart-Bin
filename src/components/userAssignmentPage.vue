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
                    <option v-for="user in registeredUsers" :key="index">{{ user }}</option>
                </select>
                <input type="button" id="confirm" value="Potwierdź" @click="addUser(userToRegister)">
            </div>
            <div id="main-remove">
                <p>Usuń użytkownika:</p>
                <select v-model="userToRemove">
                    <option v-for="user in selectedUsers" :key="index">{{ user }}</option>
                </select>
                <input type="button" id="confirm" value="Potwierdź" @click="removeUser(userToRemove)">
            </div>
            <div id="main-current">
                <p>Przypisani użytkownicy:</p>
                <ul>
                    <li v-for="user in selectedUsers" :key="index">{{ user }}</li>
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
import { ref } from 'vue';

export default
{
    setup()
    {
        var registeredUsers = ref([])
        var selectedUsers = ref([])
        var userToRegister = ref()
        var userToRemove = ref()

        for(let i = 0; i < 10; i++)
        {
            registeredUsers.value.push(`user ${i}`)
        }

        const addUser = (value) =>
        {
            selectedUsers.value.push(value)
        }

        const removeUser = (value) =>
        {
            const indexToRemove = selectedUsers.value.findIndex(user => user === value);
            if (indexToRemove !== -1)
            {
                selectedUsers.value.splice(indexToRemove, 1);
            }
        }

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
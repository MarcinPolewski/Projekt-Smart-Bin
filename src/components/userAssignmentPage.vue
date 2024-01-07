<template>
    <div id="main">
        <div id="top">
            <a>Teraz konfigurujesz: Kosz pod zlewem</a>
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
                <h4>Przypisani użytkownicy:</h4>
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
    #main
    {
        width: 100%;
        min-height: 70vh;
        display: flex;
        flex-direction: column;
        align-items: center;

        #top
        {
            margin-top: 5%;
            width: 20%;
        }

        #center
        {
            margin-top: 5%;
            width: 50%;
            display: flex;
            justify-content: space-between;

            div
            {
                width: 25%;
            }

            #main-assign, #main-remove
            {
                display: flex;
                flex-direction: column;

                & #confirm
                {
                    margin-top: 20%;
                }
            }
        }

        #harmonogram
        {
            margin-top: 5%;
            display: flex;
            flex-direction: column;
        }

        #konfiguracja
        {
            margin-top: 5%;
            display: flex;
            flex-direction: column;
        }
    }
</style>
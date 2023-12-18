<template>
    <div id="main">
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
        justify-content: space-around;
        margin-top: 10%;

        & div
        {
            width: 25%;
        }

        &-assign, &-remove
        {
            display: flex;
            flex-direction: column;

            & #confirm
            {
                margin-top: 20%;
            }
        }
    }
</style>
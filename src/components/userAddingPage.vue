<template>
    <div id="main">
        <div id="main-form">
            <h4>Dodaj użytkownika</h4>
            <input type="email" placeholder="email" v-model="currentUserMail"/>
            <input type="text" placeholder="name" v-model="currentUserName"/>
            <select>
                <option selected hidden disabled>Jak często chcesz otrzymywać statystyki na email?</option>
                <option>Codziennie</option>
                <option>Co tydzień</option>
                <option>Co miesiąc</option>
                <option>Co trzy miesiące</option>
            </select>
            <select>
                <option selected hidden disabled>Który kosz wynosisz?</option>
                <option>Kosz pod zlewem</option>
            </select>
            <input type="button" value="Potwierdź" @click="addUser"/>
            <p>Oto lista stworzonych użytkowników:</p>
            <ul>
                <li v-for="user in userList" :key="index">{{ user.name }}, {{ user.mail }}</li>
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
        var userList = ref([])
        var currentUserMail = ref()
        var currentUserName = ref()

        const addUser = () =>
        {
            let newUser =
            {
                name: currentUserName.value,
                mail: currentUserMail.value
            }

            userList.value.push(newUser)
        }

        return {userList, currentUserMail, currentUserName, addUser}
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
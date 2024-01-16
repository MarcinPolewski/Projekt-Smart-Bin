<template>
    <div id="main">
        <div class="points" v-for="user in userList" :key="user">
            <h2>{{user.user_name}}</h2>
            <a>{}pkt</a>
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
            }
            catch (error)
            {
                console.error(error);
            }
        }
        refreshUsers()

        return {userList}
    }
}
</script>
<style scoped lang="scss">
    #main
    {
        min-height: 80vh;
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-evenly;

        .points
        {
            background-color: white;
            width: 45%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-evenly;
            height: 50vh;
            margin-top: 5%;

            h2
            {
                word-break: break-all;
                text-align: center;
            }
        }
    }

    @media only screen and (min-width: 1000px)
    {
        #main
        {
            min-height: 80vh;
            width: 100%;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-evenly;
            margin-bottom: 5%;

            .points
            {
                background-color: white;
                width: 19%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: space-evenly;
                height: 50vh;
                margin-top: 5%;
            }
        }
    }
</style>
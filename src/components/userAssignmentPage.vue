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
                    <option disabled selected hidden value="">Przypisz użytkownika do: Kosz pod zlewem</option>
                    <option v-for="user in registeredUsers" :key="user" :value="user">{{ user.user_name }}</option>
                </select>
                <input type="button" id="confirm" value="Potwierdź" @click="addUser(userToRegister)">
            </div>
            <div id="main-remove">
                <p>Usuń użytkownika:</p>
                <select v-model="userToRemove">
                    <option disabled selected hidden value="">Usuń użytkownika z: Kosz pod zlewem</option>
                    <option v-for="user in selectedUsers" :key="user" :value="user">{{ user.user_name }}</option>
                </select>
                <input type="button" id="confirm" value="Potwierdź" @click="removeUser(userToRemove)">
            </div>
            <div id="main-current">
                <p>Użytkownicy przypisani do: Kosz pod zlewem:</p>
                <ul>
                    <li v-for="user in selectedUsers" :key="user" :value="user">{{ user.user_name }}</li>
                </ul>
            </div>
        </div>
        <div id="harmonogram">
            <h2>Dodaj harmonogram</h2>
            <label for="date">Ustaw datę wyniesienia
                <input type="date" id="date" v-model="takeoutDate"/>
            </label>
            <!-- <select v-model="userTakeout">
                <option disabled selected hidden value="">Wybierz użytkownika, który ma wynieść śmieci</option>
                <option v-for="user in selectedUsers" :key="user" :value="user">{{ user.user_name }}</option>
            </select> -->
            <input type="button" id="confirm" value="Potwierdź" @click="addSchedule(takeoutDate)">
            <a>{{ scheduleError }}</a>
        </div>
        <div id="konfiguracja">
            <h2>Pozostałe ustawienia</h2>
            <label>
                Po ilu godzinach ma przychodzić powiadomienie o niewyniesieniu kosza?
                <input type="number" min="0" v-model="notification"/>
            </label>
            <label>
                Punkty przyznawane za wyniesienie kosza
                <input type="number" min="0" v-model="pointsToAdd"/>
            </label>
            <label>
                Punkty odbierane za niewyniesienie kosza
                <input type="number" min="0" v-model="pointsToRemove"/>
            </label>
            <a id="points-error">{{ pointsError }}</a>
            <input type="button" id="confirm" value="Potwierdź" @click="changePoints()">
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

        var userToRegister = ref("")
        var userToRemove = ref("")

        var notification = ref(0)
        var pointsToAdd = ref(0)
        var pointsToRemove = ref(0)

        var takeoutDate = ref("")

        var scheduleError = ref("")
        var pointsError = ref("")

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
                userToRegister.value = ""
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
                userToRemove.value = ""
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

        const fetchPoints = async () =>
        {
            try
            {
                const response = await axios.get(`${endpoint}bins/1/`);

                notification.value = response.data.emp_reminder
                pointsToAdd.value = response.data.adding_points
                pointsToRemove.value = response.data.subtrack_points
            }
            catch (error)
            {
                console.error(error);
            }
        }

        const changePoints = async () =>
        {
            let bin_data
            try
            {
                const response = await axios.get(`${endpoint}bins/1/`);
                bin_data = response
            }
            catch(error)
            {
                console.error(error)
            }

            let data =
            {
                id_bin: bin_data.data.id_bin,
                bin_name: bin_data.data.bin_name,
                bin_depth: bin_data.data.bin_depth,
                emp_calendar: bin_data.data.emp_calendar,
                emp_reminder: notification.value,
                adding_points: pointsToAdd.value,
                subtrack_points: pointsToRemove.value,
                bin_status: bin_data.data.bin_status
            }
            let dataJ = JSON.stringify(data)

            try
            {
                await axios.put(`${endpoint}bins/1/`, dataJ,
                {
                    withCredentials: true,
                    headers: {
                    'Content-Type': 'application/json',
                    }
                })
                userToRegister.value = ""
                pointsError.value = "Prawidłowo zmieniono ustawienia"
            }
            catch (error)
            {
                console.error(error);
                pointsError.value = "Błędne dane"
            }
        }

        const addSchedule = async (value) =>
        {
            if(!value)
            {
                scheduleError.value = "Nieprawidłowa data"
                return
            }

            let data =
            {
                data: value,
                bin_id: 1
            }
            let dataJ = JSON.stringify(data)

            try
            {
                await axios.post(`${endpoint}schedule/`, dataJ,
                {
                    withCredentials: true,
                    headers: {
                    'Content-Type': 'application/json',
                    }
                })
                takeoutDate.value = ""
                scheduleError.value = "Harmonogram dodany prawidłowo"
            }
            catch (error)
            {
                console.error(error);
            }
        }

        fetchRegisteredUsers()
        fetchSelectedUsers()
        fetchPoints()

        return {registeredUsers, selectedUsers, userToRegister, userToRemove, takeoutDate, scheduleError, pointsToAdd, pointsToRemove, notification, pointsError, addUser, removeUser, addSchedule, changePoints}
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

        #points-error
        {
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
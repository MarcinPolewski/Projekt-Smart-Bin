<template>
    <div id="baner">
        <router-link to="/" id="baner-logo">
            
        </router-link>
        <div id="baner-nav">
            <router-link to="/add-user">Dodaj Użytkownika</router-link>
            <router-link to="/assign-user">Przypisz Użytkownika</router-link>
            <router-link to="/punctation">Punktacja</router-link>
            <router-link to="/filling-level">Zapełnienie Kosza</router-link>
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
    #baner
    {
        height: 100px;
        border-bottom: 1px solid $border-color2;
        display: flex;
        justify-content: space-around;

        &-logo
        {
            height: 100px;
            width: 100px;
            background-image: url('../assets/smietnik.png');
            background-size: contain;
            background-repeat: no-repeat;
        }
        &-nav 
        {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 40%;
            height: 100%;
            
            & a
            {
                text-decoration: none;
                color: $font-color;
                cursor: pointer;
            }
        }
    }
</style>